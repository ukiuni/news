---
  layout: post
  title: "Show HN: I replaced Beads with a faster, simpler Markdown-based task tracker - Beadsを置き換えた、より高速でシンプルなMarkdownベースのタスクトラッカー"
  date: 2026-01-06T07:10:34.176Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/wedow/ticket"
  source_title: "GitHub - wedow/ticket: Fast, powerful, git-native ticket tracking in a single bash script. Dependency graphs, priority levels, zero setup."
  source_id: 46487580
  excerpt: "単一のBashスクリプトでGitネイティブなMarkdownチケット管理を即導入できる軽量トラッカー"
  image: "https://opengraph.githubassets.com/b7e0cc04a3c369bba916426df4bb5a08bbac2320c7391a5b36ebe0a15a5b567d/wedow/ticket"
---

# Show HN: I replaced Beads with a faster, simpler Markdown-based task tracker - Beadsを置き換えた、より高速でシンプルなMarkdownベースのタスクトラッカー
CLIで完結する“tk”——1つのBashスクリプトでGitネイティブなチケット管理を即戦力化する方法

## 要約
単一のBashスクリプト「tk」は、.tickets/ 以下のMarkdownファイル（YAMLフロントマター付き）でチケットを管理し、依存関係グラフや優先度をGitワークフローに自然に統合する軽量チケットトラッカーです。

## この記事を読むべき理由
日本の開発現場ではモノリポ／Git中心ワークフロー、CLI志向、小さなチームでの迅速な立ち上げが好まれます。tkはDBや常駐デーモン不要でCI／エディタ連携しやすく、既存のBeadsユーザーや軽量な課題管理を求めるチームに即戦力になります。

## 詳細解説
- データモデル：各チケットは .tickets/ に置かれたMarkdownファイル。先頭にYAMLフロントマターでメタ（id、status、priority、assignee、depsなど）を持つため、人間にもAIにも読みやすい。
- 実装：単一のportableなBashスクリプト（coreutilsのみ依存）。クエリにはjqを使用し、ripgrep(rg)があればそれを使うフォールバックあり。最小限の外部依存でどのPOSIX環境でも動く設計。
- 主なコマンド（抜粋）：
  - create [title]（--description, --type, --priority, --assignee 等）
  - start/close/reopen/status（ステータス管理）
  - dep / dep tree / undep（依存関係操作・ツリー表示）
  - ls / blocked / ready（状態別一覧）
  - show / edit / add-note（表示・編集・追記）
  - query [jq-filter]（JSON出力でカスタム集計が可能）
  - migrate-beads（Beadsからの移行サポート）
- Gitとの親和性：チケットがファイルなのでgit logやIDEの「Ctrl/Cmd+Click」で直接チケットへジャンプできる。差分も通常のGit操作で管理。
- AIエージェント対応：CLAUDE.mdやAGENTS.mdに一行追加すれば、Claude等のエージェントが自然にチケットを参照できる（長大なJSONLを投げない設計が利点）。
- インストール・要件：Homebrew/AUR/ソースから。jq必須。bash＋coreutilsだけで動くためサーバやWSLでも手軽に使える。

## 実践ポイント
- 試用はサイドブランチで：まず既存リポジトリに .tickets/ を作ってtkを導入し、少数チケットで運用感を確認。
- Beads移行が簡単：tk migrate-beads を使えば既存データをMarkdown化できる。移行後は .beads を削除してコミット。
- CI連携例：tk query | jq を使い、PR作成時に未解決依存や優先度0チケットの有無をチェックするワークフローを追加。
- エディタとの親和性：VS CodeなどでチケットIDをファイル名にしておけば、ログやPR本文から直接開ける。チームのテンプレート（CLAUDE.md）に操作方法を追記しておくとエージェント連携がスムーズ。
- カスタム集計：tk query のJSON出力にjqフィルタをかけるだけで、スプリントレポートやリリース向けの一覧を自動生成できる。

簡単な使い方例：
```bash
# bash
tk create "ログインのSSE接続管理を追加" -t feature -p 1 -a alice
tk dep nw-5c46 nw-4a12         # nw-5c46はnw-4a12に依存
tk status nw-5c46 in_progress
tk query '.[] | select(.status=="in_progress") | {id, title, priority}'
```

最後に：重厚な課題管理ツールが合わない、小回り良くGit中心で回したい日本のチームには有力な選択肢。まずは数日試してCIとエディタ連携を作るだけで、運用コストが大きく下がる可能性があります。
