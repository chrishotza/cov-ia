import assert from 'node:assert/strict';
import fs from 'node:fs';
const readme=fs.readFileSync(new URL('../README.md',import.meta.url),'utf8');
const svg=fs.readFileSync(new URL('../assets/core-breach-header.svg',import.meta.url),'utf8');
const tile=fs.readFileSync(new URL('../assets/core-breach-tile.svg',import.meta.url),'utf8');
const mines=new Set([2,8,10,19,27,31,34]),SIZE=6;
function clue(i){
  if(mines.has(i))return '💥 MINA';
  const x=i%SIZE,y=Math.floor(i/SIZE);let n=0;
  for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){
    if(dx===0&&dy===0)continue;
    const nx=x+dx,ny=y+dy;
    if(nx>=0&&nx<SIZE&&ny>=0&&ny<SIZE&&mines.has(ny*SIZE+nx))n++;
  }
  return n===0?'✓':String(n);
}
const rows=readme.split('\n').filter(line=>line.startsWith('| <details><summary><img'));
assert.equal(rows.length,6,'six table rows');
const pattern=/<details><summary><img alt="Abrir nodo ([1-6])-([1-6])" src="\.\/assets\/core-breach-tile\.svg" width="33"\/><\/summary><strong>(.*?)<\/strong><\/details>/g;
let count=0, bombs=0,safe=0;
for(let y=0;y<SIZE;y++){
 const cells=[...rows[y].matchAll(pattern)];
 assert.equal(cells.length,SIZE,`row ${y+1} must have six valid playable controls`);
 for(let x=0;x<SIZE;x++){
  const [,rr,cc,value]=cells[x];
  assert.equal(Number(rr),y+1);
  assert.equal(Number(cc),x+1);
  assert.equal(value,clue(y*SIZE+x),`mine count mismatch at ${y+1}-${x+1}`);
  count++;if(value==='💥 MINA')bombs++;else safe++;
 }
}
assert.equal(count,36);
assert.equal(bombs,7);
assert.equal(safe,29);
assert.match(readme,/\| 01 \| 02 \| 03 \| 04 \| 05 \| 06 \|/);
assert.match(svg,/<animate attributeName="x"/);
assert.match(tile,/<svg/);
assert.match(readme,/No se registran estadísticas ni se compara automáticamente el número de casillas seguras/);
assert.ok(readme.length<10000,'README size budget');
console.log('PASS: 6x6 in-README interactive table, 36 independent controls, 7 bombs, 29 valid clue cells, SVG assets, no fake win state');
