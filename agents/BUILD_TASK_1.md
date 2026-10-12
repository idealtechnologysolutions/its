# Build task 1: design system, homepage and first service page

## Goal

Set up the site's design system and build two pages that together cover almost every layout the site needs: the homepage and the Managed IT & Infrastructure service page. Once Shahbaz approves these, the other service pages reuse the same parts in task 2.

## Part A: design plan (stop after this)

Write `docs/DESIGN_PLAN.md` covering:
- Color tokens and where each is used, including the contrast rules in CLAUDE.md
- Type scale (sizes, weights, line heights) for Bricolage Grotesque headings and the Public Sans body
- Spacing scale and page width
- ASCII wireframes, desktop and mobile, for: site header and navigation, homepage hero, the five service summaries, the industries list, selected work, the "Why ITS" and "Where we work" sections, the closing call to action band, the service page hero, a service sub-section, the steps layout, the case study block and the footer
- How the bridge mark appears in the homepage hero and how its one animation works
- One paragraph on what makes this design specific to ITS rather than a generic IT company template

Then stop and wait for approval.

## Part B: build (after approval)

1. Create `site/assets/css/main.css` and `site/assets/js/main.js` from the approved plan.
2. Build `site/index.html` from `content/homepage.md`.
3. Build `site/services/managed-it-infrastructure/index.html` from `content/pillar-1-managed-it.md`.
4. Create stubs for every other slug these two pages link to, following CLAUDE.md.
5. Navigation: Services (the five service pages), Industries (the seven industry pages), Our Work, About, and the "Book a 30 minute call" button. Use the slugs in `agents/PROJECT_BRIEF.md`.
6. Footer: logo, the five services, the seven industries, About, Our Work, Contact, and "Southfield, Michigan". Copyright line: "© 2026 Ideal Technology Solutions". No phone, email or street address yet; add a `[NEEDS INPUT: footer contact details]` marker.
7. Draw the visuals listed in each page's build notes as inline SVG. Use labeled placeholders for screenshots.

## Check before reporting

- Both pages at 375px, 768px and 1280px
- Every link on both pages resolves to a built page or a stub
- Keyboard: tab through each page, open and close the mobile menu
- The hero animation shows its finished state with reduced motion turned on
- No text outside `content/` appears on a page, apart from navigation, footer labels, stub lines and placeholder labels

Then commit on `build/task-1` and write your report.
