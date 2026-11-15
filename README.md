# IHE Demolition website

Static site for IHE Demolition (I H Equipment Ltd), hosted on Cloudflare Pages.

- Plain HTML and CSS, no build step. Cloudflare Pages settings: **Framework preset: None**, **Build command: empty**, **Build output directory: `/`**.
- Fonts (Archivo, Inter) are self-hosted under `assets/fonts` (SIL Open Font License), so no visitor data goes to Google Fonts.
- `_redirects` maps the old Squarespace addresses to the new ones. `_headers` sets security headers and keeps `*.pages.dev` previews out of Google.

## To do before launch
- Images are temporarily loaded from the Squarespace CDN. Replace them with local copies in `assets/img/` before Squarespace is cancelled.
- Confirm the phone number (01977 644489) and full address and postcode with Jack.
- Build the Services, Projects, About and Contact pages (Phase 2).
