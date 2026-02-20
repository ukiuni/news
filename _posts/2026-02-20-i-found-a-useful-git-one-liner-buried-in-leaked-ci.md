---
layout: post
title: "I found a useful Git one liner buried in leaked CIA developer docs - CIAの流出開発ドキュメントにあった便利なGitワンライナー"
date: 2026-02-20T14:55:19.512Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://spencer.wtf/2026/02/20/cleaning-up-merged-git-branches-a-one-liner-from-the-cias-leaked-dev-docs.html"
source_title: "Cleaning up merged git branches: a one-liner from the CIA's leaked dev docs | spencer.wtf"
source_id: 47088181
excerpt: "流出ドキュメント由来の安全なGitワンライナーで、マージ済みローカルブランチを一括整理"
image: "https://spencer.wtf/assets/images/ogimage.png"
---

# I found a useful Git one liner buried in leaked CIA developer docs - CIAの流出開発ドキュメントにあった便利なGitワンライナー
Gitブランチの「墓場」を一瞬で片付ける、CIA流ワンライナー

## 要約
ローカルに溜まったマージ済みの不要ブランチを安全に一括削除するワンライナーを紹介。main/masterや現行ブランチを除外しつつ、未マージのブランチを誤削除しない点がポイント。

## この記事を読むべき理由
ブランチが増え続けると作業効率が落ち、管理が煩雑になります。日本のチームでもリポジトリの見通しを良くし、日常的な手間を減らす実用的なTIPSです。

## 詳細解説
元ネタはVault7流出資料の中にあった内部開発メモ。要は「現在のブランチ（*）や main/master を残して、マージ済みのローカルブランチだけを削除する」コマンドです。構成は次の通り：

- git branch --merged [基準ブランチ]  
  → 指定ブランチに既にマージ済みのローカルブランチ一覧を出力
- grep -vE "^\s*(\*|main|develop)"  
  → 現在のブランチ（*）や除外したいブランチ名を除外
- xargs -n 1 git branch -d  
  → 1行ずつ安全に削除（-d は未マージなら削除を拒否）

例（現在は main を基準に）:
```bash
git branch --merged origin/main | grep -vE "^\s*(\*|main|develop)" | xargs -n 1 git branch -d
```

ポイント：
- 小文字の -d は「未マージのブランチは残す」ため安全。強制削除は -D。
- 多くのプロジェクトで master → main に名称が変わっているので除外対象を更新する必要あり。
- origin/main を基準にするとリモートの main と同期した状態が基準になる（ローカル main で実行するのが無難）。

設定例（シェルのエイリアス）:
```bash
alias ciaclean='git branch --merged origin/main | grep -vE "^\s*(\*|main|develop)" | xargs -n 1 git branch -d'
```

あるいは Git のエイリアス（.gitconfig）にしても便利:
```ini
[alias]
    ciaclean = "!git branch --merged origin/main | grep -vE \"^\\s*(\\*|main|develop)\" | xargs -n 1 git branch -d"
```

## 実践ポイント
- 実行前に必ずプッシュ/フェッチして origin/main を最新化する（git fetch origin）。
- まずは「削除予定」を確認：  
  ```bash
  git branch --merged origin/main | grep -vE "^\s*(\*|main|develop)"
  ```
  または削除コマンドを preview する：
  ```bash
  git branch --merged origin/main | grep -vE "^\s*(\*|main|develop)" | xargs -n 1 echo git branch -d
  ```
- CIやチームの運用ルール（保護ブランチやリリースブランチ）を除外リストに追加する。
- 定期的に（デプロイ後や週次）実行する習慣をつけるとリポジトリがすっきり保てる。
