# Build task 2: the other four service pages

## Goal

Build the remaining four service pages from the parts approved in task 1, so Michael can review the homepage and all five service pages together. The design is approved. Reuse the existing parts; do not restyle anything that already exists.

## Pages

Build each page from its copy file, replacing its stub:

| Page | Copy file |
|---|---|
| /services/cloud-cybersecurity/ | content/pillar-2-cloud-cybersecurity.md |
| /services/custom-software-digital-products/ | content/pillar-3-custom-software.md |
| /services/data-ai-automation/ | content/pillar-4-data-ai-automation.md |
| /services/digital-transformation-consulting/ | content/pillar-5-digital-transformation.md |

## Notes

1. **Steps layout.** The "How we work" steps on the Digital Transformation page are the first real use of the `steps` part from the design plan. Build it as planned.
2. **Case studies.** Several pages mention The Chemico Group and other clients. Use the `case-study` part with labeled screenshot placeholders, as on the homepage.
3. **Visuals.** Draw the visuals listed in each page's build notes as inline SVG, in the same style as the task 1 diagrams. Where a build note asks for motion, keep the visual still; the homepage hero is the only animation.
4. **Conflicts.** If a build note conflicts with CLAUDE.md or the design plan, follow CLAUDE.md and the plan, and list the conflict in your report.
5. **New parts.** If a page needs a layout no existing part covers, stop and describe it in your report before building it.

## Share image

Create one Open Graph image for the whole site at `site/assets/brand/og-image.png`, 1200 by 630 pixels: the Bridge mark and "Ideal Technology Solutions" in white on navy, with the cyan line. Generate it from an HTML card with your screenshot tool, and keep the source HTML under `tools/`. Add it to every page's head through `tools/generate_pages.py`.

## Before reporting

- Run `tools/generate_pages.py`, then `--check`
- Every link on every built page resolves
- No text inside `<main>` that is not in `content/`, apart from placeholder labels
- No sideways scrolling and no touch targets under 44px at 375, 768 and 1280
- Keyboard check on each new page
- Screenshots of all six built pages in `docs/screenshots/`

Commit on a new branch, `build/task-2`, starting from `build/task-1`. Then write your report.
