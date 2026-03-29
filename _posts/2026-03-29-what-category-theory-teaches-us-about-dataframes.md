---
layout: post
title: "What Category Theory Teaches Us About DataFrames - データフレームから学ぶ圏論が教えること"
date: 2026-03-29T12:23:31.473Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mchav.github.io/what-category-theory-teaches-us-about-dataframes/"
source_title: "What Category Theory Teaches Us About DataFrames – Michael Chavinda – A collection of my thoughts on the various topics I find myself interested in."
source_id: 1035269760
excerpt: "圏論でデータフレームは3類($\Delta,\Sigma,\Pi$)に還元され、API設計と最適化が劇的に簡素化"
---

# What Category Theory Teaches Us About DataFrames - データフレームから学ぶ圏論が教えること
たった3つのパターンで理解するデータフレーム設計：冗長APIを圧縮して安全・最適化しやすくする設計原則

## 要約
圏論的な観点からデータフレーム操作を整理すると、Petersohnらの「データフレーム代数（約15の基本演算）」がさらに下位の3つの本質的パターンに圧縮できることが分かる：再構成、合流、結合（圏論ではそれぞれ $\\Delta,\\Sigma,\\Pi$）。

## この記事を読むべき理由
日本のデータ分析・データ基盤開発で使われるpandas/Polars/Spark/ModinなどのAPI設計や最適化、分散化に直結する理論的基盤を短時間で理解でき、ライブラリ設計・クエリ最適化・API整理に実践的な示唆を与えるため。

## 詳細解説
- Petersohnらはデータフレームを形式的に (A, R, C, D) — データ配列、行ラベル、列ラベル、列のドメイン— と定義し、200超のpandas操作を約15の演算に圧縮した（選択・射影・結合・グループ化・転置・行毎適用など）。
- そのうちスキーマを変化させる演算群は本質的に3種類に分類できる：
  - 再構成（Restructuring）: 列の選択・除外・改名など。データは変えずスキーマだけを変える。
  - 合流（Merging）: groupBy＋aggregate のように複数行をキーで集約する。
  - 結合（Pairing）: 異なる表をキーで結び付けて列を横に拡張する（join）。
- 圏論的にはスキーマをカテゴリ（オブジェクト＝列やテーブル、射＝外部キー）とみなし、スキーマ写像に対して出現するデータ移動操作はちょうど三つのデータ移送関手に対応する：
  - $\\Delta$（デルタ）：写像に沿ってデータを制限・再構成（データを発明・合流しない）。
  - $\\Sigma$（シグマ）：写像に沿ってデータを合流・集約（多対一を集める）。
  - $\\Pi$（パイ）：写像に沿ってデータをペアリング・問い合わせ（条件を満たす組合せだけを残す）。
- これらは隣接関係（adjoint triple）を持ち、形式的に
  $$
  \Sigma \dashv \Delta \dashv \Pi
  $$
  と書ける。隣接性は異なるスキーマ間の変換を安全に合成できることを保証するため、select→join→groupBy のような組合せがスキーマ整合性を保つ理由を説明する。
- スキーマを変えない操作（selection, sort, window）はインスタンス内の射であり、転置・map・toLabels/fromLabels はデータフレーム特有でリレーショナル核の外にある。

## 実践ポイント
- API設計：スキーマを変える操作はまず $\\Delta,\\Sigma,\\Pi$ のいずれかに還元できるように設計し、ユーザーAPIはそれらの合成で実装する。
- オプティマイザ：$\\Delta$ 系（列操作）は出力スキーマを入力スキーマと引数だけで決められるため、順序入れ替えや事前検証に最適。安価に再配置可能と扱う。
- 集約設計：$\\Sigma$ は「集める」ことの基本。collect を基本にしてから sum/mean 等を折り畳む設計にすると表現が明瞭。
- 結合実装：$\\Pi$ は「共通キーでの直積を制限する」操作と捉えるとNULL扱いや外部結合の型設計が楽になる。
- 日本の現場での応用：pandasスクリプトの最適化やModin/Polars等の分散実装、データ変換パイプライン設計にこの分類を適用すると、テスト、ドキュメント、最適化ルールの設計が簡潔になる。

短く言えば、「スキーマ変更の本質は3つだけ」と認識すると、APIの表面積を減らし実装と最適化が格段に楽になる。
