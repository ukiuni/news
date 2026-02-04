---
layout: post
title: "Fitting Some Files Through A Stdout-Shaped Hole - stdout 形の穴を通してファイルを渡す"
date: 2026-02-04T03:01:33.387Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rtpg.co/2026/02/03/fitting-some-files-through-a-stdout-shaped-hole/"
source_title: "Fitting Some Files Through A Stdout-Shaped Hole"
source_id: 727592838
excerpt: "stdout経由で100台のCSVを一括回収・ログから復元する即効ワザ"
---

# Fitting Some Files Through A Stdout-Shaped Hole - stdout 形の穴を通してファイルを渡す
100台のサーバからCSVだけ回収したいときに――stdout経由で“ごまかす”現場テクニック

## 要約
コマンドが生成するファイルを直接回収する手段がないとき、標準出力にファイルを埋め込んでログ経由で回収・復元する簡易ワークアラウンドを紹介します。

## この記事を読むべき理由
運用ツールが「コマンド実行とログ保存」しかできない環境は日本の企業でもよくあり、レビュープロセスやリリース手続きを待てない時に即効性のある実践策が役立ちます。

## 詳細解説
問題点
- コマンド(my_command)は期待通りCSVを生成するが、生成先は各ノードのディスク。
- 管理ツールはコマンド実行のstdout/stderrだけを中央に集める。作成ファイルの収集機能はない。

考えた解決法
- 各ファイルをcatしてstdoutに出力し、明確な区切り文字（マーカー）を挿入する。
- 管理ツールが保存したログを後でパースして、ファイルを復元する。

メリット・注意点
- すぐに実行可能でレビューやリリースを待たずに済む。
- ログサイズ増加、機密情報漏洩、バイナリデータや改行を含む場合の破損に注意。
- 長期的にはS3やアーティファクト保存など正規の収集フローに直すべき。

実装例（実行側の一行コマンド）
```bash
# bash
internal-box-mgmt-tool command -f some-filter \
  "my_command; echo '===CSV_START:widgets.csv==='; cat widgets.csv; echo '===CSV_END==='; \
   echo '===CSV_START:thingies.csv==='; cat thingies.csv; echo '===CSV_END==='; \
   echo '===CSV_START:stuff.csv==='; cat stuff.csv; echo '===CSV_END==='" \
  -o logs/
```

復元スクリプト例（Python）
```python
# python
from pathlib import Path
import re

LOG_DIR = Path("logs")
OUT_DIR = Path("results")
OUT_DIR.mkdir(exist_ok=True)

marker_re = re.compile(r"===CSV_START:(.*?)===\n(.*?)\n===CSV_END===", re.S)

for log in LOG_DIR.iterdir():
    text = log.read_text()
    box_dir = OUT_DIR / log.stem
    box_dir.mkdir(parents=True, exist_ok=True)
    for name, content in marker_re.findall(text):
        (box_dir / name).write_text(content)
```

## 実践ポイント
- マーカーはユニークで衝突しない文字列にする（タイムスタンプやUUIDを付与）。
- バイナリや特殊文字がある場合はbase64でエンコードして復元側でデコードする。
- ログ増大が問題なら圧縮（gzip）や一時的なS3アップロードを検討。
- セキュリティ監査や長期運用が必要な場合は、この方法は暫定策とし、正式な収集フローを整備する。
