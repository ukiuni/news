---
layout: post
title: "Engineering a Columnar Database in Rust: Lessons on io_uring, SIMD, and why I avoided Async/Await - Rustで作るカラム型DB：io_uring・SIMD・Async/Awaitを使わなかった理由から学ぶこと"
date: 2026-01-17T18:49:04.343Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Frigatebird-db/frigatebird"
source_title: "GitHub - Frigatebird-db/frigatebird: 🪶 columnar SQL database built from scratch"
source_id: 424374744
excerpt: "Rustでio_uringとSIMDで高速化した組み込み向けカラムDB設計の実践解説"
image: "https://opengraph.githubassets.com/7152e0e25c51aefb795c194517dbe29ee5334e6fb6a6d09709fc640815989b8d/Frigatebird-db/frigatebird"
---

# Engineering a Columnar Database in Rust: Lessons on io_uring, SIMD, and why I avoided Async/Await - Rustで作るカラム型DB：io_uring・SIMD・Async/Awaitを使わなかった理由から学ぶこと
魅力的タイトル: 「Rustで自作DBを突き詰めたら見えた、io_uringとSIMDで高速化する“現場の技術”」

## 要約
FrigatebirdはRustでゼロから作られた組み込み向けカラム型SQLデータベースで、push型パイプライン＋morsel（塊）並列処理、遅延マテリアライゼーション、io_uring＋O_DIRECTによる高速I/O、SIMDベースのベクトル処理を組み合わせて高性能を狙っている。

## この記事を読むべき理由
日本のプロダクトや現場では、IoTログ、分析ワークロード、エッジ組み込みなど「読み取りが重い」「選択的に高速に取り出したい」用途が増えている。Frigatebird の設計はこうしたケースで実践的に効く手法の実装例を示しており、Rustでの低レイヤ最適化やLinux I/O周りの現実問題が学べる。

## 詳細解説
- カラム型ストレージと利点  
  データを列単位で保持するため、特定列だけを読み出す分析系クエリでI/Oを大幅に削減できる。Frigatebirdは列ごとにファイルを持ち、ページはLZ4で圧縮、4KB境界で配置してO_DIRECTに備える。

- プッシュ型（Volcanoの逆）パイプラインとmorsel-driven並列処理  
  クエリは演算子のパイプラインにコンパイルされ、各演算子がバッチを下流へ「押し出す」設計。データは50k行程度の「morsel（塊）」単位で並列に処理され、ロックフリーな原子操作でワーカーが塊を奪い合って実行する。これにより各ステップが独立に並列化される。

- 遅延マテリアライゼーション（Late materialization）  
  フィルタを上流でかけ、最終投影列は最後に必要な行だけで読み込む。READMEの例では総読み込み値が750kから226kに減り、約70%のI/O削減となる。

- SIMD／ベクトル化による高速フィルタリング  
  ビットマップ演算などで複数行を1命令で処理する。CPUのワイド演算を活かして64行単位程度で並列比較や論理演算を行うことで、行単位処理より遥かに速くなる。

- I/O最適化：io_uring と O_DIRECT  
  Linuxのio_uringを使い、OSページキャッシュを迂回するO_DIRECTでバッチ非同期I/Oを行う。これによりユーザ空間での効率的なI/Oスケジューリングと低い遅延が期待できる（ただし対応するカーネルと注意点あり）。

- WAL（Write-Ahead Logging）と耐障害性  
  書き込みはWALで保護し、三相コミットなどの仕組みでクラッシュリカバリを実現する点も実務向けの重要な設計。

- なぜAsync/Awaitを避けたか（設計上の判断）  
  細かい並列ワーク（morsel）のスケジューリングや低レベルI/Oのバッチ制御を直接扱うため、言語の高レベルなasync/awaitの抽象がかえってオーバーヘッドや制御のブラックボックス化を招くと判断した模様。代わりに明示的なワーカースレッド＋チャネル＋io_uringバッチで遅延やメモリ配置をコントロールしている。

## 実践ポイント
- 試す：Linux環境でリポジトリをcloneし、READMEのCLI例（CREATE TABLE / INSERT / SELECT）で動作を確認する。cargo test を実行して挙動を見ると良い。
- 環境注意：io_uringやO_DIRECTはカーネルとファイルシステムの制約があるため、導入前に動作するカーネルバージョンや設定を確認する。
- ベンチ：選択的クエリ（多数の行から少数列を抽出するパターン）で遅延マテリアライゼーションと圧縮の効果を計測してみると、効果が実感しやすい。
- 設計活用：エッジ系や組み込み型アプリで、Rustの安全性と低レイヤ制御（SIMD、io_uring）を組み合わせたい場合、本プロジェクトのアプローチは参考になる。
- 日本市場への応用例：工場やビルセンサーデータの時系列集約、ログ分析、オンプレの分析エンジンなど、読み取り中心の分析ワークロードに適合する。

この記事で紹介した設計は「どのレイヤを手で最適化するか」を考える良い教材になる。RustとLinuxの最新I/Oを用いた実装パターンを実際のコードで追い、ローカル環境で手を動かしてみることをおすすめする。
