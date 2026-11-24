# VX SPORTS ACADEMY：検索・AI検索向けの改修（タイトル・説明文・構造化データ・FAQ・説明セクション）
import json, re, sys, os

ROOT = sys.argv[1]
BASE = 'https://ippey0320.github.io/vx-sports-academy/'
LINE = 'https://lin.ee/uKvQIEB'
IG = 'https://www.instagram.com/vx_sports_academy/'
UPDATED_ISO = '2026-11-18'
UPDATED_JP = '情報更新日：2026年11月18日'

ORG = {
    '@type': 'SportsOrganization', '@id': BASE + '#org',
    'name': 'VX SPORTS ACADEMY', 'url': BASE,
    'logo': BASE + 'assets/apple-touch-icon.png', 'image': BASE + 'assets/og-image.png',
    'description': 'サッカーのパーソナル指導（VX PERSONAL）、キッズからアスリートまでのジム（VX GYM・東京 西麻布）、U-12・U-9のサッカーチーム（VX SOCCER）、アパレルブランド（VX APPAREL）を運営するスポーツアカデミー。',
    'sport': ['サッカー', 'Soccer'],
    'founder': {'@type': 'Person', '@id': BASE + '#founder', 'name': 'シノヅカイッペイ', 'alternateName': ['イッペイ・シノヅカ', 'Ippey Shinozuka', '篠塚一平'], 'jobTitle': '代表',
                'description': '元プロサッカー選手（MF）。U-18ロシア代表。スパルタク・モスクワ、横浜F・マリノス、大宮アルディージャ、柏レイソル、アルビレックス新潟でプレー。Jリーグ通算95試合11ゴール9アシスト（J1・J2リーグ戦）。',
                'image': BASE + 'assets/founder.jpg', 'sameAs': ['https://en.wikipedia.org/wiki/Ippey_Shinozuka']},
    'sameAs': [IG, 'https://www.instagram.com/vx.gym.official/', 'https://www.instagram.com/vx.apparel.official/', 'https://x.com/vxsportsacademy'],
    'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'customer service', 'url': LINE, 'availableLanguage': ['ja']},
                     {'@type': 'ContactPoint', 'contactType': 'sponsorship', 'url': IG, 'availableLanguage': ['ja']}],
}
JPY = lambda p, name, extra=None: dict({'@type': 'Offer', 'name': name, 'price': str(p), 'priceCurrency': 'JPY'}, **(extra or {}))

PAGES = {
 'index': dict(
  path='', title='VX SPORTS ACADEMY｜サッカーのパーソナル指導・キッズからアスリートまでのジム',
  desc='VX SPORTS ACADEMYは、サッカーのパーソナル指導「VX PERSONAL」、年齢を問わず、キッズからアスリートを目指す選手までの運動能力を数字で伸ばす「VX GYM」（東京・西麻布／2027年1月オープン予定）、U-12・U-9のサッカーチーム「VX SOCCER」、アパレルブランド「VX APPAREL」を運営するスポーツアカデミーです。',
  og='プロの視点を、すべての選手に。サッカーのパーソナル指導・キッズ〜アスリート・サッカーチーム・ウェア。',
  name='ホーム',
  faq=[
   ('VX SPORTS ACADEMYとは何ですか？', 'サッカーの技術と、年齢を問わずキッズからアスリートを目指す選手までの運動能力を伸ばすスポーツアカデミーです。サッカーのパーソナル指導「VX PERSONAL」、キッズからアスリートまでのジム「VX GYM」、サッカーチーム「VX SOCCER」、アパレルブランド「VX APPAREL」の4つを運営しています。'),
   ('代表はどんな人ですか？', '代表のシノヅカイッペイは元プロサッカー選手（MF）です。U-18ロシア代表、スパルタク・モスクワ（ロシア）を経て、横浜F・マリノス、大宮アルディージャ、柏レイソル、アルビレックス新潟でプレーしました。Jリーグ通算95試合11ゴール9アシスト（J1・J2リーグ戦）です。'),
   ('どこにありますか？', 'VX GYMは東京・西麻布に2027年1月オープン予定です。VX PERSONALは東京・神奈川・千葉・埼玉で対応しています。'),
   ('今申し込めるサービスは？', 'VX PERSONAL（初回体験 ¥5,500・税込）は受付中です。VX GYMは先行予約、VX SOCCERはU-12・U-9のメンバーを募集中、VX APPARELは予約注文を受け付けています。'),
   ('スポンサー・協賛の依頼はどこからできますか？', 'LINE公式アカウント、またはInstagram（@vx_sports_academy）のDMからお送りください。'),
   ('問い合わせ方法は？', 'LINE公式アカウントから、メッセージでお問い合わせください。最新情報はInstagram（@vx_sports_academy）でもお知らせしています。'),
  ]),
 'personal': dict(
  path='personal.html', title='キッズからアスリートまで、サッカーのパーソナルトレーニング｜VX PERSONAL',
  desc='VX PERSONALは、身体能力（スピード・アジリティ・パワー・体幹）とサッカーの技術を、マンツーマンで伸ばすパーソナル指導です。年齢を問わず、キッズからアスリートを目指す選手まで、初心者から上級者まで対応。初回体験 ¥5,500、本レッスン ¥16,500／回（税込）。東京・神奈川・千葉・埼玉で対応。',
  og='身体能力とサッカーの技術を、マンツーマンで伸ばす。初回体験 ¥5,500（税込）。',
  name='VX PERSONAL',
  faq=[
   ('VX PERSONALでは何を教えてもらえますか？', '身体能力（スピード・アジリティ・パワー・体幹）と、止める・蹴るの基礎から上級スキルまでのサッカーの技術を、マンツーマンで指導します。'),
   ('料金はいくらですか？', '初回体験 ¥5,500、本レッスン ¥16,500／回（最低4回から）、初月の1ヶ月契約（週1回）¥66,000、2ヶ月目以降の3ヶ月契約 ¥198,000です。すべて税込です。'),
   ('対象年齢はありますか？', 'ありません。キッズからアスリートを目指す選手まで、年齢を問わず受けられます。'),
   ('初心者でも受けられますか？', 'はい。初心者から上級者まで、一人ひとりのレベルと課題に合わせて指導します。'),
   ('どのエリアで受けられますか？', '東京・神奈川・千葉・埼玉で対応しています。ご希望のエリアはLINEでお知らせください。'),
   ('どのくらいの頻度で通えばいいですか？', '週1回の継続をおすすめしています。続けて取り組むことで、確実な成長を目指します。'),
   ('申し込み方法は？', 'LINE公式アカウントから初回体験をお申し込みください。'),
  ],
  extra=lambda: [{
   '@type': 'Service', '@id': BASE + 'personal.html#service', 'name': 'VX PERSONAL',
   'serviceType': 'サッカーのパーソナルトレーニング', 'provider': {'@id': BASE + '#org'},
   'description': '身体能力とサッカーの技術を、マンツーマンで伸ばすパーソナル指導。年齢を問わず、キッズからアスリートを目指す選手まで、初心者から上級者まで。',
   'areaServed': [{'@type': 'AdministrativeArea', 'name': n} for n in ['東京都', '神奈川県', '千葉県', '埼玉県']],
   'offers': [JPY(5500, '初回体験（1回）'), JPY(16500, '本レッスン（1回・最低4回から）'), JPY(66000, '初月 1ヶ月契約（週1回）'), JPY(198000, '2ヶ月目以降 3ヶ月契約')],
  }]),
 'gym': dict(
  path='gym.html', title='西麻布のキッズ・アスリートジム｜VX GYM（2027年1月オープン予定）',
  desc='VX GYMは、東京・西麻布に2027年1月オープン予定の、年齢を問わず、キッズからアスリートを目指す選手まで通えるジムです。競技を問わず、パワー・ジャンプ・スピードを毎回計測して成長をグラフで記録。年代別グループクラス（定員8人）。月額 ¥17,800〜（税込）。LINEで先行予約受付中。',
  og='お子さんの成長が、数字で見える。西麻布・2027年1月オープン予定。先行予約受付中。',
  name='VX GYM',
  faq=[
   ('VX GYMはいつ、どこにオープンしますか？', '東京・西麻布に2027年1月オープン予定です。現在、LINEで先行予約を受け付けています。'),
   ('どんな人が対象ですか？', 'サッカー、野球、バスケ、陸上など競技を問わず、運動能力を伸ばしたいキッズから、アスリートを目指す選手まで、年齢を問わず対象です。クラスは年代別のグループで、定員8人・指導者1人です。'),
   ('何を計測しますか？', 'パワー出力（W）、ジャンプ（cm）、スピード（秒）を毎回計測し、入会時からの伸びをグラフで記録します。'),
   ('料金はいくらですか？', '月額（税込）で、週1回（月4回）¥17,800、週2回（月8回）¥28,000です。月1回のマンツーマンと測定結果のフィードバックがつく「エリート」は＋¥15,000で追加できます。'),
   ('先行予約に料金はかかりますか？', 'かかりません。先行予約は、オープン日・料金・体験会のご案内を優先してお送りするための登録です。'),
  ],
  extra=lambda: [{
   '@type': 'Service', '@id': BASE + 'gym.html#service', 'name': 'VX GYM',
   'serviceType': 'キッズからアスリートまでのジム（年齢不問のアスレチックトレーニング）', 'provider': {'@id': BASE + '#org'},
   'description': '東京・西麻布に2027年1月オープン予定。競技を問わず、パワー・ジャンプ・スピードを毎回計測して、年齢を問わずキッズからアスリートを目指す選手までの運動能力を伸ばすジム。年代別グループクラス（定員8人・指導者1人）。',
   'areaServed': {'@type': 'Place', 'name': '東京都港区西麻布'},
   'audience': {'@type': 'PeopleAudience', 'audienceType': 'キッズからアスリートを目指す選手まで（年齢不問）'},
   'offers': [JPY(17800, '週1回（月4回）月額', {'availability': 'https://schema.org/PreOrder'}), JPY(28000, '週2回（月8回）月額', {'availability': 'https://schema.org/PreOrder'}), JPY(15000, 'エリート（追加・月額）', {'availability': 'https://schema.org/PreOrder'})],
  }]),
 'soccer': dict(
  path='soccer.html', title='U-12・U-9の新しいサッカーチーム｜VX SOCCER メンバー募集',
  desc='VX SOCCERは、身体能力を本気で伸ばすトレーニングとトップレベルのサッカー教育を両立する新しいサッカーチームです。カテゴリーはU-12・U-9。アジリティ・フィジカル・運動能力・パスサッカー。メンバー募集中、入団のお問い合わせはLINEから。',
  og='選手一人ひとりが、生き生きとサッカーできるチームを。U-12・U-9 メンバー募集。',
  name='VX SOCCER',
  faq=[
   ('VX SOCCERはどんなチームですか？', '身体能力を本気で伸ばすトレーニングと、トップレベルのサッカー教育を両立する新しいチームです。全員でボールをつなぐパスサッカーを目指します。'),
   ('募集しているカテゴリーは？', 'U-12とU-9です。'),
   ('練習日と会場は？', '決まり次第お知らせします。最新情報はInstagram（@vx_sports_academy）でお知らせします。'),
   ('入団の問い合わせ方法は？', 'LINE公式アカウント、またはInstagramのDMからお問い合わせください。'),
   ('ユニフォームはありますか？', 'HOME（ブラック）・AWAY（ホワイト）・THIRD（グレー）のオフィシャルユニフォームがあります。シャツ・パンツ・ソックスのセットで、背中に名前と背番号を入れられます。'),
  ],
  extra=lambda: [{
   '@type': 'SportsTeam', '@id': BASE + 'soccer.html#team', 'name': 'VX SOCCER', 'sport': 'サッカー',
   'parentOrganization': {'@id': BASE + '#org'},
   'description': '身体能力を伸ばすトレーニングとトップレベルのサッカー教育を両立する新しいサッカーチーム。カテゴリーはU-12・U-9。',
   'audience': {'@type': 'PeopleAudience', 'audienceType': 'U-12・U-9の子ども'},
  }]),
 'apparel': dict(
  path='apparel.html', title='VX APPAREL｜普段着にもなるTシャツ・ショーツ・ソックス 予約受付中',
  desc='VX SPORTS ACADEMYのアパレル（VX T-SHIRT・VX SHORTS・VX SOCKS）の予約注文を受付中。Tシャツ ¥7,700、ショーツ ¥7,700、ソックス ¥2,200、3点セット ¥15,400（税込）。軽量・速乾、4方向ストレッチ、撥水。6色・S〜XL。',
  og='動ける服を、毎日の服に。VX APPAREL 3点セット ¥15,400（税込）。予約受付中。',
  name='VX APPAREL',
  faq=[
   ('何を買えますか？', 'Tシャツ ¥7,700、ショーツ ¥7,700、ソックス ¥2,200、3点セット ¥15,400です（すべて税込）。3点セットは単品合計より¥2,200お得です。'),
   ('カラーとサイズは？', 'Ink Black・Sage Green・Powder Blue・Petal Pink・Mist Lavender・Cloud Whiteのユニセックス6色、サイズはS・M・L・XLです。ソックスも同じ6色です。'),
   ('どんな素材・機能ですか？', '軽量・速乾で、4方向ストレッチと撥水性、動きやすいスリット、夜でも目立つリフレクティブがついています。トレーニングにも普段着にも使えます。'),
   ('いつ届きますか？', '予約注文のため、予約締切後の生産となります。お届け時期とお支払い方法はLINEでご案内します。'),
  ],
  extra=lambda: [
   {'@type': 'Product', 'name': n, 'brand': {'@type': 'Brand', 'name': 'VX SPORTS ACADEMY'}, 'description': d,
    'image': BASE + 'assets/apparel/' + img + '.webp', 'url': BASE + page + '.html',
    'color': 'Ink Black, Sage Green, Powder Blue, Petal Pink, Mist Lavender, Cloud White', 'size': 'S, M, L, XL',
    'offers': JPY(p, n, {'availability': 'https://schema.org/PreOrder', 'url': BASE + page + '.html', 'seller': {'@id': BASE + '#org'}})}
   for n, p, d, img, page in [('VX 3点セット（T-SHIRT・SHORTS・SOCKS）', 15400, 'Tシャツ・ショーツ・ソックスを同じ色でそろえるセット。ユニセックス6色・S〜XL。', 'set-front_sage-green', 'set'),
                   ('VX T-SHIRT', 7700, '高通気・速乾メッシュ。4方向ストレッチ、裾のスリット、反射ライン。', 'set-front_ink-black', 'tee'),
                   ('VX SHORTS', 7700, '4方向ストレッチ・撥水。両サイドポケット、反射ライン。', 'shorts-back_ink-black', 'shorts'),
                   ('VX SOCKS', 2200, '約22cm丈・ウェアと同じ6色。', 'socks_ink-black', 'socks')]]),
}

# ---- 英語・中国語（言語切替用） ----
TR = {
 'スポンサー・協賛の依頼はどこからできますか？': ('How can I propose a sponsorship or partnership?', '如何提出赞助・合作请求？'),
 'LINE公式アカウント、またはInstagram（@vx_sports_academy）のDMからお送りください。': ('Message us on our official LINE account or by Instagram DM (@vx_sports_academy).', '请通过LINE官方账号或Instagram（@vx_sports_academy）私信联系。'),
 'VX SPORTS ACADEMY 代表': ('Founder, VX SPORTS ACADEMY', 'VX SPORTS ACADEMY 代表'),
 '代表 シノヅカイッペイ': ('Founder: Ippey Shinozuka', '代表 Ippey Shinozuka'),
 'シノヅカイッペイ': ('Ippey Shinozuka', 'Ippey Shinozuka'),
 '代表・元プロサッカー選手（MF）': ('Founder · Former professional footballer (MF)', '代表・前职业足球运动员（中场）'),
 '試合': ('Apps', '出场'),
 'ゴール': ('Goals', '进球'),
 'アシスト': ('Assists', '助攻'),
 'Jリーグ通算（J1・J2リーグ戦／2017〜2022年）出典：Football LAB': ('J.League career totals (J1 & J2 league matches, 2017–2022). Source: Football LAB', 'J联赛生涯合计（J1・J2联赛，2017〜2022年）。来源：Football LAB'),
 'U-18ロシア代表': ('Russia U-18 national team', '俄罗斯U-18国家队'),
 'スパルタク・モスクワ（ロシア）': ('Spartak Moscow (Russia)', '莫斯科斯巴达克（俄罗斯）'),
 '横浜F・マリノス（J1）': ('Yokohama F. Marinos (J1)', '横滨水手（J1）'),
 '大宮アルディージャ（J2）': ('Omiya Ardija (J2)', '大宫松鼠（J2）'),
 '柏レイソル（J1）': ('Kashiwa Reysol (J1)', '柏太阳神（J1）'),
 'アルビレックス新潟（J2）': ('Albirex Niigata (J2)', '新潟天鹅（J2）'),
 '16歳でロシアへ渡り、スパルタク・モスクワでプロのキャリアをスタート。U-18ロシア代表を経て、Jリーグでは4クラブでプレーしました。': ('Moved to Russia at 16 and began his professional career at Spartak Moscow. After playing for Russia at U-18 level, he played for four J.League clubs.', '16岁远赴俄罗斯，在莫斯科斯巴达克开始职业生涯。入选俄罗斯U-18国家队后，在J联赛效力过4家俱乐部。'),
 'トップレベルで戦ってきた経験を、次の世代の選手へ。': ('Passing on what he learned at the top level to the next generation of players.', '将在顶级舞台积累的经验，传给下一代球员。'),
 '代表はどんな人ですか？': ('Who is the founder?', '代表是谁？'),
 '代表のシノヅカイッペイは元プロサッカー選手（MF）です。U-18ロシア代表、スパルタク・モスクワ（ロシア）を経て、横浜F・マリノス、大宮アルディージャ、柏レイソル、アルビレックス新潟でプレーしました。Jリーグ通算95試合11ゴール9アシスト（J1・J2リーグ戦）です。': ('Founder Ippey Shinozuka is a former professional footballer (midfielder). After Russia U-18 and Spartak Moscow, he played for Yokohama F. Marinos, Omiya Ardija, Kashiwa Reysol and Albirex Niigata, with 95 appearances, 11 goals and 9 assists in the J.League (J1 and J2 league matches).', '代表Ippey Shinozuka是前职业足球运动员（中场）。曾入选俄罗斯U-18国家队、效力莫斯科斯巴达克，之后在横滨水手、大宫松鼠、柏太阳神、新潟天鹅踢球。J联赛（J1・J2联赛）生涯出场95次，进球11个，助攻9次。'),
 '対象年齢はありますか？': ('Is there an age limit?', '有年龄限制吗？'),
 'ありません。キッズからアスリートを目指す選手まで、年齢を問わず受けられます。': ('No. Anyone can join, at any age, from kids to players aiming to become athletes.', '没有。从儿童到立志成为运动员的选手，不限年龄均可参加。'),
 'キッズ〜アスリート・年齢不問': ('Kids to athletes, any age', '儿童到运动员・不限年龄'),
 'はい。初心者から上級者まで、一人ひとりのレベルと課題に合わせて指導します。': ('Yes. We coach beginners through advanced players, matched to each player\'s level and goals.', '可以。从初学者到高水平球员，我们都会根据每个人的水平和课题进行指导。'),
 'ユニフォーム': ('Kit', '队服'),
 '予約': ('Order', '预订'),
 'よくある質問': ('Frequently asked questions', '常见问题'),
 UPDATED_JP: ('Last updated: Nov 18, 2026', '信息更新日期：2026年11月18日'),
 'VX SPORTS ACADEMYとは': ('About VX SPORTS ACADEMY', '关于VX SPORTS ACADEMY'),
 'VX SPORTS ACADEMYは、シノヅカイッペイが代表を務める、サッカーの技術と、年齢を問わずキッズからアスリートを目指す選手までの運動能力を伸ばすスポーツアカデミーです。':
   ('VX SPORTS ACADEMY is a sports academy led by Ippei Shinozuka that develops football skill and athletic ability for every age, from kids to aspiring athletes.', 'VX SPORTS ACADEMY是由Ippey Shinozuka担任代表、致力于提升足球技术，以及不限年龄、从儿童到立志成为运动员的选手的运动能力的体育学院。'),
 '元プロ・専門コーチ陣が、身体能力とサッカーの技術を一人ひとりに合わせて指導します。':
   ('Former pros and specialist coaches tailor athletic and football training to each player.', '由前职业球员和专业教练根据每位学员的情况指导身体素质与足球技术。'),
 'VX PERSONAL｜サッカーのパーソナル指導（受付中）': ('VX PERSONAL | Personal football coaching (open)', 'VX PERSONAL｜足球私教指导（接受报名中）'),
 'VX GYM｜キッズからアスリートまでのジム（東京・西麻布／2027年1月オープン予定）': ('VX GYM | Gym for kids to athletes, any age (Nishi-Azabu, Tokyo / opening Jan 2027)', 'VX GYM｜儿童到运动员健身房（不限年龄）（东京・西麻布／预计2027年1月开业）'),
 'VX SOCCER｜U-12・U-9の新しいサッカーチーム（メンバー募集中）': ('VX SOCCER | New U-12・U-9 football team (recruiting)', 'VX SOCCER｜全新U-12・U-9足球队（招募中）'),
 'VX APPAREL｜普段着にもなるアパレル（予約受付中）': ('VX APPAREL | Everyday apparel (pre-orders open)', 'VX APPAREL｜日常服饰（接受预订中）'),
 # index
 'VX SPORTS ACADEMYとは何ですか？': ('What is VX SPORTS ACADEMY?', 'VX SPORTS ACADEMY是什么？'),
 'サッカーの技術と、年齢を問わずキッズからアスリートを目指す選手までの運動能力を伸ばすスポーツアカデミーです。サッカーのパーソナル指導「VX PERSONAL」、キッズからアスリートまでのジム「VX GYM」、サッカーチーム「VX SOCCER」、アパレルブランド「VX APPAREL」の4つを運営しています。':
   ('A sports academy that develops football skill and athletic ability for every age, from kids to aspiring athletes. We run four services: VX PERSONAL (personal football coaching), VX GYM (gym for kids to athletes, any age), VX SOCCER (football team) and VX APPAREL (apparel brand).', '一所提升足球技术及不限年龄、从儿童到立志成为运动员的选手的运动能力的体育学院，运营足球私教「VX PERSONAL」、儿童到运动员健身房（不限年龄）「VX GYM」、足球队「VX SOCCER」和服饰品牌「VX APPAREL」四项服务。'),
 'どこにありますか？': ('Where are you located?', '在哪里？'),
 'VX GYMは東京・西麻布に2027年1月オープン予定です。VX PERSONALは東京・神奈川・千葉・埼玉で対応しています。': ('VX GYM opens in Nishi-Azabu, Tokyo in January 2027. VX PERSONAL is available in Tokyo, Kanagawa, Chiba and Saitama.', 'VX GYM预计于2027年1月在东京西麻布开业。VX PERSONAL可在东京、神奈川、千叶、埼玉提供服务。'),
 '今申し込めるサービスは？': ('What can I sign up for now?', '现在可以报名哪些服务？'),
 'VX PERSONAL（初回体験 ¥5,500・税込）は受付中です。VX GYMは先行予約、VX SOCCERはU-12・U-9のメンバーを募集中、VX APPARELは予約注文を受け付けています。': ('VX PERSONAL is open (trial session ¥5,500 incl. tax). VX GYM is taking early registrations, VX SOCCER is recruiting U-12 and U-9 players, and VX APPAREL is taking pre-orders.', 'VX PERSONAL正在接受报名（首次体验 ¥5,500，含税）。VX GYM接受预约登记，VX SOCCER正在招募U-12・U-9成员，VX APPAREL接受预订。'),
 '問い合わせ方法は？': ('How do I contact you?', '如何咨询？'),
 'LINE公式アカウントから、メッセージでお問い合わせください。最新情報はInstagram（@vx_sports_academy）でもお知らせしています。': ('Message us on our official LINE account. News is also posted on Instagram (@vx_sports_academy).', '请通过LINE官方账号发送消息咨询。最新信息也会在Instagram（@vx_sports_academy）发布。'),
 # personal
 'VX PERSONALでは何を教えてもらえますか？': ('What does VX PERSONAL teach?', 'VX PERSONAL教什么？'),
 '身体能力（スピード・アジリティ・パワー・体幹）と、止める・蹴るの基礎から上級スキルまでのサッカーの技術を、マンツーマンで指導します。': ('One-on-one coaching in athleticism (speed, agility, power, core) and football skill, from first touch and passing basics to advanced skills.', '一对一指导身体素质（速度、敏捷、力量、核心）以及从停球、踢球基础到高级技巧的足球技术。'),
 '料金はいくらですか？': ('How much does it cost?', '费用是多少？'),
 '初回体験 ¥5,500、本レッスン ¥16,500／回（最低4回から）、初月の1ヶ月契約（週1回）¥66,000、2ヶ月目以降の3ヶ月契約 ¥198,000です。すべて税込です。': ('Trial ¥5,500; regular lesson ¥16,500 each (minimum 4); first month (weekly) ¥66,000; from month two, 3-month plan ¥198,000. All prices include tax.', '首次体验 ¥5,500；正式课程每次 ¥16,500（至少4次）；首月1个月合约（每周1次）¥66,000；第二个月起3个月合约 ¥198,000。均含税。'),
 '初心者でも受けられますか？': ('Can beginners join?', '初学者可以参加吗？'),
 'はい。初心者から上級者まで、一人ひとりのレベルと課題に合わせて指導します。': ('Yes. We coach beginners through advanced players, matched to each player\'s level and goals.', '可以。从初学者到高水平球员，我们都会根据每个人的水平和课题进行指导。'),
 'どのエリアで受けられますか？': ('Which areas do you cover?', '可以在哪些地区上课？'),
 '東京・神奈川・千葉・埼玉で対応しています。ご希望のエリアはLINEでお知らせください。': ('Tokyo, Kanagawa, Chiba and Saitama. Tell us your preferred area on LINE.', '可在东京、神奈川、千叶、埼玉上课。请通过LINE告知您希望的地区。'),
 'どのくらいの頻度で通えばいいですか？': ('How often should I train?', '多久上一次课比较好？'),
 '週1回の継続をおすすめしています。続けて取り組むことで、確実な成長を目指します。': ('We recommend once a week, consistently. Steady training leads to real progress.', '建议每周1次并坚持下去，持续训练才能稳步成长。'),
 '申し込み方法は？': ('How do I sign up?', '如何报名？'),
 'LINE公式アカウントから初回体験をお申し込みください。': ('Book a trial session through our official LINE account.', '请通过LINE官方账号报名首次体验。'),
 # gym
 'VX GYMはいつ、どこにオープンしますか？': ('When and where does VX GYM open?', 'VX GYM何时在哪里开业？'),
 '東京・西麻布に2027年1月オープン予定です。現在、LINEで先行予約を受け付けています。': ('In Nishi-Azabu, Tokyo, planned for January 2027. Early registration is open on LINE.', '预计2027年1月在东京西麻布开业。目前正在通过LINE接受预约登记。'),
 'どんな人が対象ですか？': ('Who is it for?', '面向哪些人？'),
 'サッカー、野球、バスケ、陸上など競技を問わず、運動能力を伸ばしたいキッズから、アスリートを目指す選手まで、年齢を問わず対象です。クラスは年代別のグループで、定員8人・指導者1人です。': ('Anyone, at any age, from kids to players aiming to become athletes, whatever the sport: football, baseball, basketball, track and more. Classes are grouped by age, up to 8 per coach.', '不限年龄，面向从儿童到立志成为运动员的选手，不限项目：足球、棒球、篮球、田径等。按年龄分组上课，每班最多8人、1名教练。'),
 '何を計測しますか？': ('What do you measure?', '测量哪些项目？'),
 'パワー出力（W）、ジャンプ（cm）、スピード（秒）を毎回計測し、入会時からの伸びをグラフで記録します。': ('Power output (W), jump (cm) and speed (s), every session, with progress since joining recorded on a graph.', '每次测量爆发力（W）、跳跃（cm）、速度（秒），并用图表记录入会以来的成长。'),
 '月額（税込）で、週1回（月4回）¥17,800、週2回（月8回）¥28,000です。月1回のマンツーマンと測定結果のフィードバックがつく「エリート」は＋¥15,000で追加できます。': ('Monthly, incl. tax: once a week (4/month) ¥17,800; twice a week (8/month) ¥28,000. Add "Elite" (a monthly one-on-one plus feedback on results) for +¥15,000.', '月费（含税）：每周1次（每月4次）¥17,800；每周2次（每月8次）¥28,000。可追加「精英」（每月1次一对一＋测量结果反馈）+¥15,000。'),
 '先行予約に料金はかかりますか？': ('Does early registration cost anything?', '预约登记需要付费吗？'),
 'かかりません。先行予約は、オープン日・料金・体験会のご案内を優先してお送りするための登録です。': ('No. It simply puts you first in line for news on the opening date, prices and trial sessions.', '不需要。预约登记只是为了优先向您发送开业日期、费用和体验会的信息。'),
 # soccer
 'VX SOCCERはどんなチームですか？': ('What kind of team is VX SOCCER?', 'VX SOCCER是什么样的球队？'),
 '身体能力を本気で伸ばすトレーニングと、トップレベルのサッカー教育を両立する新しいチームです。全員でボールをつなぐパスサッカーを目指します。': ('A new team that combines serious athletic training with top-level football education, playing a passing game where everyone keeps the ball moving.', '一支兼顾认真提升身体素质的训练与顶级足球教育的新球队，追求全员传控的传球足球。'),
 '募集しているカテゴリーは？': ('Which age groups are you recruiting?', '招募哪些年龄组？'),
 'U-12とU-9です。': ('U-12 and U-9.', 'U-12和U-9。'),
 '練習日と会場は？': ('When and where is training?', '训练时间和场地是？'),
 '決まり次第お知らせします。最新情報はInstagram（@vx_sports_academy）でお知らせします。': ('We\'ll announce them once decided. Follow Instagram (@vx_sports_academy) for updates.', '确定后会通知。最新信息将在Instagram（@vx_sports_academy）发布。'),
 '入団の問い合わせ方法は？': ('How do I ask about joining?', '如何咨询入队？'),
 'LINE公式アカウント、またはInstagramのDMからお問い合わせください。': ('Message us on our official LINE account or by Instagram DM.', '请通过LINE官方账号或Instagram私信咨询。'),
 'ユニフォームはありますか？': ('Is there a team kit?', '有队服吗？'),
 'HOME（ブラック）・AWAY（ホワイト）・THIRD（グレー）のオフィシャルユニフォームがあります。シャツ・パンツ・ソックスのセットで、背中に名前と背番号を入れられます。': ('Yes: official HOME (black), AWAY (white) and THIRD (grey) kits. Each is a shirt, shorts and socks set, with name and number on the back.', '有。官方队服分为HOME（黑）、AWAY（白）、THIRD（灰），包括球衣、球裤和球袜，背后可印名字和号码。'),
 # apparel
 '何を買えますか？': ('What can I buy?', '可以买什么？'),
 'Tシャツ ¥7,700、ショーツ ¥7,700、ソックス ¥2,200、3点セット ¥15,400です（すべて税込）。3点セットは単品合計より¥2,200お得です。': ('T-shirt ¥7,700, shorts ¥7,700, socks ¥2,200, or the 3-piece set for ¥15,400 (all incl. tax), ¥2,200 less than buying separately.', 'T恤 ¥7,700、短裤 ¥7,700、袜子 ¥2,200、三件套 ¥15,400（均含税），比单买合计便宜¥2,200。'),
 'カラーとサイズは？': ('Which colours and sizes?', '有哪些颜色和尺码？'),
 'Ink Black・Sage Green・Powder Blue・Petal Pink・Mist Lavender・Cloud Whiteのユニセックス6色、サイズはS・M・L・XLです。ソックスも同じ6色です。': ('Six unisex colours (Ink Black, Sage Green, Powder Blue, Petal Pink, Mist Lavender, Cloud White) in S, M, L and XL. Socks come in the same six colours.', '共6色（Ink Black、Sage Green、Powder Blue、Petal Pink、Mist Lavender、Cloud White），男女同款，尺码S、M、L、XL。袜子也有同样6色。'),
 'どんな素材・機能ですか？': ('What are the materials and features?', '面料和功能如何？'),
 '軽量・速乾で、4方向ストレッチと撥水性、動きやすいスリット、夜でも目立つリフレクティブがついています。トレーニングにも普段着にも使えます。': ('Lightweight and quick-drying, with four-way stretch, water repellency, side slits for movement and reflective details for night. Made for training and everyday wear.', '轻量速干，四向弹力、防泼水，带便于活动的开衩和夜间醒目的反光设计，训练和日常都适用。'),
 'いつ届きますか？': ('When will it arrive?', '什么时候送达？'),
 '予約注文のため、予約締切後の生産となります。お届け時期とお支払い方法はLINEでご案内します。': ('It\'s made to order after pre-orders close. We\'ll confirm delivery timing and payment on LINE.', '因是预订商品，将在预订截止后生产。送达时间和付款方式将通过LINE告知。'),
}

def faq_html(items):
    qa = '\n'.join(f'        <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in items)
    return f'''  <section class="band on-ink faq" id="faq" style="border-top:1px solid var(--line-dark)">
    <div class="wrap stack">
      <div class="sec-head">
        <p class="en sub">FAQ</p>
        <h2 class="catch">よくある質問</h2>
      </div>
      <div class="faq-list">
{qa}
      </div>
      <p class="faq-upd">{UPDATED_JP}</p>
    </div>
  </section>

'''

FOUNDER = '''  <section class="band on-ink founder" id="founder" style="border-top:1px solid var(--line-dark)">
    <div class="wrap stack">
      <div class="sec-head">
        <p class="en sub">Founder</p>
        <h2 class="catch">代表 シノヅカイッペイ</h2>
      </div>
      <figure class="f-photo"><img src="assets/founder.jpg" alt="横浜F・マリノス在籍時にプレーするシノヅカイッペイ" loading="lazy" width="660" height="440"></figure>
      <div class="f-name">
        <p class="f-ja">シノヅカイッペイ</p>
        <p class="f-en">IPPEY SHINOZUKA</p>
        <p class="f-role">代表・元プロサッカー選手（MF）</p>
      </div>
      <div class="f-stats" role="group" aria-label="Jリーグ通算成績">
        <div><b>95</b><span>試合</span></div>
        <div><b>11</b><span>ゴール</span></div>
        <div><b>9</b><span>アシスト</span></div>
      </div>
      <p class="f-src">Jリーグ通算（J1・J2リーグ戦／2017〜2022年）出典：Football LAB</p>
      <ol class="f-career">
        <li><span class="y">2012–13</span><span class="c">U-18ロシア代表</span></li>
        <li><span class="y">2012–17</span><span class="c">スパルタク・モスクワ（ロシア）</span></li>
        <li><span class="y">2017–19</span><span class="c">横浜F・マリノス（J1）</span></li>
        <li><span class="y">2019–20</span><span class="c">大宮アルディージャ（J2）</span></li>
        <li><span class="y">2021</span><span class="c">柏レイソル（J1）</span></li>
        <li><span class="y">2022</span><span class="c">アルビレックス新潟（J2）</span></li>
        <li><span class="y">NOW</span><span class="c">VX SPORTS ACADEMY 代表</span></li>
      </ol>
      <p class="f-text">16歳でロシアへ渡り、スパルタク・モスクワでプロのキャリアをスタート。U-18ロシア代表を経て、Jリーグでは4クラブでプレーしました。</p>
      <p class="f-msg">トップレベルで戦ってきた経験を、次の世代の選手へ。</p>
    </div>
  </section>

'''

ABOUT = '''  <section class="band on-ink about" id="about" style="border-top:1px solid var(--line-dark)">
    <div class="wrap stack">
      <div class="sec-head">
        <p class="en sub">About</p>
        <h2 class="catch">VX SPORTS ACADEMYとは</h2>
      </div>
      <p class="about-lead">VX SPORTS ACADEMYは、シノヅカイッペイが代表を務める、サッカーの技術と、年齢を問わずキッズからアスリートを目指す選手までの運動能力を伸ばすスポーツアカデミーです。</p>
      <p class="about-lead">元プロ・専門コーチ陣が、身体能力とサッカーの技術を一人ひとりに合わせて指導します。</p>
      <ul class="about-list">
        <li><a href="personal.html">VX PERSONAL｜サッカーのパーソナル指導（受付中）</a></li>
        <li><a href="gym.html">VX GYM｜キッズからアスリートまでのジム（東京・西麻布／2027年1月オープン予定）</a></li>
        <li><a href="soccer.html">VX SOCCER｜U-12・U-9の新しいサッカーチーム（メンバー募集中）</a></li>
        <li><a href="apparel.html">VX APPAREL｜普段着にもなるアパレル（予約受付中）</a></li>
      </ul>
    </div>
  </section>

'''

H1_SWAPS = {
 'gym': ('<p class="gym-catch">お子さんの成長が、<br><em>数字</em>で見える。</p>', '<h1 class="gym-catch">お子さんの成長が、<br><em>数字</em>で見える。</h1>'),
 'soccer': ('<p class="catch" style="font-weight:900;font-size:27.1px;line-height:1.45">選手一人ひとりが、<br>生き生きとサッカーできるチームを。</p>', '<h1 class="catch big">選手一人ひとりが、<br>生き生きとサッカーできるチームを。</h1>'),
 'apparel': ('<p class="catch">動ける服を、<br>毎日の服に。</p>', '<h1 class="catch">動ける服を、<br>毎日の服に。</h1>'),
}

esc = lambda s: s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')

for key, p in PAGES.items():
    f = os.path.join(ROOT, key + '.html')
    s = open(f, encoding='utf-8').read()
    url = BASE + p['path']
    # 古いSEOブロックを消してから入れ直す（何度実行しても同じ結果）
    s = re.sub(r'\n<!-- SEO -->.*?<!-- /SEO -->', '', s, flags=re.S)
    s = re.sub(r'  <section class="band on-ink faq" id="faq".*?</section>\n\n', '', s, flags=re.S)
    s = re.sub(r'  <section class="band on-ink about" id="about".*?</section>\n\n', '', s, flags=re.S)
    s = re.sub(r'  <section class="band on-ink founder" id="founder".*?</section>\n\n', '', s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', f'<title>{p["title"]}</title>', s, count=1)
    s = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{esc(p["desc"])}">', s, count=1)
    s = re.sub(r'<meta property="og:title"[^>]*>', f'<meta property="og:title" content="{esc(p["title"])}">', s, count=1)
    s = re.sub(r'<meta property="og:description"[^>]*>', f'<meta property="og:description" content="{esc(p["og"])}">', s, count=1)
    s = re.sub(r'<meta property="og:image"[^>]*>', f'<meta property="og:image" content="{BASE}assets/og-{key}.jpg">', s, count=1)

    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'VX SPORTS ACADEMY', 'item': BASE}]
    if key != 'index':
        crumbs.append({'@type': 'ListItem', 'position': 2, 'name': p['name'], 'item': url})
    graph = [ORG,
             {'@type': 'WebSite', '@id': BASE + '#website', 'url': BASE, 'name': 'VX SPORTS ACADEMY', 'inLanguage': 'ja', 'publisher': {'@id': BASE + '#org'}},
             {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': p['title'], 'description': p['desc'], 'inLanguage': 'ja',
              'isPartOf': {'@id': BASE + '#website'}, 'about': {'@id': BASE + '#org'}, 'dateModified': UPDATED_ISO,
              'primaryImageOfPage': BASE + f'assets/og-{key}.jpg'},
             {'@type': 'BreadcrumbList', 'itemListElement': crumbs},
             {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in p['faq']]}]
    graph += p.get('extra', lambda: [])()
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))
    block = f'''
<!-- SEO -->
<meta name="google-site-verification" content="3zVP4AfZtZoqzpeqEUuoPGedQ1RHEeVxRpytjptbPYk">
<meta name="msvalidate.01" content="FFAA17851A2F6A55200AE1E326148E97">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ja" href="{url}">
<link rel="alternate" hreflang="en" href="{BASE}en/{p['path']}">
<link rel="alternate" hreflang="zh-Hans" href="{BASE}zh/{p['path']}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="VX SPORTS ACADEMY">
<meta property="og:locale" content="ja_JP">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}assets/og-{key}.jpg">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<script type="application/ld+json">{ld}</script>
<!-- /SEO -->'''
    s = s.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="website">' + block, 1)

    marker = '  <section class="band on-ink" id="contact"'
    assert marker in s, key
    s = s.replace(marker, (FOUNDER + ABOUT if key == 'index' else '') + faq_html(p['faq']) + marker, 1)
    if key in H1_SWAPS:
        a, b = H1_SWAPS[key]
        if a in s: s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s)
    print('ok', key, len(ld))

# 翻訳を i18n.js の辞書に足す
j = os.path.join(ROOT, 'assets/i18n.js')
s = open(j, encoding='utf-8').read()
s = re.sub(r'\n  /\* SEO-TR \*/.*?/\* /SEO-TR \*/', '', s, flags=re.S)
add = json.dumps({k: {'en': v[0], 'zh': v[1]} for k, v in TR.items()}, ensure_ascii=False)
s = s.replace('\n  var nodes=[];', f'\n  /* SEO-TR */ Object.assign(D, {add}); /* /SEO-TR */\n  var nodes=[];', 1)
open(j, 'w', encoding='utf-8').write(s)

# 翻訳もれチェック
missing = [t for p in PAGES.values() for qa in p['faq'] for t in qa if t not in TR]
print('missing translations:', missing)
