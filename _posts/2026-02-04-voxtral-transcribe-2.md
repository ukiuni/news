---
layout: post
title: "Voxtral Transcribe 2 - Voxtral Transcribe 2（ボクストラル・トランスクライブ2）"
date: 2026-02-04T15:57:34.837Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mistral.ai/news/voxtral-transcribe-2"
source_title: "Voxtral transcribes at the speed of sound. | Mistral AI"
source_id: 46886735
excerpt: "Voxtral Transcribe 2：サブ200ms低遅延で低コスト高精度な13言語対応音声認識"
image: "https://mistral.ai/img/mistral-cover.png"
---

# Voxtral Transcribe 2 - Voxtral Transcribe 2（ボクストラル・トランスクライブ2）
サブ200msで会話をほぼリアルタイム文字化――低コスト×高精度を両立したMistralの最新音声認識

## 要約
Mistralが発表した「Voxtral Transcribe 2」は、バッチ向けのVoxtral Mini Transcribe V2と低遅延のVoxtral Realtimeを軸に、13言語対応・話者分離（diarization）・単語単位のタイムスタンプを低コストで提供する音声認識スイートです。

## この記事を読むべき理由
日本のカスタマーサポート、会議録作成、ライブ字幕やボイスエージェントの低遅延化といった実務ニーズに直結する進化で、オンプレ展開やエッジ実行が可能なためプライバシー対応やコスト削減にも有効です。

## 詳細解説
- モデル構成  
  - Voxtral Mini Transcribe V2：バッチ処理向け、長時間（最大3時間）処理、話者分離・単語タイムスタンプ・コンテキストバイアス（最大100語）をサポート。FLEURSベンチで約4%の平均WER（低いほど良い）。価格は約$0.003/分。  
  - Voxtral Realtime：ストリーミング専用アーキテクチャで、音声到着に合わせて逐次文字化。遅延は設定可能でサブ200msまで対応。4Bパラメータでエッジ実行も想定、Apache 2.0でウェイト公開（Hugging Faceで入手可）。API利用は約$0.006/分。  
- 性能と特徴  
  - 13言語対応（日本語含む）で非英語の性能も強化。  
  - 話者分離（diarization）、単語単位の開始/終了タイムスタンプ、コンテキストバイアス（固有名詞や業界語の補助。英語最適化、他言語は実験的）。  
  - ノイズ耐性と低コスト性能（他社モデルと比較してコスト効率が高いと主張）。  
  - Mistral Studioの「オーディオプレイグラウンド」から最大1GB・最大10ファイルをアップロードして即テスト可能（.mp3/.wav/.m4a/.flac/.ogg対応）。  
- 制約・挙動  
  - 重なり話者（オーバーラップ）では一般に一方の話者のみを文字化する傾向あり。  
  - コンテキストバイアスの多言語対応はまだ完全ではない点に注意。  
- 企業向け配慮  
  - オープンウェイトでオンプレ・プライベートクラウド展開が可能なため、GDPRや医療系の規制対応（HIPAA相当）に適した導入がしやすい。

## 実践ポイント
- まずMistral Studioのオーディオプレイグラウンドで手持ち音声を試す（フォーマット・サイズ上限あり）。  
- リアルタイム応答が必要な音声UIやボイスエージェントはVoxtral Realtimeを検討（サブ200msで自然な会話体験）。  
- 会議録・インタビューの大量処理はMini V2でコスト削減（話者ラベル・単語タイムスタンプで検索や字幕生成が容易）。  
- 固有名詞や業界用語はコンテキストバイアスを活用。ただし日本語など非英語は結果を検証しつつ運用する。  
- プライバシー要件が高い場合はApache 2.0のRealtimesウェイトを利用してオンプレ展開を検討する。

以上を踏まえ、まずはプレイグラウンドで品質・遅延・話者分離の挙動を確認すると早いです。
