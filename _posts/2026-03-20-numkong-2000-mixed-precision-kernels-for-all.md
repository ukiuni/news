---
layout: post
title: "NumKong: 2'000 Mixed Precision Kernels for All - NumKong：2,000以上の混合精度カーネルを誰でも使える形で"
date: 2026-03-20T21:23:00.346Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ashvardanian.com/posts/numkong/"
source_title: "NumKong: 2'000 Mixed Precision Kernels For All 🦍 | Ash's Blog"
source_id: 47459447
excerpt: "超軽量NumKongで2000超の混合精度カーネルを即導入し検索・AIを劇的高速化"
image: "https://ashvardanian.com/numkong/NumKong-v7.jpg"
---

# NumKong: 2'000 Mixed Precision Kernels for All - NumKong：2,000以上の混合精度カーネルを誰でも使える形で
魅力的な日本語タイトル: 小さく速い混合精度ライブラリ「NumKong」で、AI/検索のボトルネックを一気に解消する方法

## 要約
NumKongは、7言語対応・5MB未満の小さな配布で2000以上のSIMDカーネル（混合精度対応）を提供するオープンソースライブラリで、RISC‑V、x86（AVX2/AVX‑512/AMX）、Arm（SME/SVE）、WASMなど幅広いハードで高速化を狙う取り組みです。

## この記事を読むべき理由
・日本でも増えるオンプレ／クラウドのAI・ベクトル検索ワークロードにおいて、「量子化（Int8/Float8等）」や「低精度演算」を効率よく使うことがコストと性能両面で重要になっています。NumKongはそのための実装群と実践ノウハウを一括提供します。

## 詳細解説
- 概要と規模  
  NumKongはMixed‑Precision（Float118〜Float4、Int4/Int8など含む）に対応したSIMDカーネルを大量に用意。Python/C/C++23/Rust/Swift/JS/Goなど7言語のバインディングがあり、配布は非常に小さく軽量（数MB級）に収められています。

- ハードウェアごとの特徴と最適化戦略  
  - Intel AMX：大きなタイル（TMM）と専用TMULでタイル化GEMMが得意。bf16/f16/i8系をタイルで効率的に処理。サーバ系で特に威力を発揮。  
  - Arm SME＋SVE：Apple M4/M5で先行して利用可能な「ストリーミング＋外積」モデル。柔軟で複合カーネル（外積＋マスク処理など）に強く、Sparseや複雑なアルゴリズムに向く。  
  - RISC‑V RVV：命令セットは巨大だが、segmented loadsや幅拡張FMAなどユニークな命令で一部アルゴリズム（分散ロード、幅拡張積和）に利点。ただしハードの普及・仕様の揺れが課題。  
  - WebAssembly SIMD（Relaxed）：ブラウザやエッジでのAI/検索サンドボックス向けに最適化したバックエンドを用意。

- 精度とスピードのトレードオフ  
  NumKongは「用途に応じた精度選択」を前提に実装。低精度（Int8/Float8/BFloat16）で大きくスループットを伸ばしつつ、必要な場面ではCompensated SummationやOzaki法など高精度スキームも備えています。ライブラリ全体で数千のカーネルを用意することで、データレイアウトやストライド、複素数/非対称ドット積など細かい状況に最適化できます。

- 実運用事例と応用領域  
  元プロジェクトは検索エンジン向け（USearch）に設計され、ClickHouse/DuckDB/ScyllaDB等でのベクトル検索や、地理空間計算（Vincenty）、メッシュ整列（Kabsch/Umeyama）、ColBERT型のLate-Interactionスコアリングなどで高速化実績があるとのこと。ブラウザやエッジでの軽量AIにも対応。

## 実践ポイント
- まずは試す：Pythonホイールや他言語バインディングが用意されているので、手持ちのベンチでFloat16/BFloat16/Int8の単体カーネルを動かしてみる。  
- バックエンド選択：開発対象の実機（Apple Mシリーズ／Intel Xeon(AMX)／AVX VNNI 搭載機／RISC‑V 試験機）に合わせたNumKongバックエンドを選ぶ。M系列ならSME、サーバならAMXが有効。  
- 精度管理：精度要件の低いランキング系やベクトル類似検索はInt8/BFloat16で大幅加速。数値誤差が許容できない処理はCompensated Summationや高精度カーネルを組み合わせる。  
- プロファイリング：単スレッド性能の差が大きいので、まずはシングルコアのホットループを計測して最適なカーネルを選ぶ。  
- デプロイ/サイズ：NumKongは非常に小さく配布される設計なので、エッジやブラウザ導入でバイナリサイズ制約がある環境に有利。WASMバックエンドでブラウザ実行を検討する価値あり。  
- 互換性チェック：RISC‑V等は実装・仕様差があるため、実機での動作確認を必ず行う。  

短くまとめると、NumKongは「混合精度を実用レベルで大量に用意し、未利用のハード機能を引き出す」ライブラリです。日本でも増える量子化・エッジAI・検索ワークロードに強く、まずは手元の環境で低精度カーネルを試し、精度とスピードのバランスを評価することをおすすめします。
