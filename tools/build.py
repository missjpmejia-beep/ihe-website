#!/usr/bin/env python3
"""Build the IHE Demolition static site.

Each file in tools/pages/ is one page: a first-line HTML comment holding JSON
metadata (path, title, description, ...) followed by the page's <main> content.
This script wraps every page in the shared header and footer and writes it to
<path>/index.html at the repo root, then regenerates sitemap.xml.

Run from the repo root:  python3 tools/build.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "tools" / "pages"
SITE = "https://www.ih-equipment.co.uk"

PHONE_DISPLAY = "01977 644489"
PHONE_TEL = "+441977644489"
EMAIL = "info@ih-equipment.co.uk"

CDN = "https://images.squarespace-cdn.com/content/v1/6a7302817f3fb1112d021c76"
LOGO = f"{CDN}/c9e92a08-e444-4384-bd46-8329bb491598/croppedvecot.png?format=300w"
DEFAULT_OG = f"{CDN}/74ae87dd-11e6-4ccd-84b9-2c824a75ea47/Askern.png?format=1500w"

PHONE_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
              '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 '
              '2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 '
              '2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>')

NAV = [("services", "/services/", "Services"), ("projects", "/projects/", "Projects"),
       ("about", "/about/", "About"), ("contact", "/contact/", "Contact")]

BUSINESS_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "GeneralContractor",
    "name": "IHE Demolition",
    "legalName": "I H Equipment Ltd",
    "url": SITE + "/",
    "telephone": "+44 1977 644489",
    "email": EMAIL,
    "description": "Family-run demolition contractor offering demolition, soft strip, dismantling, asbestos management and waste recycling across Yorkshire.",
    "address": {"@type": "PostalAddress", "addressLocality": "South Kirkby",
                "addressRegion": "West Yorkshire", "addressCountry": "GB"},
    "areaServed": {"@type": "AdministrativeArea", "name": "Yorkshire"},
    "knowsAbout": ["Demolition", "Soft strip", "Strip out", "Dismantling", "Asbestos removal",
                   "Site clearance", "Concrete crushing", "Waste management"],
}


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def header(active):
    items = "\n".join(
        f'          <li><a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
        for key, href, label in NAV)
    return f'''  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap header-inner">
      <a class="logo" href="/" aria-label="IHE Demolition home">
        <img src="{LOGO}" alt="IHE Demolition" width="160" height="88">
      </a>

      <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>

      <nav class="nav" id="site-nav" aria-label="Main">
        <ul>
{items}
        </ul>
        <div class="header-cta">
          <a class="header-phone" href="tel:{PHONE_TEL}">
            {PHONE_ICON}
            {PHONE_DISPLAY}
          </a>
          <a class="btn btn-primary" href="/contact/">Get a free quote</a>
        </div>
      </nav>
    </div>
  </header>
'''


FOOTER = f'''  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <a class="footer-logo" href="/"><img src="{LOGO}" alt="IHE Demolition" width="160" height="88" loading="lazy"></a>
          <p>Family-run demolition contractor based in South Kirkby, West Yorkshire, working across Yorkshire and beyond.</p>
        </div>
        <div>
          <h3>Services</h3>
          <ul>
            <li><a href="/services/demolition/">Demolition</a></li>
            <li><a href="/services/soft-strip/">Soft strip</a></li>
            <li><a href="/services/dismantling/">Dismantling</a></li>
            <li><a href="/services/asbestos/">Asbestos</a></li>
            <li><a href="/services/waste-recycling/">Waste &amp; recycling</a></li>
          </ul>
        </div>
        <div>
          <h3>Company</h3>
          <ul>
            <li><a href="/projects/">Projects</a></li>
            <li><a href="/about/">About</a></li>
            <li><a href="/faq/">FAQs</a></li>
            <li><a href="/contact/">Contact</a></li>
          </ul>
        </div>
        <div>
          <h3>Get in touch</h3>
          <ul>
            <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>South Kirkby, West Yorkshire</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span data-year>2026</span> I H Equipment Ltd, trading as IHE Demolition. Registered in England &amp; Wales, company no. 05791418.</span>
        <span><a href="/privacy/">Privacy</a> &middot; Constructionline Gold &middot; NFDC member</span>
      </div>
    </div>
  </footer>

  <div class="call-bar" aria-label="Quick contact">
    <a class="call" href="tel:{PHONE_TEL}">
      {PHONE_ICON}
      Call us
    </a>
    <a class="quote" href="/contact/">Free quote</a>
  </div>
'''


CTA_BAND = f'''
    <section class="cta-band" aria-labelledby="cta-title">
      <div class="wrap">
        <div>
          <h2 id="cta-title">Got a job coming up?</h2>
          <p>Tell us what you need and we'll get back to you within 48 hours.</p>
        </div>
        <div class="actions">
          <a class="btn btn-primary" href="/contact/">Get a free quote</a>
          <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
        </div>
      </div>
    </section>
'''


def page_hero(meta):
    """Blue title band for inner pages, with visible breadcrumb."""
    if "hero" not in meta:
        return ""
    h = meta["hero"]
    crumbs = meta.get("breadcrumb", [])
    trail = " <span aria-hidden=\"true\">/</span> ".join(
        f'<a href="{href}">{name}</a>' if i < len(crumbs) - 1 else f'<span aria-current="page">{name}</span>'
        for i, (name, href) in enumerate(crumbs))
    lead = f'\n          <p class="lead">{h["lead"]}</p>' if h.get("lead") else ""
    eyebrow = f'\n          <span class="eyebrow">{h["eyebrow"]}</span>' if h.get("eyebrow") else ""
    return f'''    <section class="page-hero">
      <div class="wrap">
        <nav class="breadcrumb" aria-label="Breadcrumb">{trail}</nav>
        <div class="page-hero-inner">{eyebrow}
          <h1>{h["title"]}</h1>{lead}
        </div>
      </div>
    </section>
'''


def render(meta, body):
    path = meta["path"]
    body = page_hero(meta) + body.rstrip() + "\n" + (CTA_BAND if meta.get("cta", True) and path != "/" else "")
    url = SITE + path
    og_image = meta.get("og_image", DEFAULT_OG)
    robots = '\n  <meta name="robots" content="noindex">' if meta.get("noindex") else ""
    schema = ""
    if meta.get("schema"):
        schema = ('\n  <script type="application/ld+json">\n  '
                  + json.dumps(BUSINESS_SCHEMA, indent=2).replace("\n", "\n  ")
                  + "\n  </script>")
    if meta.get("breadcrumb"):
        crumbs = [{"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + href}
                  for i, (name, href) in enumerate(meta["breadcrumb"])]
        schema += ('\n  <script type="application/ld+json">\n  '
                   + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                                 "itemListElement": crumbs}, indent=2).replace("\n", "\n  ")
                   + "\n  </script>")
    scripts = '  <script src="/assets/js/main.js" defer></script>'
    for extra in meta.get("scripts", []):
        scripts += f'\n  <script src="{extra}" defer></script>'

    return f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(meta["title"])}</title>
  <meta name="description" content="{esc(meta["description"])}">
  <link rel="canonical" href="{url}">{robots}
  <meta name="theme-color" content="#003d95">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="IHE Demolition">
  <meta property="og:title" content="{esc(meta["title"])}">
  <meta property="og:description" content="{esc(meta["description"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:locale" content="en_GB">

  <link rel="preload" href="/assets/fonts/archivo-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/styles.css">{schema}
</head>
<body>
{header(meta.get("nav", ""))}
  <main id="main">
{body.rstrip()}
  </main>

{FOOTER}
{scripts}
</body>
</html>
'''


def main():
    built = []
    for f in sorted(PAGES.glob("*.html")):
        text = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--(.*?)-->\s*\n", text, re.S)
        if not m:
            raise SystemExit(f"{f.name}: missing metadata comment")
        meta = json.loads(m.group(1))
        body = text[m.end():]
        out = ROOT / meta["path"].strip("/") / "index.html" if meta["path"] != "/" else ROOT / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(meta, body), encoding="utf-8")
        built.append(meta)
        print("built", meta["path"])

    urls = "\n".join(f"  <url><loc>{SITE}{m['path']}</loc></url>"
                     for m in sorted(built, key=lambda m: (m["path"] != "/", m["path"]))
                     if not m.get("noindex"))
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8")
    print(f"sitemap: {sum(1 for m in built if not m.get('noindex'))} urls")


if __name__ == "__main__":
    main()
