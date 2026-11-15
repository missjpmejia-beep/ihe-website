# IHE Demolition website

Static site for IHE Demolition (I H Equipment Ltd), hosted on Cloudflare (Workers static assets, deployed from GitHub).

- Plain HTML and CSS, no build step. `wrangler.jsonc` serves the repo root as static assets with `404.html` as the not-found page; `.assetsignore` keeps repo files out of the upload.
- Fonts (Archivo, Inter) are self-hosted under `assets/fonts` (SIL Open Font License), so no visitor data goes to Google Fonts.
- `_redirects` maps the old Squarespace addresses to the new ones. `_headers` sets security headers and keeps the workers.dev preview out of Google.

## To do before launch
- Images are temporarily loaded from the Squarespace CDN. Replace them with local copies in `assets/img/` before Squarespace is cancelled.
- Confirm the phone number (01977 644489) and full address and postcode with Jack.
- Build the Services, Projects, About and Contact pages (Phase 2).
