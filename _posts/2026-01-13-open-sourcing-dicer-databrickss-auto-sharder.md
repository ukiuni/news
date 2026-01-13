---
layout: post
title: "Open sourcing Dicer: Databricks's auto-sharder - Dicerをオープンソース化：Databricksの自動シャーダー"
date: 2026-01-13T23:17:06.760Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.databricks.com/blog/open-sourcing-dicer-databricks-auto-sharder"
source_title: "Open Sourcing Dicer: Databricks’ Auto-Sharder | Databricks Blog"
source_id: 46606902
excerpt: "*DatabricksのDicerで状態保持サービスを低コストかつ再起動耐性で自動シャード運用*"
image: "https://www.databricks.com/sites/default/files/2026-01/open-sourcing-dicer-databricks-auto-sharder-og-image.svg"
---

# Open sourcing Dicer: Databricks's auto-sharder - Dicerをオープンソース化：Databricksの自動シャーダー
再起動しても壊れない「状態を持つサービス」を安く速く運用する――DatabricksのDicerが変える設計

## 要約
Databricksが自社の自動シャーディング基盤「Dicer」を公開。動的にキー領域を分割・再配置して、低遅延かつ高可用に状態を持つサービスを運用できる仕組みです。Unity CatalogやSQLオーケストレーションでの導入により、再起動時の可用性低下を排し、pod再起動時でもキャッシュヒット率90%以上を維持しています。

## この記事を読むべき理由
日本のクラウド費用やGPUコストが高騰する中、状態を持つ高速サービス（KVキャッシュ、セッション、LLM推論用アダプタ等）をコスト効率よく安定稼働させる手法は必須です。Dicerは「ステートフル＋自動的に柔軟な再配置」を実現するため、国内のSaaS事業者やAIサービス運用者に即効性のある選択肢を提供します。

## 詳細解説
- 問題意識：  
  - ステートレスはDB/リモートキャッシュに往復が発生し、ネットワーク遅延・(デ)シリアライズ負荷・「overread」による無駄が大きい。  
  - 静的シャーディング（consistent hashing等）は再起動やノード障害時にsplit-brainやホットキー問題、ダウンタイムを招く。  

- Dicerのコア概念：  
  - SliceKey: アプリケーションキーのハッシュ。  
  - Slice: 連続するSliceKeyの範囲（＝キーレンジ）。  
  - Assignment: 全キー空間をカバーするSliceの集合と、それぞれのSliceに割り当てられたResource（pod）。  
  - 動的操作: Sliceの分割（split）、統合（merge）、複製／解除（replicate/dereplicate）、移動をリアルタイムに行い、負荷変化やノード状態に応じて割り当てを調整。  
  - コンポーネント:  
    - Slicelet（サーバー側ライブラリ）: 現在のAssignmentをローカルに保持・監視し、負荷統計を非同期で送る。  
    - Clerk（クライアント側ライブラリ）: クライアントがキーの割当先podを高速に参照できるローカルキャッシュを保つ。  
    - Assigner（コントローラ）: 全ターゲットに対して割当を計算・配布する多重テナントの制御プレーン。  
  - 設計トレードオフ: Assignmentは最終的整合性（eventual consistency）を優先し、可用性と迅速な回復を重視する。強整合が必要なケースには今後対応予定。

- 運用効果と用途例：  
  - 実績: Unity CatalogやSQLオーケストレーションで採用。ローリング再起動中もキャッシュヒット率90%超を維持し、可用性低下を解消。  
  - 応用例: インメモリ／GPUサービング（LLM推論アダプタの効率配置）、バッチやパーティショニング、マルチテナンシー、ソフトリーダー選出など。

## 実践ポイント
- まずはリポジトリをクローンして小さなサービスで試す（Dev環境でSlicelet/Clerkを組み込み、Assignerの動作観察）。  
- 指標はキャッシュヒット率、レイテンシ、スライスの分割頻度、ホットキー検出時間を中心に監視。  
- ホットキー対策：負荷閾値を設定して自動でSliceを分割・複製するポリシーを設計する。  
- LLM/GPU活用：GPU上のモデルやLoRAアダプタをSlice単位でアフィニティさせると利用効率が上がる。  
- 設計上の注意：Assignmentは最終的整合性なので副作用がある処理は冪等化し、短時間の不一致を許容できる設計にする。  
- 日本向けの価値：クラウドコスト削減、GPUリソースの効率化、SLA改善を目指す国内プロダクト運用に直結する。

Dicerは「状態を大事にしつつ、現実的に運用できる自動化」を目指すツールです。まずは小さなワークロードで挙動を確かめ、可用性とコストの両立を図ってみてください。
