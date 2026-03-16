---
layout: post
title: "My Journey to a reliable and enjoyable locally hosted voice assistant - 信頼できて楽しいローカル音声アシスタントを作るまでの道のり"
date: 2026-03-16T16:38:06.398Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://community.home-assistant.io/t/my-journey-to-a-reliable-and-enjoyable-locally-hosted-voice-assistant/944860"
source_title: "My Journey to a reliable and enjoyable locally hosted voice assistant - Voice Assistant - Home Assistant Community"
source_id: 47398534
excerpt: "ホームアシスタントとローカル言語モデルで作る実用的で高速なオフライン音声アシスタント構築法"
image: "https://community-assets.home-assistant.io/optimized/4X/a/9/d/a9dbf25a9917cdee80a3f9e4d20450b5b5f8c291_2_937x1024.png"
---

# My Journey to a reliable and enjoyable locally hosted voice assistant - 信頼できて楽しいローカル音声アシスタントを作るまでの道のり
ローカルで動く音声アシスタントを「実用レベル」に仕上げるための最短ルートと落とし穴

## 要約
Home Assistant とローカルLLM（llama.cpp 等）を組み合わせ、プライバシーを保ちながら実用的な音声アシスタントを構築した実体験レポート。ハードウェア選定、音声認識/合成、プロンプト調整、音楽再生の自動化など具体的な改善点を共有します。

## この記事を読むべき理由
- Google/クラウド依存を避けたい日本の家庭や店舗向けに「オフラインで使える実用案」を知れる。  
- 初級者でも取り組める具体的ステップや注意点（モデル選び・プロンプト・Wakeword）が分かる。

## 詳細解説
- 構成要旨  
  - Home Assistant（HA）を中核に、ローカルLLMを Assist に接続。モデル実行は llama.cpp を推奨（ローカル高速化と低遅延のため）。  
  - 音声入力（STT）は Wyoming ONNX ASR（OpenVINO最適化）や Rhasspy / Faster Whisper、Nvidia Parakeet V2 を併用。音声出力（TTS）は Kokoro TTS や Piper（CPU実行）を検証。  
  - ハードは UnRaid 上のHA＋別途 Voice サーバ（Beelink Mini PC＋USB4 eGPU）が安定。GPUは性能で応答速度が変わる（下記参照）。

- GPU と体感応答（要約）  
  - RTX 3090 / RX 7900XTX (24GB)：高速（1–2s）で大規模モデル対応。  
  - RTX 5060Ti / RX 9060XT (16GB)：十分実用的（1.5–4s）。  
  - RTX 3050 (8GB)：小型モデル向け、基本機能なら可（約3s）。

- モデルと機能性  
  - GGML/GGUF 形式の高品質モデルを Hugging Face 等で選定。低量子化モデルだとツール呼び出しや誤認識の耐性が下がる。  
  - ある程度の「ツール呼び出し」「文脈理解」「誤聴解釈耐性」を期待するなら 9B〜20B級のモデルや MoE（混合専門家）モデルが望ましい。

- キモは「プロンプト」  
  - Assist の挙動はプロンプト次第で大きく変わる。ツールを確実に呼ばせる、不要な絵文字や冗長出力を排する、天気・営業時間などは専用セクションで指示するなどが効果的。実例を用意して反復チューニングする。

- 音楽再生と自動化の扱い  
  - LLM単体で完結しない場合、HA の automation（会話トリガー）＋ Music Assistant を組み合わせるパターンが有効。衛星デバイス（satellite）ごとに再生先をマッピングすることで自然な動作に。

- ウェイクワード  
  - WAF（家庭受容度）のためにカスタムウェイクワード（例: "Hey Robot"）を学習・導入。短時間でGPU上でトレーニング可能で実用域に。

- 注意点  
  - 初期設定やトラブルシュート（Wi‑Fi遅延、STTの誤認識、モデルの誤動作）は多い。根気と小さな検証を重ねる必要あり。

## 実践ポイント
1. ハード選定：まずは16GB級GPU（中古でも可）で試す。性能に不満なら上位へ。  
2. ランナー：llama.cpp を採用して低遅延化。GGUF 高品質モデルを使う。  
3. STT/TTS：OpenVINO最適化のSTTや Kokoro TTS を試し、応答の滑らかさを確認。  
4. プロンプト改善：各ツール（天気・検索・音楽）専用セクションと出力例を書いて繰り返し調整する。  
5. 音楽自動化：LLMに任せきれないところは会話トリガー＋Music Assistantで安定化。例（簡略）：  

```yaml
# yaml
alias: Music Shortcut
trigger:
  - platform: conversation
    command: "Play {music}"
action:
  - service: music_assistant.play_media
    data:
      media_id: "{{ trigger.slots.music }}"
    target:
      entity_id: "{{ states('input_select.last_active_speaker') }}"
  - service: conversation.set_response
    data:
      text: "Playing {{ trigger.slots.music }}"
mode: single
```

6. Wakeword：Microwakeword リポジトリでカスタム学習を行い、VPE/衛星へ配布。  
7. 日本語対応：日本語TTS/STTや日本語対応モデルを優先（モデルの日本語性能は要検証）。

最後に：すぐに「完璧」にはなりませんが、上記の段階を踏めばプライバシー重視で実用的なローカル音声アシスタントが作れます。興味があれば、どのステップから始めるか一緒に決めましょう。
