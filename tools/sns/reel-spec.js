// 台本（JSON）からリール（1080×1920・30fps・無音）を作る。撮影がない週の「代わりのリール」用。
//   node tools/sns/reel-spec.js <台本.json> <出力.mp4>
// 写真はサイトの assets/ にある本物だけを使う。音はアプリで流行の音源をつける前提で無音。
// 台本の形：{"scenes":[
//   {"dur":2.4,"photo":"personal-coach.webp","pos":"center","kicker":"PRO EYE","title":"大きい文字<br>2行目","sub":"小さい文字"},
//   {"dur":2.4,"photo":"football-kit.webp","whole":true,...}  ← 写真を切らずに上に全部見せる
//   {"dur":2.4,"kicker":"..","list":[["01","項目"],["02","項目"]]},
//   {"dur":2.4,"kicker":"..","title":"..","price":[["初回体験","¥5,500"],["本レッスン","¥16,500"]],"note":"税込"},
//   {"dur":3,"end":true,"title":"続きは、体験で。","sub":"プロフィールのLINEで「体験」と送ってください。"}]}
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..', '..');
const NM = path.resolve(__dirname, '..', 'node_modules');
const SPEC = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = path.resolve(process.argv[3] || 'reel.mp4');
const FPS = 30;
const FR = OUT.replace(/\.mp4$/, '') + '-frames';
// 台本に "theme":"apparel" で、VX APPAREL 用（写真はカラーのまま・差し色は白・下の文字は @vx.apparel.official）
const APPAREL = SPEC.theme === 'apparel';
const GYM = SPEC.theme === 'gym'; // VX GYM 用（写真はカラー・差し色ネオン・下の文字は @vx.gym.official）
const NEON = APPAREL ? '#f0ede8' : '#d4ff2a';

const asset = (f) => 'data:image/' + (f.endsWith('.svg') ? 'svg+xml' : f.endsWith('.webp') ? 'webp' : 'jpeg') + ';base64,' + fs.readFileSync(path.join(ROOT, 'assets', f)).toString('base64');
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

const scenes = SPEC.scenes;
let acc = 0;
const starts = scenes.map((s) => { const a = acc; acc += s.dur; return a; });
const DUR = acc;

const sceneHtml = (s, i) => {
  const k = s.kicker ? `<p class="kicker">${s.kicker}</p>` : '';
  const list = s.list ? `<div class="list">${s.list.map(([b, t]) => `<div><b>${b}</b><span>${t}</span></div>`).join('')}</div>` : '';
  const price = s.price ? `<div class="price">${s.price.map(([t, b], j) => `<div class="${j === s.price.length - 1 && s.hlLast ? 'hl' : ''}"><span>${t}</span><b>${b}</b></div>`).join('')}</div>${s.note ? `<p class="note">${s.note}</p>` : ''}` : '';
  const logo = s.end ? `<img class="logo" src="${asset('logo.svg')}">` : '';
  const photo = !s.photo ? '' : s.whole
    ? `<img class="whole" id="p${i}" src="${asset(s.photo)}">`
    : `<div class="ph" id="p${i}" style="background-image:url(${asset(s.photo)});background-position:${s.pos || 'center'}"></div><div class="sh"></div>`;
  const place = s.photo ? 'bottom:260px' : 'top:50%;transform:translateY(-50%)';
  const tag = s.tag ? `<div style="position:absolute;right:64px;top:150px;z-index:6;font-family:'Noto Sans JP';font-size:26px;color:#e6e6ea;background:rgba(0,0,0,.45);padding:8px 16px;border-radius:8px">${s.tag}</div>` : '';
  return `<div class="s" id="s${i}">${photo}${tag}<div class="c" style="${place}"><div id="t${i}">${k}${s.title ? `<p class="jp">${s.title}</p>` : ''}${s.sub ? `<p class="sub">${s.sub}</p>` : ''}${list}${price}${logo}</div></div></div>`;
};

const HTML = `<html><head><style>${fontCss()}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#0a0a0b;color:#fff;font-family:Archivo,'Noto Sans JP',sans-serif;font-feature-settings:"palt";overflow:hidden}
.s{position:absolute;inset:0;opacity:0}
.ph{position:absolute;inset:-4%;background-size:cover;filter:${APPAREL ? 'brightness(.92)' : GYM ? 'brightness(.85)' : 'grayscale(1) contrast(1.1) brightness(.8)'}}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,11,.4),rgba(10,10,11,0) 28%,rgba(10,10,11,.2) 50%,rgba(10,10,11,.95) 80%)}
.c{position:absolute;left:96px;right:96px}
.whole{position:absolute;left:0;top:260px;width:1080px;height:auto;transform-origin:center top}
.kicker{font-stretch:125%;font-weight:600;font-size:30px;letter-spacing:.32em;color:${NEON};margin-bottom:34px}
.jp{font-family:'Noto Sans JP';font-weight:700;font-size:92px;line-height:1.4;letter-spacing:.02em}
.sub{font-family:'Noto Sans JP';font-weight:500;font-size:40px;color:#d6d6da;line-height:1.65;letter-spacing:.04em;margin-top:34px}
.list{margin-top:50px;border-top:2px solid #2a2a2e}
.list div{display:grid;grid-template-columns:150px 1fr;align-items:baseline;padding:34px 0;border-bottom:2px solid #2a2a2e}
.list b{font-stretch:112%;font-weight:600;font-size:40px;color:${NEON}}
.list span{font-family:'Noto Sans JP';font-weight:700;font-size:54px;letter-spacing:.03em}
.price{margin-top:50px;border-top:2px solid #2a2a2e}
.price div{display:grid;grid-template-columns:1fr auto;align-items:baseline;padding:34px 0;border-bottom:2px solid #2a2a2e}
.price span{font-family:'Noto Sans JP';font-weight:500;font-size:44px}
.price b{font-stretch:112%;font-weight:600;font-size:64px}
.price .hl b{color:${NEON}}
.note{font-family:'Noto Sans JP';font-size:32px;color:#8d8d95;margin-top:30px;line-height:1.6}
.logo{width:300px;display:block;margin-top:100px}
.foot{position:absolute;left:96px;right:96px;bottom:120px;display:flex;justify-content:space-between;font-stretch:110%;font-size:22px;letter-spacing:.18em;color:#7d7d85;z-index:5;white-space:nowrap;gap:40px}
.top{position:absolute;left:96px;top:130px;z-index:5}.top img{height:40px}
</style></head><body>
${scenes.map(sceneHtml).join('')}
<div class="top"><img src="${asset('logo.svg')}"></div>
<div class="foot">${APPAREL ? '<span>THE PRO PERSPECTIVE.</span><span>@vx.apparel.official</span>' : GYM ? '<span>VX GYM｜NISHI-AZABU</span><span>@vx.gym.official</span>' : '<span>VX SPORTS ACADEMY</span><span>@vx_sports_academy</span>'}</div>
</body></html>`;

function render(t, starts, durs) {
  const clamp = (x) => Math.max(0, Math.min(1, x));
  const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
  const n = starts.length;
  for (let i = 0; i < n; i++) {
    const a = starts[i], b = a + durs[i];
    const fin = i === 0 ? 1 : clamp((t - a) / 0.25);           // 最初の場面は0秒目から見せる（1秒目が勝負）
    const fout = i === n - 1 ? 1 : clamp((b + 0.25 - t) / 0.25);
    const el = document.getElementById('s' + i);
    el.style.opacity = t >= a - 0.01 && t < b + 0.25 ? Math.min(fin, fout) : 0;
    const p = document.getElementById('p' + i);
    if (p) p.style.transform = p.tagName === 'IMG' ? `scale(${1 + 0.04 * clamp((t - a) / durs[i])})` : `scale(${1.12 - 0.08 * clamp((t - a) / durs[i])})`;
    const tx = document.getElementById('t' + i);
    const k = i === 0 ? 1 : ease((t - a - 0.1) / 0.5);
    tx.style.opacity = k; tx.style.transform = `translateY(${36 * (1 - k)}px)`;
  }
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
  const durs = scenes.map((s) => s.dur);
  for (let f = 0; f < Math.round(FPS * DUR); f++) {
    await p.evaluate(([t, s, d]) => window.render(t, s, d), [f / FPS, starts, durs]);
    await p.screenshot({ path: path.join(FR, `f${String(f).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 90 });
  }
  // 確認用の静止画（各場面の真ん中）
  for (let i = 0; i < scenes.length; i++) {
    await p.evaluate(([t, s, d]) => window.render(t, s, d), [starts[i] + durs[i] * 0.7, starts, durs]);
    await p.screenshot({ path: OUT.replace(/\.mp4$/, `-check${i + 1}.jpg`), type: 'jpeg', quality: 70 });
  }
  await browser.close();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(FR, 'f%04d.jpg'), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT]);
  fs.rmSync(FR, { recursive: true, force: true });
  console.log(OUT, DUR.toFixed(1) + 's');
})();
