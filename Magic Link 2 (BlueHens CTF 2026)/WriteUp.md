# Magic Link 2

Magic Link 2 was solved by continuing from the information leak in the first stage rather than attacking the login flow directly. The application at `https://bluehens-magic-link.chals.io/` presented the same magic-link login page, so the first step was to perform basic reconnaissance on common helper files and hidden paths.

Requesting `robots.txt` revealed several interesting entries:

```txt
User-agent: *
Disallow: /inbox
Disallow: /dashboard
Disallow: /.env
The most important path here was /.env, since environment files frequently contain sensitive configuration values. I requested it directly and received the following:

TEDDYS_EMAIL=teddy@udctf.com
TEDDYS_TOKEN=udctf{d0n7_h057_y0ur_3nv_f113}
ADMIN_EMAIL=admin@udctf.com
INBOX_URL=http://localhost:5050/inbox?token=${TEDDYS_TOKEN}
This already gave the stage 1 flag, but for Magic Link 2 the useful part was the leaked Teddy token and the inbox URL pattern. The application exposed an /inbox route that was meant to be hidden, and the .env file showed that access to the inbox depended on a token parameter.

I then visited the inbox using Teddy’s leaked token:

curl -k --ssl-no-revoke --http1.1 "https://bluehens-magic-link.chals.io/inbox?token=udctf%7Bd0n7_h057_y0ur_3nv_f113%7D"
The inbox page was very noisy and contained a huge amount of blank HTML, so the next step was to generate a fresh magic link and then inspect the inbox contents for the new entry. I triggered a login email for Teddy:

curl -k --ssl-no-revoke --http1.1 -X POST https://bluehens-magic-link.chals.io/login -F "email=teddy@udctf.com"
The server returned a JSON response containing a UUID, but the more important result was that Teddy’s inbox now had a fresh login message. After saving the inbox HTML locally and extracting the meaningful content, I found a login link and a paragraph containing the flag:

<a href="/login/umlwYmgMGtWSuY09y-ZPkQ">Click here to login</a>
<p>udctf{m4g1c_l1nks_4r3_w31rd}</p>
So the intended weakness in this stage was that the hidden inbox could be accessed with a leaked token from the exposed .env file, allowing an attacker to read magic-link emails that should have remained private. Once the inbox was accessible, the flag was directly visible in the message content.

Flag: udctf{m4g1c_l1nks_4r3_w31rd}
