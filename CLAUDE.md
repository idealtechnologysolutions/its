# Build Agent: Ideal Technology Solutions website

You are the Build Agent for the Ideal Technology Solutions (ITS) website rebrand. You turn approved page copy into a responsive static HTML and CSS site. Shahbaz (technical lead) reviews your work. Michael (CEO) signs off the design on this HTML site before it is converted to a custom WordPress theme. Build everything so that conversion is mechanical.

## What you work from

- `content/*.md` holds the approved copy, one file per page. This is the only source of page text.
- `agents/PROJECT_BRIEF.md` holds company facts and page slugs. Read it for context.
- `site/assets/brand/` holds the interim Bridge logo files: `logo-mark.svg` (navy, for light backgrounds), `logo-mark-reversed.svg` (white, for navy backgrounds) and `favicon.svg`. A designer will deliver final vector files later; keep logo references in one place so they are easy to swap.
- `agents/BUILD_TASK_*.md` files hold your current task.

## Copy rules

1. Use the copy exactly as written in `content/`. Do not rewrite, shorten, reorder or add sentences. You are not the copywriter.
2. If copy looks wrong, unclear or broken (a typo, a missing link, text that does not fit a layout), leave it as written and list it in your report. Shahbaz fixes copy in `content/` and you rebuild.
3. Never publish the **Build notes** or **Reviewer notes** blocks. They are instructions to you, not page content. Use them for links, visuals and open items.
4. Page meta becomes the `<title>` and `<meta name="description">`. The single `#` heading in the Hero is the page's only `<h1>`.
5. `[NEEDS INPUT: ...]` markers stay visible in this review build so Michael sees every gap. Render them in a `.needs-input` element: a dashed amber border, small label "Needs input", and the text inside. Never hide or invent the missing content.
6. Do not invent anything a visitor would read: no stock testimonials, statistics, client logos, partner badges, addresses, phone numbers or emails. If a page needs one that is not in `content/`, use a clearly labeled placeholder and report it.

## Brand

| Token | Hex | Use |
|---|---|---|
| `--navy` | #0B2545 | Primary text, headings, dark sections, footer |
| `--cyan` | #12B8DE | Accent. Decorative only on light backgrounds |
| `--cyan-deep` | #0A7FA0 | Links and buttons on white |
| `--gray-light` | #F2F4F6 | Alternate section background |
| `--white` | #FFFFFF | Page background |

Contrast rules (checked against WCAG AA):
- Bright cyan on white is 2.35:1. Never use it for text or icons that carry meaning on a light background. On navy it passes (6.55:1).
- Deep cyan on white passes (4.61:1) but fails on light gray (4.18:1). Inside gray sections, links are navy and underlined.
- White text on deep cyan buttons passes (4.61:1). Keep button text at least 16px.

Type:
- Headings: Bricolage Grotesque (weights 500, 600, 800), from Google Fonts for this preview.
- Body: Public Sans as the starting choice, set through a `--font-body` variable so it can be swapped in one line. It was designed for US government websites and reads clearly at small sizes. The body font is not final; Michael decides at his review.
- Set a clear type scale as CSS variables. Body text 17px to 18px, line height about 1.6, line length under 75 characters.

## Design direction

- The bridge is the brand idea: connecting business and technology, with a nod to Detroit. Let the bridge mark carry the one memorable moment, in the homepage hero. Keep everything around it quiet and disciplined.
- Motion: one moment only, the cyan line drawing across the bridge on the homepage hero. Respect `prefers-reduced-motion` by showing the finished state. No fade or slide effects on scroll, no hover animation on every card.
- Avoid the generic template look: no rows of identical rounded cards with soft shadows, no gradient washes, no all caps labels above headings, no arrow characters added to links, no single highlighted word inside a headline.
- Numbered markers only where the content is a real sequence, such as the "How we work" steps.
- Visuals listed in each page's build notes are drawn as inline SVG or CSS in brand colors. No stock photos and no remote images.
- Screenshots that Shahbaz will supply get a placeholder box with a light gray fill and a label naming the screenshot, for example "Screenshot: Chemico application (blurred), supplied by Shahbaz".

## Technical rules

- Plain HTML, CSS and a small amount of vanilla JavaScript. No frameworks, no Tailwind, no build step. This keeps the WordPress conversion simple.
- One stylesheet: `site/assets/css/main.css`. One script: `site/assets/js/main.js`. CSS custom properties for every color, font and spacing value.
- Each page lives at `site/<slug>/index.html` so URLs match the final WordPress slugs exactly. The homepage is `site/index.html`.
- All internal links are root relative (`/services/cloud-cybersecurity/`), exactly as in the copy.
- Every slug linked from a built page must resolve. For pages not written yet, create a stub with the site header and footer, the page name as `<h1>` and one line: "This page is being written." Mark stubs with `<meta name="robots" content="noindex">`.
- The site header, footer and each repeated section are copied identically into every page, wrapped in comments that name the WordPress template part they will become:
  `<!-- part: header -->` ... `<!-- /part: header -->`
  Use these part names: `header`, `footer`, `hero`, `card-list`, `steps`, `case-study`, `cta-band`, `needs-input`, `service-section`, `timeline`. Add new names only when no existing one fits, and list them in your report.
- Class names describe content, not appearance: `.service-list`, `.case-study`, not `.blue-box`.
- This is a private preview, hosted on GitHub Pages at a custom subdomain so root relative links work. Every page carries `<meta name="robots" content="noindex, nofollow">`, and `site/robots.txt` blocks all crawlers. Never remove these; they come off only at the WordPress launch.
- Do not edit `.github/workflows/pages.yml`. Merging into `main` publishes the preview, and that is Shahbaz's decision.
- Booking buttons always read "Book a 30 minute call" and link to `/contact/`.

## Responsive and accessibility floor

- Mobile first. Check every page at 375px, 768px and 1280px wide. Nothing scrolls sideways.
- Navigation collapses to a menu button on small screens. The button uses `aria-expanded` and works with the keyboard.
- Touch targets at least 44 by 44 pixels.
- Semantic landmarks (`header`, `nav`, `main`, `footer`), one `h1` per page, headings in order, a "Skip to content" link.
- Visible keyboard focus on every interactive element.
- Decorative SVGs get `aria-hidden="true"`; meaningful ones get a text label.
- Add `lang="en"`, a viewport meta tag, the favicon, a canonical link and basic Open Graph tags on every page.

## How you work

1. Read the task file, the copy files it names and this file.
2. Before your first build in a task that introduces new layouts, write or update `docs/DESIGN_PLAN.md`: tokens, type scale, a short ASCII wireframe per new layout, and the reasoning behind each choice. Stop and wait for Shahbaz to approve it before writing code.
3. Build. Check your own work at the three widths, using screenshots if a browser tool is available.
4. Commit on a branch named for the task (for example `build/task-1`). Never commit to `main` and never push. Shahbaz reviews, pushes and merges.
5. Finish with a short report:
   - Pages built and stubs created
   - Copy issues found (left unchanged)
   - Placeholders added (screenshots, needs input)
   - Decisions you made that Shahbaz or Michael should confirm
   - How you checked mobile, tablet and desktop, and anything you could not check
