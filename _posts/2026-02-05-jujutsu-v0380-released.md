---
layout: post
title: "jujutsu v0.38.0 released - jujutsu v0.38.0 リリース"
date: 2026-02-05T17:06:37.693Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jj-vcs/jj/releases/tag/v0.38.0"
source_title: "Release v0.38.0 · jj-vcs/jj · GitHub"
source_id: 759847242
excerpt: "jj v0.38.0：設定を外部化し安全化、Git2.41必須化やrevset強化の影響を確認"
image: "https://opengraph.githubassets.com/45d26bb828538d4e9e0c47378e4db12018bec068ff472ab21290f476a780f2be/jj-vcs/jj/releases/tag/v0.38.0"
---

# jujutsu v0.38.0 released - jujutsu v0.38.0 リリース
魅力的なタイトル: 「jjが大幅アップデート：設定の安全化とGit 2.41依存で何が変わるのか？」

## 要約
jj v0.38.0ではリポジトリ外への設定移動（セキュリティ向上）、Git 2.41以上の必須化、revset／テンプレート周りの機能追加と多くのバグ修正が導入されました。既存リポジトリは自動移行されます。

## この記事を読むべき理由
日本でもjjはGit互換の代替VCSとして注目を集めています。今回のリリースは開発フロー（ローカル設定の安全性、リモート連携、CI／macOS環境）に直結するため、プロジェクト運用者や個人開発者は影響を把握して対応する必要があります。

## 詳細解説
- 設定の保護：per-repo・per-workspaceの設定がリポジトリ内から外部へ移動。セキュリティ目的での変更で、旧来の .jj/repo/config.toml や .jj/workspace-config.toml は使われなくなります。既存リポジトリは自動で新フォーマットに移行されるため手動移行は基本不要ですが、運用ポリシーを確認してください。
- Gitバージョン制約：最小サポートGitが 2.41.0 に引き上げられました。macOSユーザーはDeveloper Toolsを26へアップデートするか、Homebrew等でGitを入れ替える必要があります。
- 互換性・廃止：ui.always-allow-large-revsets と all: revset modifier の廃止、diff_contains() → diff_lines() など関数名の変更、legacy placeholder（unset user.name/user.email）の挙動変更など、いくつかの破壊的/非推奨変更があります。
- 新機能ハイライト：
  - jj git fetch が放棄された（abandoned）コミットの詳細を表示。
  - jj git push --bookmark <name> が未追跡ブックマークを自動追跡。
  - git_web_url([remote]) テンプレート関数：remote URL をブラウザ用URLに変換。
  - divergent() revset、remote_tags() revset、タグのフィルタリングなど revset 機能強化。
  - revset／テンプレートでエイリアスによる文字列置換が可能に（例：grep(x) = description(regex:x)）。
  - hyperlink() テンプレート関数が非端末出力時に安全にフォールバック。
  - 実験的：jj git fetch --tag によりタグ取得の振る舞いを細かく制御可能。
- バグ修正：Git worktree内での colocate 初期化拒否、fetch/push時のstderr転送改善、Watchman利用時の .gitignore 変更検知向上、コンフリクトラベルの復元精度向上など、日常の運用で遭遇しやすい問題が多数改修。

## 実践ポイント
- まずやること：
  1. ローカル環境で Git を 2.41.0 以上に更新（macOSはDeveloper Tools更新または Homebrew Git）。
  2. jj を最新版にアップデートして、既存リポジトリの自動移行を確認する（バックアップ推奨）。
- 設定の見直し：
  - .jj/repo/config.toml 等の古い設定ファイルが残っていないか確認し、新しい配置やグローバル設定方針を決める。
  - 廃止された設定(ui.always-allow-large-revsets 等)や変更された関数名(diff_contains→diff_lines)をCIやスクリプトで検索し更新。
- 新機能を試す：
  - git_web_url() や hyperlink() をテンプレートに組み込んでレビューやツール連携を改善。
  - jj git fetch の放棄コミット表示や --tag オプション、divergent()/remote_tags() でリモート同期の可視化を試す。
- チームでの共有：
  - リポジトリ運用ルールやCI設定（Gitバージョン要件含む）を周知。mac/macOSでのビルドサーバやチェックランナーの確認も忘れずに。

短めにまとめると、今回のv0.38.0は「セキュリティ（設定移動）＋運用改善（Git必須バージョン、revset/テンプレート強化）」が主眼です。アップデート前にGitバージョンと設定の互換性をチェックしてください。
