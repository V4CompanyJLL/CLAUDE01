// usage: node render.js <svgdir> <outdir> [scale] [pdfpath]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [svgdir, outdir, scale = '1', pdf] = process.argv.slice(2);
  fs.mkdirSync(outdir, { recursive: true });
  const files = fs.readdirSync(svgdir).filter(f => f.endsWith('.svg')).sort();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: +scale });
  for (const f of files) {
    const svg = fs.readFileSync(path.join(svgdir, f), 'utf8');
    await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
    await page.screenshot({ path: path.join(outdir, f.replace('.svg', '.png')), clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  }
  if (pdf) {
    const body = files.map(f => `<div class="p">${fs.readFileSync(path.join(svgdir, f), 'utf8')}</div>`).join('');
    await page.setContent(`<html><head><style>@page{size:1920px 1080px;margin:0}body{margin:0}.p{width:1920px;height:1080px;overflow:hidden;break-after:page}.p svg{display:block}</style></head><body>${body}</body></html>`);
    await page.pdf({ path: pdf, width: '1920px', height: '1080px', printBackground: true, pageRanges: '' });
  }
  await browser.close();
})();
