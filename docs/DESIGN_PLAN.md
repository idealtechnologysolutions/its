# Design plan: ITS preview site (Build task 1, Part A)

Status: **approved by Shahbaz on 2026-10-12**, with the answers recorded in section 8.

Covers the design system, the homepage (`content/homepage.md`) and the Managed IT & Infrastructure page (`content/pillar-1-managed-it.md`). Task 2 reuses the same parts for the other service pages.

---

## 1. Color tokens

All colors live as custom properties on `:root` in `main.css`. No hex value appears anywhere else in the stylesheet or in inline SVG (SVGs use `currentColor` or `var(--…)` through classes).

### Brand tokens (from CLAUDE.md)

| Token | Hex | Where it is used |
|---|---|---|
| `--navy` | #0B2545 | All body text and headings on light backgrounds. Background of the "Why ITS" and history sections and the footer. Bridge mark on light backgrounds. Industry icons. Michigan on the map. |
| `--cyan` | #12B8DE | Decoration only on light backgrounds: the bridge deck line, the hero line animation, the Atlanta area ring, accent strokes in icons. On navy it may carry meaning: timeline line and markers, the button on navy, focus ring on navy. |
| `--cyan-deep` | #0A7FA0 | Links and buttons on white. Service icons (line art). |
| `--gray-light` | #F2F4F6 | Alternate section background. Screenshot placeholder fill. |
| `--white` | #FFFFFF | Page background. Text on navy and on deep cyan buttons. |

### Supporting tokens (new, need your OK)

These are needed for states the brand table does not cover. Every one is checked for contrast.

| Token | Hex | Use | Contrast |
|---|---|---|---|
| `--navy-soft` | #44546A | Secondary text (footer legal line, placeholder labels) | 7.7:1 on white, 7.0:1 on gray |
| `--on-navy-soft` | #B8C4D3 | Secondary text on navy (footer address line, copyright) | 8.7:1 on navy |
| `--rule` | #C9D1DA | Hairline dividers between list rows. Decorative only. | n/a |
| `--grid-line` | navy at 7% opacity | Street grid texture in the homepage hero. Decorative only. | n/a |
| `--amber-border` | #B7791F | Dashed border of `.needs-input` | 3.6:1 on white (passes 3:1 for UI) |
| `--amber-text` | #8A4B00 | "Needs input" label | 6.4:1 on its fill |
| `--amber-fill` | #FFF8EB | `.needs-input` background, so the marker reads the same on white, gray or navy | n/a |

### Contrast rules, applied

- **Bright cyan never carries meaning on white or gray.** It appears there only as decoration (deck line, icon accents, the Atlanta ring, which the paragraph also describes in words).
- **Links on white:** `--cyan-deep`, underlined, hover to navy. 4.61:1.
- **Links inside gray sections:** `--navy`, underlined. (Deep cyan is 4.18:1 on gray, which fails.) Handled with one rule: `.section--gray a:not(.button) { color: var(--navy); }`.
- **Links on navy:** white, underlined, hover to cyan.
- **Buttons on white and gray:** `--cyan-deep` fill, white text, 17px Public Sans 600 (never under 16px). Hover and active: navy fill.
- **Buttons on navy:** `--cyan` fill, navy text (6.55:1). Deep cyan on navy is only 3.3:1 as a shape, so the button swaps rather than reusing the light version.
- **Focus ring:** `--focus-ring` variable, navy on light sections and cyan on navy sections. 3px outline, 3px offset, on every link, button and form control via `:focus-visible`.

---

## 2. Typography

Fonts from Google Fonts for the preview (one request, `display=swap`):

- Headings: **Bricolage Grotesque**, weights 500, 600, 800, optical size axis on (`font-optical-sizing: auto`), so big headings tighten and small ones open up.
- Body: **Public Sans** 400, 400 italic and 600, set through `--font-body`. Swapping the body font is one line plus the Google Fonts URL.

```css
--font-heading: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
--font-body:    "Public Sans", "Segoe UI", system-ui, sans-serif;
```

### Type scale

Fluid sizes with `clamp()`, from 375px to 1280px wide. Root stays at 16px so browser zoom and user font settings still work.

| Token | 375px | 1280px | Font, weight | Line height | Used for |
|---|---|---|---|---|---|
| `--text-display` | 40px | 68px | Bricolage 800, -0.025em | 1.04 | Homepage `h1` only |
| `--text-h1` | 36px | 54px | Bricolage 800, -0.02em | 1.06 | Service page `h1` |
| `--text-h2` | 28px | 40px | Bricolage 600, -0.015em | 1.15 | Section headings |
| `--text-h3` | 21px | 25px | Bricolage 600 | 1.25 | Service summaries, case studies |
| `--text-numeral` | 32px | 48px | Bricolage 500 | 1.0 | Timeline years, step numbers |
| `--text-lede` | 19px | 22px | Public Sans 400 | 1.5 | Hero paragraph |
| `--text-body` | 17px | 18px | Public Sans 400 | 1.6 | All running text, lists |
| `--text-small` | 15px | 15px | Public Sans 400 / 600 | 1.5 | Footer legal, placeholder labels, "Needs input" label |
| `--text-button` | 17px | 17px | Public Sans 600 | 1.2 | Buttons, nav links |

- Line length: `--measure: 66ch` on every text block (about 640px at 18px), well under 75 characters.
- Headings sit closer to the text below than to the text above (margin top 2x, bottom 0.5x), so each heading clearly belongs to its section.
- No all caps anywhere, no eyebrow labels above headings, no highlighted single words.

---

## 3. Spacing, width and grid

### Spacing scale (4px base)

| Token | Value | Typical use |
|---|---|---|
| `--space-1` | 4px | Icon to label |
| `--space-2` | 8px | Tight stacks |
| `--space-3` | 12px | List item gaps |
| `--space-4` | 16px | Paragraph spacing |
| `--space-5` | 24px | Grid gap on mobile, heading to body |
| `--space-6` | 32px | Grid gap on desktop |
| `--space-7` | 48px | Between blocks inside a section |
| `--space-8` | 64px | Section padding on mobile |
| `--space-9` | 96px | Section padding on tablet |
| `--space-10` | 128px | Section padding on desktop (hero only) |

`--section-pad: clamp(64px, 6vw + 40px, 112px)` gives sections their vertical rhythm.

### Width

- `--page-max: 1200px` content width.
- `--gutter: clamp(20px, 5vw, 48px)` side padding. At 375px that is 20px a side and 335px of content.
- `--measure: 66ch` for text.

### Grid and breakpoints

CSS custom properties cannot be used inside media queries, so the breakpoints are fixed values, documented at the top of `main.css`:

| Name | Width | What changes |
|---|---|---|
| base | 0 to 767px | One column. Menu button. Designed at 375px. |
| `md` | 768px | Two column lists. Header shows the booking button beside the menu button. |
| `lg` | 1080px | Full navigation. The "split" layout: section heading in the left 4 of 12 columns, content from column 6 to 12. |

The **split layout** is the backbone of the site. Every content section reads the same way: heading on the left, text on the right, hairline rule across the top. It is calm, easy to scan, and maps to one WordPress block pattern.

Corners: 4px radius on buttons and the menu panel only. Sections, placeholders and lists are square. No box shadows anywhere; separation comes from rules and background changes.

---

## 4. Wireframes

Legend: `[Button]` is a button, `__text__` is a link, `{ICON}` is an inline SVG, `░` is a gray-light fill, `▓` is navy, `═` is the cyan deck line, `┄` is a dashed amber needs-input box.

### 4.1 Site header and navigation  (`part: header`)

Desktop, 1080px and up:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [skip to content, visible on focus only]                                     │
│ {MARK} Ideal Technology      Services ▾  Industries ▾  Our Work  About       │
│        Solutions                                       [Book a 30 minute call]│
└──────────────────────────────────────────────────────────────────────────────┘
                          ┌──────────────────────────────────┐
  Services ▾ opens:       │ Managed IT & Infrastructure       │  white panel,
                          │ Cloud & Cybersecurity             │  1px rule border,
                          │ Custom Software & Digital Products│  navy 3px top edge,
                          │ Data, AI & Automation             │  44px tall rows
                          │ Digital Transformation & ...      │
                          └──────────────────────────────────┘
```

- `Services` and `Industries` are **buttons** with `aria-expanded`, not links, because the brief has no `/services/` or `/industries/` index page and I must not invent a slug. Escape closes a panel and returns focus to its button; clicking outside closes it.
- The `▾` is a small CSS chevron, not a text character.
- Current page gets `aria-current="page"` and a 2px navy underline.

Tablet 768px:

```
┌──────────────────────────────────────────────┐
│ {MARK} Ideal Technology   [Book a 30 min…] [≡ Menu] │
│        Solutions                              │
└──────────────────────────────────────────────┘
```

Mobile 375px (menu closed, then open):

```
┌───────────────────────────────┐   ┌───────────────────────────────┐
│ {MARK} Ideal Technology [Menu]│   │ {MARK} Ideal Technology [Close]│
│        Solutions              │   │        Solutions               │
└───────────────────────────────┘   ├───────────────────────────────┤
                                    │ Services                       │  group label
                                    │   Managed IT & Infrastructure  │  48px rows
                                    │   Cloud & Cybersecurity        │
                                    │   … (5)                        │
                                    │ Industries                     │
                                    │   Government & Public Sector   │
                                    │   … (7)                        │
                                    │ Our Work                       │
                                    │ About                          │
                                    │ [Book a 30 minute call]        │  full width
                                    └───────────────────────────────┘
```

- One menu button, 48x48px, labeled "Menu" in text plus an icon, `aria-expanded` and `aria-controls`. Inside the open mobile panel, Services and Industries are plain group headings with their links listed, not nested toggles, so nothing hides two levels deep on a phone.
- The panel pushes the page down (no overlay, no slide animation). Escape closes it and returns focus to the button.
- Without JavaScript, the nav renders open below the logo on small screens, so every link is still reachable.

### 4.2 Homepage hero  (`part: hero`, `.hero--home`)

Desktop:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                         ╲   │   ╱  street grid texture,       │
│  Metro Detroit IT support                ╲  │  ╱   very faint navy lines,     │
│  and custom software                  ────╲─┼─╱────  right half only          │
│  since 2001                     (h1)       ▐▌            ▐▌                    │
│                                            ▐▌╲          ╱▐▌                    │
│  Ideal Technology Solutions keeps          ▐▌ ╲│ │ │ │╱ ▐▌                    │
│  your computers, network and cloud    ═════▐▌══════════▐▌═════  cyan deck     │
│  running, and builds the software…  (lede)                        draws L→R    │
│                                                                                │
│  [Book a 30 minute call]                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
   text: columns 1–6                        bridge: columns 7–12, about 520px
```

Mobile:

```
┌───────────────────────────────┐
│ Metro Detroit IT              │
│ support and custom            │
│ software since 2001     (h1)  │
│                               │
│ Ideal Technology Solutions    │
│ keeps your computers…  (lede) │
│                               │
│ [Book a 30 minute call]       │  full width button
│                               │
│   ▐▌╲            ╱▐▌          │  bridge below the text,
│   ▐▌ ╲│ │ │ │ │ ╱ ▐▌          │  full content width (max 360px),
│ ══▐▌══════════════▐▌══        │  texture behind it only
└───────────────────────────────┘
```

Text comes first in the source and on mobile, so the `h1` and the button are on screen without scrolling at 375px.

### 4.3 The five service summaries  (`part: card-list`, `.service-list`)

Not a row of cards. A ruled index: one row per service, navy 2px rule on top of the list, hairline rules between rows. White section.

Desktop:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ What we do (h2)                                                               │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ ░{ICON}░  Managed IT &          We look after your computers, servers and     │
│ ░░░░░░░░  Infrastructure (h3)   network. We also manage Microsoft 365 …       │
│                                 __Learn about managed IT__                    │
│ ───────────────────────────────────────────────────────────────────────────── │
│ ░{ICON}░  Cloud & Cybersecurity We set up secure Microsoft cloud services …   │
│                                 __Learn about cloud and security__            │
│ ───────────────────────────────────────────────────────────────────────────── │
│   … three more rows                                                           │
└──────────────────────────────────────────────────────────────────────────────┘
  icon tile 64px | title cols 2–5 | text and link cols 6–12 (measure-limited)
```

Mobile:

```
┌───────────────────────────────┐
│ What we do                    │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ ░{ICON}░ Managed IT &         │
│          Infrastructure       │
│ We look after your computers, │
│ servers and network. …        │
│ __Learn about managed IT__    │
│ ───────────────────────────── │
│ … four more                   │
└───────────────────────────────┘
```

Icons: server and laptop, shield over cloud, code window, bar chart with spark, roadmap. Drawn as 2px line art in deep cyan with one bright cyan accent stroke each, on a 64px gray-light square tile. See decision D3.

### 4.4 Industries list  (section: industries)

A compact directory, not cards: each industry is one full-row link with a 28px navy icon. Copy order kept (Government first). Gray-light section, so links are navy.

Desktop:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Who we work with   │ ┌─────────────────────────────┬────────────────────────┐ │
│ (h2)               │ │{i} Government & Public      │{i} Healthcare          │ │
│                    │ │    Sector                   │                        │ │
│                    │ ├─────────────────────────────┼────────────────────────┤ │
│                    │ │{i} Automotive               │{i} Manufacturing       │ │
│                    │ ├─────────────────────────────┼────────────────────────┤ │
│                    │ │{i} Retail & Service         │{i} Education,          │ │
│                    │ │                             │    including K-12      │ │
│                    │ ├─────────────────────────────┼────────────────────────┤ │
│                    │ │{i} Nonprofits & Community   │                        │ │
│                    │ │    Organizations            │                        │ │
│                    │ └─────────────────────────────┴────────────────────────┘ │
│                    │ Public agencies and K-12 schools get a written scope …   │
└──────────────────────────────────────────────────────────────────────────────┘
```

Mobile: the same list in one column, each row at least 56px tall, hairline rules between rows, paragraph below.

### 4.5 Selected work  (`part: case-study`, one per project)

White section. The first project gets a wide row; the next two sit side by side. No card borders or shadows; each project is an image placeholder, a heading, a paragraph and a link.

Desktop:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Selected work (h2)                                                            │
│ ┌──────────────────────────────────────┐  Sean Anderson Foundation (h3)       │
│ │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  The foundation wanted a site its    │
│ │░ Screenshot: Sean Anderson ░░░░░░░░░│  own staff could keep current …      │
│ │░ Foundation website, supplied by ░░░│  __Read the Sean Anderson Foundation │
│ │░ Shahbaz ░░░░░░░░░░░░░░░░░░░░░░░░░░│    story__                            │
│ └──────────────────────────────────────┘                                      │
│ ┌──────────────────────────────────┐  ┌──────────────────────────────────┐    │
│ │░ Screenshot: Chemico application │  │░ Screenshot: DPSCD Foundation    │    │
│ │░ (blurred), supplied by Shahbaz ░│  │░ website, supplied by Shahbaz ░░░│    │
│ └──────────────────────────────────┘  └──────────────────────────────────┘    │
│ The Chemico Group (h3)                 DPSCD Foundation (h3)                  │
│ Chemico first came to us for web …     Donors want to see the work before …   │
│ __Read the Chemico story__             __Read the DPSCD Foundation story__     │
│                                                                                │
│ __See all our work__                                                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

Mobile: one column, placeholder (16:10) above each heading.

Placeholders: gray-light fill, 1px dashed `--navy-soft` border, label centered in `--text-small`. Marked `role="img"` with the label as its accessible name, so a screen reader announces the gap too.

### 4.6 "Why ITS" and "Where we work"  (`part: timeline` inside "Why ITS")

"Why ITS" is the one navy section on the homepage. The timeline sits under the heading and reads 2001, 2004, Today along a cyan deck line. The three paragraphs follow in the right column.

Desktop:

```
┌▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┐
▓ Why ITS (h2, white)                                                          ▓
▓                                                                              ▓
▓  2001              2004                                     Today            ▓
▓  ●═════════════════●══════════════════════════════════════════●              ▓
▓                                                                              ▓
▓                     │ We opened in 2001, supporting Windows, Novell, Cisco …  ▓
▓                     │ … Today our headquarters is in __Southfield, Michigan__.▓
▓                     │                                                         ▓
▓                     │ Our monitoring systems check your computers …           ▓
▓                     │                                                         ▓
▓                     │ We don't publish a price list. …                        ▓
└▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┘
```

The gap between 2004 and Today is drawn to scale (3 years vs 22 years), which quietly makes the 25-year point. Mobile: the timeline turns vertical (years down the left edge), then the paragraphs.

"Where we work" is white, split layout, with the map beside the two paragraphs.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Where we work (h2)          │  Metro Detroit and Michigan are home. …         │
│                             │                                                 │
│ ┌───────────────────────┐   │  We also work with clients in the Atlanta …     │
│ │  faint gray US         │   │                                                 │
│ │        ▓▓ Michigan ●   │   │                                                 │
│ │           Southfield   │   │                                                 │
│ │      ◯ Atlanta area    │   │                                                 │
│ └───────────────────────┘   │                                                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

Mobile: heading, paragraphs, then map at full width.

Map: generalized lower-48 outline in faint gray, Michigan (both peninsulas) solid navy with a cyan pin at Southfield (cyan with a navy ring so it holds up on white), and a cyan ring around the Atlanta area with no pin. Two small navy labels, "Southfield" and "Atlanta area" (see D5). The SVG has `role="img"` and an `aria-label`. I will generate the outline from public-domain US Census boundaries (the `us-atlas` dataset), projected and simplified to keep the inline SVG small; nothing loads remotely at runtime.

### 4.7 Closing call to action band  (`part: cta-band`)

Gray-light, split layout. Same part on every page; only the heading and paragraph change.

```
Desktop
┌░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░┐
░ Talk to a client advisor (h2)   │ Book a 30 minute appointment with a client  ░
░                                 │ advisor. Tell us what you need, and we …    ░
░   {small bridge mark, navy}     │                                             ░
░                                 │ [Book a 30 minute call]                     ░
└░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░┘

Mobile
┌░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░┐
░ Talk to a client advisor      ░
░ Book a 30 minute appointment… ░
░ [Book a 30 minute call]       ░  full width
└░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░┘
```

The small bridge mark is the logo file itself (`<img>`, `alt=""`), shown from `lg` up only.

### 4.8 Service page hero  (`part: hero`, `.hero--service`)

Same part as the homepage hero, quieter: smaller `h1`, no street grid, no animation.

```
Desktop
┌──────────────────────────────────────────────────────────────────────────────┐
│ Technology that keeps your           ┌──┐            ●───●                   │
│ business running (h1)                │▤▤│ ▐▌╲    ╱▐▌  │ ╲ │                   │
│                                      │▤▤│ ▐▌ ╲││╱ ▐▌  ●───●                   │
│ We look after the computers,         │▤▤│═▐▌═════▐▌═══ ●                     │
│ networks and software …  (lede)    building   bridge    network nodes        │
│                                                                                │
│ [Book a 30 minute call]                                                        │
└──────────────────────────────────────────────────────────────────────────────┘

Mobile: h1, lede, button, then the illustration at full width (max 360px).
```

The illustration is static. See D2 for the "slow pulse" in the build notes.

### 4.9 Service sub-section  (`part: service-section`, new name)

Used five times on this page (Managed IT Services, IT Support, Network Design, Hardware & Software Sales, Microsoft 365 & Licensing) and on every pillar page in task 2. White, hairline rule on top, split layout. A section can hold an optional diagram after its text.

```
Desktop
┌──────────────────────────────────────────────────────────────────────────────┐
│ ──────────────────────────────────────────────────────────────────────────── │
│ ░{ICON}░                    │ Our monitoring tools check your computers and   │
│ Managed IT Services (h2)    │ servers all day, every day, weekends included.… │
│                             │                                                 │
│                             │ Each client gets a structured service plan …    │
│                             │                                                 │
│                             │ ▪ Automated monitoring of computers and servers…│
│                             │ ▪ Email alerts sent at any hour                 │
│                             │ ▪ …                                             │
│                             │                                                 │
│                             │ Security, backup and cloud services are covered │
│                             │ on our __Cloud & Cybersecurity page__.          │
│                             │                                                 │
│                             │ ┌ diagram ──────────────────────────────────┐   │
│                             │ │ {computer}──{check}──{envelope}──{team}    │   │
│                             │ └───────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘

Mobile: icon, h2, text, list, diagram, all in one column. The flow diagram
turns vertical below 768px.
```

List bullets are small navy squares (a nod to the bridge towers), not dots or check marks.

**Diagrams on this page**
- Monitoring flow (in Managed IT Services): computer and server, automated check, email alert at any hour, team response in business hours.
- Network diagram (in Network Design): main office, second site and a remote worker connected through a firewall; cameras and sensors on their own separate segment.

The other content sections on this page (intro, government and K-12, pricing) use the same split layout without an icon. "For government and K-12 buyers" is gray-light, so it stands apart for public buyers. "Supporting Metro Detroit businesses since 2001" is navy with the same `timeline` part as the homepage, and holds the case study needs-input marker.

### 4.10 Steps layout  (`part: steps`)

Neither task 1 page has a numbered sequence, so this part is designed now and first used in task 2 (Pillar 5, "How we work": three numbered steps). The number is the real step order, set as a large Bricolage numeral, connected by a thin navy line.

```
Desktop (3 steps)
┌──────────────────────────────────────────────────────────────────────────────┐
│ How we work (h2)                                                              │
│                                                                                │
│  1 ─────────────────────────  2 ─────────────────────────  3                   │
│  We assess what you have (h3) We recommend a plan in       You decide what     │
│                               writing (h3)                 happens next (h3)   │
│  We meet your team, review    You receive a written …      You choose what …   │
│  your systems …                                                                │
└──────────────────────────────────────────────────────────────────────────────┘

Mobile
┌───────────────────────────────┐
│ 1 │ We assess what you have   │   numbers in a left rail,
│   │ We meet your team, …      │   navy line runs down the rail
│ 2 │ We recommend a plan …     │
│   │ You receive a written …   │
│ 3 │ You decide what happens … │
└───────────────────────────────┘
```

Markup is an `<ol>`, so the order is real for screen readers. The visible number comes from the list counter; the copy's "1." prefix is not duplicated.

### 4.11 Case study block  (`part: case-study`)

The same part as 4.5, in two sizes. On pillar pages the wide version is the default: placeholder left (5 columns), text right. Where a page has no case study yet (Pillar 1), the slot holds the needs-input marker instead.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ┌──────────────────────────────┐   The Chemico Group: Credit Hold … (h3)     │
│ │░ Screenshot: Chemico ░░░░░░░│   ITS first provided web services for …     │
│ │░ application (blurred), ░░░░│   __Read the case study__                    │
│ │░ supplied by Shahbaz ░░░░░░░│                                              │
│ └──────────────────────────────┘                                              │
└──────────────────────────────────────────────────────────────────────────────┘

Pillar 1, no case study yet:
┌┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┐
┆ Needs input                         ┆   part: needs-input
┆ case study for this page            ┆   dashed amber border, amber fill,
└┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘   small amber label, navy text
```

When a needs-input marker sits inside a paragraph (government paragraph on Pillar 1), it renders inline as a `<span class="needs-input">` on its own line after the sentence, so the paragraph text is untouched.

### 4.12 Footer  (`part: footer`)

Navy, with a 4px cyan rule along its top edge: the deck line from the logo.

```
Desktop
═══════════════════════════════════════════════════════════════════════════════ cyan
┌▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┐
▓ {MARK reversed}         Services             Industries           Company    ▓
▓ Ideal Technology        Managed IT & …       Government & …       About      ▓
▓ Solutions               Cloud & …            Healthcare           Our Work   ▓
▓ Southfield, Michigan    Custom Software …    Automotive           Contact    ▓
▓                         Data, AI & …         Manufacturing                   ▓
▓ ┄ Needs input ┄┄┄┄┄┄┄┄  Digital Trans…       Retail & Service                ▓
▓ ┆ footer contact     ┆                       Education                       ▓
▓ ┆ details            ┆                       Nonprofits & Community …        ▓
▓ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄                                                       ▓
▓ ──────────────────────────────────────────────────────────────────────────── ▓
▓ © 2026 Ideal Technology Solutions                                             ▓
└▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┘

Tablet: logo block full width, then the three link columns.
Mobile: logo block, then Services, Industries, Company stacked;
        each link at least 44px tall.
```

Column labels ("Services", "Industries", "Company") are footer labels, which the task allows. Each column is a `<nav aria-label="…">`.

---

## 5. The bridge mark in the homepage hero

**Construction.** The hero bridge is an inline SVG redrawn from the geometry of `logo-mark.svg` (two towers, the cable curve, five suspenders, the deck), scaled to about 520px wide on desktop. It has to be inline so CSS can animate the deck. Everywhere else (header, footer, CTA band) the logo is an `<img>` pointing at the files in `site/assets/brand/`, so swapping the designer's final files updates those places with no code change. The hero SVG and the service hero illustration are the only two places that copy the geometry; both are marked with a `<!-- logo geometry: update when final vectors arrive -->` comment.

- Towers, cable and suspenders: navy.
- Deck: a single cyan stroke (`<line>` with `pathLength="1"`), extended a little past each tower so it reads as a road meeting land on both sides: business on one side, technology on the other.
- Behind the bridge: the street grid texture, in very faint navy. It is drawn from Detroit's real street plan: Woodward, Gratiot, Grand River and Michigan Avenue fanning out from the riverfront, crossed by the mile road grid that runs north through Southfield. Abstracted, no labels, no map accuracy claimed. It covers only the bridge's half of the hero so the text stays on clean white.
- `aria-hidden="true"` on the whole illustration. It is decorative; the `h1` says what matters.

**The one animation.** On page load the cyan deck draws from left to right across the bridge, once.

```css
/* Finished state is the default. */
.hero-bridge__deck { stroke-dasharray: 1; stroke-dashoffset: 0; }

@media (prefers-reduced-motion: no-preference) {
  .hero-bridge__deck {
    stroke-dashoffset: 1;
    animation: deck-draw 1.4s cubic-bezier(0.65, 0, 0.35, 1) 0.3s forwards;
  }
}
@keyframes deck-draw { to { stroke-dashoffset: 0; } }
```

- CSS only, no JavaScript. Runs once, does not loop, does not replay on scroll.
- With reduced motion turned on, the rule never applies, so the finished bridge shows from the first frame. The same is true in any browser that does not run CSS animations.
- Nothing else on the site moves: no scroll reveals, no hover lifts. Links change color and buttons change fill on hover, instantly.

---

## 6. What makes this ITS and not a template

A generic IT company site leads with a stock photo of a server room, a gradient, and a grid of identical rounded cards with icons. This design is built from the one thing only ITS owns: the bridge. The logo's cyan deck becomes the site's structural line: it draws across the hero, runs the 2001 to today timeline, and caps the footer. The faint texture behind the hero is Detroit's own street plan, Woodward's avenues spreading from the river and the mile roads running up to Southfield, which says "Metro Detroit since 2001" before anyone reads the headline. The page structure is borrowed from engineering drawings rather than marketing templates: a strict heading-left, text-right layout, ruled lists instead of cards, square edges, and real numbers drawn to scale (the long stretch between 2004 and today is the 25 years). It is quiet on purpose, so the one moment that moves, the deck drawing across the bridge, is the thing a visitor remembers.

---

## 7. Template parts

Existing names used: `header`, `footer`, `hero`, `card-list`, `steps`, `case-study`, `cta-band`, `needs-input`.

New names proposed (need your OK):
- `service-section`: a service sub-section (heading, icon, text, optional list and diagram). Repeats five times on Pillar 1 and on every pillar page.
- `timeline`: the 2001, 2004, Today strip. Used on the homepage and Pillar 1, and likely Pillar 5.

Sections that appear on only one page (industries list, map) are wrapped in `<!-- section: name -->` comments instead, so the converter can see they belong to that page's template and are not shared parts.

---

## 8. Decisions (approved 2026-10-12)

Shahbaz's answers:
- D1 yes, D2 keep the Managed IT hero still, D3 yes, D4 keep the copy order (it matches the industry priority in the brief), D5 short phrases taken word for word from the copy.
- D6 canonical and Open Graph base: `https://idealtechnologysolutions.us` (no www).
- D7 and D8 approved. `service-section` and `timeline` are added to the part names in CLAUDE.md.
- This plan lives at `docs/DESIGN_PLAN.md`, outside the published `site/` folder.

The original questions follow for the record.

**D1. Cross links in Pillar 1.** The copy has no inline links, but the build notes list cross links. I plan to link existing words without changing any text:
- "Cloud & Cybersecurity page" (Managed IT Services) and "Firewalls" (Network Design) to `/services/cloud-cybersecurity/`
- "Technology lifecycle management…" and "Infrastructure modernization…" bullets to `/services/digital-transformation-consulting/`
- "Public agencies" to `/industries/government-public-sector/`, "school districts" to `/industries/education/`
- "production line" to `/industries/manufacturing/`
- "ITS started in 2001" (history section) to `/about/`
- Both "Book a 30 minute call" buttons to `/contact/` (the copy gives no target; CLAUDE.md does)

**D2. No pulse on the service hero.** Pillar 1's build notes ask for a "slow CSS pulse across the bridge". CLAUDE.md allows one motion moment on the whole site, the homepage hero. I plan to keep the service hero static. Pillar 3's notes also ask for "subtle CSS animation along the lines"; I would treat that the same way in task 2.

**D3. Service icon color.** The homepage notes say "cyan line icons on light gray"; Pillar 1 says "deep cyan line icons". Bright cyan on gray is about 2.2:1 and looks washed out. I plan one icon family for both pages: deep cyan lines (passes 3:1 for graphics) with one bright cyan accent stroke, on a gray-light tile.

**D4. Industry order.** The homepage notes say "Government and Education first", but the copy lists Education sixth and CLAUDE.md says never reorder. I plan to keep the copy order. If Education should move up, please change it in `content/homepage.md`.

**D5. Words inside diagrams.** Small labels make the diagrams readable, but they would be text that is not in `content/`. I plan to use only short phrases lifted verbatim from the paragraph each diagram illustrates, and to mark the SVGs `aria-hidden` (the paragraph already says it all):
- Map: "Southfield", "Atlanta area"
- Timeline: "2001", "2004", "Today"
- Monitoring flow: "computers and servers", "monitoring tools", "email alert", "our team"
- Network: "offices", "more than one location", "working from home", "Firewalls", "security cameras", "sensors"

The alternative is icon-only diagrams with no words. Tell me which you prefer.

**D6. Canonical URL.** Every page needs a canonical link and Open Graph URL, which must be absolute. The repo has no custom domain set. Which base should I use: the final production domain (please confirm it), or the preview subdomain? I will not guess a domain.

**D7. Supporting colors.** Approve the seven supporting tokens in section 1 (`--navy-soft`, `--on-navy-soft`, `--rule`, `--grid-line`, and the three amber tokens for needs-input).

**D8. New part names.** Approve `service-section` and `timeline` (section 7).

**D9. Section backgrounds.** Homepage order: hero white, What we do white, Who we work with gray, Selected work white, Why ITS navy, Where we work white, CTA gray, footer navy. Pillar 1: everything white with hairline rules, except government and K-12 (gray), history (navy) and the CTA (gray).

---

## 9. Copy notes found while planning (left unchanged)

- Pillar 1, Hero and closing: `[Book a 30 minute call]` has no link target in the copy. I will link it to `/contact/` per CLAUDE.md.
- Pillar 1 has no inline links even though its build notes list cross links (see D1).
- Homepage build notes ask for Government and Education first; the copy order differs (see D4).
- `PROJECT_BRIEF.md` gives the standard CTA as "30-minute appointment" with a hyphen; the copy and CLAUDE.md both use "30 minute" with no hyphen. I will follow the copy.
