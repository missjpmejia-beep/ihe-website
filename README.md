# IHE Demolition website

Static site for IHE Demolition (I H Equipment Ltd), hosted on Cloudflare (Workers static assets, deployed from GitHub).

- Plain HTML and CSS, no build step. `wrangler.jsonc` serves the repo root as static assets with `404.html` as the not-found page; `.assetsignore` keeps repo files out of the upload.
- Fonts (Archivo, Inter) are self-hosted under `assets/fonts` (SIL Open Font License), so no visitor data goes to Google Fonts.
- `_redirects` maps the old Squarespace addresses to the new ones. `_headers` sets security headers and keeps the workers.dev preview out of Google.

## Editing pages
Page content lives in `tools/pages/*.html` (first line is JSON metadata: path, title, description, breadcrumb, hero). The shared header, footer and call-to-action are in `tools/build.py`. After editing, run:

    python3 tools/build.py

This regenerates every page's `index.html` and `sitemap.xml`. Commit the results; Cloudflare deploys on push.

## Contact form
The form posts to Web3Forms. Until a real access key replaces `WEB3FORMS_ACCESS_KEY` in `tools/pages/contact.html`, the form shows a call/email message instead of sending.

## To do before launch
- Images are temporarily loaded from the Squarespace CDN. Replace them with local copies in `assets/img/` before Squarespace is cancelled.
- Confirm the phone number (01977 644489) and full address and postcode with Jack.
- Build the Services, Projects, About and Contact pages (Phase 2).
