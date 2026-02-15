---
layout: post
title: "Instead of AI reviewing code, I want AI to help humans review code - AIにコードをレビューさせるのではなく、人間のレビューを支援してほしい"
date: 2026-02-15T19:17:17.614Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Lee-WonJun/github-diff-ai-order-extension"
source_title: "GitHub - Lee-WonJun/github-diff-ai-order-extension"
source_id: 440958716
excerpt: "GitHub PRをAIが優先順に並べ替え、忙しいレビューの着手点を瞬時に示すChrome拡張"
image: "https://opengraph.githubassets.com/c1f7063d5a5b89e4f24e268b5beb6e5f6b0cf786f48e8c47f5076b6a3aa3ec70/Lee-WonJun/github-diff-ai-order-extension"
---

# Instead of AI reviewing code, I want AI to help humans review code - AIにコードをレビューさせるのではなく、人間のレビューを支援してほしい
AIが「どのファイルから見ればいいか」を並べ替えてくれるChrome拡張で、忙しいレビュー作業を認知的に楽にするアイデア。

## 要約
GitHubのPR差分ページでファイル表示順をAIが「レビュー優先度」順に並べ替えるChrome拡張。AIはファイルを論理的にグループ化して、リスクや理解しやすさに基づきスコア付けして並べ替える。

## この記事を読むべき理由
日本でもコードレビューはチームの生産性を左右します。大規模リポジトリやモノレポで「どこから読むべきか」が分からない問題に対して、AIで「見る順」を最適化する発想は即効性のある現場改善案です。

## 詳細解説
- 仕組み
  - Chrome拡張（MV3）でGitHubのPR差分ページのSPA遷移を検知し、差分ブロックを再配列するUIパネル（Original / AI Order）を出す。
  - AIにはファイルパスと切り詰めたパッチを送り、各ファイルに0–100のスコアとグループ情報を返してもらう。拡張はDOM上でスコア順にdiffブロックを並べ替える。
- AIのプロンプト方針（3段階）
  1. 論理的に結びつくファイルをグループ化
  2. グループをリスク順（例：セキュリティ→コアロジック→マイグレーション→パフォーマンス→リファクタ→テスト）で並べ替え
  3. 各グループ内は理解しやすさ優先（インターフェース→実装→呼び出し箇所→テスト）
- 実装と制約
  - GitHubの差分UIはReact＋仮想化されており、DOMを直接移動するとReactの内部状態とズレて「新しいレビューが作れない」などの問題が発生する（致命的な既知問題）。
  - GitHubのUI変更や差分のバーチャライゼーションに脆弱で、動作保証なし。現状はGroq（llama-3.3系）での動作確認のみ。
  - キャッシュはPRのhead SHAや設定に基づきローカルに保存（HEADありでTTL7日、なければ1日）。
  - オプションでプロンプトプロファイル（nodejs, csharpなど）、無視パターン（lockファイルやdist等）、AIプロバイダ設定を変更可能。
- 作者コメント
  - 多くはAIがコード生成。DOM操作部分で手作業と試行錯誤が必要になったため、安定公開（Chrome Web Store）予定はない。

## 実践ポイント
- 試す手順：リポジトリをクローン→chrome://extensionsでデベロッパーモード→Load unpackedで extension/ を読み込む→PRを /changes 経由で開く。
- 使い方：AI Orderで並べ替え、元に戻すにはOriginal。必ず「書き込み前はOriginalに戻す」こと（新規レビューが作れなくなるため）。
- 設定のコツ：無視パターンにビルド成果物やロックファイルを入れて不要な差分をAIに送らない。プロンプトプロファイルを言語/コンテキストごとに用意。
- 運用注意：機密リポジトリや企業ポリシー下ではAPIキーの取り扱いに注意。まずは公開リポジトリや小さなPRで挙動を確認すること。
- アイデア拡張：並べ替え結果をレビュー用チェックリストに自動変換する、あるいは差分ブロックをコピーしてローカルで段階的に読むワークフローなど、現場向けの発展が考えられる。

短時間で「どこを先に見るか」を提示してくれるシンプルな提案は、レビュー工数削減のヒントになりますが、現状の技術的制約（DOM操作による副作用）を踏まえ、まずは慎重に試すのが現実的です。
