---
layout: post
title: "Git Worktrees: the cure for “stash hell” and branch whiplash - Git Worktrees：stash地獄とブランチ揺れの解毒剤"
date: 2026-03-02T15:45:56.157Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://open.substack.com/pub/codepluscontext/p/git-worktrees-the-cure-for-stash?utm_source=share&amp;utm_medium=android&amp;r=46orlb"
source_title: "Git Worktrees: the cure for “stash hell” and branch whiplash"
source_id: 392672004
excerpt: "git worktreeでstash不要、別フォルダで複数ブランチを同時作業しホットフィックス迅速化"
image: "https://substackcdn.com/image/fetch/$s_!_l5u!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a46d0f6-b766-45f2-b3af-9ded76cedcb0_445x530.png"
---

# Git Worktrees: the cure for “stash hell” and branch whiplash - Git Worktrees：stash地獄とブランチ揺れの解毒剤
魅力的なタイトル: 「stashに頼らない開発習慣へ：Git Worktreesでブランチを同時に開く技術」

## 要約
Gitのworktreeを使えば、同じリポジトリの複数ブランチを別フォルダで同時に開ける。stashやWIPコミット、余分なクローンに頼らず、作業コンテキストを壊さずにホットフィックスやレビューができる。

## この記事を読むべき理由
日本のチーム開発やリモートワークで「途中の作業を壊したくないからブランチを切り替えられない」場面は頻出。Worktreesは手戻りや無駄なコミットを減らし、レビュー/リリース対応を高速化する現場改善テクニックです。

## 詳細解説
- 概念：通常は1つの.gitと1つの作業ディレクトリだが、worktreeは.gitを共有しつつ複数の作業ディレクトリを持てる。各ディレクトリは別ブランチやコミットにチェックアウト可能。
- 主な利点：
  - コンテキスト切替コストゼロ：元の作業はそのまま維持。
  - stash不要：忘却リスクや雑なWIPコミットを避けられる。
  - 軽量：履歴オブジェクトは共有されるため再クローンより高速でディスク効率良好。
  - PRレビューがクリーン：PR用フォルダを維持しておける。
- 実務シナリオ例：featureを進めたままリリースブランチでホットフィックス→別フォルダで修正、コミット、プッシュしてPR作成。エディタやターミナルを並べて異なる「現実」を同時進行可能。
- 注意点：
  1. 同じブランチを2つのworktreeに同時チェックアウトできない（必要なら --detach を使う）。
  2. チェックアウト中のブランチを削除しようとすると失敗する。先にworktreeを削除すること。
  3. node_modulesやvendorは共有されないので依存は各フォルダで準備が必要（ただしキャッシュで実害は小さいことが多い）。

## 実践ポイント
よく使うコマンド集（実例）
```bash
# 既存ブランチを作業フォルダに追加
git worktree add ../app-hotfix origin/release/1.9

# 新しいブランチを作成して同時にworktree追加
git worktree add -b feature/new-onboarding ../app-onboarding main

# worktree一覧
git worktree list

# 終わったら削除
git worktree remove ../app-hotfix

# 削除や移動後のメタデータ掃除
git worktree prune

# 誤削除防止でロック / アンロック
git worktree lock ../app-hotfix
git worktree unlock ../app-hotfix

# 同じコミットを別フォルダで使いたいとき（ブランチ名の衝突回避）
git worktree add --detach ../app-temp HEAD
```

運用のコツ
- フォルダ命名規約：~/code/app, ~/code/app--hotfix, ~/code/app--review のように `--` を区切りに使うとエクスプローラでまとまる。
- 小さな試し運用を推奨：次に git stash しそうになったら一度 worktree を作ってみるだけで効果が分かる。
- CIやIDE（VS Code等）は各worktreeを別プロジェクトとして扱えるので、そのままテストやデバッグが行える。

短時間で導入でき、日々の枝分かれ作業や緊急対応がぐっと楽になります。まずは一度「git worktree add ../app--quickfix <branch>」を試してみてください。
