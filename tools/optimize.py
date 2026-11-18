# 表示速度・アクセシビリティの仕上げ（日本語ページに適用 → そのあと build-langs.js で英中ページを作る）
# 何度実行しても同じ結果になるように書いてある。
#   python3 tools/optimize.py .
import glob, os, re, sys
from PIL import Image

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)
PAGES = ['index.html', 'personal.html', 'gym.html', 'soccer.html', 'apparel.html', 'tokushoho.html']

# 1) 写真を WebP に（スマホ用 800px と 元サイズ）
SIZES = {}
for jpg in glob.glob('assets/*.jpg'):
    if os.path.basename(jpg).startswith('og-'):  # SNS共有画像はそのまま
        continue
    base = jpg[:-4]
    im = Image.open(jpg).convert('RGB')
    w, h = im.size
    full = base + '.webp'
    if not os.path.exists(full) or os.path.getmtime(full) < os.path.getmtime(jpg):
        im.save(full, 'WEBP', quality=80, method=6)
    variants = [(full, w)]
    if w > 900:
        small = base + '-800.webp'
        if not os.path.exists(small) or os.path.getmtime(small) < os.path.getmtime(jpg):
            im.resize((800, round(h * 800 / w)), Image.LANCZOS).save(small, 'WEBP', quality=78, method=6)
        variants.insert(0, (small, 800))
    SIZES[jpg] = variants

def img_tag(m):
    tag = m.group(0)
    src = m.group(1)
    if src not in SIZES or 'srcset=' in tag:
        return tag
    v = SIZES[src]
    srcset = ', '.join(f'{p} {w}w' for p, w in v)
    tag = tag.replace(f'src="{src}"', f'src="{v[-1][0]}" srcset="{srcset}" sizes="(max-width: 480px) 100vw, 480px"', 1)
    return tag

LOGO = 'width="332" height="104"'
LABELS = {'personal.html': 'VX PERSONALを見る', 'gym.html': 'VX GYMを見る', 'soccer.html': 'VX SOCCERを見る', 'apparel.html': 'VX APPARELを見る'}
FONT_RE = re.compile(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/[^"]+)">')

for f in PAGES:
    if not os.path.exists(f):
        continue
    s = open(f, encoding='utf-8').read()
    # 写真
    s = re.sub(r'<img [^>]*src="(assets/[^"]+\.jpg)"[^>]*>', img_tag, s)
    # ロゴの縦横サイズ（表示がずれないように）
    s = re.sub(r'<img ((?:class="[^"]*" )?)src="assets/logo\.svg" alt="([^"]*)">', lambda m: f'<img {m.group(1)}src="assets/logo.svg" alt="{m.group(2)}" {LOGO}>', s)
    # 写真だけのリンクに名前をつける
    for href, label in LABELS.items():
        s = s.replace(f'<a class="cat-img" href="{href}">', f'<a class="cat-img" href="{href}" aria-label="{label}">')
    s = re.sub(r'(<img src="assets/personal-coach\.webp"[^>]*?) alt=""', r'\1 alt="VX PERSONALでマンツーマン指導をするコーチ"', s)
    # 文字の読み込みで最初の表示を止めない
    s = FONT_RE.sub(lambda m: f'<link rel="preload" as="style" href="{m.group(1)}" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="{m.group(1)}"></noscript>', s)
    # 見出しの順番（h1 → h2 → h3）
    if f == 'personal.html':
        s = re.sub(r'<p class="catch">(一人ひとりの課題に合わせて、.*?)</p>', r'<h2 class="catch">\1</h2>', s, flags=re.S)
    if f == 'soccer.html':
        s = re.sub(r'(<div class="point"><p class="en">[^<]*</p>)<h3>([^<]*)</h3>', r'\1<h2>\2</h2>', s)
    if f == 'apparel.html':
        s = s.replace('<h3>PRE-ORDER</h3>', '<h2>PRE-ORDER</h2>')
    # ページで最初に見える写真はすぐ読み込む
    if f in ('gym.html', 'apparel.html'):
        s = re.sub(r'(<img (?:class="[^"]*" )?src="assets/[^"]+\.webp"[^>]*?) loading="lazy"', r'\1 fetchpriority="high"', s, count=1)
    # トップの背景写真を先に読み込む
    if f == 'index.html' and 'rel="preload" as="image"' not in s:
        s = s.replace('<link rel="preconnect" href="https://fonts.googleapis.com">',
                      '<link rel="preload" as="image" href="assets/gym-entrance-800.webp" media="(max-width: 800px)" fetchpriority="high">\n<link rel="preload" as="image" href="assets/gym-entrance.webp" media="(min-width: 801px)" fetchpriority="high">\n<link rel="preconnect" href="https://fonts.googleapis.com">', 1)
    open(f, 'w', encoding='utf-8').write(s)
    print('optimized', f)

# CSS：背景写真を WebP に、見出しタグを変えた所の見た目を保つ
c = open('assets/site.css', encoding='utf-8').read()
c = c.replace('background: url(gym-entrance.jpg) center 40% / cover no-repeat;', 'background: url(gym-entrance.webp) center 40% / cover no-repeat;')
if '/* optimize.py */' not in c:
    c += '''
/* optimize.py */
@media (max-width: 800px) { .hero2-bg { background-image: url(gym-entrance-800.webp); } }
.point h2 { font-size: 18px; font-weight: 700; letter-spacing: .04em; line-height: 1.45; font-feature-settings: "palt" 1; }
.order h2 { font-family: var(--display); font-weight: 300; font-stretch: 125%; letter-spacing: .3em; font-size: 14px; }
'''
open('assets/site.css', 'w', encoding='utf-8').write(c)
print('css ok')
