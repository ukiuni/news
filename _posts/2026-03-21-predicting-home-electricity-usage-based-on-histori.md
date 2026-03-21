---
layout: post
title: "Predicting home electricity usage based on historical patterns in Home Assistant - Home Assistantで過去の利用パターンに基づく家庭の電力消費予測"
date: 2026-03-21T19:29:42.428Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.cyplo.dev/posts/2026/03/load-prediction-in-home-assistant/"
source_title: "Predicting home electricity usage based on historical patterns in Home Assistant"
source_id: 847469895
excerpt: "Home Assistantの履歴で30分単位の電力消費を予測し、蓄電・料金最適化に活かす方法を解説"
---

# Predicting home electricity usage based on historical patterns in Home Assistant - Home Assistantで過去の利用パターンに基づく家庭の電力消費予測

家の電気を「先読み」して、半時間単位で賢く充電・運用する方法 — Home Assistantと記録DBを使った実践的予測手法

## 要約
Home Assistantの履歴データを使い、曜日・時間帯ごとの過去の半時間スロットを重み付け平均して将来の消費（kWh/30分）を予測する手法を紹介。直近データは高精度に、7〜56日前は統計データを活用して安定化させる。

## この記事を読むべき理由
変動料金（30分刻み）や家庭用蓄電池・給湯の最適化が普及する日本では、半時間解像度の負荷予測が電気代削減と運用効率向上に直結します。Home Assistantユーザーなら既存データだけで実装可能です。

## 詳細解説
- 目的：30分スロット（例 09:00–09:30）の将来消費を予測し、蓄電池の充放電や電気温水器のタイミングを決める材料にする。  
- データ源：Home AssistantのDB内の「states」テーブル（高頻度、生データ）と「statistics」テーブル（長期、1時間粒度）。statesは直近7日を高精度で使い、7〜56日はstatisticsを半分に分けて擬似的に半時間化して利用する。  
- 半時間積算方法：状態値を時間で台形積分（trapezoidal integration）してWhを算出し、30分ごとのkWhに変換する（短い欠損は無視するなどのフィルタあり）。  
- 曜日・時刻依存性：同じ曜日・同じスロットの過去データを集め、日付降順で重み付け（上位6件に対して 0.40, 0.25, 0.15, 0.10, 0.06, 0.04）して曜日平均を作る。データ不足時は単純平均やデフォルト値で補完。  
- 直近の「昨日」「一昨日」をブレンド：曜日平均に対して昨日・一昨日の同スロット実測を混ぜる（基本ブレンド係数は $0.65$（曜日平均）:$0.25$（昨日）:$0.10$（2日前））。数式で表すと  
  $$
  \text{pred} = 0.65\cdot D + 0.25\cdot Y_{1} + 0.10\cdot Y_{2}
  $$  
  （Yが欠ける場合は係数を正規化）  
- 出力：曜日と時刻キー（例 "0_09:00" = 日曜 09:00-09:30）で336エントリのルックアップ表を返し、各スロットの予測kWhを得られる。  
- 実装上の注意：センサ名や閾値（例 0.01〜5.0 kWh/30分など）、履歴範囲、欠損フィルタ、重みは家庭ごとに調整が必要。週ごとのパターン変化や突発負荷により過少予測になることもあるため、継続的なチューニングが重要。

## 実践ポイント
- まずはHome AssistantのDBを参照できるようにして、対象センサ（例: sensor.growatt_invpowertolocalload）を確認する。  
- 直近7日分はstatesテーブルから台形積分で半時間消費を出し、7〜56日はstatisticsを半分に展開して補う。  
- ブレンド係数（$0.65/0.25/0.10$）と曜日内の降順重み（0.40→0.04）を初期値として、2〜8週で精度を確認し調整する。  
- 予測を蓄電池運用ルールや料金最適化（30分刻みの電価反映）に組み込むと即効性がある。  
- 可視化とログを用意して外れ値や季節変化を検出し、重みや閾値を定期的に見直す。

元記事の考え方はシンプルで応用しやすく、日本の家庭でも半時間料金・蓄電池運用の最適化に直接役立ちます。必要なら、あなたのセンサ名に合わせたSQLの調整ポイントやパラメータ推奨を短く提示します。どの情報が見たいですか？
