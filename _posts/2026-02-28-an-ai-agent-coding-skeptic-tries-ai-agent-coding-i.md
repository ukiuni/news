---
layout: post
title: "An AI agent coding skeptic tries AI agent coding, in excessive detail - AIエージェントでのコーディングを懐疑していた人が、徹底検証してみた話"
date: 2026-02-28T07:29:49.080Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://minimaxir.com/2026/02/ai-agent-coding/"
source_title: "An AI agent coding skeptic tries AI agent coding, in excessive detail | Max Woolf's Blog"
source_id: 728382299
excerpt: "懐疑派がOpus 4.5で実プロジェクトを自動実装、AGENTS.mdで安全運用を検証"
image: "https://minimaxir.com/2026/02/ai-agent-coding/featured.png"
---

# An AI agent coding skeptic tries AI agent coding, in excessive detail - AIエージェントでのコーディングを懐疑していた人が、徹底検証してみた話
エージェントは本当に使えるのか？懐疑派が実プロジェクトで試して得た“現実的な成果”と注意点

## 要約
著者は懐疑的だったが、最新LLM（特にAnthropicのOpus 4.5）に既存プロジェクトの改良や一連の開発タスクを任せたところ、高品質なPython実装、データ解析ノートブック、軽量Webアプリまで一発で出力でき、生産性向上を確認した。ただし設定（AGENTS.md）や秘密管理の注意が必須。

## この記事を読むべき理由
- 日本のエンジニアやデータサイエンティストが、実務で「エージェントに任せて良いこと／悪いこと」を見極めるための実例が得られる。  
- CopilotやClaude/Opusのようなツールを導入検討中のチームにとって、具体的な運用ルールや落とし穴が参考になる。

## 詳細解説
- 検証対象と経緯：著者は自作のgemimg（Nano Banana系API用ラッパー）を複数LLMに投げ、コード補完・リファクタリングを試行。結果としてdocstring／型注釈追加やよりPythonicな実装提案が得られた。
- AGENTS.mdの重要性：プロジェクトルートに置く指示ファイルで、コード整形や振る舞い（例：「MUST」「NEVER emoji」「.envのみ秘密を保持」など）を厳密に定義。これがエージェント結果の安定化に決定的だった。
- Opus 4.5の成果：YouTube Data APIをREST（httpx）で叩き、SQLiteへメタデータを蓄積するスクリプトを一発生成。続けてpolarsを使うJupyter Notebookでの探索的解析、FastAPI+HTMX+PicoCSSを使った簡易Webアプリ生成まで行い、いずれも実用レベルの品質だった。  
- 問題点と注意：ログにAPIキーが出力されるような実装ミスが残る場合があり、秘密管理のルール（.envを.gitignoreにする等）は必須。LLMは仕様を「読めない」ため、プロンプトやAGENTS.mdで細かく指示する必要がある。
- Rustやニッチ言語について：従来LLMはRust生成が弱かったが、モデル更新で改善傾向。とはいえ中級以上の言語理解はまだ人間による検証が必要。

## 実践ポイント
- プロジェクトに必ずAGENTS.md（ClaudeはCLAUDE.md）を用意し、守るべきルールを明記する（MUST/NEVER形式で重要ルールを強調）。  
- 大きなプロンプトはMarkdownファイルとして管理し、エージェントに実装させたら手動レビュー→明確なコミットメッセージで履歴を残す。  
- シークレットは.envと.gitignoreで運用、ログ出力での漏洩をチェックする自動テストを追加する。  
- 軽量なフロントはHTMX＋PicoCSS＋FastAPIの組み合わせで十分な場合が多く、日本の中小チームでも採用しやすい。  
- 初期は「単機能で検査しやすいタスク」から試し、成功パターンをAGENTS.mdに反映して運用を拡張する。

短く言えば：エージェントは“設定と監視”をきちんと行えば実用的。過度な期待は禁物だが、正しく使えば現場の生産性を確実に押し上げる。
