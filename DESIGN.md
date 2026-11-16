# DESIGN.md: Guilherme Candeias Martins portfolio

> **A darkroom gallery for an engineer:** warm walnut darkness, cream type and one painting's worth of colour. ORYZO's editorial restraint, painted in the greens, browns and blossoms of Van Gogh.

This file is the design system for the six-page site described in CONTEXT.md and written in COPY.md. It merges five reference style guides with Guilherme's own brand.

**Precedence (decided by Guilherme)**
1. **Colours and fonts:** the brand wins. The brand is built from his stated likes: green, brown, Van Gogh's *Almond Blossoms* and *Sunflowers*. Fonts are Fraunces and Inter.
2. **Layout and feel:** the references win, with **ORYZO as the lead reference**. The other four (Structured, monopo, Freshman, Flying Papers) contribute only the specific items named in section 6.

Anything not covered here defaults to ORYZO's behaviour, re-coloured and re-typeset with the brand.

---

## 1. Colours

**Theme:** dark (warm). One canvas, a two-step surface stack, cream text, and colour used like paint, sparingly.

### Tokens

| Name | Hex | Token | Source | Role |
|---|---|---|---|---|
| Walnut | `#16100a` | `--color-walnut` | Chosen (brown; ORYZO's warm near-black, made slightly browner) | Page canvas. Every page sits on it. |
| Bark | `#2b1f14` | `--color-bark` | Chosen (brown) | Raised surface: expander panels, quote block, header on scroll. |
| Moss | `#1f2a1e` | `--color-moss` | Chosen (green, darkened from Branch) | Alternate band behind the Home highlights and the About exchanges, for variety without leaving the dark. |
| Blossom | `#f4eee2` | `--color-blossom` | Chosen (the almond-blossom petals: warm off-white) | All primary text, headings, button fill, outlines that carry meaning. Replaces pure white everywhere. |
| Sage | `#b8c3aa` | `--color-sage` | Sampled from `almond_blossoms.png` | Secondary text: dates, places, captions, meta lines, footer. |
| Almond Sky | `#7fadb1` | `--color-sky` | Sampled from `almond_blossoms.png` (dominant sky tone) | Inline links and the active nav item. |
| Branch | `#5d7562` | `--color-branch` | Sampled from `almond_blossoms.png` | Non-text graphics only: hairline dividers on Moss, bullet marks, focus-ring outer halo. |
| Sunflower | `#e8b130` | `--color-sunflower` | Chosen (ochre in the spirit of *Sunflowers*; **not** sampled, since there is no image file) | The single accent. At most one element per viewport: the hover state of the email button, the keyboard focus ring and the active language in the EN/PT toggle. |
| Cork | `#3e3528` | `--color-cork` | Chosen (warm, from ORYZO's `#40372e`) | Decorative hairline and dashed dividers on Walnut and Bark. Never the only cue for anything. |

### Contrast (WCAG 2.x, computed)

| Text / mark | on Walnut | on Bark | on Moss | Use allowed |
|---|---|---|---|---|
| Blossom | 16.3:1 | 13.9:1 | 12.9:1 | All text |
| Sage | 10.3:1 | 8.7:1 | 8.1:1 | All text |
| Almond Sky | 7.7:1 | 6.5:1 | 6.0:1 | All text (links) |
| Sunflower | 9.7:1 | 8.2:1 | 7.6:1 | Text and focus ring |
| Branch | 3.8:1 | 3.2:1 | 3.0:1 | Non-text graphics and large text only, **never body text** |
| Cork | 1.6:1 | 1.3:1 | 1.2:1 | Decorative only |
| Walnut text on a Blossom button | 16.3:1 | | | Button label |
| Walnut text on a Sunflower button (hover) | 9.7:1 | | | Button label |

### Rules
- Never use pure `#ffffff` text or a pure `#000000` background. Blossom and Walnut are the system.
- Sunflower appears at most once per viewport and never as a large fill or background block.
- Links are Almond Sky **and** underlined (1px, offset 3px), so they never rely on colour alone.
- No gradients and no shadows anywhere in the interface. The only rich colour lives in the images.

---

## 2. Fonts

| Family | Token | Weights | Role |
|---|---|---|---|
| **Fraunces** (Google Fonts, variable, optical size axis on) | `--font-display` | 300, 400; italic 300 | Headings H1–H3, the hero name, the pull quote. Its soft, slightly painterly serif is the nod to Van Gogh. |
| **Inter** (Google Fonts, variable) | `--font-body` | 400, 500 | Body copy, nav, buttons, labels, meta, footer, lists. |

**Load:** `https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..400;1,9..144,300&family=Inter:wght@400;500&display=swap`
**Fallbacks:** Fraunces → `Georgia, 'Times New Roman', serif` · Inter → `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif`

### Type scale (responsive; mobile → desktop)

| Role | Font | Weight | Size | Line height | Tracking | Case | Token |
|---|---|---|---|---|---|---|---|
| Display (hero name) | Fraunces | 300 | `clamp(2.75rem, 8vw, 6.5rem)` (44→104px) | 0.95 | -0.01em | Mixed | `--text-display` |
| H1 (page title) | Fraunces | 300 | `clamp(2.25rem, 5.5vw, 4rem)` (36→64px) | 1.0 | -0.01em | Mixed | `--text-h1` |
| H2 (section) | Fraunces | 400 | `clamp(1.625rem, 3vw, 2.25rem)` (26→36px) | 1.1 | 0 | Mixed | `--text-h2` |
| H3 (role / project) | Fraunces | 400 | `clamp(1.25rem, 2vw, 1.5rem)` (20→24px) | 1.2 | 0 | Mixed | `--text-h3` |
| Lead (opening lines) | Inter | 400 | `clamp(1.125rem, 1.8vw, 1.5rem)` (18→24px) | 1.45 | 0 | Mixed | `--text-lead` |
| Body | Inter | 400 | `1.0625rem` (17px) | 1.6 | 0 | Mixed | `--text-body` |
| Meta (dates, places) | Inter | 400 | `0.9375rem` (15px) | 1.5 | 0 | Mixed | `--text-meta` |
| Label (nav, buttons, eyebrows) | Inter | 500 | `0.8125rem` (13px) | 1.2 | 0.06em | **UPPERCASE** | `--text-label` |
| Quote | Fraunces | 300 italic | `clamp(1.25rem, 2.4vw, 1.75rem)` | 1.35 | 0 | Mixed | `--text-quote` |

### Rules
- **Two voices, as in ORYZO:** UPPERCASE Inter 500 for anything that labels (nav, buttons, eyebrows, footer headings). Mixed-case for anything you *read*. Headings are mixed-case Fraunces, not uppercase.
- Never bold Fraunces above 400. Large type whispers.
- Body text is never smaller than 15px; labels never below 13px.
- Body measure is capped at 68ch.
- Portuguese runs about 15% longer than English, so no layout may depend on a heading fitting on one line.

---

## 3. Spacing, shapes and layout

**Base unit:** 4px · **Density:** comfortable (spacious between sections, compact within entries)

| Token | Value | Use |
|---|---|---|
| `--space-1` | 4px | Icon gaps |
| `--space-2` | 8px | Meta line gaps |
| `--space-3` | 12px | Label-to-content |
| `--space-4` | 18px | Element gap (ORYZO) |
| `--space-5` | 24px | Card / panel padding (ORYZO) |
| `--space-6` | 40px | Between entries in a list |
| `--space-7` | 68px | Between sections, mobile |
| `--space-8` | 120px | Between sections, desktop |
| `--gutter` | `max(16px, 4vw)` | Page side gutter (16px minimum at phone width) |

### Radius vocabulary (one system)

| Element | Radius | Origin |
|---|---|---|
| Buttons, language toggle, tags | `999px` (full pill) | ORYZO / monopo pill |
| Panels (expander, quote block) | `12px` | ORYZO card radius |
| Images and photos | `0px` | Editorial: images are content, not cards |
| Inputs, links, dividers | `0px` | |

No other radius values are allowed.

### Layout
- **Container:** max-width `1120px`, centred, side gutter `--gutter`. Full-bleed only for the Home hero and the Moss bands.
- **Grid:** 12 columns on desktop, 1 column below 760px.
- **Entry layout (desktop):** a two-column "label / content" row borrowed from ORYZO's flanking text. Dates and place sit in a 3-column left rail in Sage; the content takes 8 columns. On mobile the rail stacks above the content.
- **Section dividers:** 1px dashed Cork (ORYZO), full container width.
- **Sections are content height, not 100vh.** Only the Home hero is near full height (`min-height: 88svh`).
- **Alignment:** headings and body are always left-aligned. Nothing is centred except the hero's scroll cue.
- **No horizontal scroll at any width.**

### Motion
- Easing: `cubic-bezier(0.19, 1, 0.22, 1)` (from monopo) for reveals. Durations: 0.6s for reveals, 0.25s for hover/colour.
- Reveal: content fades and moves up 12px once, on first scroll into view.
- Expander: height animates over 0.4s.
- All motion is disabled under `prefers-reduced-motion: reduce`.

---

## 4. Imagery

- **Hero image:** a crop of `almond_blossoms.png` (from the repo). It sits behind or beside the Home hero as the site's one large painting, edge-to-edge, with no frame, overlay text kept to the left of the blossoms, and a Walnut scrim (60% → 0% from left) so text stays at ≥7:1. It must be exported to WebP at ≤ 400 KB; the source file is 23 MB and must not ship as-is.
- **Profile photo** (`perfil.jpg`): Home and About, rectangular, 0px radius, 4:5 crop, never a circle.
- **Hobby photos** (`guitar.jpg`, `gym.JPG`, `travel.png`): About page, a row of three 4:5 crops (stacked on mobile), each with a Sage caption below.
- **Organisation logos** (`IST_Logo.png`, `it.png`, `AEIST.png`, `golp.png`, `silicongate.png`): shown at 28px height beside each entry's H3. They sit on a small Blossom tile (12px radius, 6px padding) so dark-on-transparent logos stay visible on the dark canvas. No colour filtering.
- **Sunflowers:** no image file is in the repo. *Sunflowers* contributes the Sunflower accent colour only, unless an image is added later (see decision log).
- No stock photos, no illustration, no icons beyond tiny line glyphs (arrow, external-link, chevron) at 1.5px stroke in the current text colour.

---

## 5. Components

Every component below is needed by COPY.md. Nothing else is built.

### 5.1 Header and navigation
- Fixed, transparent over the hero; turns Bark with a 1px Cork bottom border after 24px of scroll.
- Left: wordmark "Guilherme Candeias Martins" in Fraunces 400, 18px (mobile: "G. C. Martins").
- Right: six links (Home · Experience · Projects · Education & Skills · About · Contact) in Label style, Blossom. The active page is Almond Sky with a 1px dashed underline (ORYZO).
- Far right: language toggle (5.2), then the email button (5.3, compact).
- Below 960px: links collapse into a "Menu" label button that opens a full-screen Walnut panel. The links there are set in H2 size, and the email button is at the bottom.

### 5.2 Language toggle (EN | PT)
- Two Label-style text buttons separated by a thin Cork rule, in a pill outline (1px Cork).
- The active language is Sunflower; the inactive one is Blossom.
- It switches between the parallel `/` and `/pt/` pages (one URL per language, for search) and sets `lang="en"` or `lang="pt-PT"`.

### 5.3 Email button (the main action)
- **Default:** filled pill, Blossom fill, Walnut text, Label style, padding 14px 24px. ORYZO's "one filled button" rule: it is the only filled button on any screen.
- **Hover/focus:** fill changes to Sunflower over 0.25s; the label is unchanged.
- **Focus-visible:** 2px Sunflower outline, offset 3px.
- **Text:** "Email me" / "Envie-me um email". `href="mailto:gcandeiasmarti@tudelft.nl"`.
- **Compact variant** in the header: padding 10px 18px.

### 5.4 Ghost button (secondary)
- Transparent, 1px Blossom border, Blossom Label text, pill radius, padding 12px 22px. Used for LinkedIn and "See my experience" style links.
- **Hover:** border and text change to Almond Sky.

### 5.5 Home hero
- The almond-blossom painting is on the right or behind, with the text on the left.
- Eyebrow (Label, Sage): "Electrical and Computer Engineer · MSc TU Delft".
- Display name in Fraunces 300.
- Subheading (Lead, Blossom) and location line (Meta, Sage).
- Email button + LinkedIn ghost button.
- A small "Scroll" Label with a down arrow, bottom-left (a nod to monopo's scroll badge, but static, not rotating).

### 5.6 "Looking for" list
- Three items, each an H3-sized Fraunces line with a Branch dash bullet. It sits directly under the hero.

### 5.7 Highlight row (Home)
- On a full-bleed Moss band: three columns (stacked on mobile).
- Each has a number in Fraunces 300 italic, Sage ("01"), an H3 title, a body paragraph, and a text link "See my experience →".
- No card chrome; columns are separated by 1px Branch vertical hairlines on desktop.

### 5.8 Page header (inner pages)
- An eyebrow with the page name (Label, Sage), then the H1 and the opening lines in Lead.
- A dashed Cork divider below.

### 5.9 Entry (role, education, project, volunteering, exchange)
- Two-column layout as in section 3: the left rail holds dates and place (Meta, Sage), and the right holds the logo tile + H3 title, organisation line (Body, Sage), summary (Body) and an optional note in italics.
- 40px between entries, with a dashed Cork divider between groups.

### 5.10 Expander ("Show full technical detail")
- A ghost button with a chevron. `aria-expanded` and `aria-controls` point to the panel.
- Panel: Bark surface, 12px radius, 24px padding, a bulleted list in Body with Branch bullet marks.
- Closed by default. Works without JS: built with `<details><summary>`.

### 5.11 Pull quote
- Bark panel, 12px radius, 32px padding.
- A 3px Sunflower left rule (the quote's single accent).
- Quote text in Fraunces 300 italic; attribution in Label style (name) plus Meta in Sage (titles).

### 5.12 Fact lists (skills, awards, languages, equipment)
- A two-column definition list on desktop: the term (Label, Sage) and its value (Body).
- Awards: title in Body and year right-aligned in Meta.

### 5.13 Photo row (About)
- Three 4:5 images with 0px radius and a Sage caption below each. Stacks on mobile.

### 5.14 Link list (proof)
- Each link is Almond Sky, underlined, followed by an external-link glyph. `rel="noopener"` and `target="_blank"` on external links only.

### 5.15 Next step block
- Ends every page: an H2 ("Let's talk" and others from COPY.md), one line of Lead text, the email button, and a "Next: [page] →" text link to the right.

### 5.16 Footer
- Walnut with a dashed Cork top divider.
- Three columns: copyright; email + LinkedIn; the language toggle repeated.
- Meta size, Sage. No other links.

---

## 6. What was taken from each reference, and what was rejected

| Reference | Taken | Rejected |
|---|---|---|
| **ORYZO AI** (lead) | Warm-dark canvas and two-step surface stack; cream instead of white; one filled button; UPPERCASE 500 labels vs mixed-case reading text; pill buttons and 12px panels; dashed hairline dividers; flanking label/content layout; generous negative space; no shadows | 100vh sections (the copy is too long); 29px body (too large for long bilingual text); 8px micro-text (unreadable); "no people" imagery (the profile and hobby photos are approved); uppercase-only headings (Fraunces is mixed-case); Ember orange (the brand palette wins) |
| **Structured** | A painting as the single atmospheric image; serif display paired with a neutral grotesk; alternating bands (as Walnut/Moss, both dark) | Putty canvas and Davinci/Helvetica (brand wins); 374px cropped wordmark; circular crops and hexagons |
| **monopo saigon** | The cubic-bezier(0.19, 1, 0.22, 1) easing; colour lives only in imagery, never in UI fills; a scroll cue | Roobert, the monochrome palette and iridescent gradient (brand wins); 225px display; underline-free links (accessibility) |
| **Freshman** | "One saturated accent per viewport", applied to Sunflower; type-only, low-chrome navigation | Pure black canvas; handwritten flourish font; bottom project ticker |
| **Flying Papers** | Nothing beyond confirming the pill-vs-sharp contrast | Violet stage, confetti colours, mascots, 341px display (the opposite of the chosen feel) |

**Errors in the reference files that were not copied:** ORYZO lists `#40372` in places (a truncated hex; the correct value is `#40372e`). Freshman's `--section-gap: 48-80px` and `--card-padding: 12-20px` are not valid CSS values.

---

## 7. CSS quick start

```css
:root {
  /* Colours */
  --color-walnut: #16100a;
  --color-bark: #2b1f14;
  --color-moss: #1f2a1e;
  --color-blossom: #f4eee2;
  --color-sage: #b8c3aa;
  --color-sky: #7fadb1;
  --color-branch: #5d7562;
  --color-sunflower: #e8b130;
  --color-cork: #3e3528;

  /* Fonts */
  --font-display: 'Fraunces', Georgia, 'Times New Roman', serif;
  --font-body: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;

  /* Type scale */
  --text-display: clamp(2.75rem, 8vw, 6.5rem);
  --text-h1: clamp(2.25rem, 5.5vw, 4rem);
  --text-h2: clamp(1.625rem, 3vw, 2.25rem);
  --text-h3: clamp(1.25rem, 2vw, 1.5rem);
  --text-lead: clamp(1.125rem, 1.8vw, 1.5rem);
  --text-quote: clamp(1.25rem, 2.4vw, 1.75rem);
  --text-body: 1.0625rem;
  --text-meta: 0.9375rem;
  --text-label: 0.8125rem;

  /* Spacing */
  --space-1: 4px;  --space-2: 8px;  --space-3: 12px; --space-4: 18px;
  --space-5: 24px; --space-6: 40px; --space-7: 68px; --space-8: 120px;
  --gutter: max(16px, 4vw);
  --container: 1120px;
  --section-gap: var(--space-7);

  /* Radii */
  --radius-pill: 999px;
  --radius-panel: 12px;

  /* Motion */
  --ease-glide: cubic-bezier(0.19, 1, 0.22, 1);
  --dur-reveal: 0.6s;
  --dur-hover: 0.25s;
}
@media (min-width: 760px) { :root { --section-gap: var(--space-8); } }
@media (prefers-reduced-motion: reduce) { :root { --dur-reveal: 0s; --dur-hover: 0s; } }
```

---

## 8. Decision log

Every design choice is recorded here. **Status:** *decided* means Guilherme chose it; *proposed* means Claude chose it and it is awaiting his approval. New entries go at the bottom.

| # | Date | Decision | Reason | Source | Status |
|---|---|---|---|---|---|
| 1 | 2026-11-16 | Brand wins on colours and fonts; references win on layout and feel | Guilherme's instruction | Guilherme | Decided |
| 2 | 2026-11-16 | ORYZO AI is the lead reference for layout and feel | "I specially love the ORYZO AI one" | Guilherme | Decided |
| 3 | 2026-11-16 | No brand kit file exists; the brand palette is built from his likes: green, brown, *Almond Blossoms*, *Sunflowers* | The brand kit did not arrive; he chose "build from my likes" | Guilherme | Decided |
| 4 | 2026-11-16 | Old site's pink `#ff80ab` and Bebas Neue are retired | Replaced by the new brand (decisions 3 and 5) | Guilherme | Decided |
| 5 | 2026-11-16 | Fonts: Fraunces (headings) + Inter (body and UI) | Chosen from three options | Guilherme | Decided |
| 6 | 2026-11-16 | Dark theme only, on the Walnut canvas | Follows ORYZO; brown is a brand colour | Claude | Proposed |
| 7 | 2026-11-16 | Palette values: Walnut, Bark, Moss, Blossom, Cork chosen; Sage, Almond Sky, Branch sampled from `almond_blossoms.png`; Sunflower chosen (no image file) | Turns the stated likes into tokens with ≥4.5:1 text contrast | Claude | Proposed |
| 8 | 2026-11-16 | Email button: Blossom filled pill, Sunflower on hover/focus | The main action needs to stand out, but ORYZO forbids the accent as a fill and allows one filled button | Claude | Proposed |
| 9 | 2026-11-16 | Headings in mixed-case Fraunces; UPPERCASE Inter only for labels | ORYZO's all-caps rule clashes with a serif display | Claude | Proposed |
| 10 | 2026-11-16 | Sections at content height (hero ~88svh); body 17px, not ORYZO's 29px | Long bilingual copy; readability | Claude | Proposed |
| 11 | 2026-11-16 | Profile, hobby photos and logos are used despite ORYZO's "no people" rule; logos sit on Blossom tiles | Approved assets in CONTEXT.md; visibility on a dark canvas | Claude | Proposed |
| 12 | 2026-11-16 | `almond_blossoms.png` is the single hero painting, compressed to WebP ≤ 400 KB | One painting per site (Structured/monopo); the source is 23 MB | Claude | Proposed |
| 13 | 2026-11-16 | Links are always underlined; minimum text size 13px (labels) and 15px (meta) | Accessibility over monopo's underline-free links and ORYZO's 8px text | Claude | Proposed |
| 14 | 2026-11-16 | Separate URLs per language (`/` and `/pt/`) rather than a JS-only toggle | Each language can rank for its own searches (COPY.md) | Claude | Proposed |
| 15 | 2026-11-16 | Radius vocabulary: pill (999px), 12px panels, 0px everything else | One system instead of five | Claude | Proposed |
| 16 | 2026-11-16 | Very faint film-grain texture over the walnut canvas (7% opacity, fixed) | Adds a painted, darkroom feel without a gradient or shadow | Claude (build) | Proposed |
| 17 | 2026-11-16 | Fraunces and Inter are self-hosted in `assets/fonts/` instead of linked from Google Fonts | "No third-party embeds": the site makes zero requests to other hosts | Claude (build) | Proposed |
| 18 | 2026-11-16 | Reveal motion is a scroll-driven glide (CSS `animation-timeline: view()`), and content is always visible at rest | A JS fade-in would leave link previews and thumbnails blank | Claude (build) | Proposed |
| 19 | 2026-11-16 | The hero painting gets a Walnut shade along its top edge as well as its left edge | Header links and the EN/PT toggle were unreadable over the light sky of the painting | Claude (build) | Proposed |
| 20 | 2026-11-16 | Logos appear only where the repo has the file (SiliconGate, GOLP, IT, AEIST, IST); TU Delft, Celera, Sentinel and its partners appear as text | Never invent logos | Claude (build) | Proposed |
| 21 | 2026-11-16 | UI text not in COPY.md is limited to navigation chrome: "Skip to content", "Menu", "EN/PT", and the short wordmark "G. C. Martins" on phones | Needed for accessibility and the phone layout; carries no claims | Claude (build) | Proposed |
| 22 | 2026-11-16 | Pages are generated by `tools/build_site.py`; `tools/check_copy.py` verifies every COPY.md sentence appears verbatim on its page | Keeps the site and COPY.md in step | Claude (build) | Proposed |
