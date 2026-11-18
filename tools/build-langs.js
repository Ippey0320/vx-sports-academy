// 英語（/en/）・中国語（/zh/）のページを、日本語ページと翻訳辞書（assets/i18n.js）から作る
// 使い方：node tools/build-langs.js   （日本語ページや翻訳を変えたら毎回実行）
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const BASE = 'https://ippey0320.github.io/vx-sports-academy/';
const PAGES = ['index', 'personal', 'gym', 'soccer', 'apparel'];

const META = {
  en: {
    locale: 'en_US', htmlLang: 'en',
    index: ['VX SPORTS ACADEMY | Personal football coaching & a gym for kids to athletes, any age, in Tokyo',
      'VX SPORTS ACADEMY runs VX PERSONAL (one-on-one football coaching), VX GYM (a gym for kids to athletes, any age in Nishi-Azabu, Tokyo, opening January 2027), VX SOCCER (a new U-12 and U-9 team) and VX APPAREL (apparel brand).'],
    personal: ['Personal football training for kids to athletes, any age | VX PERSONAL',
      'One-on-one coaching in athleticism (speed, agility, power, core) and football skill, for all ages, from kids to aspiring athletes, beginners to advanced. Trial ¥5,500, lessons ¥16,500 each (incl. tax). Tokyo, Kanagawa, Chiba and Saitama.'],
    gym: ['Gym for kids to athletes, any age in Nishi-Azabu, Tokyo | VX GYM (opening Jan 2027)',
      'VX GYM opens in Nishi-Azabu, Tokyo in January 2027: a gym for all ages, from kids to players aiming to become athletes, in any sport. Power, jump and speed measured every session. From ¥17,800/month (incl. tax). Early registration open on LINE.'],
    soccer: ['New U-12 & U-9 football team | VX SOCCER',
      'VX SOCCER is a new football team combining serious athletic training with top-level football education. U-12 and U-9 players wanted. Ask about joining on LINE.'],
    apparel: ['VX COACH KIT: everyday apparel, pre-orders open | VX APPAREL',
      'Pre-order VX everyday apparel. T-shirt ¥11,000, shorts ¥8,800, socks ¥2,200, 3-piece set ¥19,800 (incl. tax). Lightweight, quick-dry, four-way stretch. Six colours, S–XL.'],
  },
  zh: {
    locale: 'zh_CN', htmlLang: 'zh-Hans',
    index: ['VX SPORTS ACADEMY｜足球私教・儿童到运动员健身房（不限年龄）（东京）',
      'VX SPORTS ACADEMY运营足球私教「VX PERSONAL」、东京西麻布儿童到运动员健身房（不限年龄）「VX GYM」（预计2027年1月开业）、全新U-12・U-9足球队「VX SOCCER」以及服饰品牌「VX APPAREL」。'],
    personal: ['足球私教训练（儿童到运动员・不限年龄）｜VX PERSONAL',
      '一对一提升身体素质（速度、敏捷、力量、核心）与足球技术，不限年龄，儿童到运动员、初学者到高水平均可。首次体验 ¥5,500，正式课程每次 ¥16,500（含税）。东京・神奈川・千叶・埼玉。'],
    gym: ['东京西麻布 儿童到运动员健身房（不限年龄）｜VX GYM（预计2027年1月开业）',
      'VX GYM预计2027年1月在东京西麻布开业，不限年龄，面向从儿童到立志成为运动员的选手，不限运动项目。每次测量爆发力、跳跃、速度。月费 ¥17,800起（含税）。可通过LINE预约登记。'],
    soccer: ['全新U-12・U-9足球队 招募中｜VX SOCCER',
      'VX SOCCER是一支兼顾身体素质训练与顶级足球教育的新球队，正在招募U-12・U-9成员。入队咨询请通过LINE。'],
    apparel: ['VX COACH KIT 日常服饰 接受预订｜VX APPAREL',
      'VX服饰接受预订。T恤 ¥11,000、短裤 ¥8,800、袜子 ¥2,200、三件套 ¥19,800（含税）。轻量速干、四向弹力。6色、S〜XL。'],
  },
};

const esc = (s) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.addInitScript(() => { window.vxNoRedirect = true; });
  await page.route(/^https?:\/\//, (r) => r.abort()); // 外部の読み込みは不要
  for (const lang of ['en', 'zh']) {
    fs.mkdirSync(path.join(ROOT, lang), { recursive: true });
    for (const name of PAGES) {
      const file = name + '.html';
      await page.goto('file://' + path.join(ROOT, file));
      await page.evaluate((l) => window.vxSet(l), lang);
      let html = await page.evaluate((l) => {
        document.documentElement.setAttribute('data-static-lang', l);
        document.querySelectorAll('script[type="application/ld+json"]').forEach((s) => s.remove());
        return '<!doctype html>\n' + document.documentElement.outerHTML;
      }, lang);
      const m = META[lang], [title, desc] = m[name];
      const own = BASE + lang + '/' + (name === 'index' ? '' : file);
      html = html
        .replace(/<title>[\s\S]*?<\/title>/, `<title>${esc(title)}</title>`)
        .replace(/<meta name="description"[^>]*>/, `<meta name="description" content="${esc(desc)}">`)
        .replace(/<meta property="og:title"[^>]*>/, `<meta property="og:title" content="${esc(title)}">`)
        .replace(/<meta property="og:description"[^>]*>/, `<meta property="og:description" content="${esc(desc)}">`)
        .replace(/<meta property="og:locale"[^>]*>/, `<meta property="og:locale" content="${m.locale}">`)
        .replace(/<link rel="canonical"[^>]*>/, `<link rel="canonical" href="${own}">`)
        .replace(/<meta property="og:url"[^>]*>/, `<meta property="og:url" content="${own}">`)
        .replace(/(src|href)="assets\//g, '$1="../assets/')
        .replace(/href="tokushoho\.html"/g, 'href="../tokushoho.html"')
        .replace(/srcset="([^"]*)"/g, (m, v) => 'srcset="' + v.replace(/(^|, )assets\//g, '$1../assets/') + '"')
        .replace(/<html[^>]*>/, `<html lang="${m.htmlLang}" data-static-lang="${lang}">`);
      fs.writeFileSync(path.join(ROOT, lang, file), html);
      console.log('wrote', lang + '/' + file);
    }
  }
  await browser.close();
})();
