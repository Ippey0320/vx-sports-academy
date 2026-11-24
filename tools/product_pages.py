# 商品の個別ページ（Tシャツ・ショーツ・ソックス・3点セット）を日英中で作る
# 使い方：python3 tools/product_pages.py   （文言・価格・写真を変えたらここを直して実行）
import json, os, html

BASE = "https://ippey0320.github.io/vx-sports-academy/"
LINE = "https://lin.ee/uKvQIEB"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = ROOT + "/"
import re as _re
_m = _re.search(r"site\.css\?v=(\d+)", open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "apparel.html"), encoding="utf-8").read())
V = _m.group(1) if _m else "1"

COLORS = [
    ("ink-black", "Ink Black", "#1C1C1E"),
    ("sage-green", "Sage Green", "#C2D1C3"),
    ("powder-blue", "Powder Blue", "#CAD6E6"),
    ("petal-pink", "Petal Pink", "#ECD9E3"),
    ("mist-lavender", "Mist Lavender", "#D5CDE0"),
    ("cloud-white", "Cloud White", "#F0EDE8"),
]

T = {
    "ja": dict(
        lang="ja", html_lang="ja", static="", locale="ja_JP",
        preorder="予約受付中 ／ PRE-ORDER", tax="税込", color="カラー", size="サイズ", qty="数量",
        total="合計（税込）", textlabel="LINEに送る予約内容", btn="コピーしてLINEで予約",
        copyhint="コピーされたら、開いたLINEのトークに貼り付けて送信してください。",
        done="予約内容をコピーしました。LINEのトークに貼り付けて送信してください。",
        fail="上の予約内容を長押しでコピーして、LINEに貼り付けてください。",
        note="予約注文のため、お届けは予約締切後の生産となります。お支払い方法とお届け時期はLINEでご案内します。",
        features="特長", spec="仕様", others="ほかのアイテム", back="VX APPARELのページへ戻る",
        spec_color="カラー", spec_color_v="6色（ユニセックス）", spec_size="サイズ", spec_size_v="S・M・L・XL（サイズの詳細はLINEでお問い合わせください）",
        spec_ship="お届け", spec_ship_v="予約締切後に生産します。締切日はInstagramとLINEでお知らせします。",
        views=dict(tee_back="Tシャツ後ろ", shorts_back="ショーツ後ろ", front="前", back="後ろ", fabric="生地", reflective="反射ライン", slit="スリット", waist="ウエスト・ポケット", socks="ソックス"),
        steps_t="予約は、3ステップ。",
        steps=[("色とサイズを選ぶ", "上で選んだ内容が、予約文になります。"), ("LINEで送信", "ボタンを押すとコピーされ、VXのLINEが開きます。"), ("締切後に生産・お届け", "お支払い方法とお届け時期は、LINEでご案内します。")],
        gallery_hint="写真をタップすると、ほかの角度に切り替わります",
        minus="1つ減らす", plus="1つ増やす",
        drawer=[("index.html", "HOME", "VX SPORTS ACADEMY"), ("personal.html", "VX PERSONAL", "サッカーのパーソナル指導"), ("gym.html", "VX GYM", "キッズからアスリートまでのジム"), ("soccer.html", "VX SOCCER", "新しいサッカーチーム"), ("apparel.html", "VX APPAREL", "アパレル")],
        line_contact="LINEでお問い合わせ", legal="特定商取引法に基づく表記", cta="LINEで予約・お問い合わせ", cta_s="予約",
        home_aria="VX SPORTS ACADEMY トップへ",
    ),
    "en": dict(
        lang="en", html_lang="en", static="en", locale="en_US",
        preorder="Now Taking Pre-Orders ／ PRE-ORDER", tax="incl. tax", color="Color", size="Size", qty="Quantity",
        total="Total (incl. tax)", textlabel="Order details to send on LINE", btn="Copy & Order on LINE",
        copyhint="Once copied, paste it into the LINE chat that opens and send.",
        done="Copied. Paste it into the LINE chat and send.",
        fail="Long-press to copy the details above, then paste them into LINE.",
        note="As a pre-order, items are produced after the order window closes. We'll share payment and delivery details on LINE.",
        features="Features", spec="Details", others="More items", back="Back to VX APPAREL",
        spec_color="Colours", spec_color_v="6 colours (unisex)", spec_size="Sizes", spec_size_v="S, M, L, XL (ask us on LINE for measurements)",
        spec_ship="Delivery", spec_ship_v="Made after the pre-order deadline. We'll announce the deadline on Instagram and LINE.",
        views=dict(tee_back="T-shirt back", shorts_back="Shorts back", front="Front", back="Back", fabric="Fabric", reflective="Reflective", slit="Side slit", waist="Waist & pocket", socks="Socks"),
        steps_t="Ordering takes 3 steps.",
        steps=[("Choose colour and size", "Your choices fill in the order text."), ("Send on LINE", "The button copies it and opens VX on LINE."), ("Made and delivered after the deadline", "We'll explain payment and delivery timing on LINE.")],
        gallery_hint="Tap a photo to see another angle",
        minus="One less", plus="One more",
        drawer=[("index.html", "HOME", "VX SPORTS ACADEMY"), ("personal.html", "VX PERSONAL", "Personal football coaching"), ("gym.html", "VX GYM", "Gym for kids to athletes, any age"), ("soccer.html", "VX SOCCER", "A new football team"), ("apparel.html", "VX APPAREL", "Apparel")],
        line_contact="Contact us on LINE", legal="Legal notice (Specified Commercial Transactions Act)", cta="Order / ask on LINE", cta_s="Order",
        home_aria="VX SPORTS ACADEMY home",
    ),
    "zh": dict(
        lang="zh", html_lang="zh-Hans", static="zh", locale="zh_CN",
        preorder="接受预订中 ／ PRE-ORDER", tax="含税", color="颜色", size="尺码", qty="数量",
        total="合计（含税）", textlabel="发送到LINE的预订内容", btn="复制并通过LINE预订",
        copyhint="复制后，请粘贴到打开的LINE聊天中发送。",
        done="已复制。请粘贴到LINE聊天中发送。",
        fail="请长按复制上方内容，并粘贴到LINE。",
        note="因属预订商品，将在预订截止后生产。付款方式与交货时间将通过LINE告知。",
        features="特点", spec="规格", others="其他商品", back="返回 VX APPAREL",
        spec_color="颜色", spec_color_v="6色（男女同款）", spec_size="尺码", spec_size_v="S・M・L・XL（具体尺寸请通过LINE咨询）",
        spec_ship="交货", spec_ship_v="预订截止后开始生产。截止日期将在Instagram和LINE公布。",
        views=dict(tee_back="T恤背面", shorts_back="短裤背面", front="正面", back="背面", fabric="面料", reflective="反光条", slit="开衩", waist="腰部・口袋", socks="袜子"),
        steps_t="预订只需3步。",
        steps=[("选择颜色和尺码", "所选内容会自动生成预订文字。"), ("通过LINE发送", "点击按钮即可复制，并打开VX的LINE。"), ("截止后生产・配送", "付款方式和配送时间将通过LINE告知。")],
        gallery_hint="点击照片可切换其他角度",
        minus="减少1件", plus="增加1件",
        drawer=[("index.html", "HOME", "VX SPORTS ACADEMY"), ("personal.html", "VX PERSONAL", "足球私教指导"), ("gym.html", "VX GYM", "儿童到运动员健身房（不限年龄）"), ("soccer.html", "VX SOCCER", "全新的足球队"), ("apparel.html", "VX APPAREL", "服饰")],
        line_contact="通过LINE咨询", legal="特定商交易法相关标示", cta="通过LINE预订・咨询", cta_s="预订",
        home_aria="返回VX SPORTS ACADEMY首页",
    ),
}

ITEMS = {
    "tee": dict(
        code="VX T-SHIRT", price=11000, order_item="Tシャツ", thumb="set-front_ink-black",
        name=dict(ja="Tシャツ", en="T-Shirt", zh="T恤"),
        catch=dict(ja="汗をかいても、<br>そのまま出かけられる。", en="Sweat in it.<br>Head out in it.", zh="出汗后，<br>也能直接出门。"),
        lead=dict(
            ja="速乾メッシュで、練習のあとも着替えずに街へ。裾のスリットで動きやすく、袖と背中の反射ラインで夜道でも目立ちます。",
            en="Quick-dry mesh means no change of clothes after training. Side slits let you move freely, and reflective lines on the sleeves and back stand out at night.",
            zh="速干网眼面料，训练后无需换衣即可出门。下摆开衩便于活动，袖子和背部的反光条在夜间也很醒目。"),
        feats=dict(
            ja=[("高通気・速乾メッシュ", "汗をかいても、すぐ乾く。"), ("4方向ストレッチ", "どの方向にも伸びて、動きを邪魔しない。"), ("裾のサイドスリット", "脚を大きく動かしても、裾が突っ張らない。"), ("リフレクティブ", "袖と背中の反射ラインが、夜でも光る。")],
            en=[("Breathable quick-dry mesh", "Dries fast, even after a sweat."), ("Four-way stretch", "Stretches every way and never holds you back."), ("Side slits at the hem", "The hem stays free, however big the movement."), ("Reflective", "Lines on the sleeves and back catch the light at night.")],
            zh=[("高透气速干网眼", "出汗后也能很快变干。"), ("四向弹力", "向各个方向延展，不妨碍动作。"), ("下摆侧开衩", "大幅度活动时，下摆也不紧绷。"), ("反光设计", "袖子和背部的反光条，夜间也会发光。")]),
        views=[("front", "set-front_{c}"), ("back", "tee-back_{c}"), ("fabric", "detail-fabric"), ("reflective", "detail-reflective"), ("slit", "detail-slit")],
    ),
    "shorts": dict(
        code="VX SHORTS", price=8800, order_item="ショーツ", thumb="shorts-back_ink-black",
        name=dict(ja="ショーツ", en="Shorts", zh="短裤"),
        catch=dict(ja="走っても、しゃがんでも、<br>気にならない。", en="Run, squat, sprint.<br>It moves with you.", zh="奔跑、下蹲，<br>都不受拘束。"),
        lead=dict(
            ja="4方向ストレッチで、どの動きにもついてくる。撥水生地で、汗や急な雨にも強い。両サイドのポケットと、裾の反射ラインつきです。",
            en="Four-way stretch follows every move, and water-repellent fabric handles sweat and sudden rain. With side pockets and a reflective line at the hem.",
            zh="四向弹力，跟随每个动作；防泼水面料，不怕汗水和突来的雨。两侧带口袋，裤脚有反光条。"),
        feats=dict(
            ja=[("4方向ストレッチ", "どの方向にも伸びて、動きを邪魔しない。"), ("撥水", "水をはじく生地。"), ("両サイドポケット", "鍵やスマホを入れておける。"), ("リフレクティブ", "裾の反射ラインが、夜でも光る。")],
            en=[("Four-way stretch", "Stretches every way and never holds you back."), ("Water-repellent", "Fabric that sheds water."), ("Side pockets", "Room for keys or a phone."), ("Reflective", "A line at the hem catches the light at night.")],
            zh=[("四向弹力", "向各个方向延展，不妨碍动作。"), ("防泼水", "能防泼水的面料。"), ("两侧口袋", "可以放钥匙或手机。"), ("反光设计", "裤脚的反光条，夜间也会发光。")]),
        views=[("front", "set-front_{c}"), ("back", "shorts-back_{c}"), ("waist", "detail-waist"), ("fabric", "detail-fabric")],
    ),
    "socks": dict(
        code="VX SOCKS", price=2200, order_item="ソックス", thumb="socks_ink-black",
        name=dict(ja="ソックス", en="Socks", zh="袜子"),
        catch=dict(ja="足元まで、<br>同じ色でそろえる。", en="Match it<br>all the way down.", zh="从头到脚，<br>同一颜色。"),
        lead=dict(
            ja="約22cm丈のクルーソックス。ウェアと同じ6色から選べるので、上から下まで色をそろえられます。",
            en="Crew socks, approx. 22 cm, in the same six colours as the wear, so you can match head to toe.",
            zh="约22cm的中筒袜，与服装同样6色可选，从上到下统一颜色。"),
        feats=dict(
            ja=[("約22cm丈", "ショーツに合わせやすいクルー丈。"), ("ウェアと同じ6色", "Tシャツ・ショーツと色をそろえられる。"), ("VXロゴ", "正面にさりげなく入ったロゴ。")],
            en=[("Approx. 22 cm", "A crew length that works with the shorts."), ("Same 6 colours as the wear", "Match your T-shirt and shorts."), ("VX logo", "A small logo on the front.")],
            zh=[("约22cm长", "易于搭配短裤的中筒长度。"), ("与服装同样6色", "可与T恤、短裤统一颜色。"), ("VX标志", "正面低调的标志。")]),
        views=[("socks", "socks_{c}")],
    ),
    "set": dict(
        code="VX FULL KIT", price=19800, order_item="3点セット", thumb="set-front_sage-green",
        name=dict(ja="3点セット", en="3-Piece Set", zh="三件套"),
        catch=dict(ja="上から下まで、<br>1色で決まる。", en="One colour,<br>head to toe.", zh="一种颜色，<br>从头到脚。"),
        lead=dict(
            ja="Tシャツ・ショーツ・ソックスを同じ色でそろえたセット。単品でそろえるより¥2,200お得です。",
            en="T-shirt, shorts and socks in one colour, ¥2,200 less than buying them separately.",
            zh="T恤、短裤、袜子同色套装，比单买便宜¥2,200。"),
        feats=dict(
            ja=[("Tシャツ ¥11,000", "高通気・速乾メッシュ、裾のスリット。"), ("ショーツ ¥8,800", "4方向ストレッチ・撥水、両サイドポケット。"), ("ソックス ¥2,200", "約22cm丈、ウェアと同じ色。"), ("単品合計より¥2,200お得", "単品合計 ¥22,000 → セット ¥19,800。")],
            en=[("T-shirt ¥11,000", "Breathable quick-dry mesh, side slits."), ("Shorts ¥8,800", "Four-way stretch, water-repellent, side pockets."), ("Socks ¥2,200", "Approx. 22 cm, same colour as the wear."), ("Save ¥2,200", "¥22,000 separately → ¥19,800 as a set.")],
            zh=[("T恤 ¥11,000", "高透气速干网眼，下摆开衩。"), ("短裤 ¥8,800", "四向弹力・防泼水，两侧口袋。"), ("袜子 ¥2,200", "约22cm长，与服装同色。"), ("比单买便宜¥2,200", "单买合计 ¥22,000 → 套装 ¥19,800。")]),
        views=[("front", "set-front_{c}"), ("tee_back", "tee-back_{c}"), ("shorts_back", "shorts-back_{c}"), ("socks", "socks_{c}"), ("fabric", "detail-fabric")],
    ),
}
ORDER = ["tee", "shorts", "socks", "set"]

META = {
    "tee": dict(ja=("VX T-SHIRT｜速乾Tシャツ ¥11,000（税込）6色・予約受付中｜VX APPAREL", "VX APPARELのTシャツ。高通気・速乾メッシュ、4方向ストレッチ、裾のスリット、反射ライン。¥11,000（税込）。ユニセックス6色・S〜XL。予約受付中。"),
                en=("VX T-SHIRT: quick-dry tee ¥11,000, 6 colours, pre-order | VX APPAREL", "VX APPAREL T-shirt: breathable quick-dry mesh, four-way stretch, side slits, reflective lines. ¥11,000 incl. tax. Six unisex colours, S–XL. Pre-orders open."),
                zh=("VX T-SHIRT｜速干T恤 ¥11,000（含税）6色・接受预订｜VX APPAREL", "VX APPAREL T恤：高透气速干网眼、四向弹力、下摆开衩、反光条。¥11,000（含税）。男女同款6色，S〜XL。接受预订中。")),
    "shorts": dict(ja=("VX SHORTS｜ストレッチ撥水ショーツ ¥8,800（税込）6色・予約受付中｜VX APPAREL", "VX APPARELのショーツ。4方向ストレッチ・撥水、両サイドポケット、反射ライン。¥8,800（税込）。ユニセックス6色・S〜XL。予約受付中。"),
                   en=("VX SHORTS: stretch, water-repellent shorts ¥8,800, 6 colours | VX APPAREL", "VX APPAREL shorts: four-way stretch, water-repellent, side pockets, reflective line. ¥8,800 incl. tax. Six unisex colours, S–XL. Pre-orders open."),
                   zh=("VX SHORTS｜弹力防泼水短裤 ¥8,800（含税）6色｜VX APPAREL", "VX APPAREL 短裤：四向弹力、防泼水、两侧口袋、反光条。¥8,800（含税）。男女同款6色，S〜XL。接受预订中。")),
    "socks": dict(ja=("VX SOCKS｜クルーソックス ¥2,200（税込）6色・予約受付中｜VX APPAREL", "VX APPARELのソックス。約22cm丈、ウェアと同じ6色。¥2,200（税込）。予約受付中。"),
                  en=("VX SOCKS: crew socks ¥2,200, 6 colours, pre-order | VX APPAREL", "VX APPAREL crew socks, approx. 22 cm, in the same six colours as the wear. ¥2,200 incl. tax. Pre-orders open."),
                  zh=("VX SOCKS｜中筒袜 ¥2,200（含税）6色・接受预订｜VX APPAREL", "VX APPAREL 中筒袜，约22cm，与服装同样6色。¥2,200（含税）。接受预订中。")),
    "set": dict(ja=("VX 3点セット｜Tシャツ・ショーツ・ソックス ¥19,800（税込）｜VX APPAREL", "Tシャツ・ショーツ・ソックスを同じ色でそろえる3点セット。¥19,800（税込）、単品合計より¥2,200お得。ユニセックス6色・S〜XL。予約受付中。"),
                en=("VX 3-Piece Set: T-shirt, shorts & socks ¥19,800 | VX APPAREL", "T-shirt, shorts and socks in one colour. ¥19,800 incl. tax, ¥2,200 less than buying separately. Six unisex colours, S–XL. Pre-orders open."),
                zh=("VX 三件套｜T恤・短裤・袜子 ¥19,800（含税）｜VX APPAREL", "T恤、短裤、袜子同色三件套。¥19,800（含税），比单买便宜¥2,200。男女同款6色，S〜XL。接受预订中。")),
}

LINE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 4C7 4 3 7.2 3 11.2c0 3.6 3.2 6.6 7.5 7.1-.2.9-.6 2.1-.7 2.4 0 .3.3.5.6.3 1.2-.8 4.3-2.8 5.9-4.3 2.3-1.3 3.7-3.3 3.7-5.5C21 7.2 17 4 12 4Z"/></svg>'

CSS = ""


def esc(s):
    return html.escape(s, quote=True)


def img_paths(p, key):
    return f"{p}assets/apparel/{key}.webp", f"{p}assets/apparel/{key}-800.webp"


def page(item, L):
    t = T[L]
    it = ITEMS[item]
    p = "" if L == "ja" else "../"
    title, desc = META[item][L]
    fname = f"{item}.html"
    url = BASE + ("" if L == "ja" else L + "/") + fname
    first = it["views"][0][1].format(c="ink-black")
    og = BASE + f"assets/apparel/{first}.webp"
    name = it["name"][L]

    # JSON-LD
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": it["code"] + (" " if L != "ja" else "（") + name + ("" if L != "ja" else "）"),
         "brand": {"@type": "Brand", "name": "VX SPORTS ACADEMY"},
         "description": desc,
         "image": [BASE + f"assets/apparel/{it['views'][0][1].format(c=c[0])}.webp" for c in COLORS],
         "color": ", ".join(c[1] for c in COLORS),
         "size": "S, M, L, XL",
         "offers": {"@type": "Offer", "price": str(it["price"]), "priceCurrency": "JPY",
                    "availability": "https://schema.org/PreOrder", "url": url,
                    "seller": {"@id": BASE + "#org"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "VX SPORTS ACADEMY", "item": BASE + ("" if L == "ja" else L + "/")},
            {"@type": "ListItem", "position": 2, "name": "VX APPAREL", "item": BASE + ("" if L == "ja" else L + "/") + "apparel.html"},
            {"@type": "ListItem", "position": 3, "name": it["code"], "item": url}]}]}

    alts = "\n".join(
        f'<link rel="alternate" hreflang="{hl}" href="{BASE}{"" if ll == "ja" else ll + "/"}{fname}">'
        for ll, hl in [("ja", "ja"), ("en", "en"), ("zh", "zh-Hans")]) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{fname}">'

    static_attr = f' data-static-lang="{t["static"]}"' if t["static"] else ""
    lang_btns = "".join(
        f'<button type="button" data-l="{l}" aria-pressed="{"true" if l == L else "false"}">{lab}</button>'
        for l, lab in [("ja", "JP"), ("en", "EN"), ("zh", "中文")])
    drawer = "\n".join(
        f'  <a{" class=\"on\"" if h == "apparel.html" else ""} href="{h}" data-c="{h[:-5]}"><b>{b}</b><span>{s}</span></a>'
        for h, b, s in t["drawer"])

    # views per colour for JS
    vdata = {c[0]: [it_v[1].format(c=c[0]) for it_v in it["views"]] for c in COLORS}
    vlabels = [t["views"][v[0]] for v in it["views"]]

    thumbs = "".join(
        f'<button type="button" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}" aria-label="{esc(lab)}"><img src="{p}assets/apparel/{vdata["ink-black"][i]}-800.webp" alt="" loading="lazy" width="800" height="1055"><span>{esc(lab)}</span></button>'
        for i, lab in enumerate(vlabels))
    if len(vlabels) == 1:
        thumbs_html = ""
        hint = ""
    else:
        thumbs_html = f'<div class="pd-thumbs" role="group" aria-label="{esc(t["views"]["front"])}">{thumbs}</div>'
        hint = f'<p class="pd-hint">{esc(t["gallery_hint"])}</p>'

    src, src800 = img_paths(p, vdata["ink-black"][0])
    swatches = "".join(
        f'<label title="{n}"><input type="radio" name="color" value="{n}" data-slug="{s}"{" checked" if i == 0 else ""}><span class="sw-b" style="background:{h}"></span><span class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">{n}</span></label>'
        for i, (s, n, h) in enumerate(COLORS))
    sizes = "".join(
        f'<label><input type="radio" name="size" value="{s}"{" checked" if s == "M" else ""}><span>{s}</span></label>'
        for s in ["S", "M", "L", "XL"])
    feats = "".join(f"<li><b>{esc(a)}</b><span>{esc(b)}</span></li>" for a, b in it["feats"][L])
    steps = "".join(f'<li><b>0{i+1}</b><div><h3>{esc(a)}</h3><p>{esc(b)}</p></div></li>' for i, (a, b) in enumerate(t["steps"]))
    others = "".join(
        f'<a href="{o}.html"><img src="{p}assets/apparel/{ITEMS[o]["thumb"]}-800.webp" alt="" loading="lazy" width="800" height="1055"><b>{esc(ITEMS[o]["name"][L])}</b><span>¥{ITEMS[o]["price"]:,}</span></a>'
        for o in ORDER if o != item)

    js = f"""<script>
(function(){{
  var LINE='{LINE}', V={json.dumps(vdata)}, P='{p}assets/apparel/', ITEM='{it["order_item"]}', PRICE={it["price"]};
  var MSG={json.dumps({"done": t["done"], "fail": t["fail"]}, ensure_ascii=False)};
  var f=document.getElementById('order-form'), main=document.getElementById('pd-main-img');
  var thumbs=[].slice.call(document.querySelectorAll('.pd-thumbs button')), cn=document.getElementById('pd-colorname');
  var q=1, vi=0, out=document.getElementById('q-val'), total=document.getElementById('total'), ta=document.getElementById('order-text'), msg=document.getElementById('copy-msg');
  function val(n){{var e=f.querySelector('input[name="'+n+'"]:checked');return e?e:null;}}
  function yen(n){{return '¥'+n.toLocaleString('ja-JP');}}
  function show(){{
    var c=val('color').dataset.slug, k=V[c][vi];
    main.src=P+k+'.webp'; main.srcset=P+k+'-800.webp 800w, '+P+k+'.webp 1092w';
    thumbs.forEach(function(b,i){{b.setAttribute('aria-pressed',i===vi?'true':'false');b.querySelector('img').src=P+V[c][i]+'-800.webp';}});
    cn.textContent=val('color').value;
  }}
  function update(){{
    var price=PRICE*q; out.textContent=q; total.textContent=yen(price);
    ta.value='【VX APPAREL 予約】\\nアイテム：'+ITEM+'\\nカラー：'+val('color').value+'\\nサイズ：'+val('size').value+'\\n数量：'+q+'\\n合計：'+yen(price)+'（税込）\\nお名前：\\n';
  }}
  thumbs.forEach(function(b,i){{b.addEventListener('click',function(){{vi=i;show();}});}});
  main.addEventListener('click',function(){{if(thumbs.length){{vi=(vi+1)%thumbs.length;show();}}}});
  f.addEventListener('change',function(e){{if(e.target.name==='color')show();update();}});
  document.getElementById('q-minus').onclick=function(){{if(q>1){{q--;update();}}}};
  document.getElementById('q-plus').onclick=function(){{if(q<20){{q++;update();}}}};
  f.addEventListener('submit',function(e){{
    e.preventDefault();
    var done=function(){{msg.textContent=MSG.done;}};
    var fail=function(){{ta.select();msg.textContent=MSG.fail;}};
    try{{ navigator.clipboard.writeText(ta.value).then(done,fail); }}catch(err){{ fail(); }}
    window.open(LINE,'_blank','noopener');
  }});
  var m=(location.search.match(/[?&]color=([a-z-]+)/)||[])[1];
  if(m){{var r=f.querySelector('input[data-slug="'+m+'"]'); if(r) r.checked=true;}}
  show(); update();
}})();
</script>"""

    return f"""<!doctype html>
<html lang="{t['html_lang']}"{static_attr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(desc)}">
<link rel="icon" type="image/svg+xml" href="{p}assets/favicon.svg">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og}">
<meta property="og:type" content="product">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="VX SPORTS ACADEMY">
<meta property="og:locale" content="{t['locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og}">
<link rel="canonical" href="{url}">
{alts}
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300;62..125,400;62..125,500;62..125,600&family=Noto+Sans+JP:wght@400;500;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300;62..125,400;62..125,500;62..125,600&family=Noto+Sans+JP:wght@400;500;700&display=swap"></noscript>
<link rel="stylesheet" href="{p}assets/site.css?v={V}">
{CSS}
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <div class="topbar"><button type="button" class="menu-btn" aria-expanded="false" aria-controls="drawer" aria-label="Menu"><span></span><span></span><span></span></button><a class="brand" href="index.html" aria-label="{esc(t['home_aria'])}">
        <img src="{p}assets/logo.svg" alt="VX" width="332" height="104">
        <span>SPORTS ACADEMY</span>
      </a><div class="lang" role="group" aria-label="Language">
      {lang_btns}
    </div></div>
    <nav class="tabs" aria-label="VX">
      <a href="personal.html" data-c="personal">PERSONAL</a>
      <a href="gym.html" data-c="gym">GYM</a>
      <a href="soccer.html" data-c="soccer">SOCCER</a>
      <a class="main" href="apparel.html" data-c="apparel">APPAREL</a>
    </nav>
  </div>
</header>
<div class="drawer-bg" hidden></div>
<nav class="drawer" id="drawer" aria-label="Menu" hidden>
  <div class="drawer-head"><img src="{p}assets/logo.svg" alt="VX" width="332" height="104"><button type="button" class="drawer-close" aria-label="Close">✕</button></div>
{drawer}
  <a class="drawer-line" href="{LINE}" target="_blank" rel="noopener">{LINE_SVG}{esc(t['line_contact'])}</a>
  <a class="drawer-legal" href="{p}tokushoho.html">{esc(t['legal'])}</a>
</nav>

<main id="top">
<section class="band on-ink" id="product">
  <div class="wrap stack">
    <p class="pd-crumb"><a href="apparel.html">VX APPAREL</a> ／ {esc(it['code'])}</p>
    <div class="pd-gallery">
      <div class="pd-main"><img id="pd-main-img" src="{src}" srcset="{src800} 800w, {src} 1092w" sizes="(max-width: 480px) 100vw, 480px" alt="{esc(it['code'])}" fetchpriority="high" width="1092" height="1440"></div>
      {thumbs_html}
      {hint}
    </div>
    <div class="pd-head">
      <span class="status fill">{esc(t['preorder'])}</span>
      <p class="pd-code">{esc(it['code'])}</p>
      <h1 class="catch">{it['catch'][L]}</h1>
      <p class="pd-name">{esc(name)}</p>
      <p class="pd-price">¥{it['price']:,}<small>{esc(t['tax'])}</small></p>
      <p class="lead sub">{esc(it['lead'][L])}</p>
    </div>

    <form class="order" id="order-form" aria-label="PRE-ORDER">
      <h2>PRE-ORDER</h2>
      <div class="field"><span>{esc(t['color'])}</span>
        <div class="pd-swatches" id="f-color">{swatches}</div>
        <p class="pd-colorname" id="pd-colorname" aria-live="polite">Ink Black</p>
      </div>
      <div class="field"><span>{esc(t['size'])}</span>
        <div class="chips" id="f-size">{sizes}</div>
      </div>
      <div class="field"><span>{esc(t['qty'])}</span>
        <div class="qty"><button type="button" id="q-minus" aria-label="{esc(t['minus'])}">−</button><output id="q-val">1</output><button type="button" id="q-plus" aria-label="{esc(t['plus'])}">＋</button></div>
      </div>
      <div class="summary"><span class="sub">{esc(t['total'])}</span><span class="total" id="total">¥{it['price']:,}</span></div>
      <label class="field" for="order-text"><span>{esc(t['textlabel'])}</span><textarea class="order-text" id="order-text" readonly></textarea></label>
      <div class="btn-row on-ink">
        <button type="submit" class="btn btn-solid">{LINE_SVG}{esc(t['btn'])}</button>
      </div>
      <p class="copy-msg" id="copy-msg" aria-live="polite">{esc(t['copyhint'])}</p>
      <p class="sub" style="font-size:14px">{esc(t['note'])}</p>
    </form>

    <div class="sec-head"><p class="en sub">Features</p><h2 class="catch">{esc(t['features'])}</h2></div>
    <ul class="pd-feats">{feats}</ul>

    <div class="sec-head"><p class="en sub">Details</p><h2 class="catch">{esc(t['spec'])}</h2></div>
    <dl class="pd-spec">
      <dt>{esc(t['spec_color'])}</dt><dd>{esc(t['spec_color_v'])}<br>{' / '.join(c[1] for c in COLORS)}</dd>
      <dt>{esc(t['spec_size'])}</dt><dd>{esc(t['spec_size_v'])}</dd>
      <dt>{esc(t['spec_ship'])}</dt><dd>{esc(t['spec_ship_v'])}</dd>
    </dl>

    <div class="s10 s10-steps"><div class="sec-head"><p class="en sub">Start</p><h2 class="catch">{esc(t['steps_t'])}</h2></div><ol class="s10-list">{steps}</ol></div>

    <div class="sec-head"><p class="en sub">More</p><h2 class="catch">{esc(t['others'])}</h2></div>
    <div class="pd-others">{others}</div>
    <p><a class="pd-back" href="apparel.html">← {esc(t['back'])}</a></p>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <span class="en">VX SPORTS ACADEMY</span>
    <a class="f-legal" href="{p}tokushoho.html">{esc(t['legal'])}</a>
    <span>© 2026 VX SPORTS ACADEMY</span>
  </div>
</footer>

<div class="cta-bar">
  <a class="p" href="{LINE}" target="_blank" rel="noopener">{LINE_SVG}{esc(t['cta'])}</a>
  <a class="s" href="#order-form">{esc(t['cta_s'])}</a>
</div>
{js}
<script src="{p}assets/i18n.js?v={V}"></script>
</body>
</html>
"""


for L in ["ja", "en", "zh"]:
    d = OUT + ("" if L == "ja" else L + "/")
    os.makedirs(d, exist_ok=True)
    for item in ORDER:
        open(d + item + ".html", "w", encoding="utf-8").write(page(item, L))
print("product pages ok")
