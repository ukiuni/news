---
layout: post
title: "Teenage Engineering's PO-32 acoustic modem and synth implementation - Teenage Engineering の PO-32 アコースティックモデムとシンセ実装"
date: 2026-03-31T20:33:16.323Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ericlewis/libpo32"
source_title: "GitHub - ericlewis/libpo32: C99 library for PO-32 acoustic transfers and drum synthesis. · GitHub"
source_id: 47550433
excerpt: "PO-32の音転送を再現しWAV生成・復号・合成可能なCライブラリ"
image: "https://opengraph.githubassets.com/582b8fbc8865656f8742a5d3c58fd33e9b8a6d5267fe5f6f504650d1d4ab36bc/ericlewis/libpo32"
---

# Teenage Engineering's PO-32 acoustic modem and synth implementation - Teenage Engineering の PO-32 アコースティックモデムとシンセ実装
PO-32に“音でデータを送る”を再現するCライブラリ──ハードを鳴らし、ローカルでプレビューまでできる開発者向けツール

## 要約
libpo32は、Teenage EngineeringのPO-32が使うアコースティック転送（音声でデータを送る）プロトコルを再実装したC99ライブラリで、転送フレームの生成・音声レンダリング・復号・21パラメータのドラム合成までをカバーします。

## この記事を読むべき理由
PO-32やハードウェアシンセを改造・連携したい開発者／ミュージシャン、組み込みやbare‑metal開発に挑戦したいエンジニア、日本のライブ/ハードウェア愛好家にとって「音で設定を送る」仕組みを理解し実験できる実用的なツールだからです。

## 詳細解説
- 提供機能：PO-32のパッチ／パターン／ステートのパケット生成、DPSK相当の転送フレームをWAVへレンダリングするアコースティックモデム、転送音からのフレーム復号器、そしてPO-32互換の21パラメータドラム音源（ローカル再生用）。
- 技術的特徴：フリースタンディングなC99実装（<stddef.h>と<stdint.h>のみ）、外部DSPやOS依存API不要で埋め込み環境やbare‑metalでの使用に適合。転送は「パッチ（左右エンドポイント）」「パターン（ステップ割当）」「ステート（テンポ等）」の構造化データを音声に変換してデバイスへ送り、デバイス側が内部シンセで音にします。
- ワークフロー：ソフトでパケットを組み立て→音声にレンダリング（WAVかライブ出力）→PO‑32を受信モードにして再生→デバイス側でデコードして書き込み。ライブラリ内のデモはエンコード→レンダリング→復号→ローカル合成のラウンドトリップを検証します。
- 実装と例：CMakeでビルド（例: cmake -S . -B build -DCMAKE_BUILD_TYPE=Release 等）。付属の実行ファイルに po32_demo（demo_modem.wav / demo_kick.wav出力）、po32_pattern_editor、po32_decode_capture などがあり、実機テストや解析に便利。公開APIは core/include/po32.h と core/include/po32_synth.h に整理。
- ライセンス：MIT。改変・組み込み・商用利用のハードルが低い点も魅力。

## 実践ポイント
- まずリポジトリをクローンし、CMakeでビルドして po32_demo を実行して生成されるdemo_modem.wavをPO‑32に再生してみる。ラウンドトリップで正しく復号できれば転送成功。
- パッチやパターンをソフトで生成してWAV化→ライブパフォーマンスで即座にPO‑32へ反映させるワークフローに応用可能。
- 組み込み機器やマイク入力のあるデバイス上で動かす際は、フリースタンディングC実装を活かして低レイテンシな送受信モジュールを作ると面白い。
- 日本のライブ／チップチューンコミュニティ向けに、ワークショップ教材やハード改造キットの基盤として活用すると敷居が下がる。

原典（ライブラリ・デモ・ドキュメント）は GitHub: ericlewis/libpo32（MIT, C99）を参照。
