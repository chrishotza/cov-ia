// Deterministic README builder. Node.js >=18, no external dependencies.
import fs from 'node:fs';
const buildReadme = function buildReadme(){
 const mines=new Set([2,8,10,19,27,31,34]),SIZE=6;
 function clue(i){if(mines.has(i))return "💥";let x=i%SIZE,y=Math.floor(i/SIZE),n=0;for(let j=-1;j<=1;j++)for(let k=-1;k<=1;k++){if(!j&&!k)continue;const xx=x+k,yy=y+j;if(xx>=0&&xx<SIZE&&yy>=0&&yy<SIZE&&mines.has(yy*SIZE+xx))n++;}return n;}
 const columns=["01","02","03","04","05","06"];
 const head=`| ${columns.join(" | ")} |\n|${columns.map(()=>" :--: ").join("|")}|`;
 const rows=Array.from({length:SIZE},(_,y)=>{
   const cells=Array.from({length:SIZE},(_,x)=>{const i=y*SIZE+x;let v=clue(i),reveal=v==="💥"?"<strong>💥 MINA</strong>":v===0?"<strong>✓</strong>":`<strong>${v}</strong>`;return `<details><summary><img alt="Abrir nodo ${y+1}-${x+1}" src="./assets/core-breach-tile.svg" width="33"/></summary>${reveal}</details>`});
   return `| ${cells.join(" | ")} |`;
 }).join("\n");
 return `<!-- NATIVE README GAME. 36 INDEPENDENT DETAILS, NO SCRIPTS. EXPERIMENTAL ONLY. -->
![CORE BREACH / animated title](./assets/core-breach-header.svg)

### DEFUSE THE GRID

**07 minas · 29 casillas seguras · 00 instalaciones · 00 redirecciones**

Una cuadrícula real con minas y números calculados a partir de una distribución fija. **Hacé clic sobre cada nodo para descubrirlo.** El número indica cuántas minas hay en las ocho casillas vecinas. Evitá todas las minas y abrí los 29 nodos seguros para superar el desafío.

${head}
${rows}

<details><summary>◈ AYUDA / REGLAS</summary>

- **1–8**: cantidad de minas adyacentes, incluyendo diagonales.
- **✓**: casilla libre de minas vecinas.
- **💥 MINA**: pisaste una mina. La partida termina según las reglas; el HTML no puede desactivar otros clics.
- **Reiniciar:** F5. No se registran estadísticas ni se compara automáticamente el número de casillas seguras.
- **Limitación del prototipo:** sin banderas, autodespeje, cronómetro, victoria automática ni bloqueo tras derrota. Es un **minijuego de revelación y deducción**, no un motor de física.

</details>

<sub>GitHub native / GFM table + HTML details + SVG graphics. El navegador no ejecuta código del autor. Esta rama es experimental y no es el README de \`chrishotza\`.</sub>
`;
};
fs.writeFileSync(new URL('../README.md', import.meta.url),buildReadme(),'utf8');
console.log('README.md generated; 36 independent clickable nodes');
