---
layout: post
title: "Show HN: Context Mode – 315 KB of MCP output becomes 5.4 KB in Claude Code - Show HN: Context Mode — 315 KBのMCP出力がClaude Codeで5.4 KBに"
date: 2026-02-25T06:50:47.455Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mksglu/claude-context-mode"
source_title: "GitHub - mksglu/claude-context-mode: Stop losing context to large outputs."
source_id: 47148025
excerpt: "Context Modeで315KBを5.4KBに削減、Claude Codeの文脈枯渇を防ぐ"
image: "https://opengraph.githubassets.com/4e4f5352253729c9827417b94f92ab4106e4ab3db74a103ab545b9120c65fdf3/mksglu/claude-context-mode"
---

# Show HN: Context Mode – 315 KB of MCP output becomes 5.4 KB in Claude Code - Show HN: Context Mode — 315 KBのMCP出力がClaude Codeで5.4 KBに

あなたのAIが「コンテキスト不足」で止まるのを防ぐ――出力をサンドボックス化して200KB窓を守る新ツール

## 要約
MCP（Model-Connector-Protocol）経由のツール出力でトークン残量を圧迫する問題に対し、Context Modeは出力をサンドボックスで処理して要点だけをモデルに渡すことで、315KBを5.4KBに削減（約98%節約）する仕組みを提供します。

## この記事を読むべき理由
Claude CodeなどMCP対応エージェントを使うと、テスト結果・ログ・スクレイプ等の大きな出力ですぐコンテキストが埋まります。日本の開発現場でもCIログ・大規模レポジトリ解析・ドキュメント検索で同じ問題が起きるため、この技術は生産性向上に直結します。

## 詳細解説
- 問題点：MCPはツール定義と生の出力をそのままコンテキストに入れるため、複数ツール利用で200K窓が瞬時に消費される。例：Playwrightスナップショット56KB、20件のGitHub Issueで59KBなど。
- アプローチ：Context ModeはClaude Codeとツールの間にMCPサーバを挟み、ツール出力をサンドボックスで実行・解析。生データは外に出さず、要約や検索可能な抜粋だけをコンテキストに送る。
- サンドボックス：各execute呼び出しは独立プロセスで実行。stdoutのみを取り込み、ファイルやAPIレスポンス等の生データは隔離。JS/TS/Python/Ruby/Go/Rustなど10言語対応、Bunで高速化。gh/aws/gcloud等のCLIは資格情報を透過で使えるが会話側には露出しない。
- 意図駆動フィルタ：出力量が5KBを超え、意図（intent）がある場合は全文をインデックス化して関連部分だけを抽出して返す。これにより必要な箇所だけコンテキストへ。
- ナレッジベース：Markdownを見出し単位でチャンク化してSQLite FTS5に格納。検索はBM25＋ポーター語幹処理で関連スニペットを賢く抜き出す（切り出しは単純切り取りではない）。
- 運用機能：進行中のセッションで消費統計を出すstatsツール、過剰な検索を抑えるプログレッシブスロットリング、サブエージェント向けの自動ルーティング（PreToolUse hook）で面倒な設定不要。
- 実測例：Playwright 56.2KB→299B、20件Issue 58.9KB→1.1KB、全体で315KB→5.4KB。セッション持続時間を約30分から約3時間に延長。

## 実践ポイント
- 必要要件：Node.js 18+、Claude Code（MCP対応）。Bunは任意で高速化。
- 試し方：リポジトリをクローンしてローカルで起動、またはClaudeのプラグインとしてインストールすると自動ルーティングが働きます。導入後は /context-mode stats で節約効果を確認。
- 運用ヒント：大量ログ解析やリポジトリ調査は batch_execute や search(queries: [...]) でまとめて投げる。fetch_and_indexでWebページを取り込みつつ生データを保護できる。
- 期待効果：CIログやドキュメント検索、スクレイピング結果の扱いが楽になり、MCPベースのエージェントを長時間・大規模に運用しやすくなる。

（参考：GitHub リポジトリ "mksglu/claude-context-mode" のREADMEに実装・ベンチマークと導入手順あり）
