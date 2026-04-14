---
layout: post
title: "Build a Talking Robot with Gemini Live and Reachy Mini - Gemini Live と Reachy Mini で会話するロボットを作る"
date: 2026-04-14T23:12:29.496Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/googleai/build-a-talking-robot-with-gemini-live-and-reachy-mini-20e2"
source_title: "Build a Talking Robot with Gemini Live and Reachy Mini - DEV Community"
source_id: 3477336
excerpt: "机上のReachy MiniがGemini Liveで会話・表情・ダンスする低遅延実装ガイド"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fbr8pwufki7xmua8ahpn4.png"
---

# Build a Talking Robot with Gemini Live and Reachy Mini - Gemini Live と Reachy Mini で会話するロボットを作る
机の上に「聞いて、話して、踊る」小型ロボットを置こう — Gemini Liveでリアルタイム音声LLMとReachy Miniをつなぐ方法

## 要約
Gemini Live（リアルタイム音声LLM）とReachy Miniを連携させ、マイク入力→LLM→モーター／ツール呼び出しまでを低遅延で回すオープンソースの会話アプリを紹介。音声対話・表情・ダンス・顔追跡を統合し、プロファイルで性格を簡単に切替可能。

## この記事を読むべき理由
日本のハード×ソフト好き、教育・研究・プロトタイプ開発者にとって、手元のロボットを「会話するインターフェース」に変える具体的手法と実装アーキテクチャが学べるから。実機がなくてもシミュレーションで試せる点も実践的。

## 詳細解説
- アーキテクチャ（4層）
  - マイク（16bit PCM, 16kHz）→ fastrtc（低遅延WebRTC I/O・サンプリング変換）
  - Gemini Live / OpenAI Realtime ハンドラ（MODEL_NAMEで切替可）— セッション経由で双方向ストリーム
  - ツールディスパッチ層 — ダンス、表情、カメラ、頭追従などを関数呼び出しとして扱う
  - MovementManager（60Hzループ）— プライマリ（順次再生）とセカンダリ（加算オフセット：発話揺れ・顔追跡）を合成して動作指令を送る

- オーディオループ
  - マイク→16kHzでLLMへ送信。LLM側の応答は音声チャンク（24kHzで再生キューへ）、入力/出力文字起こし、ツール呼び出し、割込みシグナルなどを同一セッションで受信。

- ツール呼び出し（Function Calls）
  - LLMが dance(name='macarena') のように関数呼び出しを行うと、BackgroundToolManagerが非同期でタスク実行し、結果をFunctionResponseとしてLLMに返す（音声ストリームをブロックしない設計）。

- 動きと常時表現
  - MovementManagerは60Hzで動作。何もないときは「呼吸アニメ」（軽い揺れ＋アンテナ）で常時生気を演出。

- 映像（任意）
  - カメラ接続時は1FPSでJPEGを送信して視覚コンテキストを提供。自動的に見たものについてコメント可能。

- パーソナリティ（プロファイル）
  - profiles/ 以下の instructions.txt（システムプロンプト）と tools.txt（有効ツール）で性格を定義。可搬な断片（テンプレート）で複合的に組み合わせ可能。Pythonファイルでカスタムツールも追加できる。

- デプロイと切替
  - ローカル推奨。MODEL_NAMEでGemini Live（既定）かOpenAI Realtimeを選択。カメラやローカルVLM等のオプションも extras でインストール可能。

## 実践ポイント
- 必要なもの
  - Python 3.10+, Reachy Mini（物理 or MuJoCoシミュレーション）、Gemini APIキー、マイク／スピーカー
- リポジトリ取得と環境構築（例）
```bash
# Clone
git clone https://github.com/pollen-robotics/reachy_mini_conversation_app.git
cd reachy_mini_conversation_app

# 仮想環境（uv使用例）
uv venv --python python3.12 .venv
source .venv/bin/activate
uv sync
```
- 環境変数設定
```bash
cp .env.example .env
# .env に GEMINI_API_KEY=your-gemini-api-key-here を設定
```
- Reachy Mini デーモン（別ターミナルで常時実行）
```bash
# 物理
reachy-mini-daemon
# シミュレーション
reachy-mini-daemon --simulation
```
- 会話アプリ起動
```bash
reachy-mini-conversation-app
# Web UI（Gradio）
reachy-mini-conversation-app --gradio
```
- カスタマイズのコツ
  - プロファイルを profiles/ に作り instructions.txt と tools.txt を用意すれば、Pythonを書かずに性格変更可能。
  - 独自ツールは profiles/<name>/ に Python ファイルを置き tools.txt に追加。
  - ハードがないときはシミュレータ＋ローカルVLM（extras）で日本語評価やUI実験ができる。
  - OpenAI Realtimeを試す場合は MODEL_NAME=gpt-realtime、OPENAI_API_KEY を設定。

日本語の会話や日本語プロンプトを試す際は、プロファイル内 instructions.txt に日本語で明示的な振る舞いを指定すると安定して期待通りの応答が得られる。
