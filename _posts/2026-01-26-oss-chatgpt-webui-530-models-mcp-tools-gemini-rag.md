---
layout: post
title: "OSS ChatGPT WebUI – 530 Models, MCP, Tools, Gemini RAG, Image/Audio Gen - OSS版 ChatGPT WebUI：530モデル、MCP、ツール、Gemini RAG、画像／音声生成"
date: 2026-01-26T16:16:48.845Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://llmspy.org/docs/v3"
source_title: "v3 Release Notes"
source_id: 46766432
excerpt: "530超モデル対応＆拡張自在なOSS WebUIで社内RAGや画像・音声生成を即試せる"
image: "http://localhost:3000/og/docs/v3/image.png"
---

# OSS ChatGPT WebUI – 530 Models, MCP, Tools, Gemini RAG, Image/Audio Gen - OSS版 ChatGPT WebUI：530モデル、MCP、ツール、Gemini RAG、画像／音声生成
魅力的タイトル: 「手元で“何でもできる”AIデスクトップ — 530モデル対応の拡張自在なOSS WebUIがもたらす現場変革」

## 要約
llms.py v3はmodels.dev連携で530以上のモデルに対応し、拡張性を最優先に再設計されたOSSのWeb UI。Gemini RAGやツール呼び出し、画像/音声生成、SQLite保存など実務向け機能が一気に増強された。

## この記事を読むべき理由
日本の開発現場やプロダクト運用では「社内データで安全にRAGを回す」「多様なモデルを試す」「軽量に配布する」ニーズが高い。本改良はそれらをOSSレベルで実現でき、国内の検証や導入コストを大幅に下げる可能性があるから。

## 詳細解説
- 530+モデル（24プロバイダ）
  - models.devカタログ採用で幅広いモデルへ即アクセス。プロバイダごとの固有機能も拡張で活用可能。
- 新・モデルセレクタ
  - 検索、フィルタ、ソート、お気に入り、リッチカードで大量モデルから最適モデルを発見しやすく。
- 拡張（Extensions）アーキテクチャ
  - UI/Server双方をプラグイン化。拡張は ~/.llms/extensions に置くか GitHub からインストール可能。コア機能も拡張として扱うためカスタム構成が容易。
  - サーバフック：__parser__, __install__, __load__, __run__ を利用。
  - UI拡張は ui/index.mjs の install(ctx) でコンポーネント登録可能。
- Gemini RAG拡張
  - Google Gemini File Search Stores と同期するフィルストア管理、ドラッグ＆ドロップアップロード、カテゴリ管理、RAGチャットでソース付き応答を実現。
  - バックグラウンドワーカーで非同期に文書をインデックス化。
- ツール（Function Calling）サポート
  - Python関数をツールとして登録し、LLMからローカル環境呼び出しが可能（例：時刻取得など）。エージェント的な自動化が容易に。
- MCP（Model Context Protocol）対応
  - 外部MCPサーバ接続で拡張ツール能力や分散実行が可能。
- メディア生成・再生
  - 画像生成（Google/OpenAI/Nvidia/Chutes等）、音声合成（Gemini TTS など）、メディアギャラリーで生成物管理。
- 開発者UX強化
  - Run Code UI（Python/JS/TS/C#実行）、Calculator UI、KaTeXレンダリング、CodeMirror エディタなど。
- 永続化と運用性
  - IndexedDB からサーバサイド SQLite に移行（同時利用と堅牢性向上）。アセットキャッシュとメタデータ保存。
- 自動プロバイダ更新
  - providers.json は日次更新。ローカルで必要なプロバイダのみ保持可能。
- デプロイと導入
  - pip install llms-py、Dockerやカスタムビルドで軽量配布可能。llms コマンドで拡張管理。

## 実践ポイント
- まず試す（ローカル検証）
  - pip install llms-py
  - llms --update-providers
- Gemini RAGを試す
  - llms --add gemini でフィルストアを追加し、日本語の社内マニュアルをアップしてRAGで検証。
- プロバイダ有効化（例）
```json
{
  "openai": { "enabled": true },
  "xai": { "enabled": true }
}
```
- 拡張運用
  - 必要な機能は拡張化して管理（例：社内認証、独自プロバイダ、検索ツール）。
- 本番配備
  - SQLiteストレージ＋Dockerでチーム共有サーバを立て、アクセス管理とバックアップを整備する。
- セキュリティ注意
  - RAG用データやAPIキーはローカル/社内サーバへ保管し、公開クラウド連携は用途を吟味する。

短くまとめると、llms.py v3は「多数のモデル選択肢」と「拡張自在なプラグイン構造」で、社内RAGやプロトタイピングを迅速に進められる実務向けOSSです。日本語データでのRAG運用や軽量デプロイを検討しているチームには即チェック推奨。
