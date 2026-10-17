# LAB 005 · JUEGO REAL EN UN README, SIN SALIR DE LA PÁGINA

**Investigación experimental en rama aislada. NO es el perfil.**

La nueva hipótesis: GitHub permite una **cuadrícula visual auténtica** de decisiones nativas usando `<table>` + `<details>` + imágenes. A diferencia del árbol de tres en raya de 813 estados, estas casillas son **independientes** y no aumentan exponencialmente el tamaño.

## EXPERIMENTO A · CAMPO MINADO · 6 × 6

**Objetivo:** descubrir todas las casillas seguras sin abrir ninguna mina. Hay **7 minas ocultas** y **29 casillas seguras**. Tocá cada loseta. Al abrirla, aparece la cantidad de minas vecinas (incluye diagonales).

**Limitaciones declaradas:** juego de lógica y riesgo con reglas verificables y revelado real; sin marcador automático, cascada de casillas vacías, banderas persistentes ni bloqueo tras perder. Reinicio: recargar esta misma página. Sin JavaScript. **No está diseñado para su publicación definitiva.**

<table>
<tbody>
<tr><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 1:1 cerrada"></summary>

✅ Despejado

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 1:2 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 1:3 cerrada"></summary>

💥 **MINA — PERDISTE**

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 1:4 cerrada"></summary>

🔹 **3** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 1:5 cerrada"></summary>

🔹 **1** mina adyacente

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 1:6 cerrada"></summary>

🔹 **1** mina adyacente

</details></td></tr>
<tr><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 2:1 cerrada"></summary>

✅ Despejado

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 2:2 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 2:3 cerrada"></summary>

💥 **MINA — PERDISTE**

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 2:4 cerrada"></summary>

🔹 **3** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 2:5 cerrada"></summary>

💥 **MINA — PERDISTE**

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 2:6 cerrada"></summary>

🔹 **1** mina adyacente

</details></td></tr>
<tr><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 3:1 cerrada"></summary>

🔹 **1** mina adyacente

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 3:2 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 3:3 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 3:4 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 3:5 cerrada"></summary>

🔹 **1** mina adyacente

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 3:6 cerrada"></summary>

🔹 **1** mina adyacente

</details></td></tr>
<tr><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 4:1 cerrada"></summary>

🔹 **1** mina adyacente

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 4:2 cerrada"></summary>

💥 **MINA — PERDISTE**

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 4:3 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 4:4 cerrada"></summary>

🔹 **1** mina adyacente

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 4:5 cerrada"></summary>

🔹 **1** mina adyacente

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 4:6 cerrada"></summary>

✅ Despejado

</details></td></tr>
<tr><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 5:1 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 5:2 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 5:3 cerrada"></summary>

🔹 **3** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 5:4 cerrada"></summary>

💥 **MINA — PERDISTE**

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 5:5 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 5:6 cerrada"></summary>

🔹 **1** mina adyacente

</details></td></tr>
<tr><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 6:1 cerrada"></summary>

🔹 **1** mina adyacente

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 6:2 cerrada"></summary>

💥 **MINA — PERDISTE**

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 6:3 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 6:4 cerrada"></summary>

🔹 **2** minas adyacentes

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 6:5 cerrada"></summary>

💥 **MINA — PERDISTE**

</details></td><td align="center"><details><summary><img src="./assets/grid-hidden.svg" width="51" alt="Celda 6:6 cerrada"></summary>

🔹 **1** mina adyacente

</details></td></tr>
</tbody>
</table>

<details><summary>Reglas y valores de prueba (abrir solo para QA)</summary>

- Celda numerada: número de minas en las ocho celdas vecinas.
- Mina abierta: derrota, aunque el README no puede bloquear clicks posteriores.
- Para QA determinista, la casilla 1,1 es segura, la casilla 1,3 contiene mina y 1,2 muestra exactamente **2** minas adyacentes.
- Hay 36 elementos `details` independientes, no estados precalculados anidados.

</details>

## EXPERIMENTO B · Lista de tareas Markdown nativa

Estas casillas son sintaxis GFM, **no** `input` HTML arbitrario. Importa si un visitante anónimo puede activar el control sin editar el archivo.

- [ ] GAMETASK_ALPHA
- [ ] GAMETASK_BETA
- [x] GAMETASK_COMPLETED

## EXPERIMENTO C · Hotspots `map`/`area` y anclas internas

¿Permite GitHub zonas clicables diferentes sobre **una misma imagen**? Si HTML `map` y `area` son eliminados, no aparecerán hotspots reales. Si los conserva, hay que comprobar que solo hacen navegación a fragmentos internos, **no estado arbitrario ni game loop**.

<img src="./assets/grid-hidden.svg" alt="Imagen de prueba para zonas interactuables" width="164" height="164" usemap="#maze-hotspots" />
<map name="maze-hotspots">
  <area shape="rect" coords="0,0,81,164" href="#hotspot-left" alt="LEFT">
  <area shape="rect" coords="82,0,164,164" href="#hotspot-right" alt="RIGHT">
</map>

### HOTSPOT LEFT

<details id="hotspot-left"><summary>HOTSPOT_LEFT_DESTINATION</summary>LEFT_CLICK_RECORDED_VISUALLY</details>

### HOTSPOT RIGHT

<details id="hotspot-right"><summary>HOTSPOT_RIGHT_DESTINATION</summary>RIGHT_CLICK_RECORDED_VISUALLY</details>

## EXPERIMENTO D · Controles de escena por enlaces locales

La sintaxis Markdown `[acción](#...)` crea navegación a una sección de **esta misma página**. No es un botón de movimiento ni una simulación de teclado. Queremos saber si las anclas funcionan y si su desplazamiento altera también la URL/hash.

[Ir a casilla izquierda](#hotspot-left) | [Ir a casilla derecha](#hotspot-right)

## Criterio de aprobación

1. Tablero de 6 × 6 se ve ordenado como una grilla y no desborda hacia una lista vertical.
2. Tocando una sola casilla se revela **su valor real**, permaneciendo el resto oculto.
3. Se pueden revelar casillas **independientemente** (sin cerrar las anteriores) sin cambiar URL.
4. Las imágenes de losetas no fuerzan una navegación ni una carga externa.
5. La cuadrícula es legible en móvil, y no hay una lista gigante debajo del tablero.
6. Anclas, hotspots y checkboxes se examinan separadamente. No atribuirles capacidades que no demuestren.

Este laboratorio no altera la rama principal ni el perfil GitHub.


---

## EXPERIMENTO E · HTML table compacta, una línea por tablero

Esta matriz de seis casillas usa HTML válido en una sola línea, sin saltos entre `td` y `details`. Sirve para detectar si el fallo de la prueba A fue por el parser Markdown y espacios extra, no por incompatibilidad fundamental.

<table><tr><td><details><summary>🔒 A1</summary>🍏 1</details></td><td><details><summary>🔒 A2</summary>🍋 2</details></td><td><details><summary>🔒 A3</summary>🧨 3</details></td></tr><tr><td><details><summary>🔒 B1</summary>🐝 4</details></td><td><details><summary>🔒 B2</summary>🌟 5</details></td><td><details><summary>🔒 B3</summary>🍎 6</details></td></tr></table>

## EXPERIMENTO F · Tabla Markdown con HTML inline

Esta variante usa la sintaxis oficial de tabla GFM, con controles `details` de una sola línea en cada celda. Debe conservar dos filas y tres columnas incluso cuando se abran dos casillas.

| 1 | 2 | 3 |
|:---:|:---:|:---:|
| <details><summary>🔒 A1</summary>🍏 1</details> | <details><summary>🔒 A2</summary>🍋 2</details> | <details><summary>🔒 A3</summary>🧨 3</details> |
| <details><summary>🔒 B1</summary>🐝 4</details> | <details><summary>🔒 B2</summary>🌟 5</details> | <details><summary>🔒 B3</summary>🍎 6</details> |

**Criterio diferencial:** si E o F se ve como 2×3 (no como una lista), hay una ruta concreta para empaquetar el campo minado con tamaño constante. Si ambas fallan, descartar tablas con controles nativos en README.
