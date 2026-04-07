---
layout: post
title: "Show HN: Gemma 4 Multimodal Fine-Tuner for Apple Silicon - Gemma 4 マルチモーダル微調整ツール（Apple Silicon向け）"
date: 2026-04-07T20:20:00.641Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mattmireles/gemma-tuner-multimodal"
source_title: "GitHub - mattmireles/gemma-tuner-multimodal: Fine-tune Gemma 4 and 3n with audio, images and text on Apple Silicon, using PyTorch and Metal Performance Shaders. · GitHub"
source_id: 47680309
excerpt: "Macで音声・画像・テキストをLoRAで手元微調整、クラウドストリーミングで大容量学習可能"
image: "https://opengraph.githubassets.com/a05af442431ed78ae7ab373206179fce68fa88696b8577d681d3d36c48daa569/mattmireles/gemma-tuner-multimodal"
---

# Show HN: Gemma 4 Multimodal Fine-Tuner for Apple Silicon - Gemma 4 マルチモーダル微調整ツール（Apple Silicon向け）

魅力タイトル：Macだけで音声・画像・テキストを微調整できる！GemmaをApple Siliconで動かす最速ハック

## 要約
Gemma（Googleの大規模マルチモーダルモデル）を、Apple Silicon（M1/M2等）のMac上でテキスト・画像・音声の各モダリティに対してLoRAベースで微調整できるツールキット。大容量データのクラウドストリーミング対応で、ローカルSSDを圧迫せずに学習可能。

## この記事を読むべき理由
- 日本でもMac（M1/M2）の開発者や研究者が増加中。GPUレンタルや巨大なローカル環境を用意せずに、手元で実用的な適応モデルを作れる点はコストとプライバシー両面で魅力的。
- 音声（ASR）・画像（キャプション/VQA）・テキストのいずれもサポートする珍しいApple Siliconネイティブの実装で、ドメイン特化モデル作成の入門になり得る。

## 詳細解説
- 対象：Gemma 3n / Gemma 4 のマルチモーダルチェックポイントを読み込み、PEFT（LoRA）で学習。Hugging Faceの重みを元にLoRAアダプタを学習し、後でマージしてエクスポート可能。
- モダリティ：
  - text：CSVベースの instruction / completion 形式で微調整（ローカルCSVがv1サポート）。
  - image：caption / VQA をサポート。CSVに画像パスとテキストを置く形で学習。image_token_budget（70〜1120）でトークン割当を調整。
  - audio：音声＋テキストの微調整をApple Siliconネイティブで実現（CUDA不要）。
- 環境と要件：macOS 12.3+、Python 3.10+、PyTorch（MPS対応）。RAMは用途に応じて16GB以上推奨。Gemma 4を使う場合は追加依存が必要。
- データ運用：GCS / BigQuery からのシャードストリーミングに対応。ローカルに terabyte 単位で落とさずに学習でき、企業データの扱いで有利。
- ワークフロー：CLI（gemma-macos-tuner）のウィザードでモデル選択／データ設定／学習実行をガイド。出力は run ディレクトリにメタ情報・メトリクス・LoRAアダプタを保存。
- 制約と注意点：大きなGemmaファミリ（26B/31B）は未対応の箇所あり。v1では一部処理がGemma 3n向けに最適化されているため、Gemma 4は追加設定が必要。MPSではbf16が推奨される場面あり。

## 実践ポイント
- まずは環境準備：arm64ネイティブPythonで仮想環境を作り、PyTorch（MPSビルド）を入れる。gemma-tunerをpip install -e .で開発インストール。
- ウィザード起動：gemma-macos-tuner wizard で対話的に設定ファイルを作成。Hugging FaceのGemmaアクセス権を事前に承認しておく。
- 小さめデータで練習：まずは低サンプルのオーバーフィットチェック（tiny_overfit）で学習パイプラインを検証。
- モダリティ別の設定に注意：image_token_budgetやtext_sub_mode（instruction/completion）など、訓練と推論で値を合わせること。
- 日本語運用のヒント：医療記録やコールセンター音声、業務書類のOCR後処理など日本語固有の語彙やアクセントに合わせたドメイン微調整で効果が出やすい。機密データはローカル学習で漏洩リスクを低減。
- リソース運用：ローカルRAM不足時はクラウドストリーミングを活用してSSD消費を抑制。大きなGemmaモデルを使う場合は別環境（GPUまたはGemma4用依存）を検討。

以上を踏まえ、まずは小さな日本語データセットでGemma 3nのLoRAを試し、実業務向けに音声認識やスクリーン理解などのドメイン適応を進めると現場価値が高いです。
