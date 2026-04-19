# Magic Link 1

Magic Link 1 was a simple web challenge that looked like it would involve attacking a magic-link authentication flow, but the actual solution was much easier. Instead of breaking the login logic, the flag could be recovered through a deployment misconfiguration.

When opening the main page at `https://bluehens-magic-link.chals.io/`, the site displayed a basic magic link login form. Since there was no obvious vulnerability directly on the page, the next step was standard web reconnaissance. 
In challenges like this, it is always worth checking common auxiliary files and hidden paths such as `robots.txt`, `sitemap.xml`, `.git`, and `.env`, because they often reveal accidental information disclosure.

The first useful result came from requesting `robots.txt`:

```bash
curl -k --ssl-no-revoke --http1.1 -i -s https://bluehens-magic-link.chals.io/robots.txt
The response was:

User-agent: *
Disallow: /inbox
Disallow: /dashboard
Disallow: /.env
This was immediately suspicious. The entry for /.env suggested that the file existed on the server,
 and environment files frequently contain secrets, tokens, email addresses, or internal configuration data. That made it the most interesting path to test next.

I then requested the .env file directly:

curl -k --ssl-no-revoke --http1.1 -i -s https://bluehens-magic-link.chals.io/.env
The server returned the following contents:

TEDDYS_EMAIL=teddy@udctf.com
TEDDYS_TOKEN=udctf{d0n7_h057_y0ur_3nv_f113}
ADMIN_EMAIL=admin@udctf.com
INBOX_URL=http://localhost:5050/inbox?token=${TEDDYS_TOKEN}

At that point the challenge was solved, because the flag was exposed directly in the environment configuration as the value of TEDDYS_TOKEN.
 No interaction with the actual magic-link flow was necessary.

This means the real vulnerability was not in authentication, but in sensitive file exposure caused by a security misconfiguration.
The application was serving its .env file over HTTP, which leaked internal configuration values that should never have been publicly accessible.
 In a real-world application, this kind of issue could expose API keys, database credentials, session secrets, internal service URLs, or authentication tokens.

The main lesson from this challenge is that even when an application appears to revolve around a more complicated feature such as email login or token verification,
 it is still important to start with basic web recon. Simple mistakes like exposed configuration files can completely bypass the intended challenge path.

Flag: udctf{d0n7_h057_y0ur_3nv_f113}
