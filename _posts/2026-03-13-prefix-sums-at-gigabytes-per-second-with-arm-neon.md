---
layout: post
title: "Prefix sums at tens of gigabytes per second with ARM NEON - ARM NEONでギガバイト毎秒のプレフィックス和"
date: 2026-03-13T06:51:27.642Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lemire.me/blog/2026/03/08/prefix-sums-at-tens-of-gigabytes-per-second-with-arm-neon/"
source_title: "Prefix sums at tens of gigabytes per second with ARM NEON &#8211; Daniel Lemire&#039;s blog"
source_id: 47301017
excerpt: "ARM NEONで16要素並列処理、毎秒数十GB級の高速プレフィックス和"
image: "https://lemire.me/blog/wp-content/uploads/2026/03/Capture-decran-le-2026-03-08-a-16.07.29-1024x798.png"
---

# Prefix sums at tens of gigabytes per second with ARM NEON - ARM NEONでギガバイト毎秒のプレフィックス和
ARM/Apple Siliconで動く「毎秒数十ギガバイト」級のプレフィックス和実装 — なぜ速いか、どう使うかを噛み砕いて解説

## 要約
単純な累積和（prefix sum）は依存性で速度が制限されるが、ARMのNEONでデータを「16要素ずつ横断的に読み出して」並列処理すると、実測でスカラー実装の約2.3倍（Apple M4で約8.9B値/s）に達する。

## この記事を読むべき理由
ARMコア（スマホ・組込み・Apple Silicon・ARMサーバ）が普及する日本の現場で、集計や解析処理のボトルネックをSIMDで突破する実用テクニックだから。データベース、ログ集計、リアルタイム解析に即効性がある。

## 詳細解説
- プレフィックス和は直感的には単純ループで実装可能だが、各要素は前の結果に依存するため理論上「1要素あたり最低1サイクル」の制約がある。例えば$4\,$GHzなら最大で約 $4\times10^9$ 値/秒が上限。
- SIMD（NEON）は1命令で複数要素を処理できるが、そのままではベクトル内にデータ依存が残る。ベクトル長$N$のプレフィックス和はシフト＋加算で$O(\log N)$ステップで解ける（例：4要素なら2段のシフト・加算）。
- Lemireのアプローチは「メモリ読み出し時にデータを4つのレーンにデインタリーブ（vld4q_u32）」して、縦方向の各レーンでローカルなプレフィックス和を並列に計算。各ブロック（16要素）ごとにローカル合計を集めてブロック間のキャリーを伝搬させる手法で、実行シーケンスをうまくまとめて実効命令数を削減している。
- 主なNEON命令例：vld4q_u32（16要素を4レーンに分配）、vaddq_u32（ベクトル加算）、vextq_u32（シフト的抽出）、vdupq_laneq_u32（ラスト要素をブロードキャスト）。この組み合わせで1ブロック当たりおおむね8命令程度にまとまるため、スカラー実装より速くなる。

## 実践ポイント
- 処理単位は16要素ブロック（vld4q_u32が効く）で設計する。余りはスカラーループで処理する。
- メモリアライメントと連続アクセスを意識する（vld4q_u32は連続16要素読み出しを想定）。
- 実装はNEONのイントリンシックを使うと移植しやすい（以下は要点サンプル）。コンパイラ最適化だけで同等性能が出るかはターゲット次第なので、必ずプロファイルする。
```c
// C (抜粋イメージ)
uint32x4x4_t vals = vld4q_u32(data + 16*i); // deinterleave 16 elems
vals.val[1] = vaddq_u32(vals.val[1], vals.val[0]);
vals.val[2] = vaddq_u32(vals.val[2], vals.val[1]);
vals.val[3] = vaddq_u32(vals.val[3], vals.val[2]); // ローカル和
// ローカル和を横方向にプレフィックス（vextq_u32/vaddq_u32等）→キャリー適用→vst4q_u32
```
- 日本の環境ではApple Silicon搭載開発機やARMサーバで効果が見込める。バッチ集計やリアルタイム解析のホットループをまず計測してから導入を検討すること。
