// Instagram カルーセル画像（1080×1350）を、サイトと同じ世界観で作る
//   node tools/sns/carousels.js <出力フォルダ> [名前...]
// 写真はサイトの assets/ にある本物だけを使う（オリジナル性の評価を落とさないため）
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const NM = path.resolve(__dirname, '..', 'node_modules');
const OUT = path.resolve(process.argv[2] || 'sns-out');
const ONLY = process.argv.slice(3);

const asset = (f) => 'data:image/' + (f.endsWith('.svg') ? 'svg+xml' : f.endsWith('.webp') ? 'webp' : 'jpeg') + ';base64,' + fs.readFileSync(path.join(ROOT, 'assets', f)).toString('base64');
const LOGO = asset('logo.svg');
const NEON = '#d4ff2a';

function fontCss() {
  let css = '';
  const add = (pkg, file, rename) => {
    let c = fs.readFileSync(path.join(NM, pkg, file), 'utf8');
    if (rename) c = c.replace(/font-family: ?'[^']+'/g, `font-family: '${rename}'`);
    css += c.replace(/url\(\.\/files\//g, `url(https://fonts.local/${pkg}/files/`);
  };
  add('@fontsource-variable/archivo', 'wdth.css', 'Archivo');
  for (const w of [400, 500, 700]) add('@fontsource/noto-sans-jp', `${w}.css`);
  return css;
}

const BASE_CSS = `
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#0a0a0b;color:#fff;font-family:Archivo,'Noto Sans JP',sans-serif;font-feature-settings:"palt";overflow:hidden;position:relative}
.top{position:absolute;left:72px;right:72px;top:64px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.top img{height:30px}.top span{font-stretch:125%;font-size:20px;letter-spacing:.3em;color:#bdbdc3}
.photo{position:absolute;inset:0;background-size:cover;background-position:center;filter:grayscale(1) contrast(1.08)}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,11,.55) 0%,rgba(10,10,11,0) 28%,rgba(10,10,11,.2) 50%,rgba(10,10,11,.96) 82%)}
.body{position:absolute;left:72px;right:72px;bottom:110px;z-index:5}
.mid{position:absolute;left:72px;right:72px;top:220px;bottom:150px;display:flex;flex-direction:column;justify-content:center;z-index:5}
.kicker{font-stretch:125%;font-size:22px;letter-spacing:.32em;color:#bdbdc3;margin-bottom:28px}
h1{font-family:'Noto Sans JP';font-weight:700;font-size:76px;line-height:1.38;letter-spacing:.02em}
h2{font-family:'Noto Sans JP';font-weight:700;font-size:64px;line-height:1.4;letter-spacing:.02em}
p.lead{font-family:'Noto Sans JP';font-weight:500;font-size:34px;line-height:1.75;color:#d6d6da;margin-top:34px;letter-spacing:.03em}
.bar{width:84px;height:5px;background:${NEON};margin:34px 0 0}
.foot{position:absolute;left:72px;right:72px;bottom:56px;display:flex;justify-content:space-between;font-stretch:125%;font-size:18px;letter-spacing:.3em;color:#7d7d85;z-index:5}
.neon{color:${NEON}}
.whole{position:absolute;left:0;top:140px;width:1080px;height:auto;display:block}
.below{position:absolute;left:72px;right:72px;bottom:110px;z-index:5}
.list{margin-top:44px;border-top:1px solid #2a2a2e}
.list div{display:grid;grid-template-columns:200px 1fr;align-items:baseline;padding:26px 0;border-bottom:1px solid #2a2a2e}
.list b{font-stretch:112%;font-weight:500;font-size:30px;color:#9a9aa2;letter-spacing:.04em}
.list span{font-family:'Noto Sans JP';font-weight:700;font-size:38px;letter-spacing:.03em}
.stats{display:grid;grid-template-columns:repeat(3,1fr);margin-top:56px;border-top:1px solid #2a2a2e;border-bottom:1px solid #2a2a2e}
.stats div{display:flex;flex-direction:column;align-items:center;padding:52px 0 40px}.stats div+div{border-left:1px solid #2a2a2e}
.stats b{font-stretch:112%;font-weight:600;font-size:150px;line-height:1;color:${NEON}}
.stats span{font-family:'Noto Sans JP';font-weight:500;font-size:30px;margin-top:18px;color:#d6d6da;letter-spacing:.1em}
.small{font-family:'Noto Sans JP';font-size:24px;color:#8d8d95;margin-top:26px;line-height:1.6}
.cta{margin-top:56px;border:2px solid #fff;padding:40px 44px}
.cta p{font-family:'Noto Sans JP';font-weight:700;font-size:40px;line-height:1.6}
.cta small{display:block;font-family:'Noto Sans JP';font-weight:500;font-size:26px;color:#bdbdc3;margin-top:14px}
.svc{margin-top:48px;display:grid;gap:18px}
.svc div{display:flex;align-items:baseline;gap:28px;padding:22px 30px;background:#141416;border-left:4px solid var(--c)}
.svc b{font-stretch:125%;font-weight:600;font-size:34px;letter-spacing:.14em;min-width:250px}
.svc span{font-family:'Noto Sans JP';font-weight:500;font-size:28px;color:#cfcfd4}
.metric{display:grid;grid-template-columns:1fr auto;align-items:end;padding:34px 0;border-bottom:1px solid #2a2a2e}
.metric b{display:block;font-stretch:125%;font-weight:600;font-size:46px;letter-spacing:.16em}
.metric span{font-family:'Noto Sans JP';font-size:30px;color:#cfcfd4}
.metric em{font-style:normal;font-stretch:112%;font-size:70px;color:${NEON}}
.price{display:grid;grid-template-columns:1fr auto;align-items:baseline;padding:30px 0;border-bottom:1px solid #2a2a2e}
.price span{font-family:'Noto Sans JP';font-weight:500;font-size:36px}
.price b{font-stretch:112%;font-weight:600;font-size:52px}
.price.hl b{color:${NEON}}
`;

const page = (n, total, inner, { photo, pos, color, whole } = {}) => `
${photo && whole ? `<img class="whole" src="${photo}">` : ''}${photo && !whole ? `<div class="photo" style="background-image:url(${photo});background-position:${pos || 'center'}${color ? ';filter:none' : ''}"></div><div class="shade"></div>` : ''}
<div class="top"><img src="${LOGO}"><span>${String(n).padStart(2, '0')} / ${String(total).padStart(2, '0')}</span></div>
${inner}
<div class="foot"><span>VX SPORTS ACADEMY</span><span>@vx_sports_academy</span></div>`;

const CTA_LINE = '体験・入会は、プロフィールのLINEで<br>「体験」と送ってください。';

const SETS = {
  founder: [
    (n, t) => page(n, t, `<div class="body"><p class="kicker">FOUNDER</p><h1>元Jリーガーが、<br>子どもを教える。</h1><div class="bar"></div><p class="lead">VX SPORTS ACADEMY 代表<br>シノヅカイッペイ</p></div>`, { photo: asset('founder.webp'), pos: '38% 40%' }),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">CAREER</p><h2>16歳で、<br>ロシアへ。</h2><p class="lead">スパルタク・モスクワで、プロのキャリアをスタート。<br>U-18ロシア代表にも選ばれました。</p></div>`),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">J.LEAGUE</p><h2>Jリーグ、4クラブ。</h2><div class="list"><div><b>2017–19</b><span>横浜F・マリノス（J1）</span></div><div><b>2019–20</b><span>大宮アルディージャ（J2）</span></div><div><b>2021</b><span>柏レイソル（J1）</span></div><div><b>2022</b><span>アルビレックス新潟（J2）</span></div></div></div>`),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">STATS</p><h2>Jリーグ通算</h2><div class="stats"><div><b>95</b><span>試合</span></div><div><b>11</b><span>ゴール</span></div><div><b>9</b><span>アシスト</span></div></div><p class="small">J1・J2リーグ戦（2017〜2022年）出典：Football LAB</p></div>`),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">VX SPORTS ACADEMY</p><h2>プロの視点を、<br>すべての選手に。</h2><div class="svc"><div style="--c:#d4746c"><b>PERSONAL</b><span>サッカーのパーソナル指導</span></div><div style="--c:${NEON}"><b>GYM</b><span>キッズからアスリートまでのジム</span></div><div style="--c:#7f9fd6"><b>SOCCER</b><span>U-12・U-9 新チーム</span></div><div style="--c:#8fbf9c"><b>APPAREL</b><span>普段着にもなるアパレル</span></div></div></div>`),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">JOIN</p><h2>トップレベルで<br>戦ってきた経験を、<br>次の世代へ。</h2><div class="cta"><p>${CTA_LINE}</p><small>キッズからアスリートまで・初回体験 ¥5,500（税込）</small></div></div>`),
  ],
  gym: [
    (n, t) => page(n, t, `<div class="body"><p class="kicker">VX GYM｜NISHI-AZABU</p><h1>成長が、<br><span class="neon">数字</span>で見える。</h1><div class="bar"></div><p class="lead">西麻布・2027年1月オープン予定<br>キッズからアスリートまで</p></div>`, { photo: asset('gym-entrance.webp'), pos: 'center 60%' }),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">MEASURE</p><h2>毎回、3つを測る。</h2><div style="margin-top:40px;border-top:1px solid #2a2a2e"><div class="metric"><div><b>POWER</b><span>パワー出力・一瞬で出せる力</span></div><em>W</em></div><div class="metric"><div><b>JUMP</b><span>ジャンプ・跳ぶ力とバネ</span></div><em>cm</em></div><div class="metric"><div><b>SPEED</b><span>スピード・走る、切り返す速さ</span></div><em>s</em></div></div></div>`),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">PROGRESS</p><h2>入会したときからの<br>伸びを、グラフに。</h2><svg viewBox="0 0 936 360" style="width:100%;margin-top:56px"><g stroke="#2a2a2e" stroke-width="2"><line x1="0" y1="90" x2="936" y2="90"/><line x1="0" y1="180" x2="936" y2="180"/><line x1="0" y1="270" x2="936" y2="270"/><line x1="0" y1="358" x2="936" y2="358"/></g><polyline points="10,330 170,310 330,286 490,250 650,210 810,150 926,110" fill="none" stroke="${NEON}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round"/><circle cx="926" cy="110" r="16" fill="${NEON}"/></svg><p class="small">※グラフはイメージです</p><p class="lead">数字で見えるから、努力が続く。成長がわかる。</p></div>`),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">PRICE｜月額・税込</p><h2>年齢を問わず、<br>年代別のクラスで。</h2><div style="margin-top:40px;border-top:1px solid #2a2a2e"><div class="price"><span>週1回（月4回）</span><b>¥17,800</b></div><div class="price"><span>週2回（月8回）</span><b>¥28,000</b></div><div class="price hl"><span>エリート（追加）</span><b>+¥15,000</b></div></div><p class="small">エリート：月1回のマンツーマン＋測定結果のフィードバック<br>年代別のグループクラス｜定員8人・指導者1人</p></div>`),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">PRE-REGISTRATION</p><h2>オープン情報を、<br>いちばん先に。</h2><div class="cta"><p>先行予約は、プロフィールのLINEで<br>「ジム」と送ってください。</p><small>オープン日・料金・体験会のご案内を優先してお送りします（無料）</small></div></div>`),
  ],
  wear: [
    (n, t) => page(n, t, `<div class="below"><p class="kicker">VX APPAREL｜PRE-ORDER</p><h1>動ける服を、<br>毎日の服に。</h1><div class="bar"></div><p class="lead">VX APPAREL</p></div>`, { photo: asset('apparel-kit-2.webp'), whole: true }),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">MATERIAL</p><h2>街でも、<br>練習でも。</h2><div class="list"><div><b>01</b><span>軽量・速乾</span></div><div><b>02</b><span>4方向ストレッチ</span></div><div><b>03</b><span>撥水</span></div><div><b>04</b><span>動きやすいスリット</span></div><div><b>05</b><span>夜でも目立つリフレクティブ</span></div></div></div>`),
    (n, t) => page(n, t, `<div class="below"><p class="kicker">6 COLORS</p><h2>ユニセックス<br>6色。</h2><p class="lead">Ink Black／Sage Green／Powder Blue<br>Petal Pink／Mist Lavender／Cloud White</p></div>`, { photo: asset('apparel-colors.webp'), whole: true }),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">PRICE｜税込</p><h2>VX APPAREL</h2><div style="margin-top:40px;border-top:1px solid #2a2a2e"><div class="price"><span>Tシャツ</span><b>¥7,700</b></div><div class="price"><span>ショーツ</span><b>¥6,600</b></div><div class="price"><span>ソックス</span><b>¥2,200</b></div><div class="price hl"><span>3点セット</span><b>¥14,300</b></div></div><p class="small">3点セットは単品合計より¥2,200お得｜サイズ S・M・L・XL</p></div>`),
    (n, t) => page(n, t, `<div class="mid"><p class="kicker">PRE-ORDER</p><h2>予約受付中。</h2><div class="cta"><p>ご予約は、プロフィールのリンクから。<br>サイズ・色のご相談はDMで。</p><small>予約締切後の生産です。お届け時期はLINEでご案内します。</small></div></div>`),
  ],
};

// 台本（JSON）からカルーセルを作る：node tools/sns/carousels.js <出力> --spec 台本.json
// 台本の形：{"name":"agility","slides":[{"type":"cover","photo":"gym-entrance.webp","kicker":"PRO EYE","title":"タイトル<br>2行目","lead":"補足"},
//   {"type":"text","kicker":"..","title":"..","lead":".."},{"type":"list","kicker":"..","title":"..","items":[["01","項目"],["02","項目"]],"small":".."},
//   {"type":"cta","kicker":"JOIN","title":"..","cta":"体験・入会は…","small":".."}]}
function fromSpec(spec) {
  const esc = (x) => String(x ?? '');
  return spec.slides.map((sl) => (n, t) => {
    const k = sl.kicker ? `<p class="kicker">${esc(sl.kicker)}</p>` : '';
    if (sl.type === 'cover') return page(n, t, `<div class="body">${k}<h1>${esc(sl.title)}</h1><div class="bar"></div>${sl.lead ? `<p class="lead">${esc(sl.lead)}</p>` : ''}</div>`, sl.photo ? { photo: asset(sl.photo), pos: sl.pos, color: sl.color } : {});
    if (sl.type === 'list') return page(n, t, `<div class="mid">${k}<h2>${esc(sl.title)}</h2><div class="list">${(sl.items || []).map(([b, s]) => `<div><b>${esc(b)}</b><span>${esc(s)}</span></div>`).join('')}</div>${sl.small ? `<p class="small">${esc(sl.small)}</p>` : ''}</div>`);
    if (sl.type === 'cta') return page(n, t, `<div class="mid">${k}<h2>${esc(sl.title)}</h2><div class="cta"><p>${esc(sl.cta || CTA_LINE)}</p>${sl.small ? `<small>${esc(sl.small)}</small>` : ''}</div></div>`);
    return page(n, t, `<div class="mid">${k}<h2>${esc(sl.title)}</h2>${sl.lead ? `<p class="lead">${esc(sl.lead)}</p>` : ''}${sl.small ? `<p class="small">${esc(sl.small)}</p>` : ''}</div>`);
  });
}
const specIdx = process.argv.indexOf('--spec');
if (specIdx > 0) {
  const spec = JSON.parse(fs.readFileSync(process.argv[specIdx + 1], 'utf8'));
  for (const k of Object.keys(SETS)) delete SETS[k];
  SETS[spec.name] = fromSpec(spec);
  ONLY.length = 0;
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const css = fontCss();
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.route('https://fonts.local/**', (r) => r.fulfill({ contentType: 'font/woff2', body: fs.readFileSync(path.join(NM, decodeURIComponent(new URL(r.request().url()).pathname.slice(1)))) }));
  for (const [name, slides] of Object.entries(SETS)) {
    if (ONLY.length && !ONLY.includes(name)) continue;
    for (let i = 0; i < slides.length; i++) {
      await p.setContent(`<html><head><style>${css}${BASE_CSS}</style></head><body>${slides[i](i + 1, slides.length)}</body></html>`, { waitUntil: 'load' });
      await p.evaluate(() => document.fonts.ready);
      const file = path.join(OUT, `${name}-${String(i + 1).padStart(2, '0')}.jpg`);
      await p.screenshot({ path: file, type: 'jpeg', quality: 92 });
      console.log(file);
    }
  }
  await browser.close();
})();
