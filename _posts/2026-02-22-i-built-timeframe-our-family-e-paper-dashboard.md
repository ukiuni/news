---
layout: post
title: "I built Timeframe, our family e-paper dashboard - 家族用eペーパーダッシュボード「Timeframe」を作った"
date: 2026-02-22T20:42:16.800Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hawksley.org/2026/02/17/timeframe.html"
source_title: "How I built Timeframe, our family e-paper dashboard - Joel Hawksley"
source_id: 47113728
excerpt: "リアルタイム表示のe‑inkとHome Assistantで家族情報を一目で確認"
image: "https://hawksley.org/img/posts/2026-02-17-timeframe/nook-wide.jpg"
---

# I built Timeframe, our family e-paper dashboard - 家族用eペーパーダッシュボード「Timeframe」を作った
朝の情報確認が変わる。紙のように落ち着いて、必要な情報だけを「一目で」伝える家庭用eペーパーダッシュボード

## 要約
著者はカレンダー・天気・スマート家電の状態を表示する家族用ダッシュボード「Timeframe」を、試作→改良→リアルタイム化を経て完成させた。高解像度e‑ink（Boox Mira Pro）とHome Assistant統合で「視認性」と「信頼性」を両立している。

## この記事を読むべき理由
日本でも「画面が多すぎる」「夜に光る端末は避けたい」と考える家庭は多いはず。実際の作例と設計判断（e‑ink選定、バックエンド構成、Home Assistant活用）は、スマートホームを現実的に改善するヒントになります。

## 詳細解説
- 初期プロトタイプ：鏡型ディスプレイや改造Kindleでカレンダーと天気を表示。Kindleは低消費で昼間の視認性も良かったが、更新間隔やメンテが課題に。表示はRailsアプリでPNG生成（IMGKit）して配信していた。
- Visionect導入：専用e‑paper端末は長時間稼働・安定だが価格やAPIの制約、ローカルバックエンドのライセンス料がネック。Raspberry Pi上のRailsから5分毎にPNGを送る方式で安定稼働。
- 大きな転機（Mira Pro）：家の再設計を機にBooxの25.3" Mira Proを採用。HDMI接続で高解像度かつリアルタイム更新が可能になり、画面に表示できる情報量と即時性が飛躍的に向上。
- バックエンド再設計：リアルタイム要件により画像生成中心の方法は限界。Home Assistant（HA）への依存を高め、既存カレンダー／天気／Sonos連携をHAに統合。結果、Rails側のデータ取得ロジックを大幅削減し、DB/Redisを廃止。Rufus Scheduler＋ファイルキャッシュで軽量化。
- 表示ポリシー：常に全部を出すのではなく「異常があるときだけ主張する」単一のステータス指標をトップに置く設計。これにより家の状態確認が一瞬で済む。
- 実運用の知見：テンプレートセンサーでルールを簡単に追加でき、コード変更不要で通知を表示できる（例：夜8時以降で食洗機の消費電力が低いならリマインド）。

例：Home Assistantのテンプレートセンサー（要旨）
```yaml
# yaml
sensor:
  - platform: template
    sensors:
      timeframe_dishwasher_reminder:
        value_template: >-
          {% if states('sensor.kitchen_dishwasher_power') | float < 2 and now().hour > 19 %}
            Run the dishwasher!
          {% else %}
            ok
          {% endif %}
        friendly_name: "Dishwasher reminder"
```

## 実践ポイント
- まずは小さく：6–13"クラスの低コストe‑paperや中古Kindleで検証。昼間の視認性と更新頻度を確認する。
- 表示ルールをシンプルに：「正常時は空白／異常時に表示」を基本にするとノイズが減る。
- Home Assistantを有効活用：既存インテグレーションで多くの外部APIを置き換えられ、運用負荷が劇的に下がる。
- ハード選定は妥協点：高解像度リアルタイム表示が必要か、低消費・長期間表示でよいかで機器が変わる（Mira Proは高機能だが高価）。
- 配布を考えるなら：デバイス費用、ローカルバックエンドのライセンス、保守性（組込み機器化）の3点を早めに評価する。

家の「見える化」を静かで心地よく実現するための実戦的な手順と設計論が詰まった事例です。自宅でまず試すなら、Home Assistant＋小型e‑inkでプロトタイプを作るのが最短ルート。
