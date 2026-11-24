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

LINE = "https://lin.ee/uKvQIEB"
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

def now(title, sub, kicker="Now"):  # 質問6（kicker を変えれば質問7の一言にも使う）
    return f'<div class="s10 s10-now"><p class="en sub">{kicker}</p><p class="s10-now-t">{title}</p><p>{sub}</p></div>'

def band(*blocks):
    return '<section class="band on-ink s10-band"><div class="wrap stack">' + "".join(blocks) + "</div></section>"

# ---- 共通の文 ----
ADD_LINE = (t("LINEで友だち追加", "Add us on LINE", "添加LINE好友"), t("下のボタンから、VXのLINEを追加します。", "Use the button below to add VX on LINE.", "点击下方按钮添加VX的LINE。"))
START_T = t("はじめ方は、3ステップ。", "Getting started takes 3 steps.", "只需3步即可开始。")
OTHER_PRACTICE = t("よくある練習", "Typical training", "常见训练")

# ---- PERSONAL ----
personal_facts = facts([t("元Jリーガーが直接指導", "Coached in person by a former J.League player", "前J联赛球员亲自指导"),
                        t("1対1のマンツーマン", "One-on-one coaching", "一对一指导"),
                        t("初回体験 ¥5,500（税込）", "First trial ¥5,500 (incl. tax)", "首次体验 ¥5,500（含税）")])
# 質問4・5（2026/11/24 一平さんの言葉から）
personal_why = why(t("伸び悩むのは、才能のせいじゃない。", "If you’ve stopped improving, it isn’t your talent.", "进步停滞，不是天赋的问题。"),
    [t("頭ではこうしたいと思っても、体がついてこない", "You know what you want to do, but your body can’t keep up", "脑子里想这样做，身体却跟不上"),
     t("思いどおりに身体を操作できず、イメージしたプレーができない", "You can’t control your body the way you want, so the play you picture never happens", "无法随心所欲地控制身体，做不出想象中的动作"),
     t("ドリブルなど技術の練習ばかりで、フィジカルを見落としている", "All dribbling and skill work — the physical side gets overlooked", "只练盘带等技术，忽视了身体素质")],
    t("土台は、体づくり。そこに技術が合わさって、はじめてやりたいプレーが表現できます。", "The foundation is the body. Add skill on top, and only then can you play the way you want.", "基础是身体。再加上技术，才能踢出你想要的比赛。"))
personal_mech = steps(t("なぜ、伸びるのか。", "Why it works.", "为什么能进步？"), [
    (t("まず、体をつくる", "Build the body first", "先打造身体"), t("スピード・アジリティ・パワー・体幹。思いどおりに動ける身体が、すべての土台です。", "Speed, agility, power and core. A body that moves the way you want is the base of everything.", "速度、敏捷、力量、核心。能随心而动的身体，是一切的基础。")),
    (t("そこに、技術を合わせる", "Then add the skill", "再结合技术"), t("止める・蹴るの基礎から上級スキルまで。身体と技術を、同じ時間で鍛えます。", "From first touch and passing to advanced skills, trained together with the body in the same session.", "从停球、踢球的基础到高级技巧，与身体训练在同一节课中完成。")),
    (t("判断が速くなり、余裕が生まれる", "Faster decisions, more time on the ball", "判断更快，踢球更从容"), t("一瞬の動きや、フェイントのあとの判断。体の土台があるから、余裕を持ってプレーできます。", "The split-second move, the decision after a feint. With a strong base, you play with time to spare.", "瞬间的动作、假动作后的判断。有了身体基础，就能从容比赛。"))],
    "How it works", cls="s10-steps s10-mech")
# 質問10（ほかとの違い）
personal_vs = vs(OTHER_PRACTICE, "VX PERSONAL", [
    (t("練習の中心", "Main focus", "训练重点"), t("ドリブルなどの技術", "Dribbling and other skills", "盘带等技术"), t("体の土台＋技術", "Physical base + skill", "身体基础＋技术")),
    (t("フィジカル", "Physical side", "身体素质"), t("見落とされがち", "Often overlooked", "常被忽视"), t("いちばん大事にする", "Our top priority", "最重视的部分")),
    (t("一瞬の動き・判断", "Split-second moves and decisions", "瞬间动作・判断"), t("技術だけでは限界", "Skill alone hits a limit", "仅靠技术有局限"), t("土台があるから、判断が速く余裕が出る", "A strong base means faster decisions and more time", "有基础，判断更快、更从容")),
    (t("人数", "Group size", "人数"), t("大人数", "Large groups", "人数多"), t("1対1", "One-on-one", "一对一"))])
# 質問3（証拠：2026/11/24 一平さんから）
personal_proof = ('<div class="s10 s10-trust">' + head("Proof", t("いまも現場で、選手を指導しています。", "Coaching players on the pitch, right now.", "现在依然在一线指导球员。"))
    + '<div class="s10-stats">'
    + f'<div><b>30+</b><span>{t("個人指導中の選手", "Players in one-on-one coaching", "正在个人指导的球员")}</span></div>'
    + f'<div><b>26</b><span>{t("12月の合宿の参加者", "Players at the December camp", "12月集训参加人数")}</span></div>'
    + f'<div><b>{t("約20", "~20", "约20")}</b><span>{t("毎回の合宿の参加者", "Players at each camp", "每次集训参加人数")}</span></div></div>'
    + f'<p class="s10-src">{t("2026年11月時点。12月14日からの合宿で4回目。", "As of November 2026. The camp from 14 December is our fourth.", "截至2026年11月。12月14日起的集训为第4次。")}</p></div>')
personal_now = now(t("マンツーマンのため、受けられる人数に限りがあります。", "Because every session is one-on-one, places are limited.", "因为是一对一，名额有限。"),
                   t("始めたいと思った今が、いちばん早いタイミングです。", "The moment you want to start is the earliest you can.", "想开始的现在，就是最早的时机。"))
personal_start = steps(START_T, [ADD_LINE,
    (t("「体験」と送る", "Send “体験” (trial)", "发送「体験」"), t("日時を選んで申し込みます。", "Choose a date and time to book.", "选择日期和时间即可预约。")),
    (t("初回体験 ¥5,500", "First trial ¥5,500", "首次体验 ¥5,500"), t("合う・合わないは人それぞれ。まず一度試して、良ければ続けてください。", "Everyone’s different. Try it once, and continue only if it suits you.", "适不适合因人而异。先试一次，觉得好再继续。"))],
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
# 質問4・5・8・10（SOCCER）
soccer_why = why(t("試合で通用しないのは、技術不足だけじゃない。", "If it isn’t working in matches, it isn’t only about skill.", "比赛中踢不开，不只是技术不足。"),
    [t("当たり負けして、ボールを失う", "You get knocked off the ball", "身体对抗落下风，丢掉球权"),
     t("一歩目が遅れて、相手に先に触られる", "Your first step is late, so the opponent gets there first", "第一步慢，被对手抢先触球"),
     t("判断が遅れて、パスがつながらない", "Slow decisions break up the passing", "判断慢，传球连不起来")],
    t("原因の多くは、体の土台。VX SOCCERは身体能力を本気で鍛えながら、全員でつなぐパスサッカーを教えます。", "Most of it comes down to the physical base. VX SOCCER builds real athleticism while teaching a passing game everyone takes part in.", "原因大多在身体基础。VX SOCCER 认真训练身体素质，同时教授全员参与的传控足球。"))
soccer_mech = steps(t("なぜ、強くなるのか。", "Why the team gets better.", "为什么能变强？"), [
    (t("体をつくる", "Build the body", "打造身体"), t("アジリティ・フィジカル・運動能力を、毎回のトレーニングで鍛えます。", "Agility, physicality and athleticism, trained every session.", "每次训练都锻炼敏捷、身体对抗和运动能力。")),
    (t("全員でつなぐ", "Pass it together", "全员传控"), t("トップレベルの指導で、全員でボールをつなぐパスサッカーを。", "Top-level coaching in a passing game where everyone keeps the ball moving.", "在顶级指导下，踢全员传控的足球。")),
    (t("判断が速くなる", "Decide faster", "判断更快"), t("体の土台があるから、余裕を持ってプレーできます。", "With a strong base, players have time to think on the ball.", "有了身体基础，就能从容比赛。"))],
    "How it works", cls="s10-steps s10-mech")
soccer_vs = vs(t("よくあるチーム", "Typical teams", "常见球队"), "VX SOCCER", [
    (t("練習の中心", "Main focus", "训练重点"), t("試合形式・技術", "Match play and skills", "比赛形式・技术"), t("身体能力×パスサッカー", "Athleticism × passing football", "身体素质×传控足球")),
    (t("フィジカル", "Physical side", "身体素质"), t("見落とされがち", "Often overlooked", "常被忽视"), t("いちばん大事にする", "Our top priority", "最重视的部分")),
    (t("指導", "Coaching", "指导"), t("チームによる", "Varies by team", "因队而异"), t("代表は元Jリーガー", "Founder is a former J.League player", "创始人是前J联赛球员"))])
soccer_now = now(t("新チームの、立ち上げメンバーを募集中。", "Now recruiting founding members for the new team.", "新球队创始成员招募中。"),
                 t("U-12・U-9。チームの最初の一歩を、一緒につくる選手を待っています。", "U-12 and U-9. Join us and help take the team’s first step.", "U-12・U-9。期待与你一起迈出球队的第一步。"))
soccer_start = steps(START_T, [ADD_LINE,
    (t("「サッカー」と送る", "Send “サッカー” (soccer)", "发送「サッカー」"), t("入団のご案内をお送りします。", "We’ll send you joining information.", "我们会发送入队说明。")),
    (t("最新情報を受け取る", "Get the latest", "获取最新信息"), t("練習日・会場は決まり次第お知らせします。", "We’ll announce practice days and venue once confirmed.", "训练日和场地确定后会通知。"))],
    "Start", cta=t("LINEで入団を問い合わせる", "Ask about joining on LINE", "通过LINE咨询入队"))

# ---- APPAREL ----
# APPARELは「憧れ型」：悩み（Q4・Q5）は打ち出さない。かっこよさ・品質（Q1・Q2）で答える（2026/11/24 一平さん）
apparel_why = why(t("かっこいいから、毎日着たくなる。", "Good-looking enough to wear every day.", "因为好看，所以每天都想穿。"),
    [t("無駄のない、シンプルなデザイン", "Clean, minimal design", "简洁利落的设计"),
     t("街に合う6色から選べる", "Six colours that work on the street", "6种适合街头的配色"),
     t("袖のリフレクティブやスリットまで、細部まで仕上げた高品質なつくり", "High-quality finish down to the reflective sleeve details and side slits", "从袖口反光到侧开衩，细节都精心打磨的高品质做工")],
    t("動ける服を、毎日の服に。", "Clothes you can move in, made for every day.", "能运动的衣服，变成每天的衣服。"), kicker="Why VX APPAREL")
apparel_mech = steps(t("なぜ、動けるのか。", "Why you can move in it.", "为什么穿着能自由活动？"), [
    (t("4方向ストレッチ", "Four-way stretch", "四向弹力"), t("どの方向にも伸びて、動きを邪魔しない。", "Stretches in every direction and never holds you back.", "向各个方向延展，不妨碍动作。")),
    (t("軽量・速乾", "Light and quick-dry", "轻量速干"), t("汗をかいても、すぐ乾く。", "Dries fast, even after a sweat.", "出汗后也能很快变干。")),
    (t("撥水", "Water-repellent", "防泼水"), t("水をはじく生地。", "Fabric that sheds water.", "能防泼水的面料。")),
    (t("リフレクティブ", "Reflective", "反光设计"), t("夜でも目立つ反射のディテール。", "Reflective details that stand out at night.", "夜间也醒目的反光细节。"))],
    "How it works", cls="s10-steps s10-mech")
# 質問10・7（APPAREL）
apparel_vs = vs(t("よくあるスポーツウェア", "Typical sportswear", "常见运动服"), "VX APPAREL", [
    (t("デザイン", "Design", "设计"), t("いかにも運動用", "Looks like gym kit", "一看就是运动服"), t("普段着として着られる", "Wearable as everyday clothes", "可以当日常服穿")),
    (t("機能", "Function", "机能"), t("運動のときだけ", "Only for workouts", "只在运动时"), t("4方向ストレッチ・速乾・撥水を毎日に", "Four-way stretch, quick-dry and water-repellent, every day", "四向弹力・速干・防泼水，天天都能用")),
    (t("着る場面", "When you wear it", "穿着场合"), t("トレーニングだけ", "Training only", "仅限训练"), t("トレーニングも、街も", "Training and the street", "训练、街头都可以"))])
apparel_trust = now(t("THE PRO PERSPECTIVE.", "THE PRO PERSPECTIVE.", "THE PRO PERSPECTIVE."),
    t("プロの視点でつくった、動ける服を、毎日の服に。", "Made from a pro’s perspective: clothes you can move in, for every day.", "以职业视角打造：能运动的衣服，变成每天的衣服。"), kicker="VX APPAREL")
apparel_now = now(t("DROP 01は、予約注文のみ。", "DROP 01 is pre-order only.", "DROP 01 仅接受预订。"),
                  t("予約締切後に生産します。締切日はInstagramとLINEでお知らせします。", "Made after the pre-order deadline. We’ll announce the deadline on Instagram and LINE.", "预订截止后开始生产。截止日期将在Instagram和LINE公布。"))
apparel_start = steps(START_T, [
    (t("色とサイズを選ぶ", "Choose colour and size", "选择颜色和尺码"), t("下のフォームで選びます。", "Pick them in the form below.", "在下方表格中选择。")),
    (t("LINEで送信", "Send on LINE", "通过LINE发送"), t("選んだ内容を、VXのLINEに送ります。", "Your choices are sent to VX on LINE.", "将所选内容发送到VX的LINE。")),
    (t("締切後に生産・お届け", "Made and delivered after the deadline", "截止后生产・配送"), t("お支払い方法とお届け時期は、LINEでご案内します。", "We’ll explain payment and delivery timing on LINE.", "付款方式和配送时间将通过LINE告知。"))], "Start")

# ---- トップ ----
index_reasons = steps(t("VXにしかない、3つのこと。", "Three things only VX offers.", "只有VX才有的三件事。"), [
    (t("プロの視点", "The pro perspective", "职业视角"), t("元Jリーガーの代表が、トップレベルで戦ってきた経験を伝えます。", "Our founder, a former J.League player, passes on what it takes at the top.", "前J联赛球员出身的创始人，传授顶级赛场的经验。")),
    (t("身体能力×技術", "Athleticism × skill", "身体素质×技术"), t("多くの練習が見落としているフィジカルから。体の土台があるから、判断が速く、余裕を持ってプレーできます。", "We start with the physical side most training overlooks. With a strong base, you decide faster and play with time to spare.", "从多数训练忽视的身体素质入手。有了身体基础，判断更快、比赛更从容。")),
    (t("成長が見える", "Progress you can see", "看得见的成长"), t("計測と、少人数・マンツーマンの指導で、一人ひとりの伸びを見逃しません。", "Measurement plus small groups and one-on-one coaching, so no one’s progress goes unnoticed.", "通过测量和小班・一对一指导，不错过每个人的进步。"))],
    "Why VX", cls="s10-steps s10-mech")
index_start = steps(START_T, [ADD_LINE,
    (t("知りたいことを送る", "Tell us what you want", "告诉我们你的需求"), t("「体験」「ジム」「サッカー」など、ひと言送るだけ。", "Just send one word, like “体験” (trial), “ジム” (gym) or “サッカー” (soccer).", "只需发送「体験」「ジム」「サッカー」等一个词。")),
    (t("ご案内が届く", "We reply with details", "收到说明"), t("日時・料金・次の流れをお送りします。", "We’ll send dates, prices and next steps.", "我们会发送日期、费用及后续流程。"))],
    "Start", cta=ADD_LINE[0])

CAMP_SHOW = False  # 合宿写真（子どもの顔あり）：保護者の許可を一平さんに確認してから True に
# 合宿（質問3の証拠：2026/11/24 一平さんの写真）
CAMP_IMGS = [("camp-01.jpg", 1600, 1201, "合宿に参加した選手たちと指導者の集合写真"),
             ("camp-02.jpg", 1600, 900, "合宿のトレーニングで選手に説明する代表"),
             ("camp-03.jpg", 1600, 1201, "ナイターのグラウンドで指導を受ける選手たち"),
             ("camp-04.jpg", 1600, 900, "合宿の夕食の時間")]
camp = ('<div class="s10 s10-camp">' + head("Camp", t("合宿も、開催しています。", "We run training camps, too.", "我们也举办集训。"))
    + '<ul class="camp-track">' + "".join(f'<li><img src="assets/{f}" alt="{a}" loading="lazy" width="{w}" height="{h}"></li>' for f, w, h, a in CAMP_IMGS) + '</ul>'
    + f'<p>{t("12月14日からの合宿で4回目。今回は総勢26人が集まっています。毎回20人前後の選手が参加し、トレーニングから食事まで、仲間と一緒に過ごしながら身体と技術を磨きます。", "The camp from 14 December is our fourth, with 26 players this time. Around 20 players join each camp, spending the days together — from training to meals — to sharpen body and skill.", "12月14日起的集训是第4次，本次共有26名球员参加。每次约20名球员参加，从训练到用餐，与伙伴们一起磨练身体与技术。")}</p>'
    + f'<p class="s10-src" data-ja-ok>{t("次回の合宿は、LINEで「合宿」と送ると優先してご案内します。", "Send “合宿” (camp) on LINE to hear first about the next camp.", "在LINE发送「合宿」，即可优先获取下次集训信息。")}</p></div>')

# ---- 差し込む場所（正規表現の直前／直後） ----
PLAN = {
    "personal.html": [
        ("hero-facts", r'(?=\s*</div>\s*</section>\s*<section class="band on-paper" id="personal">)', personal_facts),
        ("why", r'(?=<section class="band on-paper" id="personal">)', band(personal_why, personal_mech, trust(), personal_proof, personal_vs)),
        ("start", r'(?=<section class="band on-ink faq")', band(personal_now, personal_start)),
    ],
    "gym.html": [
        ("why", r'(?<=</figure>)', gym_why),
        ("start", r'(?=<section class="band on-ink faq")', band(trust(), gym_vs, gym_now, gym_start)),
    ],
    "soccer.html": [
        ("start", r'(?=<section class="band on-ink faq")', band(soccer_why, soccer_mech, trust(), soccer_vs, *([camp] if CAMP_SHOW else []), soccer_now, soccer_start)),
    ],
    "apparel.html": [
        ("why", r'(?=<div class="products">)', apparel_why + apparel_mech + apparel_vs + apparel_trust),
        ("start", r'(?=<form class="order")', apparel_now + apparel_start),
    ],
    "index.html": [
        ("why", r'(?=<section class="band on-ink founder")', band(index_reasons, personal_proof, *([camp] if CAMP_SHOW else []))),
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
