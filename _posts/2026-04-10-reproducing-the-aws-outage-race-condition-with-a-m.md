---
layout: post
title: "Reproducing the AWS Outage Race Condition with a Model Checker - モデルチェッカーで再現するAWS障害のレースコンディション"
date: 2026-04-10T14:56:27.669Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://wyounas.github.io/aws/concurrency/2025/10/30/reproducing-the-aws-outage-race-condition-with-model-checker/"
source_title: "Reproducing the AWS Outage Race Condition with a Model Checker | Waqas Younas' blog"
source_id: 365199244
excerpt: "SpinでAWSのDNSレースをモデル化し、アクティブプラン削除の反例を発見"
---

# Reproducing the AWS Outage Race Condition with a Model Checker - モデルチェッカーで再現するAWS障害のレースコンディション
なぜ「新しいはずのDNS設定が消えた」のか？Spinで暴いた並行実行の致命的な抜け穴

## 要約
AWSのポストモーテムで報告された「レースコンディション」に着目し、Spin（Promela）で簡略モデルを作って同じような障害シーケンスを再現。モデルチェッカーが並行処理の全インタリーブ（実行順序）を探索し、実際に「アクティブなプランが削除される」反例を見つける手順を示す。

## この記事を読むべき理由
クラウド依存が深い日本の企業にとって、見過ごしやすい並行性バグは稼働停止に直結する。実際の障害報告を元に形式手法で再現した例は、SREや開発者が並行処理の設計・検証を理解する上で実務的価値が高い。

## 詳細解説
- 問題の構成要素：DNS Planner（プラン生成）、DNS Enactor（適用＆クリーンアップ）、Route 53。複数のEnactorが独立に実行され、互いにプランを取り合う。
- バグの本質：Enactorが「適用→クリーンアップ」を行う際、遅れて動く別のEnactorが古い（だがまだ有効な）プランを適用してしまい、その後先に進んだEnactorのクリーンアップ処理がそのプランを削除してしまう。結果、アクティブなプランが消え、DNS不整合が発生する。
- モデル化手法：PromelaでPlannerと複数のEnactorをプロセスとして定義。チャンネルでプランを渡し、状態変数（current_plan, highest_plan_applied, dns_valid など）を操作してRoute 53の状態を模擬。Spinは全インタリーブを探索して不変条件（invariant）を検査する。
- 検証された不変条件の例（LTL）：アクティブなプランは決して削除されないべき、という条件を表現して検査し、反例（トレイル）を得ることで問題の再現に成功する。
- 修正方針：問題箇所を原子的に実行する（クリティカルセクション化）、あるいはクリーンアップの基準を変更して「最近適用された可能性のあるプラン」を安全に保つ。モデルでAtomic化すると反例が消える。

例：検査したLTL不変（簡潔化）
```promela
ltl never_delete_active { [] ( current_plan > 0 -> !plan_deleted[current_plan] ) }
```

## 実践ポイント
- 小さくてもモデルを作る：問題を単純化したPromelaモデルで再現できるか試すと、直感だけでは見えないインタリーブが可視化できる。  
- 明文化する不変条件を作る：システムの「絶対に守るべき状態」をLTLなどで書けると検査しやすい。  
- クリティカル処理は原子的に：適用→クリーンアップの境界で共有状態を壊す可能性がある場合は原子化やトランザクション化を検討。  
- 運用面の補強：マルチAZで独立動作するコンポーネントでは、より厳格なバージョン整合、リーダー選出、追加の監視アラート（「アクティブプランの削除」検知）を入れる。  
- 小さな実験をCIに：簡易モデルチェッカーや並行性テスト（フォースインタリーブ）をCIに組み込み、回帰検知を自動化する。

この記事の手法は、AWSの事例に限らず「複数ノードが非同期に設定を更新する」すべてのシステムに有効です。短時間で再現可能なモデル化は、設計ミスの早期発見に強力な武器になります。
