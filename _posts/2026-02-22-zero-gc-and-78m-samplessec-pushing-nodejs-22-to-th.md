---
layout: post
title: "Zero-GC and 78M samples/sec: Pushing Node.js 22 to the limit for Stateful DSP - Zero-GCと7800万サンプル／秒：Stateful DSPのためにNode.js 22を限界まで押し上げる"
date: 2026-02-22T04:58:28.383Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/A-KGeorge/dspx-benchmark/tree/main/charts"
source_title: "dspx-benchmark/charts at main · A-KGeorge/dspx-benchmark · GitHub"
source_id: 399695425
excerpt: "Node.js 22でGCゼロ、78Mサンプル/s達成の高速ステートフルDSP技術"
image: "https://opengraph.githubassets.com/c2a054970e547c6c75f5a3d83cebf8637c70ef17d091db7aa382b5a52878d4ae/A-KGeorge/dspx-benchmark"
---

# Zero-GC and 78M samples/sec: Pushing Node.js 22 to the limit for Stateful DSP - Zero-GCと7800万サンプル／秒：Stateful DSPのためにNode.js 22を限界まで押し上げる
はやく試したくなるタイトル：Node.jsで「GCゼロ」の音声処理が本当にできる？78M samples/sを実現した最適化テクニック

## 要約
Node.js 22上で「ゼロGC（ガベージコレクション発生ゼロ）」を目指すコーディングとベンチマークにより、ステートフルなDSP処理で $78\ \mathrm{M\ samples/s}$ を達成したという報告です。実装はバッファの再利用や割り当て回避に重点を置いています。

## この記事を読むべき理由
リアルタイム音声処理や低レイテンシな信号処理をNode.jsでやりたい開発者や、サーバーサイドで高スループットなストリーミング処理を検討する日本のエンジニアにとって、GCの影響を抑えた実装手法とその効果（性能メトリクス）はすぐ役立ちます。

## 詳細解説
- 背景：JSランタイムは自動メモリ管理（GC）で扱いやすい一方、頻繁な割り当て→回収があるとレイテンシやスループットに悪影響を与えます。DSP（デジタル信号処理）はサンプル単位で高速処理が求められるため、GCを如何に回避するかが肝になります。
- アプローチの要点：
  - バッファの事前確保と再利用：ArrayBuffer/TypedArrayをループ外で1回だけ確保し、処理ループはその領域を上書きする方式にすることで新しいオブジェクト割り当てを防ぎます。
  - インプレース演算：出力も既存バッファに書き戻す（in-place）ことで中間オブジェクトを減らす。
  - 状態管理をプリミティブで保持：クラスや頻繁に生成されるオブジェクトを避け、数値配列やプリミティブでフィルタ状態を管理。
  - スレッド分割とワーカ利用：ワーカ（Worker Threads）で重い処理を分離してメインスレッドをブロックしない。
- Node.js 22側の利点：最新のV8最適化やJIT改善により、インプレースかつ割り当てを抑えたループがより高速に動作する傾向があります。ベンチマーク結果はこの組み合わせの効果を示しています。
- 結果指標：レポートはゼロGC達成下で $78\ \mathrm{M\ samples/s}$ 程度のスループットを示し、これは同等ハードウェアでの従来実装に比べ明確な改善を意味します（実機条件に依存）。

## 実践ポイント
- まずプロファイル：自分の処理を実行してGC発生箇所を特定する（--trace-gcやprofilingツールを活用）。
- バッファ再利用を徹底する：処理ループ内でのnew/concat/mapなどの割り当てを避け、TypedArrayでバッファを使い回す。
- ローカル最適化：フィルタ係数や状態はプリミティブ配列で管理し、関数呼び出しやオブジェクト生成を減らす。
- ワーカ分離：IOやUI（ブラウザ）とは別スレッドでDSPを回す。NodeのWorker ThreadsやWebAudioのAudioWorkletの考え方に近い。
- ベンチマークを自作する：dspx-benchmarkのようなベンチチャートを参考に、自分の環境でスループットとGCの発生を測る。

この手法は、音声配信・リアルタイム分析・エッジでのDSPなど、日本でも需要が高い用途に直結します。まずは小さなモジュールでバッファ再利用と測定から始めてください。
