// サイトの自動点検：速度・アクセシビリティ・SEO・リンク切れ・翻訳漏れ・スマホのはみ出し・構造化データ・情報の鮮度
// 使い方：
//   cd tools && npm install   （初回だけ。lighthouse を入れる）
//   node tools/audit.mjs      （サイトのフォルダで実行。結果は tools/audit-report.md と標準出力）
// 終了コード：重大な問題があれば 1
import { createServer } from 'node:http';
import { readFileSync, writeFileSync, existsSync, statSync } from 'node:fs';
import { join, extname, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const TOOLS = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(TOOLS, '..');
const require = createRequire(join(TOOLS, 'package.json'));
const { chromium } = require('playwright');

const JA = ['index.html', 'personal.html', 'gym.html', 'soccer.html', 'apparel.html', 'tokushoho.html'];
const ALL = [...JA, ...['en', 'zh'].flatMap((l) => JA.slice(0, 5).map((p) => `${l}/${p}`)), '404.html'];
const BASE_PATH = '/vx-sports-academy/';
const problems = []; // {level:'重大'|'注意', where, what}
const notes = [];
const add = (level, where, what) => problems.push({ level, where, what });

// ---- 1) ローカルで本番と同じパスに配信 ----
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8' };
const server = createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (!p.startsWith(BASE_PATH)) { res.writeHead(404); return res.end(); }
  p = p.slice(BASE_PATH.length) || 'index.html';
  if (p.endsWith('/')) p += 'index.html';
  const f = join(ROOT, p);
  if (!f.startsWith(ROOT) || !existsSync(f) || statSync(f).isDirectory()) { res.writeHead(404, { 'content-type': MIME['.html'] }); return res.end(readFileSync(join(ROOT, '404.html'))); }
  res.writeHead(200, { 'content-type': MIME[extname(f)] || 'application/octet-stream' });
  res.end(readFileSync(f));
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const ORIGIN = `http://127.0.0.1:${server.address().port}`;
const url = (p) => ORIGIN + BASE_PATH + p;

// ---- 2) ファイルを読んで確かめる項目 ----
const html = Object.fromEntries(ALL.filter((p) => existsSync(join(ROOT, p))).map((p) => [p, readFileSync(join(ROOT, p), 'utf8')]));
for (const p of ALL) if (!html[p]) add('重大', p, 'ページのファイルがありません');

for (const [p, s] of Object.entries(html)) {
  const dir = p.includes('/') ? p.split('/')[0] + '/' : '';
  // リンク切れ・素材切れ（サイト内）
  const refs = [...s.matchAll(/(?:href|src)="([^"#?]+)(?:[?#][^"]*)?"/g)].map((m) => m[1])
    .concat([...s.matchAll(/srcset="([^"]+)"/g)].flatMap((m) => m[1].split(',').map((x) => x.trim().split(' ')[0])));
  for (const r of refs) {
    if (/^(https?:|mailto:|tel:|data:|javascript:)/.test(r)) continue;
    const target = r.startsWith(BASE_PATH) ? r.slice(BASE_PATH.length) : join(dir, r);
    if (!existsSync(join(ROOT, target))) add('重大', p, `リンク先・画像が見つかりません：${r}`);
  }
  if (p === '404.html') continue;
  // タイトル・説明文
  const title = (s.match(/<title>([^<]*)<\/title>/) || [])[1] || '';
  const desc = (s.match(/<meta name="description" content="([^"]*)"/) || [])[1] || '';
  if (!title) add('重大', p, 'タイトルがありません');
  if (!desc) add('重大', p, '説明文（meta description）がありません');
  if (desc && desc.length < 50) add('注意', p, `説明文が短すぎます（${desc.length}文字）`);
  if (!/<link rel="canonical"/.test(s)) add('注意', p, 'canonical がありません');
  if ((s.match(/<h1[\s>]/g) || []).length !== 1) add('注意', p, `h1 の数が ${(s.match(/<h1[\s>]/g) || []).length} 個です（1個が理想）`);
  // 構造化データ
  for (const m of s.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)) {
    try {
      const j = JSON.parse(m[1]);
      const faq = (j['@graph'] || []).find((x) => x['@type'] === 'FAQPage');
      if (faq) for (const q of faq.mainEntity) if (!s.includes(`<summary>${q.name}</summary>`)) add('重大', p, `構造化データのFAQ「${q.name}」がページに表示されていません`);
    } catch (e) { add('重大', p, '構造化データ（JSON-LD）が壊れています：' + e.message); }
  }
}

// 情報の鮮度（FAQの更新日）
const upd = (html['index.html'] || '').match(/情報更新日：(\d{4})年(\d{1,2})月(\d{1,2})日/);
if (upd) {
  const days = Math.floor((Date.now() - Date.UTC(+upd[1], +upd[2] - 1, +upd[3])) / 86400000);
  notes.push(`FAQの情報更新日：${upd[1]}/${upd[2]}/${upd[3]}（${days}日前）`);
  if (days > 90) add('注意', 'FAQ', `情報更新日が${days}日前です。内容を見直して更新日を新しくしましょう（AI検索は新しい情報を好みます）`);
}
// サイトマップに全ページが載っているか
const sitemap = existsSync(join(ROOT, 'sitemap.xml')) ? readFileSync(join(ROOT, 'sitemap.xml'), 'utf8') : '';
for (const p of ALL.filter((x) => x !== '404.html')) {
  const loc = 'https://ippey0320.github.io' + BASE_PATH + p.replace(/(^|\/)index\.html$/, '$1');
  if (!sitemap.includes(`<loc>${loc}</loc>`)) add('注意', 'sitemap.xml', `サイトマップに載っていません：${loc}`);
}

// ---- 3) ブラウザで確かめる項目（はみ出し・翻訳漏れ・JSエラー） ----
const browser = await chromium.launch();
for (const w of [320, 375, 390, 430]) {
  const page = await browser.newPage({ viewport: { width: w, height: 800 } });
  await page.route(/^https:\/\/fonts\./, (r) => r.abort());
  await page.addInitScript(() => { window.vxNoRedirect = true; });
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  for (const p of ALL) {
    await page.goto(url(p));
    const r = await page.evaluate(() => {
      const W = innerWidth, bad = [];
      document.querySelectorAll('h1,h2,h3,p,a,button,li,span,b,strong,img').forEach((e) => {
        if (e.closest('.drawer,[aria-hidden="true"]')) return;
        const b = e.getBoundingClientRect();
        if (b.width && b.right > W + 1) bad.push((e.textContent || e.getAttribute('alt') || e.tagName).trim().slice(0, 20));
      });
      return { sw: document.documentElement.scrollWidth, bad: bad.slice(0, 3) };
    });
    if (r.sw > w || r.bad.length) add('重大', `${p}（幅${w}px）`, `画面からはみ出しています：${r.bad.join(' / ') || '横スクロール'}`);
    if (w === 390 && /^(en|zh)\//.test(p)) {
      const lang = p.slice(0, 2);
      const left = await page.evaluate((lang) => {
        const out = [], w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let x; while ((x = w.nextNode())) {
          if (x.parentElement.closest('script,style,textarea')) continue;
          const t = x.nodeValue.trim(); if (!t) continue;
          if ((lang === 'en' ? /[぀-ヺー-ヿ一-鿿]/ : /[぀-ヺー-ヿ]/).test(t)) out.push(t.slice(0, 30));
        }
        return [...new Set(out)];
      }, lang).catch(() => []);
      // 中文ボタン・特商法リンクは意図した日本語表記
      const real = left.filter((t) => !['中文', '特定商取引法に基づく表記'].includes(t));
      if (real.length) add('注意', p, `翻訳されていない日本語：${real.slice(0, 5).join(' / ')}`);
    }
  }
  if (errs.length) add('重大', `JS（幅${w}px）`, 'ページでエラー：' + [...new Set(errs)].slice(0, 3).join(' / '));
  await page.close();
}
await browser.close();

// ---- 4) Lighthouse（速度・アクセシビリティ・ベストプラクティス・SEO） ----
const scores = [];
let lighthouse = null;
try { lighthouse = (await import(require.resolve('lighthouse'))).default; } catch { notes.push('Lighthouse が入っていないので速度などの採点は省略しました（cd tools && npm install）'); }
if (lighthouse) {
  const chromeLauncher = await import(require.resolve('chrome-launcher'));
  const chrome = await chromeLauncher.launch({ chromePath: chromium.executablePath(), chromeFlags: ['--headless=new', '--no-sandbox', '--disable-gpu'] });
  for (const p of [...JA, 'en/index.html']) {
    const r = await lighthouse(url(p), { port: chrome.port, output: 'json', logLevel: 'error', onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'], blockedUrlPatterns: ['*fonts.googleapis.com*', '*fonts.gstatic.com*'] });
    const c = r.lhr.categories, sc = Object.fromEntries(Object.entries(c).map(([k, v]) => [k, Math.round(v.score * 100)]));
    scores.push({ p, ...sc, lcp: r.lhr.audits['largest-contentful-paint'].displayValue });
    if (sc.performance < 90) add('注意', p, `表示速度のスコアが ${sc.performance} 点（目標90以上）`);
    if (sc.accessibility < 100) add('注意', p, `アクセシビリティ ${sc.accessibility} 点：` + Object.values(r.lhr.audits).filter((a) => a.score === 0 && r.lhr.categories.accessibility.auditRefs.some((x) => x.id === a.id)).map((a) => a.id).join(', '));
    if (sc.seo < 100) add('注意', p, `SEO ${sc.seo} 点：` + Object.values(r.lhr.audits).filter((a) => a.score === 0 && r.lhr.categories.seo.auditRefs.some((x) => x.id === a.id)).map((a) => a.id).join(', '));
  }
  await chrome.kill();
}
server.close();

// ---- 5) レポート ----
const now = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 16).replace('T', ' ');
const serious = problems.filter((x) => x.level === '重大');
let md = `# サイト自動点検レポート（${now} JST）\n\n`;
md += serious.length ? `**重大な問題：${serious.length}件**／注意：${problems.length - serious.length}件\n\n` : `**重大な問題はありません**（注意：${problems.length}件）\n\n`;
if (scores.length) {
  md += '| ページ | 速度 | アクセシビリティ | ベストプラクティス | SEO | 最大の要素の表示 |\n|---|---|---|---|---|---|\n';
  for (const s of scores) md += `| ${s.p} | ${s.performance} | ${s.accessibility} | ${s['best-practices']} | ${s.seo} | ${s.lcp} |\n`;
  md += '\n（この作業環境ではGoogle Fontsを止めて測るので、本番より少し速めに出ます）\n\n';
}
if (problems.length) md += '## 見つかったこと\n\n' + problems.map((x) => `- 【${x.level}】${x.where}：${x.what}`).join('\n') + '\n\n';
if (notes.length) md += '## メモ\n\n' + notes.map((n) => `- ${n}`).join('\n') + '\n';
writeFileSync(join(TOOLS, 'audit-report.md'), md);
console.log(md);
process.exit(serious.length ? 1 : 0);
