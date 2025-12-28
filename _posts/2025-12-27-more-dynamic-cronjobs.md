---
layout: post
title: "More Dynamic Cronjobs"
date: 2025-12-27T07:41:07.077Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://george.mand.is/2025/09/more-dynamic-cronjobs/"
source_title: "More Dynamic Cronjobs"
source_id: 46399576
excerpt: "crontabに簡単なシェル判定を入れて、月末火曜や祝日・天気でジョブ実行を柔軟に制御するワザ"
---

# 月末の火曜は飛ばすcron術 — 単行で「動的」なジョブを作る小技

## 要約
crontab に小さなシェル判定を仕込むだけで、曜日や祝日、天気やニュースなどの条件に応じて実行を制御できる。複雑なスケジュールを外部ツールなしで簡潔に実現する実用テクニックを紹介する。

## この記事を読むべき理由
オンコールや運用コストが重い日本の現場では、無駄なジョブ実行を減らすだけでログもコストも減る。systemd タイマーや外部オーケストレーションを導入する前に、既存の cron で手早く実現できる改善策は即効性が高い。

## 詳細解説
- 基本アイデア  
  cron 自体はスケジュール指定に限界があるが、crontab のコマンド側に POSIX の test（[ ... ] や test コマンド）を入れて条件判定すれば動的に振る舞わせられる。重要なのは「実行スケジュールは広めにして、実際の実行可否はコマンドで決める」こと。

- 代表例：月の最終火曜を除外する  
  macOS/BSD 系の date では「今から7日後の月と現在の月を比較」するやり方が簡潔。Linux 系では date のオプションが異なる点に注意。
  ```bash
  # macOS / BSD
  0 7 * * Tue [ "$(date -v+7d '+%m')" = "$(date '+%m')" ] && /path/to/your_command

  # Linux (GNU date)
  0 7 * * Tue [ "$(date -d '+7 days' '+%m')" = "$(date '+%m')" ] && /path/to/your_command
  ```
  7日後が同じ月なら「最終週ではない」と判断して実行する。

- 祝日除外／祝日のみ実行  
  祝日リストを定期的に取得してファイルに保存しておき、cron 側では grep で当日が含まれるか確認する。
  ```bash
  # 事前に HOLIDAYS.txt を更新するジョブを作る
  curl -s https://date.nager.at/api/v3/PublicHolidays/2025/US | jq -r '.[].date' > /path/to/HOLIDAYS.txt

  # 毎週火曜7時、祝日でなければ実行
  0 7 * * Tue ! grep -qx "$(date +%F)" /path/to/HOLIDAYS.txt && /path/to/your_command
  ```

- 外部データ（天気・ニュース）で実行制御  
  天気 API や RSS を叩いて条件に合うときだけコマンドを通す。API 呼び出しや jq の結果を grep で判定するだけで済む。
  ```bash
  # 例：晴れのときだけ毎時実行
  @hourly curl -s "https://api.weather.gov/gridpoints/TOP/32,81/forecast/hourly" \
    | jq -r '.properties.periods[0].shortForecast' | grep -qi clear && /path/to/your_command
  ```

- LLM による“実行可否判定”  
  RSS を LLM に与え「yes/no」で返させるワークフローで、ニュースが「大事件」なら実行、という運用も可能（ただしコストと安全性に注意）。

- 実行環境の注意点  
  cron は限られた環境変数で動く。絶対パス、明示的な PATH、ログ出力、タイムゾーン、rate limit や API エラー対策（タイムアウト・キャッシュ）を必ず考慮する。

## 実践ポイント
- テストは cron に登録する前にシェルで直接実行して確認する。date の挙動は macOS と Linux で異なる。  
- cron 用のラッパースクリプトを作る（ログ、リトライ、環境設定をまとめる）。cron からはそのスクリプトを実行するだけにする。  
- 外部 API を直接叩く場合はキャッシュを用意し、失敗時のフェイルセーフを設ける（エラーで実行しない等）。  
- 並列実行を避けるために flock や lockfile を使う。  
- より高度に管理したいなら systemd タイマーやジョブランナーに移行を検討するが、まずはこの「crontab + test」で素早く改善できる部分を洗い出す。

