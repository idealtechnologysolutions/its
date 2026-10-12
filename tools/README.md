# tools

## generate_pages.py

Keeps the shared parts of every page identical. It rewrites the `<head>`, the `header` part and the `footer` part of every `site/**/index.html`, and creates a stub for any linked slug that has no page yet. The page body, everything between `<!-- /part: header -->` and `<!-- part: footer -->`, is left exactly as it is.

The site itself has no build step. This script is a maintenance tool: its output is plain HTML that gets committed like any other change.

### Run it

From the repo root, with Python 3.8 or later (standard library only):

```
python tools/generate_pages.py           # update pages
python tools/generate_pages.py --check   # list pages that would change, write nothing
```

`--check` exits with code 1 if any page is out of date, so it can be used before a commit or in review.

### When to run it

- **Header, footer or head changes** (navigation links, footer text, fonts, meta tags, the logo path): edit the templates in the script, then run it. Never edit these parts page by page.
- **A page's title or description changes:** fix the `SEO title` or `Meta description` in that page's `content/*.md` file, then run it.
- **After building or editing any page:** run it so new links get stubs and the head and parts are current.

### How it decides what each page is

- **Built page:** any page whose body is not a stub. Its `<title>` and description come from the `content/*.md` file whose `URL slug` matches the page's path. The script stops with an error if no content file matches.
- **Stub:** a page whose body is the standard stub (`<h1>` with the page name and "This page is being written."). It gets the extra `<meta name="robots" content="noindex">`. Names come from `PAGE_NAMES` in the script.
- **Missing page:** any slug linked from a page or the navigation that has no file gets a new stub. If the slug is not in `PAGE_NAMES`, the script stops: check the slug against `agents/PROJECT_BRIEF.md` before adding it.

### Building a new page

1. Open the page's stub, for example `site/services/cloud-cybersecurity/index.html`.
2. Replace the stub's `<main>` element with the page body.
3. Run `python tools/generate_pages.py`. The head picks up the title and description from `content/`, the stub `noindex` comes off, and stubs are created for any new links.

## screenshots.cjs

Saves full-page screenshots of every built page (stubs are skipped) at 375, 768 and 1280px to `docs/screenshots/`, named `<page>-<width>.png`. The page name is `home` for the homepage and the last slug segment otherwise, for example `managed-it-infrastructure-375.png`. Old screenshots are deleted first, so the folder always matches the current build. Run it after every build task.

It serves `site/` itself on a free local port, so no other server is needed. It waits for the fonts and the hero animation before each capture.

### One-time setup

The script needs `puppeteer-core`, which drives your installed Chrome. Install it **outside the repo** so no `package.json` or `node_modules` ends up here:

```
npm install --prefix "%LOCALAPPDATA%\its-tools" puppeteer-core@23.11.1
```

Chrome is expected at `C:/Program Files/Google/Chrome/Application/chrome.exe`. Set `CHROME_PATH` to use another location.

### Run it

```
node tools/screenshots.cjs "%LOCALAPPDATA%\its-tools"
```

These are captured in one pass by Chrome itself. Screenshot extensions that scroll and stitch the page, such as FireShot in Chrome's phone mode, can show sections overlapping that look fine in the browser.
