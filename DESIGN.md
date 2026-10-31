---
name: N-Puzzle
description: A 3x3 sliding puzzle and search-algorithm comparison, built as a wall of Hanoi enamel house-number plates.
colors:
  cobalt: "#123c9c"
  cobalt-deep: "#0c2c76"
  shutter: "#2f6b4f"
  shutter-deep: "#24543e"
  wall: "#e3a82b"
  wall-shade: "#c48e1c"
  wall-deep: "#a67614"
  enamel: "#f6f5ee"
  enamel-shade: "#e8e6dc"
  ink: "#1a1a1a"
  ink-soft: "#48484c"
  error: "#a02c18"
  rule: "#c4c9d6"
  selected: "#dee5f5"
  hover: "#ecece8"
  disabled-fill: "#dedcd2"
  disabled-text: "#5c5a54"
typography:
  plate:
    fontFamily: "Be Vietnam Pro"
    fontSize: "72px"
    fontWeight: 700
  title:
    fontFamily: "Be Vietnam Pro"
    fontSize: "44px"
    fontWeight: 800
  count:
    fontFamily: "Be Vietnam Pro"
    fontSize: "30px"
    fontWeight: 700
  heading:
    fontFamily: "Be Vietnam Pro"
    fontSize: "20px"
    fontWeight: 700
  data:
    fontFamily: "Be Vietnam Pro"
    fontSize: "17px"
    fontWeight: 400
  data-best:
    fontFamily: "Be Vietnam Pro"
    fontSize: "17px"
    fontWeight: 700
  strong:
    fontFamily: "Be Vietnam Pro"
    fontSize: "15px"
    fontWeight: 700
  small:
    fontFamily: "Be Vietnam Pro"
    fontSize: "14px"
    fontWeight: 400
  small-bold:
    fontFamily: "Be Vietnam Pro"
    fontSize: "13px"
    fontWeight: 700
rounded:
  plate: "14px"
  panel: "14px"
  count-plate: "10px"
  control: "8px"
  row: "6px"
  mini-plate: "4px"
spacing:
  unit: "8px"
  plate-gap: "12px"
  panel-padding: "24px"
  margin: "32px"
  plate-rim: "6px"
  count-rim: "4px"
components:
  button-primary:
    backgroundColor: "{colors.shutter}"
    textColor: "{colors.enamel}"
    typography: "{typography.strong}"
    rounded: "{rounded.control}"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.shutter-deep}"
  button-secondary:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.enamel}"
    typography: "{typography.strong}"
    rounded: "{rounded.control}"
    height: "44px"
  button-secondary-hover:
    backgroundColor: "{colors.cobalt-deep}"
  button-quiet:
    backgroundColor: "{colors.enamel}"
    textColor: "{colors.cobalt}"
    typography: "{typography.strong}"
    rounded: "{rounded.control}"
    height: "44px"
  button-quiet-hover:
    backgroundColor: "{colors.hover}"
  button-disabled:
    backgroundColor: "{colors.disabled-fill}"
    textColor: "{colors.disabled-text}"
    typography: "{typography.strong}"
    rounded: "{rounded.control}"
    height: "44px"
  plate:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.enamel}"
    typography: "{typography.plate}"
    rounded: "{rounded.plate}"
    size: "136px"
  plate-won:
    backgroundColor: "{colors.shutter}"
    textColor: "{colors.enamel}"
  plate-recess:
    backgroundColor: "{colors.wall-shade}"
    rounded: "{rounded.plate}"
    size: "136px"
  count-plate:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.enamel}"
    typography: "{typography.count}"
    rounded: "{rounded.count-plate}"
    height: "64px"
  panel:
    backgroundColor: "{colors.enamel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "24px"
    size: "572px 616px"
  table-row:
    backgroundColor: "{colors.enamel}"
    textColor: "{colors.ink}"
    typography: "{typography.data}"
    height: "44px"
  table-row-hover:
    backgroundColor: "{colors.hover}"
    rounded: "{rounded.row}"
  table-row-selected:
    backgroundColor: "{colors.selected}"
    rounded: "{rounded.row}"
  segment:
    backgroundColor: "{colors.enamel}"
    textColor: "{colors.cobalt}"
    typography: "{typography.strong}"
    rounded: "{rounded.control}"
    size: "192px 44px"
  segment-selected:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.enamel}"
    rounded: "{rounded.control}"
---

# Design System: N-Puzzle

## Overview

**Creative North Star: "The House-Number Wall"**

The window is a stretch of Hanoi street wall. Ochre limewash covers the whole ground, and the board is mounted on it as cobalt enamel house-number plates with white rims and two screw points. The white enamel panel beside it is a larger sign on the same wall, carrying the comparison table and every control. Nothing floats in a grey application frame: the wall is the interface.

The density is that of a game board beside a lab table. The left column is large and physical, with 72px numerals on 136px plates, while the right column is exact and tabular. The two share one material language, so measured results read as part of the same object as the puzzle.

Motion belongs to the plates. They slide with an exponential ease-out, lift slightly when they can move, and on a win turn from cobalt to shutter green in reading order. Everything else changes state without animation.

**Key Characteristics:**
- Limewash ochre ground across the whole window, generated in code.
- Cobalt enamel plates with a white rim and two screws.
- A single white enamel panel holding table, status and controls.
- Shutter green reserved for the primary action, best results and the win.
- Be Vietnam Pro in three weights, bundled with the app.
- A fixed 1100x680 window with no alternate layouts.

## Colors

Three saturated street materials (ochre wall, cobalt enamel, shutter green) sit with warm off-white enamel and near-black ink.

### Primary
- **Cobalt Enamel** (#123c9c): the numbered plates, move-count plate, product name, panel heading, table header rule, radio marks, quiet button text and outline, selected language segment, and in-progress status text.
- **Deep Cobalt** (#0c2c76): hover fill for cobalt-filled buttons only.

### Secondary
- **Shutter Green** (#2f6b4f): the primary button, best values in the table, win and solved status text, and the end state of the win ripple.
- **Deep Shutter** (#24543e): hover fill for the primary button.

### Tertiary
- **Limewash Ochre** (#e3a82b): the wall, the base color of the generated limewash.
- **Recess Floor** (#c48e1c): the floor of the empty cell.
- **Recess Edge** (#a67614): the dark 5px top edge of the empty cell.

### Neutral
- **White Enamel** (#f6f5ee): panel, plate rims, screws, numerals and text on cobalt or green fills.
- **Enamel Shade** (#e8e6dc): the frame behind the finished-board thumbnail.
- **Ink** (#1a1a1a): table text, control labels, the "Moves" label and the focus ring.
- **Soft Ink** (#48484c): notes, hints, reference captions and empty-cell dashes in the table.
- **Brick Error** (#a02c18): notices and no-solution status text.
- **Table Rule** (#c4c9d6): row dividers and the divider above the picture controls.
- **Selected Tint** (#dee5f5): the selected table row.
- **Hover Tint** (#ecece8): hovered quiet buttons, table rows and unselected segments.
- **Disabled Fill** (#dedcd2) and **Disabled Text** (#5c5a54): disabled buttons, which also lose any outline.

### Named Rules

**The Green Is Earned Rule.** Shutter green means do this next, this is the best figure, or the board is solved. It has no decorative use.

**The Material Not Accent Rule.** Cobalt is the plate's enamel, set against ochre and white. It is never a small accent on a neutral grey interface.

## Typography

**Display Font:** Be Vietnam Pro, bundled as TTF files with no fallback
**Body Font:** Be Vietnam Pro
**Label/Mono Font:** Be Vietnam Pro; there is no mono face

**Character:** A sturdy grotesque with full Vietnamese diacritic support, so the default Vietnamese interface and the English one share the same voice. Its heavy numerals carry the enamel-sign reading on the plates.

Sizes are pixel font sizes. Every text item in the build is a single line placed by its anchor, so no line-height scale exists. Text that could overflow, namely button labels and the status line, is shortened with an ellipsis.

### Hierarchy
- **Plate numeral** (Bold 700, 72px): numbers on board plates, nudged 2px above center.
- **Title** (ExtraBold 800, 44px): the cobalt product name on the wall. This is the only use of ExtraBold.
- **Count** (Bold 700, 30px): the figure in the move-count plate.
- **Heading** (Bold 700, 20px): the panel heading and the "Moves" label.
- **Data** (Regular 400, 17px): regular table figures, drawn with equal-width digits.
- **Data best** (Bold 700, 17px): best table figures, in shutter green with the font's natural digits.
- **Strong** (Bold 700, 15px): table headers, algorithm names, button and segment labels, the status line and picture and language labels.
- **Small** (Regular 400, 14px): the note under the table and the thumbnail caption.
- **Small bold** (Bold 700, 13px): numerals on the finished-board thumbnail.

### Named Rules

**The Three Weights Rule.** Regular, Bold and ExtraBold are the only weights shipped. Hierarchy comes from size, color and these three files.

**The Equal Digits Rule.** Regular table figures are drawn digit by digit in cells as wide as the font's "0", and right-aligned, because pygame cannot enable tabular figures and the bundled font's digits are proportional. Best values stay plain bold text at the same right edge, because bold digits look split in equal-width cells and the weight and color already mark them.

## Layout

The window is fixed at 1100x680 and is not resizable, so there are no breakpoints. The base unit is 8px and the outer margin is 32px.

The left column starts at x 32 and is 432px wide. It holds the product name at y 24, the 3x3 board at y 92 (136px plates with 12px gaps), and the "Moves" label and count plate centered on y 616. The count plate's bottom edge meets the panel's at y 648.

The right column is the 572x616 panel at x 496 and y 32, leaving a 32px gutter from the board. Inside its 24px padding (524px content width) the order is heading, table, note, status line, action row, divider, then the picture controls and language switch. Table header height is 32px and row height is 44px, for five rows. Numeric columns right-align to 196, 272, 364 and 512px from the table's left edge.

The action row holds Solve at 196px, Skip at 96px, and Shuffle and Reset at 104px each, with 8px gaps. The bottom row has a 96px reference square, a 192px picture control area that splits into 96px and 88px buttons when a picture is loaded, and a 192px language switch on the right edge.

**The Fixed Wall Rule.** The composition is one measured arrangement at one size. New content must fit this window in both languages rather than introduce scrolling, tabs or a second layout.

## Elevation & Depth

Depth is physical: raised objects cast a soft warm shadow on the wall, and the empty cell is cut into it. The panel and plates are raised, while controls inside the panel stay flat.

### Shadow Vocabulary
- **Plate shadow** (`box-shadow: 0 3px 8px rgba(70, 45, 5, 0.43)`, approximating a shape blurred by 6x down-and-up scaling in code): every board plate. It moves with the plate during a slide or lift and does not change size.
- **Panel shadow** (`box-shadow: 0 4px 8px rgba(70, 45, 5, 0.27)`, same method): the white enamel panel.
- **Recess** (no shadow; a 5px #a67614 top edge above a #c48e1c floor): the empty cell, and the ground under every cell.

### Named Rules

**The Warm Shadow Rule.** Shadows are tinted brown from the wall (#462d05), never neutral black, and only raised objects on the wall cast one.

**The Hole In The Wall Rule.** The empty cell is a recess, not a missing plate. The recess is drawn under every cell, so a sliding plate always passes over a hole.

## Shapes

Corners are firmly rounded, like pressed enamel. Plates and the panel share a 14px radius, the count plate uses 10px, and controls use 8px. Table row highlights use 6px and thumbnail plates 4px. Plate rims are a white enamel border (6px on board plates, 4px on the count plate), and quiet buttons and the language switch use a 2px cobalt outline. Circles appear only as screws (4px radius) and table radio marks (7px radius). All corners are antialiased by 4x supersampling because pygame's own corners are jagged.

## Components

### Buttons
Flat, solid enamel tabs that change color without moving.
- **Shape:** gently rounded rectangles (8px), 44px high, with labels at least 8px from each side.
- **Primary:** shutter green fill with enamel text, used for "Solve with [algorithm]". Hover deepens the fill.
- **Secondary:** cobalt fill with enamel text. Hover deepens the fill. Its only use is Shuffle after a win by hand, when starting a new game is the obvious next step.
- **Quiet:** enamel fill, 2px cobalt outline and cobalt text. Hover uses the hover tint. This is the resting style of Skip, Shuffle, Reset and the picture buttons, and Solve becomes quiet while it reads "Cancel" during a solve.
- **Disabled:** disabled fill and text with no outline. Solve is disabled after a win by hand, and Skip is disabled until a solution exists.
- **Focus:** a 2px ink ring sitting 1px outside the control (3px total, 11px corner). It appears on Tab across table rows, buttons and language segments, and clears on a mouse click.
- **Pointer:** the system hand cursor over anything clickable. There is no pressed state or color transition.

**The One Fill Rule.** The action row holds at most one filled button: green Solve while solving is on offer, cobalt Shuffle after a win by hand, and neither while a solve is running.

### Comparison Table
The app's lab record, ruled like a printed table.
- **Structure:** bold ink headers over a 2px cobalt rule, then rows divided by a 1px table rule.
- **Row states:** selected rows use the selected tint and hovered rows the hover tint, both at 6px. Hover is suppressed and rows leave the Tab order while a solve runs.
- **Radio:** a 7px cobalt ring at 2px stroke, with a cobalt center of 3px radius when selected, placed 16px from the row's left edge. The algorithm name starts 32px in.
- **Figures:** see the Equal Digits Rule. Rows with no result show a soft-ink dash, memory values begin with "≈", and best values only appear once two or more algorithms have results.

### Status Line
One strong line above the action row, colored by meaning: soft ink for the hint, cobalt for searching and playback, shutter green for a finished board and brick for a failure.

### Language Switch
A 192x44 two-way segmented control with a 2px cobalt outline and 8px corners. The selected half is a complete 8px-rounded cobalt tab with enamel text. An unselected half shows cobalt text, with a hover tint inset 3px per side at a 5px radius on hover.

### Numbered Plate
The signature object, 136px square.
- **Build:** cobalt fill, 6px enamel rim, 14px corners, and a Bold 72px enamel numeral.
- **Screws:** two enamel dots (4px radius) centered horizontally, 16px from the top and bottom edges.
- **Hover:** only a plate that can move into the gap lifts, by 3px, with its shadow, and only while the mouse is over it and the player can move. There is no lift during a solve or after a win.
- **Slide:** the moved plate travels between cells in 130ms with the exponential ease-out `1 - 2^(-10t)`. Changes that alter more than two cells, such as Shuffle and Reset, snap into place.
- **Playback:** solver moves advance every 200ms, so each 130ms slide settles before the next.

### Win Ripple
When the board reaches its goal, each plate fades linearly from cobalt to shutter green over 220ms, starting 70ms after the previous cell in reading order. Across cells 0 to 7, the numbered board finishes 710ms after the win.

### Picture Plate
A user's picture center-cropped and cut across the whole board, including gaps, so the image stays continuous between plates. It shows inside a 6px rim with no screws. On a win the rim, not the picture, ripples from enamel to shutter green, and the ninth piece fades into the gap on the same schedule, finishing at 780ms.

### Move-Count Plate
A smaller sign at the foot of the board: cobalt fill, 4px enamel rim, 10px corners, 64px high, at least 88px wide, growing with the count. Its right edge stays aligned to the board. It has no screws and casts no shadow.

### Finished-Board Thumbnail
A 96px square at 8px corners showing the goal: an enamel-shade frame with eight 24px cobalt plates at 4px corners and 4px gaps, or the loaded picture in picture mode.

### Limewash Wall
Generated in code at startup and cached, so no raster ships. A seeded run (seed 7) lays 220 soft strokes of 260 to 760px by 14 to 60px, at 6 to 20 degrees either way, lightening or darkening the ochre by up to 4, 6 or 9 levels per stroke. A repeating 128px tile of pigment grain at up to 3 levels finishes it.

## Do's and Don'ts

### Do:
- **Do** paint the whole window with the generated limewash and mount every object on it.
- **Do** use the 136px plate, 6px rim and 14px corner together when drawing a board plate.
- **Do** keep the screws on numbered board plates and leave them off picture plates, where they would mark the picture.
- **Do** draw regular table figures with equal-width digits and best values in plain bold shutter green.
- **Do** keep hover lift, slide and ripple on board plates.
- **Do** check new labels in Vietnamese and English at the fixed window size.

### Don't:
- **Don't** replace the wall with a flat or grey application background.
- **Don't** split the panel's contents into a grid of cards; it is one enamel sign with rules inside it.
- **Don't** ship a raster for the wall; change the generator instead.
- **Don't** set white enamel text directly on the ochre wall, where it reaches only about 1.9:1. Use ink or cobalt.
- **Don't** add a weight or typeface beyond the three bundled Be Vietnam Pro files.
- **Don't** give raised objects a hard-edged shadow; the hard edge belongs to the recess.
- **Don't** fill two buttons in the action row at once.
