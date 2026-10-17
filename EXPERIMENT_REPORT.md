# README-native experiment: CORE BREACH

## What this proves (browser checked on GitHub)
- GitHub Flavored Markdown tables can contain compact, one-line native HTML `<details><summary>...</summary>...</details>` **within each cell**, so a 6×6 grid stays a grid.
- Distinct tiles respond to mouse clicks and remain open independently, with the same GitHub URL.
- All 36 board values are derived from one fixed mine layout; the game does not need a 813-branch precomputed decision tree.
- SVG decorative graphics loaded as `<img>` work; they do **not** expose click handlers or custom JS.
- Native script execution, CSS styling, physics, automatic victory, mine flags and real-time movement remain unavailable.

## Negative control
`experiment/readme-inplace-grid-20261017` initially used multiline HTML `<table><td><details>` markup that the browser agent reported as flattened. The same branch tested a one-line HTML table and a GFM table containing inline single-line details. Both were confirmed as 2-row by 3-column actual working grids. `CORE BREACH` uses the GFM layout and was browser tested as 6 columns × 6 rows.

## Reproducibility
- Rebuild: `node scripts/build-readme.mjs`
- Verify: `node scripts/test-readme.mjs`
- The tests check all 36 clues against the exact mine positions, all assets, and README size.

## Limits and blockers
- Clicking a bomb is a mine reveal, but GitHub cannot automatically prevent more clicks after game over.
- The win condition (all 29 safe nodes opened) is rule-based and manually judged, not programmatically detected.
- Mobile viewport/table overflow is *not yet tested*; desktop 6-column layout was confirmed.
- This branch is a research prototype; **not approved for merging to the user's main profile README**.

## Browser QA and CI evidence — 2026-10-17

- The browser automation independently rendered the branch README on GitHub and reported **six horizontal columns** rather than a vertical list.
- Opening multiple tiles was observed; previously opened tiles remained open, and the README URL stayed unchanged. The exact glyph for the second tile was not independently legible in screenshots, so the browser result for that value is **limited**, whereas the test suite verifies the source logic precisely.
- Earlier layout trial `experiment/readme-inplace-grid-20261017` demonstrated the critical trick: **one-line `<details>` inside each GitHub-flavored Markdown table cell** preserves the actual grid layout. Multiline HTML failed in the initial trial.
- GitHub Actions run `39000186315` on this branch concluded **success**, with both "Verify mines, grid, assets, layout source" and "Verify deterministic renderer" steps passing.
- The alternative keyboard trial `experiment/readme-native-controls-20261017` showed GitHub strips `accesskey`, `tabindex`, `contenteditable`, and `draggable` attributes from the rendered README. Native `<summary>` remains keyboard accessible through normal focus/Enter/Space behavior, but not as an arbitrary WASD-controlled physics game.
- Standard GitHub README task-list checkboxes are read-only to visitors; HTML `<input>` and `<canvas>` are blocked.
- This **does not** prove complete Minesweeper game-state validation, automatic victory or keyboard controls. It proves a compact, clickable, non-navigating logical game *surface* inside GitHub Markdown.

**Decision:** Keep as research prototype; do not merge to the profile until mobile visual QA and meaningful automated game-over/win handling are addressed or the intentionally simpler game design is explicitly accepted.
