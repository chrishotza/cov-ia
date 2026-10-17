# LAB 004 · GitHub Markdown / Native Controls Matrix

**Experimento aislado, no aplicación ni juego.** La hipótesis es detectar controles HTML que GitHub conserve y permita operar dentro del README, sin JS ni instalaciones.

> Criterio: no basta con que se lea el HTML fuente. El control debe verse, responder a clic o tecla, y conservar la URL. Si un elemento es eliminado, esperamos ver solo los textos de fallback.

## A · Control positivo (`details`)

<details name="control-test"><summary>CONTROL_A / abrir</summary>

**A_OPENED**. Abrí el control B: si este se cierra sin recarga, son estados mutuamente exclusivos.

</details>

<details name="control-test"><summary>CONTROL_B / abrir</summary>

**B_OPENED**. Si A se cerró automáticamente, el grupo funciona.

</details>

## B · Entradas nativas (no asumir que GitHub las admite)

**Checkbox:** antes / después deben diferir solo si hay un checkbox interactivo real.

<input type="checkbox" id="matrix-check" aria-label="CHECKBOX_INTERACTIVE" /> <label for="matrix-check">CHECKBOX_TEST</label>

**Radio:** deberían cambiar entre ALPHA/BETA.

<input type="radio" name="matrix-radio" value="a" id="matrix-a" /> <label for="matrix-a">RADIO_ALPHA</label>
<input type="radio" name="matrix-radio" value="b" id="matrix-b" /> <label for="matrix-b">RADIO_BETA</label>

**Slider:** <input type="range" min="0" max="100" value="37" aria-label="RANGE_37" />

**Select:** <select aria-label="SELECT_TEST"><option value="1">FIRST_OPTION</option><option value="2">SECOND_OPTION</option></select>

**Button (inert by default):** <button type="button">BUTTON_TEST</button>

**Form:** <form><input type="text" placeholder="FORM_TEXT_TEST" /><button type="submit">FORM_SUBMIT_TEST</button></form>

## C · Rich primitives (no inline executable code should survive)

**Canvas:** <canvas width="150" height="48">CANVAS_FALLBACK_VISIBLE</canvas>

**SVG inline (should be sanitized):**

<svg xmlns="http://www.w3.org/2000/svg" width="190" height="45" viewBox="0 0 190 45" role="img" aria-label="INLINE_SVG_RENDER"><rect x="0" y="0" width="190" height="45" rx="9" fill="#35b8a2" /><text x="10" y="26" fill="#ffffff" font-size="14">SVG_RENDERED</text><animate attributeName="opacity" dur="2s" values="1;.4;1" repeatCount="indefinite"/></svg>

**Style override:** if it survives, the next sentence will be red.

<style>.matrix-custom-style { color:red!important; font-size:24px!important }</style>
<p class="matrix-custom-style">CUSTOM_STYLE_TEST</p>

**Script:** if it somehow executes, `SCRIPT_RAN` appears on the page. This is not expected.

<span id="script-output">SCRIPT_NOT_RUN</span>
<script>document.getElementById('script-output').textContent='SCRIPT_RAN';</script>

**Event handler:** <button onclick="this.textContent='ONCLICK_RAN'">ONCLICK_NOT_RUN</button>

**Open Dialog:** <dialog open>OPEN_DIALOG_TEST</dialog>

**Embedded iframe:** <iframe title="EMBED_TEST" srcdoc="<h2>IFRAME_ACTIVE</h2>">IFRAME_FALLBACK</iframe>

**Object embed:** <object data="data:text/html,%3Ch1%3EOBJECT_ACTIVE%3C%2Fh1%3E" type="text/html">OBJECT_FALLBACK</object>

**Audio:** <audio controls aria-label="AUDIO_CONTROLS_TEST"></audio>

**Video:** <video controls width="192" height="100" aria-label="VIDEO_CONTROLS_TEST">VIDEO_FALLBACK</video>

**Progress (static):** <progress value="35" max="100">PROGRESS_FALLBACK</progress>

**Meter (static):** <meter min="0" max="10" value="7">METER_FALLBACK</meter>

## D · Baseline image and code

A regular Markdown image is allowed. The existing repo does not include a custom game PNG, so this test uses native code text as a baseline.

```text
NO_JS_EXECUTION_EXPECTED
```

### QA report requirements

For each control, report **rendered DOM versus source**, if it accepts pointer/keyboard actions, and whether any JavaScript executes. Do not infer that visible text implies a retained element. In the GitHub browser, look specifically for `input`, `select`, `button`, `canvas`, `iframe`, `object`, `video`, `dialog` elements inside the rendered README.

**Importante:** no queremos burlar la seguridad de GitHub ni ejecutar código no autorizado. Queremos saber qué funcionalidades oficialmente permitidas sobreviven al renderizado.

This experiment branch is separate from main, and is **not** the public GitHub profile.
