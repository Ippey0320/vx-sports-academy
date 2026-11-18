#!/usr/bin/env bash
# サイトを組み立て直す（日本語ページの仕上げ → 英語・中国語ページの生成 → キャッシュ対策）
#   bash tools/build.sh
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/seo.py .          # タイトル・説明文・構造化データ・FAQ・代表/About
python3 tools/optimize.py .     # 画像のWebP化・表示速度・アクセシビリティ
python3 - <<'EOF'
# CSS/JS の読み込みに新しい番号をつけて、古い表示が残らないようにする
import glob, re, time
v = str(int(time.time()))
for f in glob.glob('*.html'):
    t = open(f, encoding='utf-8').read()
    t = re.sub(r'(site\.css|i18n\.js)\?v=\d+', lambda m: m.group(1) + '?v=' + v, t)
    open(f, 'w', encoding='utf-8').write(t)
EOF
node tools/build-langs.js       # /en/ と /zh/ のページ
echo "build ok"
