---
layout: post
title: "Show HN: AutoShorts – Local, GPU-accelerated AI video pipeline for creators - AutoShorts：ローカルGPUで高速生成するAIショート動画パイプライン"
date: 2026-01-25T10:14:33.991Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/divyaprakash0426/autoshorts"
source_title: "GitHub - divyaprakash0426/autoshorts"
source_id: 46751675
excerpt: "ローカルGPUでゲーム映像を自動解析してバズ狙い縦型ショートを量産できるツール"
image: "https://opengraph.githubassets.com/f9640671f736f23f6dd08b38024b5ad89a1d6a6f9c621035d80428882c6af5d9/divyaprakash0426/autoshorts"
---

# Show HN: AutoShorts – Local, GPU-accelerated AI video pipeline for creators - AutoShorts：ローカルGPUで高速生成するAIショート動画パイプライン

ゲームプレイ動画から「バズりやすい」縦型ショートをGPUでローカル生成するオープンソースツール、AutoShortsをわかりやすく紹介します。

## 要約
AutoShortsは、GPU加速の映像解析＋AI（OpenAI/Gemini/Whisper等）でゲーム映像の見せ場を検出し、縦型ショートを自動で切り出し・字幕・音声合成まで行うローカルパイプラインです。

## この記事を読むべき理由
- 日本のゲーム配信者や動画編集者が「手間をかけず短尺コンテンツ」を量産できるため収益化や視聴者獲得に直結します。
- データをクラウドに上げずローカルで処理できるため、プライバシーやコスト面で魅力的です。

## 詳細解説
- コア機能
  - シーン解析：OpenAI（gpt-5-mini / gpt-4o）やGoogle Geminiで「action／funny／highlight／mixed」を判定。AIスコアと音声／映像ヒューリスティクスを組み合わせて重要シーンをランク付け（デフォルト音声0.6・映像0.4）。
  - 字幕：Whisperで音声転写、あるいはAI生成のキャプション。PyCapsテンプレートでスタイリング。
  - TTS：ローカルTTS（ChatterBox）で音声合成。声のクローンや感情調整、20言語以上対応（日本語含む）。
- 高速化と実装技術
  - GPU処理：decord + PyTorchでGPUストリーミング解析、cupyでCUDAベースの画像処理、NVENCで高速ハードウェアエンコード。
  - フォールバック：NVENCが使えない場合はlibx264、PyCapsが失敗したらFFmpeg焼き込み等で堅牢に動作。
- 要件と導入方法
  - 推奨：NVIDIA GPU（CUDA 12.x対応、RTX系列推奨）、Python 3.10、FFmpeg 4.4.2
  - インストール：Makefile（conda/micromamba自動）推奨／GPU対応Dockerイメージあり。
- 開発向け
  - デバッグ用環境変数で解析やレンダをスキップ可能。テストはGPUなしでもCI向けにモックで実行可。
- ライセンス：MIT

## 実践ポイント
- まず試す（基本コマンド）:
```bash
git clone https://github.com/divyaprakash0426/autoshorts.git
cd autoshorts
make install
source .venv/bin/activate
python run.py
```
- すぐに使える設定
  - .env を .env.example からコピーして AI_PROVIDER（openai/gemini/local）や SEMANTIC_GOAL（mixed推奨）、TARGET_RATIO_W/H=9:16 を設定。
  - 字幕を重視するなら ENABLE_SUBTITLES=1、音声合成を使うなら ENABLE_TTS=1 と TTS_LANGUAGE=ja を設定。
- ハードウェアがない場合：NVENCが無ければ libx264 にフォールバックするが処理は遅くなるため、小規模テストは DEBUG_SKIP_RENDER=1 で解析のみ試す。
- 日本向けの活用案：実況者や配信アーカイブを短尺化してTikTok/YouTube Shortsに展開。ローカル処理＋日本語TTSでプライバシーとブランド維持が可能。

AutoShortsは「ローカルで高速に」「ほぼ自動で」短尺を量産したいクリエイターに有望なツールです。興味があればリポジトリのREADMEでインストール手順と.env設定を確認してください。
