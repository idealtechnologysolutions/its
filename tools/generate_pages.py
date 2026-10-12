"""Regenerate the shared parts of every page in the ITS preview site.

Rewrites the <head>, the header part and the footer part of every
site/**/index.html, and creates a stub for any linked slug that has no page.
The content between the header and footer (the page body) is kept as it is.

    python tools/generate_pages.py           update pages
    python tools/generate_pages.py --check   report what would change, write nothing

Standard library only. See tools/README.md.
"""
import argparse
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CONTENT = ROOT / "content"
BASE = "https://idealtechnologysolutions.us"

HEADER_END = "<!-- /part: header -->\n"
FOOTER_START = "<!-- part: footer -->"
STUB_LINE = "This page is being written."

# Navigation and footer. Slugs from agents/PROJECT_BRIEF.md; never invent one.
SERVICES = [
    ("/services/managed-it-infrastructure/", "Managed IT & Infrastructure"),
    ("/services/cloud-cybersecurity/", "Cloud & Cybersecurity"),
    ("/services/custom-software-digital-products/", "Custom Software & Digital Products"),
    ("/services/data-ai-automation/", "Data, AI & Automation"),
    ("/services/digital-transformation-consulting/", "Digital Transformation & Technology Consulting"),
]
INDUSTRIES = [
    ("/industries/government-public-sector/", "Government & Public Sector"),
    ("/industries/healthcare/", "Healthcare"),
    ("/industries/automotive/", "Automotive"),
    ("/industries/manufacturing/", "Manufacturing"),
    ("/industries/retail-service/", "Retail & Service"),
    ("/industries/education/", "Education"),
    ("/industries/nonprofits/", "Nonprofits & Community Organizations"),
]
COMPANY = [("/about/", "About"), ("/work/", "Our Work"), ("/contact/", "Contact")]

# Page names used as the <h1> of stub pages.
PAGE_NAMES = dict(SERVICES + INDUSTRIES + COMPANY)
PAGE_NAMES.update({
    "/": "Home",
    "/work/sean-anderson-foundation/": "Sean Anderson Foundation",
    "/work/chemico-credit-hold/": "The Chemico Group",
    "/work/dpscd-foundation/": "DPSCD Foundation",
    "/work/guidepoint-systems/": "Guidepoint Systems",
    "/work/ushers-new-look/": "Usher's New Look",
    "/work/rozafa-transport/": "Rozafa Transport",
})


def e(text):
    return html.escape(text, quote=True)


def cur(href, path):
    return ' aria-current="page"' if href == path else ""


# ---------- Shared parts ----------

def head(path, title, description, stub):
    desc = f'\n<meta name="description" content="{e(description)}">' if description else ""
    ogdesc = f'\n<meta property="og:description" content="{e(description)}">' if description else ""
    stubmeta = '\n<meta name="robots" content="noindex">' if stub else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">{stubmeta}
<title>{e(title)}</title>{desc}
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ideal Technology Solutions">
<meta property="og:title" content="{e(title)}">{ogdesc}
<meta property="og:url" content="{BASE}{path}">
<link rel="icon" href="/assets/brand/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,800&amp;family=Public+Sans:ital,wght@0,400;0,600;1,400&amp;display=swap">
<link rel="stylesheet" href="/assets/css/main.css">
<noscript><style>.site-nav{{display:block}}.menu-toggle{{display:none}}.site-nav__item:hover>.site-nav__sub,.site-nav__item:focus-within>.site-nav__sub{{display:block}}</style></noscript>
<script src="/assets/js/main.js" defer></script>
</head>
<body>
'''


def nav_group(key, label, items, path):
    current = " is-current" if any(h == path for h, _ in items) else ""
    links = "\n".join(f'            <li><a href="{h}"{cur(h, path)}>{e(t)}</a></li>' for h, t in items)
    return f'''        <li class="site-nav__item">
          <span class="site-nav__heading">{label}</span>
          <button class="site-nav__toggle{current}" type="button" aria-expanded="false" aria-controls="site-nav-{key}">{label}</button>
          <ul class="site-nav__sub" id="site-nav-{key}">
{links}
          </ul>
        </li>'''


def header(path):
    return f'''<!-- part: header -->
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="site-header__inner">
    <a class="site-logo" href="/">
      <img class="site-logo__mark" src="/assets/brand/logo-mark.svg" alt="" width="56" height="32">
      <span class="site-logo__name">Ideal Technology Solutions</span>
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="menu-toggle__icon" aria-hidden="true"></span>
      <span class="menu-toggle__label">Menu</span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul class="site-nav__list">
{nav_group("services", "Services", SERVICES, path)}
{nav_group("industries", "Industries", INDUSTRIES, path)}
        <li class="site-nav__item"><a class="site-nav__link" href="/work/"{cur("/work/", path)}>Our Work</a></li>
        <li class="site-nav__item"><a class="site-nav__link" href="/about/"{cur("/about/", path)}>About</a></li>
        <li class="site-nav__item site-nav__cta-item"><a class="button" href="/contact/">Book a 30 minute call</a></li>
      </ul>
    </nav>
    <a class="button site-header__cta" href="/contact/">Book a 30 minute call</a>
  </div>
</header>
{HEADER_END}'''


def needs_input(text, indent=""):
    return (f'{indent}<!-- part: needs-input -->\n'
            f'{indent}<div class="needs-input" role="note"><span class="needs-input__label">Needs input</span>'
            f'<span class="needs-input__text">{e(text)}</span></div>\n'
            f'{indent}<!-- /part: needs-input -->')


def footer_links(key, label, items):
    links = "\n".join(f'        <li><a href="{h}">{e(t)}</a></li>' for h, t in items)
    return f'''    <nav class="site-footer__nav site-footer__nav--{key}" aria-label="{label}">
      <h2 class="site-footer__heading">{label}</h2>
      <ul class="site-footer__links">
{links}
      </ul>
    </nav>'''


def footer():
    return f'''{FOOTER_START}
<footer class="site-footer">
  <div class="site-footer__inner">
    <div class="site-footer__brand">
      <a class="site-logo site-logo--reversed" href="/">
        <img class="site-logo__mark" src="/assets/brand/logo-mark-reversed.svg" alt="" width="56" height="32">
        <span class="site-logo__name">Ideal Technology Solutions</span>
      </a>
      <p class="site-footer__place">Southfield, Michigan</p>
{needs_input("footer contact details", "      ")}
    </div>
{footer_links("services", "Services", SERVICES)}
{footer_links("industries", "Industries", INDUSTRIES)}
{footer_links("company", "Company", COMPANY)}
    <p class="site-footer__legal">© 2026 Ideal Technology Solutions</p>
  </div>
</footer>
<!-- /part: footer -->
</body>
</html>
'''


def stub_body(name):
    return f'''<main id="main" class="stub">
  <div class="section__inner">
    <h1>{e(name)}</h1>
    <p>{STUB_LINE}</p>
  </div>
</main>
'''


# ---------- Pages ----------

def content_meta():
    """Map each URL slug to (SEO title, meta description) from content/*.md."""
    meta = {}
    for md in sorted(CONTENT.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        fields = dict(re.findall(r"^- (URL slug|SEO title|Meta description): (.+?)\s*$", text, re.M))
        if "URL slug" in fields:
            meta[fields["URL slug"]] = (fields.get("SEO title"), fields.get("Meta description"), md.name)
    return meta


def page_file(path):
    return SITE / "index.html" if path == "/" else SITE / path.strip("/") / "index.html"


def page_path(file):
    rel = file.parent.relative_to(SITE).as_posix()
    return "/" if rel == "." else f"/{rel}/"


def is_stub(body):
    return f"<p>{STUB_LINE}</p>" in body and 'class="stub"' in body


def build(path, body, meta):
    if is_stub(body):
        name = PAGE_NAMES.get(path)
        if not name:
            raise SystemExit(f"error: {path} is a stub with no name. Add it to PAGE_NAMES in tools/generate_pages.py.")
        return head(path, f"{name} | ITS", None, True) + header(path) + stub_body(name) + footer()
    if path not in meta:
        raise SystemExit(f"error: {path} is a built page but no content/*.md file has 'URL slug: {path}'.")
    title, description, source = meta[path]
    if not title or not description:
        raise SystemExit(f"error: content/{source} is missing its SEO title or meta description.")
    return head(path, title, description, False) + header(path) + body + footer()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="report changes without writing")
    args = parser.parse_args()

    meta = content_meta()
    pages = {}
    for file in sorted(SITE.rglob("index.html")):
        text = file.read_text(encoding="utf-8")
        if HEADER_END not in text or FOOTER_START not in text:
            raise SystemExit(f"error: {file.relative_to(ROOT).as_posix()} has no header or footer part markers.")
        body = text.split(HEADER_END, 1)[1].split(FOOTER_START, 1)[0]
        pages[page_path(file)] = (file, text, body)

    # Every slug linked from any page, plus the navigation, must resolve.
    linked = {h for h, _ in SERVICES + INDUSTRIES + COMPANY}
    for _, text, _ in pages.values():
        linked.update(re.findall(r'href="(/[^"#?]*)"', text))
    linked = {h for h in linked if not h.startswith("/assets/") and h.endswith("/")}
    for path in sorted(linked - pages.keys()):
        name = PAGE_NAMES.get(path)
        if not name:
            raise SystemExit(f"error: {path} is linked but has no page and no name. Check the slug against "
                             "agents/PROJECT_BRIEF.md, then add it to PAGE_NAMES.")
        pages[path] = (page_file(path), None, stub_body(name))

    changed = []
    for path, (file, old, body) in sorted(pages.items()):
        new = build(path, body, meta)
        if new != old:
            changed.append(("new stub" if old is None else "updated", file))
            if not args.check:
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(new, encoding="utf-8", newline="\n")

    for kind, file in changed:
        print(f"{kind}: {file.relative_to(ROOT).as_posix()}")
    print(f"{len(pages)} pages, {len(changed)} {'would change' if args.check else 'changed'}.")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
