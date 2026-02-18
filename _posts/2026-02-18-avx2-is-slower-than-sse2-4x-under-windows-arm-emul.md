---
layout: post
title: "AVX2 is slower than SSE2-4.x under Windows ARM emulation - Windows ARM エミュレーションで AVX2 は SSE2〜4.x より遅い"
date: 2026-02-18T14:37:18.865Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blogs.remobjects.com/2026/02/17/nerdsniped-windows-arm-emulation-performance/"
source_title: "AVX2 is slower than SSE2-4.x under Windows ARM emulation"
source_id: 47061062
excerpt: "Windows ARMのエミュでAVX2がSSE2-4より約3割遅く、対策が必須"
image: "https://blogs.remobjects.com/content/images/2026/02/AdobeStock_686264219.jpeg"
---

# AVX2 is slower than SSE2-4.x under Windows ARM emulation - Windows ARM エミュレーションで AVX2 は SSE2〜4.x より遅い
Windows ARM（Prism）で「速いはず」のAVX2が逆に遅くなる理由 — エミュレーションの落とし穴

## 要約
RemObjects のベンチで、Windows 11 ARM（Prism）上での x86_64 AVX2(+FMA) エミュレーションは、同じコードを SSE2〜4.x（x64 v2）で動かした場合より約2/3の性能しか出なかった。ネイティブ x64 上では AVX2 は大幅に高速化するが、エミュレーションでは逆効果になる。

## この記事を読むべき理由
Windows ARM 上でアプリを走らせる可能性がある開発者は、「AVX2 をターゲットにすべきか」を判断するための実測データと実務的な対策が得られる。

## 詳細解説
- 測定概要：RemObjects は LLVM ベースの新しいベクトル化数学ライブラリで、64-bit double を使った21の数学関数をベンチ。各関数をベクトル化ループで10M回回し、x64 v2（SSE2〜4.x）を1.0に正規化して、x64 v3（AVX2+FMA）の相対性能を算出（幾何平均）。
- 環境：x64 実機（Tiger Lake i7, Windows 11）と ARM（Apple M2 上の Parallels で Windows 11、Prism）で比較。ネイティブ x64 では AVX2 が約2.7×速い。一方、ARM 上の AVX2 エミュレーションは SSE2〜4.x より遅く、概ね 0.67（＝2/3） の性能。
- 主な原因（推測を含む）：
  - AVX2 は 256-bit 幅、ARM の NEON は 128-bit。エミュレータは 256-bit を 128-bit の半分ずつ処理する必要がありオーバーヘッドが発生しやすい。
  - Prism の AVX2 エミュレーションは新しく、最適化が十分でない可能性（特に 64-bit double 向けの最適化が弱い）。
  - Prism が Snapdragon 系ハードウェア向けにチューニングされている点も影響（今回は Apple M2 上の Parallels）。
- 注意点：テストは実機世代やプラットフォームが異なるため絶対値比較は不可だが、相対的傾向は信頼に足る。exp() のような例外的に速い結果も一部あり。

## 実践ポイント
- パフォーマンス重視の実行環境が Windows ARM になる可能性があるなら、AVX2 を主ターゲットにしない（SSE2〜4.x レベルか ARM64 を使う）。
- マルチターゲット戦略を採る（target_clones のようなランタイム分岐や、AVX2 と SSE 両対応ビルド）。
- 重要処理はネイティブ ARM64 ビルドを用意してテストする（エミュレーションに依存しない）。
- 実機でプロファイルする：Parallels/M2 と実際の Snapdragon Windows 機で挙動が異なる可能性あり。
- ライブラリ選定時は NEON 最適化の有無を確認するか、128-bit ベースの実装を検討する。

（参考）この調査は RemObjects のベンチ結果に基づくもので、Prism の実装やハードウェアにより結果は変わる可能性があります。
