// ブランドリール（1080×1920・30fps・15秒）を作る
//   node tools/sns/reel.js <出力.mp4>
// 1コマずつ描いて ffmpeg でつなぐので、毎回同じ仕上がりになる。音はアプリで流行の音源をつける前提で無音。
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..', '..');
const NM = path.resolve(__dirname, '..', 'node_modules');
const OUT = path.resolve(process.argv[2] || 'vx-reel.mp4');
const FPS = 30, DUR = 15;
const FR = OUT.replace(/\.mp4$/, '') + '-frames';

const asset = (f) => 'data:image/' + (f.endsWith('.svg') ? 'svg+xml' : 'webp') + ';base64,' + fs.readFileSync(path.join(ROOT, 'assets', f)).toString('base64');

function fontCss() {
  let css = '';
  const add = (pkg, file, rename) => {
    let c = fs.readFileSync(path.join(NM, pkg, file), 'utf8');
    if (rename) c = c.replace(/font-family: ?'[^']+'/g, `font-family: '${rename}'`);
    css += c.replace(/url\(\.\/files\//g, `url(https://fonts.local/${pkg}/files/`);
  };
  add('@fontsource-variable/archivo', 'wdth.css', 'Archivo');
  for (const w of [500, 700]) add('@fontsource/noto-sans-jp', `${w}.css`);
  return css;
}

const HTML = `<html><head><style>${fontCss()}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#0a0a0b;color:#fff;font-family:Archivo,'Noto Sans JP',sans-serif;font-feature-settings:"palt";overflow:hidden}
.s{position:absolute;inset:0;opacity:0}
.ph{position:absolute;inset:-4%;background-size:cover;background-position:center;filter:grayscale(1) contrast(1.1) brightness(.8)}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,11,.35),rgba(10,10,11,0) 30%,rgba(10,10,11,.15) 55%,rgba(10,10,11,.92) 85%)}
.c{position:absolute;left:96px;right:96px;text-align:center}
.logo{width:420px;display:block;margin:0 auto}
.en{font-stretch:125%;font-weight:600;letter-spacing:.06em;font-size:96px;line-height:1.05}
.jp{font-family:'Noto Sans JP';font-weight:700;font-size:78px;line-height:1.45;letter-spacing:.02em}
.sub{font-family:'Noto Sans JP';font-weight:500;font-size:38px;color:#d6d6da;line-height:1.6;letter-spacing:.04em}
.neon{color:#d4ff2a}
.stat{display:grid;grid-template-columns:repeat(3,1fr);border-top:2px solid #2a2a2e;border-bottom:2px solid #2a2a2e}
.stat div{padding:70px 0 54px}.stat div+div{border-left:2px solid #2a2a2e}
.stat b{display:block;font-stretch:112%;font-weight:600;font-size:190px;line-height:1;color:#d4ff2a}
.stat span{display:block;font-family:'Noto Sans JP';font-weight:500;font-size:40px;margin-top:22px;letter-spacing:.12em;color:#d6d6da}
.word{font-stretch:125%;font-weight:600;font-size:104px;letter-spacing:.12em}
.bar{width:140px;height:8px;margin:34px auto 0}
</style></head><body>
<div class="s" id="s1"><div class="c" style="top:700px"><img class="logo" id="l1" src="${asset('logo.svg')}"><p class="en" id="t1" style="margin-top:90px">THE <span class="neon">PRO</span><br>PERSPECTIVE.</p></div></div>
<div class="s" id="s2"><div class="ph" id="p2" style="background-image:url(${asset('founder.webp')});background-position:56% 45%"></div><div class="sh"></div><div class="c" style="top:1080px" id="t2"><p class="jp">元Jリーガーの<br>目線で。</p><p class="sub" style="margin-top:28px">シノヅカイッペイ｜VX SPORTS ACADEMY 代表</p></div></div>
<div class="s" id="s3"><div class="c" style="top:560px"><p class="sub" style="margin-bottom:60px">Jリーグ通算</p><div class="stat"><div><b id="n1">0</b><span>試合</span></div><div><b id="n2">0</b><span>ゴール</span></div><div><b id="n3">0</b><span>アシスト</span></div></div><p class="sub" style="margin-top:44px;font-size:30px;color:#8d8d95">J1・J2リーグ戦（2017〜2022年）</p></div></div>
${[['PERSONAL', 'personal-coach.webp', '#d4746c', 'サッカーのパーソナル指導', 0], ['GYM', 'gym-entrance.webp', '#d4ff2a', 'キッズからアスリートまでのジム', 0], ['SOCCER', 'football-kit.webp', '#7f9fd6', 'U-12・U-9 新チーム', 0], ['APPAREL', 'apparel-kit-2.webp', '#8fbf9c', '普段着にもなるアパレル', 1]].map(([w, img, col, sub, color], i) => `
<div class="s" id="c${i}"><div class="ph" id="cp${i}" style="background-image:url(${asset(img)})${color ? ';filter:none' : ''}"></div><div class="sh"></div><div class="c" style="top:1180px"><p class="word">${w}</p><div class="bar" style="background:${col}"></div><p class="sub" style="margin-top:30px">${sub}</p></div></div>`).join('')}
<div class="s" id="s5"><div class="c" style="top:600px" id="t5"><p class="jp">プロの視点を、<br>すべての選手に。</p><img class="logo" src="${asset('logo.svg')}" style="width:300px;margin-top:110px"><p class="sub" style="margin-top:110px">体験・入会は<br>プロフィールのLINEから</p></div></div>
</body></html>`;

// t秒の画面を描く
function render(t) {
  const $ = (id) => document.getElementById(id);
  const clamp = (x) => Math.max(0, Math.min(1, x));
  const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
  const win = (a, b, fade = 0.35) => clamp(Math.min((t - a) / fade, (b - t) / fade));
  // 1 ロゴ
  $('s1').style.opacity = win(0, 2.3, 0.3);
  $('l1').style.opacity = ease((t - 0.1) / 0.7); $('l1').style.transform = `scale(${0.92 + 0.08 * ease((t - 0.1) / 0.9)})`;
  $('t1').style.opacity = ease((t - 0.7) / 0.6); $('t1').style.transform = `translateY(${40 * (1 - ease((t - 0.7) / 0.6))}px)`;
  // 2 代表
  $('s2').style.opacity = win(2.1, 5.4);
  $('p2').style.transform = `scale(${1.14 - 0.1 * clamp((t - 2.1) / 3.3)})`;
  $('t2').style.opacity = ease((t - 2.7) / 0.6); $('t2').style.transform = `translateY(${36 * (1 - ease((t - 2.7) / 0.6))}px)`;
  // 3 数字
  $('s3').style.opacity = win(5.3, 8.1);
  const k = ease((t - 5.6) / 1.4);
  $('n1').textContent = Math.round(95 * k); $('n2').textContent = Math.round(11 * k); $('n3').textContent = Math.round(9 * k);
  // 4 事業
  for (let i = 0; i < 4; i++) {
    const a = 8.0 + i * 0.8;
    $('c' + i).style.opacity = win(a, a + 0.95, 0.15);
    $('cp' + i).style.transform = `scale(${1.12 - 0.06 * clamp((t - a) / 0.95)})`;
  }
  // 5 締め
  $('s5').style.opacity = win(11.3, 15.6, 0.4);
  $('t5').style.transform = `translateY(${30 * (1 - ease((t - 11.3) / 0.7))}px)`;
}

(async () => {
  fs.rmSync(FR, { recursive: true, force: true });
  fs.mkdirSync(FR, { recursive: true });
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.route('https://fonts.local/**', (r) => r.fulfill({ contentType: 'font/woff2', body: fs.readFileSync(path.join(NM, decodeURIComponent(new URL(r.request().url()).pathname.slice(1)))) }));
  await p.setContent(HTML, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.addScriptTag({ content: `window.render=${render.toString()}` });
  for (let f = 0; f < FPS * DUR; f++) {
    await p.evaluate((t) => window.render(t), f / FPS);
    await p.screenshot({ path: path.join(FR, `f${String(f).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 90 });
  }
  await browser.close();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(FR, 'f%04d.jpg'), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT]);
  fs.rmSync(FR, { recursive: true, force: true });
  console.log(OUT);
})();
