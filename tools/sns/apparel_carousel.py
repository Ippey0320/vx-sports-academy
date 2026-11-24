# VX APPAREL のカルーセル（On のように商品画像をしっかり見せる）を作る。
#   python3 tools/sns/apparel_carousel.py <台本.json> <出力フォルダ>
# 台本の形：
# {"name":"tee","kicker":"VX T-SHIRT","title":"VX T-SHIRT","lead":"6色。","grid":"tee-back",
#  "slides":["set-front_ink-black","tee-back_ink-black",...,"detail-fabric"],
#  "end":{"kicker":"MADE TO ORDER","title":"受注生産でお届け。","rows":[["Tシャツ","¥7,700"]],"note":"税込｜ご注文から約2〜3週間でお届け"}}
# 商品画像（assets/apparel/*.webp・1092×1440）は、そのまま 1080×1440（3:4）にして並べる。
import json, sys, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
A = os.path.join(ROOT, 'assets', 'apparel')
W, H = 1080, 1440
BG, FG, Q, LINE = (10, 10, 11), (240, 237, 232), (125, 125, 133), (42, 42, 46)
COLORS = ['ink-black', 'cloud-white', 'sage-green', 'powder-blue', 'mist-lavender', 'petal-pink']
inter = lambda s, w='Bold': ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{w}.otf', s)
jp = lambda s: ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', s, index=0)


def prod(name):
    im = Image.open(os.path.join(A, name + '.webp')).convert('RGB')
    s = H / im.height
    im = im.resize((round(im.width * s), H))
    x = (im.width - W) // 2
    return im.crop((x, 0, x + W, H))


def foot(d):
    f = inter(20, 'Medium')
    d.text((72, H - 80), 'THE PRO PERSPECTIVE.', font=f, fill=Q)
    t = '@vx.apparel.official'
    d.text((W - 72 - d.textlength(t, font=f), H - 80), t, font=f, fill=Q)


def cover(sp):
    c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    d.text((72, 110), sp.get('kicker', 'VX APPAREL'), font=inter(26, 'SemiBold'), fill=Q)
    d.text((72, 160), sp['title'], font=inter(sp.get('titleSize', 104), 'Bold'), fill=FG)
    d.text((72, 310), sp.get('lead', ''), font=jp(50), fill=FG)
    tw, th, g = 296, 390, 24; x0 = (W - 3 * tw - 2 * g) // 2; y0 = 440
    items = sp.get('gridItems') or [f"{sp['grid']}_{col}" for col in COLORS]
    for i, n in enumerate(items[:6]):
        t = prod(n).crop((90, 200, W - 90, H - 150)).resize((tw, th))
        c.paste(t, (x0 + (i % 3) * (tw + g), y0 + (i // 3) * (th + g)))
    if sp.get('under'):
        d.text((72, y0 + 2 * th + g + 40), sp['under'], font=jp(30), fill=Q)
    foot(d); return c


def end(e):
    c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    d.text((72, 300), e.get('kicker', 'MADE TO ORDER'), font=inter(26, 'SemiBold'), fill=Q)
    d.text((72, 350), e.get('title', '受注生産でお届け。'), font=jp(80), fill=FG)
    y = 560
    for a, b in e['rows']:
        d.line((72, y, W - 72, y), fill=LINE, width=2)
        d.text((72, y + 36), a, font=jp(44), fill=FG)
        f = inter(52, 'SemiBold'); d.text((W - 72 - d.textlength(b, font=f), y + 30), b, font=f, fill=FG)
        y += 124
    d.line((72, y, W - 72, y), fill=LINE, width=2)
    d.text((72, y + 30), e.get('note', '税込｜ご注文から約2〜3週間でお届け'), font=jp(28), fill=Q)
    d.text((72, y + 150), e.get('cta', '色とサイズは、プロフィールのリンクから。'), font=jp(38), fill=FG)
    foot(d); return c


if __name__ == '__main__':
    sp = json.load(open(sys.argv[1])); out = sys.argv[2]
    pages = [cover(sp)] + [prod(n) for n in sp['slides']] + ([end(sp['end'])] if sp.get('end') else [])
    for i, p in enumerate(pages, 1):
        p.save(os.path.join(out, f"{sp['name']}-{i:02d}.jpg"), quality=92)
    print(f"{sp['name']}: {len(pages)}枚")
