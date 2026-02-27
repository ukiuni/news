---
layout: post
title: "Show HN: Badge that shows how well your codebase fits in an LLM's context window - LLMのコンテキストウィンドウにコードベースが収まるかを示すバッジ"
date: 2026-02-27T16:19:32.145Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/qwibitai/nanoclaw/tree/main/repo-tokens"
source_title: "nanoclaw/repo-tokens at main · qwibitai/nanoclaw · GitHub"
source_id: 47181471
excerpt: "READMEに貼るだけでリポジトリがLLMのコンテキストに収まる割合と対策を視覚化するバッジ。"
image: "https://repository-images.githubusercontent.com/1146738089/83c0975f-09b4-4452-8c80-c5fee3521005"
---

# Show HN: Badge that shows how well your codebase fits in an LLM's context window - LLMのコンテキストウィンドウにコードベースが収まるかを示すバッジ
あなたのリポジトリが「LLMのコンテキストに入るか」を一目で示すバッジで、READMEに貼ればチームや採用候補者に親切な可視化ができます。

## 要約
リポジトリ内のソースをトークン化して、指定したLLMのコンテキストウィンドウ（例: 4k/8k/32kトークン）に何％収まるかを算出し、ステータスを示すSVGバッジを生成するツールです。

## この記事を読むべき理由
日本でもモノレポ・ドキュメント大規模化が進み、LLMを活用したコード検索や自動化を安全かつ効率的に進めるには「実際にモデルに入る情報量」を把握することが重要だからです。バッジはチームに現状を即座に伝える有効な指標になります。

## 詳細解説
- なにをするか：リポジトリ内のファイルをモデルのトークナイザでトークン数に変換し、合計トークン数をモデルのコンテキストウィンドウ長で割って「フィット率」を算出。結果を色付きのSVGバッジ（OK/Warning/Too Largeなど）として出力します。  
- 技術的ポイント：
  - トークン化：実際のLLM（例: GPT系）と同じトークナイザを使うことが重要。トークン化はバイトペアやサブワードに基づくため、単純な行数では推定できません。
  - 境界条件：READMEや大きなバイナリ（.png/.jar等）は除外したい。ツールは除外パターンを設定可能です。
  - バッジ生成：SVGで生成し、READMEに直接埋め込める。CI（GitHub Actions）で定期生成して更新する運用が想定されています。
  - 運用インパクト：コンテキストが足りないときは、重要ファイルだけ抜粋する、外部KBを作りRAG（Retrieval-Augmented Generation）を採用する、埋め込み検索に切り替える等の対処が必要です。
- 実装例（オープンソース実装の流れ）：リポジトリ走査 → トークナイザ呼び出し（言語ごとに最適化）→ 合計→ モデルウィンドウとの比較 → SVG生成 → README更新/GitHub Actions経由で差し替え。

## 実践ポイント
- まずローカルで実行してフィット率を確認する（大きなファイルをまず除外する）。  
- GitHub Actionsに組み込み、PRや日次でバッジを更新して見える化する。  
- フィット率が低ければ：不要ファイル除外／重要ファイルのみ抜粋／RAG＋ベクタDB導入／より大きなコンテキストを持つモデル利用を検討する。  
- 日本語ドキュメントはトークン化で増える傾向があるため、実測での確認を必ず行う。  

以上を踏まえ、READMEにバッジを貼るだけでチーム内外に「このリポジトリがLLMにどれだけ渡せるか」を簡単に示せます。
