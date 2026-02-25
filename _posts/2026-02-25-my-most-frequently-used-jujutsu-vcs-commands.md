---
layout: post
title: "My most frequently used Jujutsu VCS commands - 私が最もよく使う Jujutsu（jj）VCS コマンド"
date: 2026-02-25T21:42:32.278Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://danverbraganza.com/writings/most-frequent-jj-commands"
source_title: "My most frequently used Jujutsu VCS commands | A Danver Braganza Extravaganza"
source_id: 396610144
excerpt: "jjコマンドでGit作業を劇的に高速化する実用チートシート（事例付き）"
---

# My most frequently used Jujutsu VCS commands - 私が最もよく使う Jujutsu（jj）VCS コマンド
jjで「日常のGit操作」をもっと速くする——覚えておくだけで生産性が上がる実用コマンド集

## 要約
日常的に使うjj（Jujutsu）コマンドだけに絞ったチートシート。少数のコマンドを覚えるだけで、Gitベースのワークフローをより快適にできる、という内容です。

## この記事を読むべき理由
日本の開発現場でもGitは標準ですが、jjはGitと共存しつつ「過去変更の編集」や「ブックマーク運用」を低摩擦で行えます。短時間で生産性改善を試したいエンジニアやチーム導入を検討する人に役立ちます。

## 詳細解説
主なコマンドと用途（簡潔に）

- jj edit <-r/-b> <ident>
  - git switch や過去コミットを直接編集する用途。jjでは履歴を気軽に編集できるため、細かな修正を頻繁に行える。
- jj b c -r@ <branchname>
  - bookmark create の短縮。gitの git switch -c / checkout -b に対応する新しいブランチ作成。
- jj rebase -b@ -dmain
  - 現在のブックマーク（@）を main にリベースする決まり文句。習慣化すると毎回コマンドを考えなくて済む。
- jj show / jj diff
  - 現在のリビジョン（デフォルト -r@）の差分や内容を確認。ファイル単位やリビジョン間比較にも使える。
- jj new -r main
  - mainから新しい作業リビジョンを切る（named bookmarkフローと併用）。
- jj git fetch / jj git push --allow-new
  - リモート同期とプッシュ。jj git fetch はリモートのブックマークを自動更新／削除する点に注意。
- jj restore
  - ファイルを特定リビジョンから戻す操作。git restore に相当。
- jj b f <branchname>
  - ローカルでブックマークを「忘れる」（forget）— リモートは残るので一時的閲覧に便利。
- jj desc -m <description>
  - 現在リビジョンの説明を設定。説明無しのリビジョンはpushを拒否される点に注意。
- jj st / jj log
  - 状態確認・履歴確認。jjは常に「リビジョン上で作業する」設計。
- jj tug / tug-
  - ブックマークを現在（または一つ前）のリビジョンに向けるエイリアス。プッシュ前の使い勝手向上に効く。
  - .jjconfig.toml にエイリアスを置くと便利：

```toml
[toml]
[aliases]
tug = ["bookmark", "move", "--from", "heads(::@- & bookmarks())", "--to", "@"]
tug- = ["bookmark", "move", "--from", "heads(::@- & bookmarks())", "--to", "@-"]
```

- jj abandon / jj undo / jj mine / jj git init --colocate
  - abandon: 草稿や不要なリビジョン破棄（ブックマーク付きに注意）。
  - undo: 最後の操作を取り消す安全弁。
  - mine: 自分が作業中のブックマーク一覧。
  - git init --colocate: 既存Gitリポジトリをjjに変換して試す入口。

（元記事では個々の頻度分析から「よく使う20%のコマンド」に絞って紹介しています）

## 実践ポイント
- まずはローカルで既存リポジトリに対して試す: jj git init --colocate で変換してみる。
- 最低限覚えるコマンド：jj edit, jj b c, jj rebase -b@ -dmain, jj show/jj diff, jj git push --allow-new。
- .jjconfig.toml に tug エイリアスを追加して作業フローを短縮する。
- チーム導入時はリモートのブックマーク削除やpushポリシー（--allow-new 等）を運用ルールに明記する。
- まずは個人ブランチや小さなフィーチャーで運用を試し、CI/PRフローとの互換性を確認する。

以上を踏まえ、まずは手元のサイドプロジェクトでjjを触ってみることをおすすめします。
