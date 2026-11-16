// Renders the favicon PNGs and the Open Graph share images with the site's own fonts.
// Run from the repo root: node tools/render_images.js
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const os = require('os');
const ROOT = path.resolve(__dirname, '..');
const A = 'file://' + ROOT + '/assets/';
const card = (sub) => `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:F;src:url(${A}fonts/fraunces-latin-standard-normal.woff2)}
@font-face{font-family:F;font-style:italic;src:url(${A}fonts/fraunces-latin-standard-italic.woff2)}
@font-face{font-family:I;src:url(${A}fonts/inter-latin-wght-normal.woff2)}
html,body{margin:0;width:1200px;height:630px;background:#16100a;overflow:hidden}
.art{position:absolute;inset:0 0 0 auto;width:640px;background:url(${A}img/almond-blossoms-1600.webp) 30% 40%/cover}
.art:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#16100a 0,rgba(22,16,10,.55) 30%,rgba(22,16,10,0) 70%)}
.t{position:absolute;left:72px;bottom:72px;width:660px;color:#f4eee2}
h1{font:300 92px/0.95 F;margin:0 0 28px;font-variation-settings:"SOFT" 100,"opsz" 144}
h1 em{color:#b8c3aa}
p{font:400 26px/1.35 I;margin:0;max-width:560px}
.m{position:absolute;left:72px;top:64px;width:36px;height:36px}
</style></head><body><div class="art"></div><img class="m" src="${A}img/favicon.svg">
<div class="t"><h1>Guilherme<br><em>Candeias</em> Martins</h1><p>${sub}</p></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const [lang, sub] of [['en', 'Electrical and Computer Engineer · MSc Electrical Engineering (Microelectronics, quantum themed), TU Delft'],
                             ['pt', 'Engenheiro Eletrotécnico e de Computadores · Mestrado em Engenharia Eletrotécnica (Microeletrónica, vertente quântica), TU Delft']]) {
    const tmp = path.join(os.tmpdir(), `og-${lang}.html`); fs.writeFileSync(tmp, card(sub));
    await p.goto('file://' + tmp, { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `${ROOT}/assets/img/og-${lang}.jpg`, type: 'jpeg', quality: 84 });
  }
  for (const [n, s] of [['favicon-32.png', 32], ['apple-touch-icon.png', 180], ['icon-512.png', 512]]) {
    const q = await b.newPage({ viewport: { width: s, height: s } });
    await q.goto(A + 'img/favicon.svg'); await q.screenshot({ path: `${ROOT}/assets/img/${n}` }); await q.close();
  }
  await b.close();
})();
