---
layout: post
title: "Comprehensive C++ Hashmap Benchmarks (2022) - 包括的なC++ハッシュマップベンチマーク（2022）"
date: 2026-03-30T13:22:59.821Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://martin.ankerl.com/2022/08/27/hashmap-bench-01/"
source_title: "Comprehensive C++ Hashmap Benchmarks 2022"
source_id: 47518264
excerpt: "29種類×1914ベンチで判明、用途別C++ハッシュマップ最速案内"
image: "http://martin.ankerl.com/img/2022/wanderfalke_edit.jpg"
---

# Comprehensive C++ Hashmap Benchmarks (2022) - 包括的なC++ハッシュマップベンチマーク（2022）
C++ハッシュマップ29種×174組合せを1914回走らせた「どのmapを選ぶべきか」が一目で分かる最速ガイド

## 要約
Martin Leitner‑Ankerl氏が2022年時点で主要なC++ハッシュマップ実装を徹底比較。29種類のコンテナ×6種類のハッシュ＝174組合せを11種類のベンチで評価し、実運用で効く性能とメモリ特性を明らかにしています。

## この記事を読むべき理由
- std::unordered_mapだけで妥協すると性能とメモリで損をする場面が多い。  
- サーバーや組み込み、文字列多用ケースなど日本の現場で直ちに役立つ選択指針を得られる。

## 詳細解説
- 実験規模：29種のマップ、6種類のハッシュ、11ベンチ、合計1914評価。  
- 実行環境：Intel i7‑8700（3200MHz固定）、clang++ 13、コンパイル最適化 -O3 -march=native。各ベンチは複数回実行して中央値を使用。  
- ベンチ種類（抜粋）：
  - コピー性能（大きいmapのコピーを何度も行う）  
  - 大量挿入→clear→再挿入→逐次削除（100M int）でリサイズ＆ピークメモリを測定  
  - ランダム挿入＋アクセス（異なる「重複率」：5%,25%,50%,100%）で挿入対参照のバランス評価  
  - ランダム挿入＆削除（ビットマスクで上位ビットも回す）で平衡サイズごとの挙動観察  
  - 反復（iterate）ベンチ、find系（0–100%ヒット率、サイズ幅あり）  
  - 文字列キーの挙動（長さ7〜1000B）—ハッシュ/比較コストの影響を評価  
  - ピークRSSを測るメモリベンチ（flat系は再配置時に一時バッファでメモリが跳ね上がる）  
- 実装タイプの違い：要素位置が安定（node系）か不安定（flat/open‑address）かで利点が異なる。open‑addressは通常高速・低間接化だが参照安定性を犠牲にする。  
- 結果ハイライト：absl::flat_hash_mapやabsl::node_hash_map、ankerl::unordered_dense などが総合で上位。だがワークロード次第で最適は変わる（数値キー探索、高頻度挿入削除、文字列キーなどで順位が変動）。

## 実践ポイント
- まずは自分のワークロードでベンチ：作者も「ジェネラル最速＝常に最善ではない」と強調。リアルなキー分布・操作比で比較すること。  
- 高速探索が最重要なら：absl::flat_hash_map や ankerl::unordered_dense を候補に。  
- ポインタ／参照の安定性が必要なら：node系（absl::node_hash_map、folly の node マップ等）を選ぶ。  
- 文字列キーが多い場合：キー長に応じてハッシュ・比較コストが支配的になるので、小〜中長さで実測比較を。  
- メモリ制約がある環境：flat/open‑address は一時的なピークメモリ増加を招くことがあるので注意。peak RSS を測ること。  
- 小手先の改善：allocator（プール/pmr）を変えるだけで std::unordered_map の挙動が改善する場合あり。  
- ビルド設定：実運用バイナリは必ず最適化（例：-O3 -march=native）で測る。  
- 最終判断は「幾つかの代表ケースでの幾何平均（geometric mean）」を見ると偏りが減る。

この記事を踏み台に、まずは自分のプロジェクトで代表的なデータと操作比を用意して複数実装を比較してみてください。
