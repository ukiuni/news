---
layout: post
title: "Building a lightning-fast highly-configurable Rust-based backtesting system - 超高速かつ高設定可能なRust製バックテスト基盤の作り方"
date: 2026-01-25T09:18:31.987Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nexustrade.io/blog/building-a-lightning-fast-highly-configurable-rust-based-backtesting-system-20260119"
source_title: "Building a lightning-fast highly-configurable Rust-based backtesting system"
source_id: 418101965
excerpt: "Rustで10年分の分足データを約30秒で回す、ノーコードの超高速バックテスト基盤"
image: "https://cdn-images-1.medium.com/max/1600/1*9gqZbKrcwh5trl6vUjk9Og.jpeg"
---

# Building a lightning-fast highly-configurable Rust-based backtesting system - 超高速かつ高設定可能なRust製バックテスト基盤の作り方
魅力的タイトル：ミリ秒で10年分を回す！コード不要で試せるRust製バックテストの正体

## 要約
JavaScriptで遅かった自前バックテストをRustで全面書き直し、単資産の長期テストが0.03秒、マルチ資産・分足での10年分が約30秒で回る高性能・ノーコードなバックテスト基盤を作った話。

## この記事を読むべき理由
日本の個人/企業アルゴリズム開発者にとって、ミニッツ〜分足レベルの大量データで高速に戦略検証ができることは、探索的アルゴ最適化やリアルタイム移行の壁を下げる。国内市場でも短期戦略や高頻度寄せの検証に有益。

## 詳細解説
- 性能改善の決定要因  
  - 言語選定：シングルスレッドでGCの影響があるNode.jsから、低レベル制御とゼロコスト抽象が得られるRustへ。  
  - アルゴリズム：移動平均などは全走査ではなくスライディングウィンドウで計算。非効率な抽象を排しホットパスを最適化した。  
  - 実測：著者の算出では$10\text{年}\times7\text{資産}\times252\text{営業日}\times390\text{分}=6{,}879{,}600$データ点を扱い、業界標準のLEANより高速。  

- 時間依存の指標（ta-rs-improved）  
  - 従来ライブラリは等間隔データ前提だったが、実データは欠損やサスペンドがあるため「期間（duration）ベース」で窓を定義するTAライブラリをフォークして実装。これにより不連続なティックでも正確な指標算出が可能に。

- 柔軟な戦略表現と監査性  
  - Strategy, Condition, Indicator, Actionといった宣言的な型を用意し、インジケータは「数値で表現できるあらゆるもの」（価格、財務指標、SNS言及数など）を想定。条件が真ならシグナルが発生し、シグナルはメタデータ付きで永続化され監査可能。

- バックテストと実運用の同一ロジック  
  - EventProcessorトレイト（インタフェース）でイベントループを共通化。バックテストは完全インメモリで同期実行、実運用はMongoDBやブローカーAPIを用いる非同期パスで実装しつつ、処理ロジックは同一に保つことで「検証で動いたものがそのまま本番で動く」保証を実現。

- 実装上の工夫  
  - ホットパスでのasync/serdeのオーバーヘッドを回避（専用ワーカースレッドで連続的なCPU実行）。注文はOrderQueueWorkerで非同期に発行し、外部APIとの整合はリコンシリエーションで処理。

## 実践ポイント
- Rustを検討する理由：CPUバウンドな大量バックテストや並列実行が必要なら候補に。  
- 指標は時間幅で定義する：欠損や市場停止を吸収するDurationベースの実装を採る。  
- 戦略は宣言的に作る：Indicator/Condition/Actionで表現するとノーコードUIや監査ログと親和性が高い。  
- ホットパスは同期で最適化し、I/Oは分離する：プロファイリング（例：flamegraphs）でボトルネックを特定。  
- バックテスト→ペーパ→本番を同一ロジックで：EventProcessorのような共通抽象を作り、インフラ層だけ差し替える。

日本市場へのヒント：国内取引所の営業日・板特性や、国内ブローカAPIのレイテンシ、東証の1分足データの取得単位を意識してデータ整備を行えば、著者のアプローチは十分に適用可能。
