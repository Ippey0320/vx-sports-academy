# 「買う人の10の質問」と「脳の3段階」に沿った、売るためのブロックを各ページに入れる
#   python3 tools/sales10.py   （build.sh から呼ばれる。何度実行しても同じ結果）
#
# 脳の3段階（ページを開いて数秒で答える）
#   1 チャンスか危険か → いちばん上で「手に入るもの」を見せる
#   2 簡単か難しいか   → 始め方は3ステップ、料金はすぐ見える
#   3 新しいか知ってるか → 知っている言葉（サッカー・ジム・服）に、新しい一点（数字・元Jリーガー）
# 10の質問
#   1 何がユニークか / 2 何が手に入るか / 3 本当だと言える証拠は / 4 今まで結果が出なかった理由は
#   5 悪いのは誰か（あなたのせいではない） / 6 なぜ今なのか / 7 なぜ信頼できるか / 8 なぜうまくいくのか
#   9 次に何をすればいいか / 10 なぜここで買うのか
# 文字はすべて、日本語・英語・中国語の3つをここで持つ（assets/i18n.js の SALES10 ブロックに書き出す）
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TR = {}  # 日本語 → {en, zh}

def t(ja, en, zh):
    TR[ja] = {"en": en, "zh": zh}
    return ja

LINE = "https://lin.ee/P7ZYT6p"
LINE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 4C7 4 3 7.2 3 11.2c0 3.6 3.2 6.6 7.5 7.1-.2.9-.6 2.1-.7 2.4 0 .3.3.5.6.3 1.2-.8 4.3-2.8 5.9-4.3 2.3-1.3 3.7-3.3 3.7-5.5C21 7.2 17 4 12 4Z"/></svg>'

def head(kicker, title):
    return f'<div class="sec-head"><p class="en sub">{kicker}</p><h2 class="catch">{title}</h2></div>'

def why(title, items, foot, kicker="Why"):  # 質問4・5
    li = "".join(f'<li><b>{i:02d}</b><span>{x}</span></li>' for i, x in enumerate(items, 1))
    return f'<div class="s10 s10-why">{head(kicker, title)}<ol class="s10-list">{li}</ol><p class="s10-foot">{foot}</p></div>'

def steps(title, items, kicker, cta=None, cls="s10-steps"):  # 質問8・9
    def ok(x):  # 英語・中国語でも日本語のまま送ってもらう言葉（「体験」など）を含むもの
        return ' data-ja-ok' if re.search(r'[぀-ヿ一-鿿]', TR.get(x, {}).get('en', '')) else ''
    li = "".join(f'<li><b>{i:02d}</b><div><h3{ok(a)}>{a}</h3><p{ok(b)}>{b}</p></div></li>' for i, (a, b) in enumerate(items, 1))
    btn = f'<div class="btn-row"><a class="btn btn-solid" href="{LINE}" target="_blank" rel="noopener">{LINE_SVG}{cta}</a></div>' if cta else ""
    return f'<div class="s10 {cls}">{head(kicker, title)}<ol class="s10-list">{li}</ol>{btn}</div>'

def facts(items):  # 脳の3段階：開いてすぐ分かる3点
    return '<ul class="s10-facts">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def trust():  # 質問3・7
    return ('<div class="s10 s10-trust">'
            + head("Trust", t("代表は、元Jリーガー。", "Our founder is a former J.League player.", "我们的创始人是前J联赛球员。"))
            + '<div class="s10-stats">'
            + f'<div><b>95</b><span>{t("試合", "Matches", "出场")}</span></div>'
            + f'<div><b>11</b><span>{t("ゴール", "Goals", "进球")}</span></div>'
            + f'<div><b>9</b><span>{t("アシスト", "Assists", "助攻")}</span></div></div>'
            + f'<p class="s10-src">{t("Jリーグ通算（J1・J2リーグ戦）", "J.League career (J1 and J2 league matches)", "J联赛通算（J1・J2联赛）")}</p>'
            + f'<p>{t("16歳でロシアへ。スパルタク・モスクワ、U-18ロシア代表を経て、横浜F・マリノスなどJリーグ4クラブでプレー。", "Moved to Russia at 16. Spartak Moscow and the Russia U-18 national team, then four J.League clubs including Yokohama F. Marinos.", "16岁赴俄罗斯。经斯巴达克莫斯科、俄罗斯U-18国家队，后效力横滨水手等4家J联赛俱乐部。")}</p>'
            + f'<a class="s10-more" href="index.html#founder"><span>{t("代表のプロフィールを見る", "See the founder’s profile", "查看创始人简介")}</span> <span aria-hidden="true">→</span></a></div>')

def vs(other, ours, rows):  # 質問1・10
    th = f'<tr><th></th><th>{other}</th><th>{ours}</th></tr>'
    tr = "".join(f'<tr><th>{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    return ('<div class="s10 s10-vs">' + head("Why VX", t("ほかと、ここが違う。", "What makes us different.", "我们的不同之处。"))
            + f'<table class="s10-table"><thead>{th}</thead><tbody>{tr}</tbody></table></div>')

def now(title, sub):  # 質問6
    return f'<div class="s10 s10-now"><p class="en sub">Now</p><p class="s10-now-t">{title}</p><p>{sub}</p></div>'

def band(*blocks):
    return '<section class="band on-ink s10-band"><div class="wrap stack">' + "".join(blocks) + "</div></section>"

# ---- 共通の文 ----
ADD_LINE = (t("LINEで友だち追加", "Add us on LINE", "添加LINE好友"), t("下のボタンから、VXのLINEを追加します。", "Use the button below to add VX on LINE.", "点击下方按钮添加VX的LINE。"))
START_T = t("はじめ方は、3ステップ。", "Getting started takes 3 steps.", "只需3步即可开始。")
OTHER_PRACTICE = t("よくある練習", "Typical training", "常见训练")

# ---- PERSONAL ----
personal_facts = facts([t("代表は元Jリーガー", "Founded by a former J.League player", "创始人为前J联赛球员"),
                        t("1対1のマンツーマン", "One-on-one coaching", "一对一指导"),
                        t("初回体験 ¥5,500（税込）", "First trial ¥5,500 (incl. tax)", "首次体验 ¥5,500（含税）")])
personal_why = why(t("伸び悩むのは、才能のせいじゃない。", "If you’ve stopped improving, it isn’t your talent.", "进步停滞，不是天赋的问题。"),
    [t("技術の練習ばかりで、身体の土台を鍛えていない", "All skill drills, no work on the athletic base", "只练技术，没有打好身体基础"),
     t("大人数の練習で、自分の課題を見てもらえない", "In big group sessions, no one looks at your own weak points", "人数太多的训练，没人关注你自己的问题"),
     t("何をどう直せばいいか、具体的に言われていない", "No one has told you exactly what to fix, and how", "没人具体告诉你该改什么、怎么改")],
    t("足りなかったのは、やり方。VX PERSONALは、この3つを1対1で変えます。", "What was missing was the method. VX PERSONAL changes all three, one-on-one.", "缺少的是方法。VX PERSONAL 以一对一的方式改变这三点。"))
personal_mech = steps(t("なぜ、伸びるのか。", "Why it works.", "为什么能进步？"), [
    (t("課題を見る", "Find the gaps", "找出问题"), t("体験で、身体の動きとプレーの課題を確かめます。", "In the trial, we check how you move and where your game needs work.", "体验课中确认身体动作和比赛中的问题。")),
    (t("身体と技術を、同時に鍛える", "Train body and skill together", "身体与技术同时训练"), t("スピード・アジリティ・パワー・体幹と、止める・蹴るを同じ時間で。", "Speed, agility, power and core, plus first touch and passing, in the same session.", "速度、敏捷、力量、核心，以及停球、踢球，在同一节课中完成。")),
    (t("週1回、続ける", "Keep going, once a week", "每周一次，坚持下去"), t("積み上げるほど、動ける身体とプレーの質が変わります。", "The more you build, the more your body and your play change.", "积累越多，身体和比赛质量变化越大。"))],
    "How it works", cls="s10-steps s10-mech")
personal_vs = vs(OTHER_PRACTICE, "VX PERSONAL", [
    (t("人数", "Group size", "人数"), t("大人数", "Large groups", "人数多"), t("1対1", "One-on-one", "一对一")),
    (t("内容", "Focus", "内容"), t("技術が中心", "Mostly skills", "以技术为主"), t("身体能力×技術", "Athleticism × skill", "身体素质×技术")),
    (t("進め方", "Approach", "方式"), t("決まったメニュー", "Fixed drills", "固定菜单"), t("一人ひとりの課題に合わせる", "Built around your gaps", "根据个人问题定制"))])
personal_now = now(t("マンツーマンのため、受けられる人数に限りがあります。", "Because every session is one-on-one, places are limited.", "因为是一对一，名额有限。"),
                   t("始めたいと思った今が、いちばん早いタイミングです。", "The moment you want to start is the earliest you can.", "想开始的现在，就是最早的时机。"))
personal_start = steps(START_T, [ADD_LINE,
    (t("「体験」と送る", "Send “体験” (trial)", "发送「体験」"), t("日時を選んで申し込みます。", "Choose a date and time to book.", "选择日期和时间即可预约。")),
    (t("初回体験 ¥5,500", "First trial ¥5,500", "首次体验 ¥5,500"), t("続けるかどうかは、体験のあとで決められます。", "Decide whether to continue after the trial.", "体验后再决定是否继续。"))],
    "Start", cta="LINEで体験を申し込む")

# ---- GYM ----
gym_why = why(t("頑張っているのに、伸びが見えない。", "Working hard, but can’t see the progress?", "很努力，却看不到进步？"),
    [t("成長を測っていないから、伸びたかどうかわからない", "Progress isn’t measured, so you can’t tell if you’ve improved", "没有测量，就不知道是否进步了"),
     t("競技の練習だけで、運動能力そのものを鍛えていない", "Only sport practice, no training for athleticism itself", "只练专项，没有训练运动能力本身"),
     t("大人数で、一人ひとりに目が届かない", "Groups too big for anyone to watch you", "人数太多，照顾不到每个人")],
    t("足りないのは、努力ではなく「見える化」。VX GYMは、毎回計って伸びを見せます。", "What’s missing isn’t effort — it’s visibility. VX GYM measures every session and shows the progress.", "缺少的不是努力，而是“可视化”。VX GYM每次测量，让进步看得见。"))
gym_vs = vs(t("よくある習い事", "Typical classes", "常见兴趣班"), "VX GYM", [
    (t("成長の確認", "Tracking progress", "确认成长"), t("感覚", "By feel", "凭感觉"), t("毎回、数字で計測", "Measured every session", "每次数据测量")),
    (t("人数", "Group size", "人数"), t("大人数", "Large groups", "人数多"), t("定員8人・指導者1人", "Max 8, one coach", "最多8人・1名教练")),
    (t("対象", "Who", "对象"), t("競技ごと", "One sport only", "限定项目"), t("競技を問わず通える", "Any sport", "不限运动项目"))])
gym_now = now(t("オープン前の今は、先行予約が無料。", "Before opening, pre-registration is free.", "开业前，预约登记免费。"),
              t("オープン日・料金・体験会のご案内を、先行予約の方に優先してお送りします。1クラスの定員は8人です。", "Pre-registered members hear first about the opening date, prices and trial days. Classes are limited to 8.", "我们会优先向预约登记者发送开业日、费用及体验会信息。每班限8人。"))
gym_start = steps(START_T, [ADD_LINE,
    (t("「ジム」と送る", "Send “ジム” (gym)", "发送「ジム」"), t("先行予約の受付をご案内します。", "We’ll guide you through pre-registration.", "我们会引导你完成预约登记。")),
    (t("オープン情報を、いちばん先に", "Hear it first", "第一时间获取信息"), t("オープン日・体験会のご案内が届きます。", "You’ll get the opening date and trial-day info.", "你将收到开业日和体验会通知。"))],
    "Start", cta="LINEで先行予約する")

# ---- SOCCER ----
soccer_now = now(t("新チームの、立ち上げメンバーを募集中。", "Now recruiting founding members for the new team.", "新球队创始成员招募中。"),
                 t("U-12・U-9。チームの最初の一歩を、一緒につくる選手を待っています。", "U-12 and U-9. Join us and help take the team’s first step.", "U-12・U-9。期待与你一起迈出球队的第一步。"))
soccer_start = steps(START_T, [ADD_LINE,
    (t("「サッカー」と送る", "Send “サッカー” (soccer)", "发送「サッカー」"), t("入団のご案内をお送りします。", "We’ll send you joining information.", "我们会发送入队说明。")),
    (t("最新情報を受け取る", "Get the latest", "获取最新信息"), t("練習日・会場は決まり次第お知らせします。", "We’ll announce practice days and venue once confirmed.", "训练日和场地确定后会通知。"))],
    "Start", cta=t("LINEで入団を問い合わせる", "Ask about joining on LINE", "通过LINE咨询入队"))

# ---- APPAREL ----
apparel_why = why(t("スポーツウェアは街で浮く。普段着は動きにくい。", "Sportswear stands out on the street. Everyday clothes hold you back.", "运动服在街上显得突兀，日常服又不方便活动。"),
    [t("運動用の服は、デザインが「いかにも」", "Training gear looks too “gym”", "运动服的设计太“运动”"),
     t("普段着は、汗や動きに弱い", "Everyday clothes can’t handle sweat or movement", "日常服怕汗、不耐动"),
     t("結局、1日に何度も着替える", "So you end up changing several times a day", "结果一天要换好几次衣服")],
    t("悪いのは、服のつくり。VX APPARELは、動ける機能を毎日のデザインに。", "The problem is how the clothes are made. VX APPAREL puts performance into everyday design.", "问题出在衣服的设计。VX APPAREL 把运动机能融入日常设计。"))
apparel_mech = steps(t("なぜ、動けるのか。", "Why you can move in it.", "为什么穿着能自由活动？"), [
    (t("4方向ストレッチ", "Four-way stretch", "四向弹力"), t("どの方向にも伸びて、動きを邪魔しない。", "Stretches in every direction and never holds you back.", "向各个方向延展，不妨碍动作。")),
    (t("軽量・速乾", "Light and quick-dry", "轻量速干"), t("汗をかいても、すぐ乾く。", "Dries fast, even after a sweat.", "出汗后也能很快变干。")),
    (t("撥水", "Water-repellent", "防泼水"), t("水をはじく生地。", "Fabric that sheds water.", "能防泼水的面料。")),
    (t("リフレクティブ", "Reflective", "反光设计"), t("夜でも目立つ反射のディテール。", "Reflective details that stand out at night.", "夜间也醒目的反光细节。"))],
    "How it works", cls="s10-steps s10-mech")
apparel_now = now(t("DROP 01は、予約注文のみ。", "DROP 01 is pre-order only.", "DROP 01 仅接受预订。"),
                  t("予約締切後に生産します。締切日はInstagramとLINEでお知らせします。", "Made after the pre-order deadline. We’ll announce the deadline on Instagram and LINE.", "预订截止后开始生产。截止日期将在Instagram和LINE公布。"))
apparel_start = steps(START_T, [
    (t("色とサイズを選ぶ", "Choose colour and size", "选择颜色和尺码"), t("下のフォームで選びます。", "Pick them in the form below.", "在下方表格中选择。")),
    (t("LINEで送信", "Send on LINE", "通过LINE发送"), t("選んだ内容を、VXのLINEに送ります。", "Your choices are sent to VX on LINE.", "将所选内容发送到VX的LINE。")),
    (t("締切後に生産・お届け", "Made and delivered after the deadline", "截止后生产・配送"), t("お支払い方法とお届け時期は、LINEでご案内します。", "We’ll explain payment and delivery timing on LINE.", "付款方式和配送时间将通过LINE告知。"))], "Start")

# ---- トップ ----
index_reasons = steps(t("VXにしかない、3つのこと。", "Three things only VX offers.", "只有VX才有的三件事。"), [
    (t("プロの視点", "The pro perspective", "职业视角"), t("元Jリーガーの代表が、トップレベルで戦ってきた経験を伝えます。", "Our founder, a former J.League player, passes on what it takes at the top.", "前J联赛球员出身的创始人，传授顶级赛场的经验。")),
    (t("身体能力×技術", "Athleticism × skill", "身体素质×技术"), t("技術だけでなく、すべてのプレーの土台になる身体から鍛えます。", "Not just skills — we build the body every play depends on.", "不只练技术，更从支撑所有动作的身体开始训练。")),
    (t("成長が見える", "Progress you can see", "看得见的成长"), t("計測と、少人数・マンツーマンの指導で、一人ひとりの伸びを見逃しません。", "Measurement plus small groups and one-on-one coaching, so no one’s progress goes unnoticed.", "通过测量和小班・一对一指导，不错过每个人的进步。"))],
    "Why VX", cls="s10-steps s10-mech")
index_start = steps(START_T, [ADD_LINE,
    (t("知りたいことを送る", "Tell us what you want", "告诉我们你的需求"), t("「体験」「ジム」「サッカー」など、ひと言送るだけ。", "Just send one word, like “体験” (trial), “ジム” (gym) or “サッカー” (soccer).", "只需发送「体験」「ジム」「サッカー」等一个词。")),
    (t("ご案内が届く", "We reply with details", "收到说明"), t("日時・料金・次の流れをお送りします。", "We’ll send dates, prices and next steps.", "我们会发送日期、费用及后续流程。"))],
    "Start", cta=ADD_LINE[0])

# ---- 差し込む場所（正規表現の直前／直後） ----
PLAN = {
    "personal.html": [
        ("hero-facts", r'(?=\s*</div>\s*</section>\s*<section class="band on-paper" id="personal">)', personal_facts),
        ("why", r'(?=<section class="band on-paper" id="personal">)', band(personal_why, personal_mech, trust(), personal_vs)),
        ("start", r'(?=<section class="band on-ink faq")', band(personal_now, personal_start)),
    ],
    "gym.html": [
        ("why", r'(?<=</figure>)', gym_why),
        ("start", r'(?=<section class="band on-ink faq")', band(trust(), gym_vs, gym_now, gym_start)),
    ],
    "soccer.html": [
        ("start", r'(?=<section class="band on-ink faq")', band(trust(), soccer_now, soccer_start)),
    ],
    "apparel.html": [
        ("why", r'(?=<div class="products">)', apparel_why + apparel_mech),
        ("start", r'(?=<form class="order")', apparel_now + apparel_start),
    ],
    "index.html": [
        ("why", r'(?=<section class="band on-ink founder")', band(index_reasons)),
        ("start", r'(?=<section class="band on-ink" id="contact")', band(index_start)),
    ],
}

for name, items in PLAN.items():
    p = ROOT / name
    s = p.read_text(encoding="utf-8")
    s = re.sub(r'<!-- S10:[a-z-]+ -->.*?<!-- /S10:[a-z-]+ -->(\n\n  )?', "", s, flags=re.S)
    for key, pat, html in items:
        tail = "\n\n  " if pat.startswith("(?=<section") else ""
        s, n = re.subn(pat, f"<!-- S10:{key} -->{html}<!-- /S10:{key} -->{tail}", s, count=1)
        if n != 1:
            raise SystemExit(f"{name}: 差し込み位置が見つからない（{key}）")
    p.write_text(s, encoding="utf-8")

# 翻訳を i18n.js に書き出す
p = ROOT / "assets/i18n.js"
s = p.read_text(encoding="utf-8")
s = re.sub(r"\n  /\* SALES10 \*/ Object\.assign\(D,.*?\);\n", "\n", s, flags=re.S)
block = "\n  /* SALES10 */ Object.assign(D," + json.dumps(TR, ensure_ascii=False) + ");\n"
s = s.replace("\n  var nodes=[];", block + "  var nodes=[];", 1)
p.write_text(s, encoding="utf-8")
print("sales10:", len(TR), "phrases")
