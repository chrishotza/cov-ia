# GitHub README: empirical execution boundary (2026-10-17)

## Objective
Find a way for ordinary, anonymous visitors to play a **real keyboard-controlled game** directly at `https://github.com/chrishotza`, with no extension, reload, navigation to another site, or separate repo file. Do **not** modify the profile until end-to-end verification passes.

## Experiment inventory
- Native STL 3D puzzle: `experiment/readme-3d-puzzle-20261016`. Proven interactive canvas, rotation, zoom, wireframe. **Not** a custom game loop.
- Native HTML details (grouped by `name`): observed working in GitHub README. Fast discrete choices. **Not** free movement/physics.
- GeoJSON + TopoJSON: `experiment/readme-geojson-native-maze-20261016`. Four distinct blocks: minimal point/polygon and 13×9 maze for both formats. Parsed/published, but actual map graphics NOT verified in browser automation. No input or collisions confirmed.
- Native HTML sanitizer: `experiment/readme-native-controls-20261017`, commit `f3507f7852200cbe308f8838bfbac60380d7df15`. Real page inspected in browser, and inline SVG separately re-tested with ordinary cursor.

## Native HTML sanitizer matrix (rendered README)
| Element/feature | Observation |
| --- | --- |
| `details` + `summary` | **Survives**. Opens/closes and `details name` exclusive groups work |
| `input` checkbox, radio, range | **Stripped**, not interactive |
| `select`, `button`, `form` | **Stripped**, fallback text |
| `canvas` | **Stripped** |
| Inline `svg` with rect/text/animate | **Stripped**. Earlier claim based on an animated fish icon was a **false positive caused by an agent cursor or page chrome**, not the test SVG. Scoped re-test confirmed no original inline SVG widget |
| `style`, `script`, `onclick` | **Stripped**; no code execution |
| `dialog`, `iframe`, `object` | **Stripped** |
| Raw `audio`, `video`, `progress`, `meter` HTML tags | **Stripped in this test**. Does not rule out GitHub's separate *asset URL* video auto-renderer |
| Plain image through Markdown `![](...)` | Supported as a display resource, but images do not expose custom game input |

**Interpretation:** the standard README HTML sanitizer prevents installing a custom JavaScript/Canvas/WASM runtime. GitHub's built-in rich code-fence viewers are a separate platform-controlled exception, not permission to execute author-supplied code.

## GeoJSON vs TopoJSON
- GeoJSON A: point + polygon; browser automation unable to confirm visible map.
- GeoJSON B: maze 13×9; unable to confirm.
- TopoJSON C: point + polygon, quantized/delta arcs; no visible map confirmed.
- TopoJSON D: maze 13×9, 119 features; no visible map confirmed.
- **Do not claim map arrows move a player.** Native camera panning and zooming, even if recovered, do not produce collision checks, player position, level-state transitions or score.
- Multiple public GitHub Discussions independently report map geometry missing under the GitHub renderer, so missing geometry cannot be assumed to be malformed.

## Remaining legitimate research avenues
1. Diagnose sandboxed map viewer availability with a **manual** trusted browser + network/error inspection; compare maps in official GitHub docs against experiment's minimal geometries.
2. Evaluate GitHub-owned interactive media surfaces that take structured input; distinguish camera input from actual game-state input.
3. Study SVG **as an image** separately from inline SVG, specifically whether only declarative timeline animation survives. Do not present animation as keyboard interactivity.
4. If nothing can consume player input and update arbitrary game state in the ordinary profile README, do **not** claim a keyboard/physics game is implemented. Accept the platform boundary instead of publishing another imitation.

## Independent evidence / docs
- GitHub's diagram documentation: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams
- GitHub map files docs: https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files
- GitHub community GeoJSON visualization bug: https://github.com/orgs/community/discussions/58244

**No user-facing profile modification is authorized by these tests.**

## SVG-as-image test (added after the initial sanitizer matrix)
Source asset: `assets/svg-image-mode-probe.svg`. It contains SMIL time animation, CSS `:hover`, SMIL `begin="click"`, and a `foreignObject` checkbox. GitHub embeds it through Markdown `![](./assets/svg-image-mode-probe.svg)` as an `img`.

Live browser results:
- External SVG visually rendered: **yes**.
- Timeline animation (SMIL changing circle `cx`): **yes**, movement observed across snapshots.
- Hover of an internal square: **no change observed**.
- Click on the internal circle with `begin="click"`: **no change observed**.
- Checkbox inside `foreignObject`: **no actionable input verified**. The QA agent speculated that the checkbox changed via timeline, but our SVG only animates `cx` of the first circle, so that speculation is **not supported by the source**. Treat the checkbox result as inconclusive, not an interaction success.

**Conclusion:** SVG-as-image is an effective declarative animation channel, but did not provide a demonstrated pointer/keyboard event channel for a game loop. Do not confuse automatic animation with visitor-controlled game state.
