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
