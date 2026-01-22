---
layout: post
title: "Show HN: CLI for working with Apple Core ML models - Apple Core MLモデルを扱うCLI"
date: 2026-01-22T21:47:27.281Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/schappim/coreml-cli"
source_title: "GitHub - schappim/coreml-cli: A native command-line interface for working with Apple Core ML models on macOS"
source_id: 46724565
excerpt: "Mac上でCore MLモデルを中身確認・実機推論・ベンチできるCLI"
image: "https://opengraph.githubassets.com/74431a1cb73639e9c5951d5cea4a57e5a09d0faae31829e0979e73eaec9bb207/schappim/coreml-cli"
---

# Show HN: CLI for working with Apple Core ML models - Apple Core MLモデルを扱うCLI
XcodeやPython不要で手元のMac上でCore MLモデルを素早く調べて実行・ベンチマークできる「coreml-cli」を試す理由

## 要約
macOS向けのネイティブCLI「coreml-cli」は、.mlmodel系ファイルの構造確認、推論、バッチ処理、ベンチマーク、コンパイル、メタデータ操作をターミナルだけで完結させるツールです。

## この記事を読むべき理由
iOS/機械学習エンジニアやプロダクト担当が「実機での推論速度」「モデルの中身」「CIでの性能監視」を手早く確認できるため、アプリ最適化や品質管理の効率が大幅に上がります。日本のモバイルアプリ開発現場にも直接役立ちます。

## 詳細解説
- 主な機能
  - Inspect: モデルの入出力やメタ情報を表示（JSON出力対応でスクリプト化可能）
  - Predict: 画像／音声／テキスト／JSONテンソル入力で単発推論
  - Batch: ディレクトリ内のファイルを並列処理してCSV等で出力
  - Benchmark: レイテンシ・スループット測定（warmup/Iterationsやデバイス指定可能）
  - Compile: .mlmodel → 最適化済み .mlmodelc にコンパイル
  - Meta: ライセンスや説明などのメタデータ参照・編集
- 入力対応例: .jpg/.png/.heic（Vision）、.wav（音声）、.txt（テキスト）、.json（数値テンソル）
- デバイス選択: cpu / gpu / ane（Apple Neural Engine）／all
- 自動化・CI連携: ベンチマーク結果をJSONで出力してGitHub Actions等で回帰検知が可能
- 動作要件: macOS 13+、Swift 5.9+（ソースビルド時）。Apple Silicon / Intel 両対応。対象モデル: .mlmodel, .mlpackage, .mlmodelc

インストール（推奨）
```bash
# Homebrew
brew tap schappim/coreml-cli
brew install coreml-cli
```

よく使うコマンド例
```bash
# モデル調査
coreml inspect MobileNetV2.mlmodel --json

# 画像推論（ANE/GPU/CPU 指定）
coreml predict MobileNetV2.mlmodel --input photo.jpg --device ane

# バッチ処理（並列）
coreml batch MobileNetV2.mlmodel --dir ./photos --out ./results --format csv --concurrency 8

# ベンチマーク（JSON出力）
coreml benchmark MobileNetV2.mlmodel -i sample.jpg --json > bench.json

# コンパイル
coreml compile MobileNetV2.mlmodel --output-dir ./compiled
```

## 実践ポイント
- まずは coreml inspect でモデルの入出力とメタを確認してから推論を試す。
- ベンチマークはデバイス（cpu/gpu/ane）ごとに定期測定し、CIで閾値超過を検知するワークフローを組むと性能劣化を早期に捕捉できる。
- 大量画像処理は coreml batch を使い、並列数を調整してスループットとメモリ消費をトレードオフする。
- 配布前に coreml compile で最適化版を生成してサイズ／互換性を確認する。
- 日本向けアプリではプライバシー配慮のため端末内推論を重視するケースが多く、Core MLの実機評価は必須。coreml-cliはその最短ルートになります。
