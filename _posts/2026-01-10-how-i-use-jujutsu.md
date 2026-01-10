---
layout: post
title: "How I use Jujutsu - 私がJujutsuを使う方法"
date: 2026-01-10T13:07:47.529Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://abhinavsarkar.net/posts/jj-usage/"
source_title: "How I use Jujutsu"
source_id: 1007565945
excerpt: "Git互換で履歴の分割・移動や実験が自在なJujutsu運用術"
---

# How I use Jujutsu - 私がJujutsuを使う方法
魅力的な日本語タイトル: Gitを卒業する前に知っておきたい「Jujutsu」の実用ワザ — 今日から使える最小セット

## 要約
Jujutsu（jj）はGitをバックエンドに使う新しい分散型バージョン管理で、ステージング無しの「変更（change）」中心ワークフローや柔軟な履歴操作が特徴。日常的に使うコマンドだけ押さえれば、移行は思ったほど大変ではない。

## この記事を読むべき理由
日本の開発現場でもGitは標準ですが、コミットの分割や移動、実験的な編集を頻繁に行う開発者にはJujutsuの操作感が生産性向上につながります。Git互換でリモートとも連携できるため、個人プロジェクトやプルリクを扱うチームでも導入障壁が低いです。

## 詳細解説
- 基本概念
  - JJはGitをバックエンドにするため、既存のGitリポジトリと共存可能。ローカルはJujutsuで操作しつつ、Gitリモートへpushできます。
  - 重要な違いは「ステージングが無い」点。ファイルは自動で追跡され、作業の単位はJJでは“change”（Gitのコミットに相当）です。作業はまずchangeを作成し、その中で編集→確定（describe/commit）する流れ。

- よく使うコマンド（実務的ポイント）
  - 初期化／複製
    - jj git init --colocate（既存のGitコマンドを併用したければcolocate）
    - jj git clone <repo> --colocate
  - 変更作成
    - jj new -m "説明"（changeを作る）
    - jj describe -m "説明"（現在のchangeに説明を付ける）
    - jj commit（describeして新しいchangeを開始）
  - 変更の編集・整理
    - jj edit '<change-id>'（過去のchangeに戻って追加編集）
    - jj squash（親と結合）
    - jj split（1つのchangeを複数に分割）
    - jj restore [--interactive|--from <change>]（ファイルを元に戻す）
    - jj rebase -s '<id>' -o '<new-parent>'（個別移動）や jj rebase -b <roots> -o main（複数ブランチのrebase）
    - jj duplicate（移動ではなくコピー）
    - jj abandon（不要なchangeを破棄）
  - 履歴確認と差分
    - jj log -r '<revset>'（revset言語で高度な検索。例: author("自分")）
    - jj diff [--from] [--to]（任意のchange間の差分）
    - jj show '<change-id>'（changeの詳細）
  - ブランチ相当
    - jj bookmark create '<name>' / jj bookmark list / jj bookmark delete '<name>'（bookmarkがブランチ代替）
    - bookmarkをpushするとGitのリモートブランチとして反映される
  - 状態管理の安全網
    - jj op log（操作履歴。opIDで復元可能）
    - jj undo / jj redo（操作単位で戻す・進める）
  - Git連携
    - jj git push / jj git fetch / jj git remote（従来のGitリモート操作をサポート）
  - 設定
    - jj config edit --user / jj config set --repo user.email someone@example.com / jj config list

## 実践ポイント
- 最初はローカルの個人プロジェクトで1〜2週間試す。gitリポジトリを--colocateで扱えば安全。
- 「まずjj newして作業、終わったらjj describe/commitで確定」という流れを意識する。
- 日々のブランチ整理はjj rebaseで簡単に。複数の機能ブランチをmainに定期的にrebaseする運用が楽になる。
- 失敗が怖ければjj op log／jj undoで安心。実験的な変更は躊躇せずabandonで破棄できる。
- チーム導入時はbookmarkとjj git pushの挙動（リモートにブランチを作る点）をドキュメント化しておくと混乱が少ない。
- untrackedファイルの扱いがGitと違うので、既存リポジトリではあらかじめ不要ファイルをコミット・削除・.gitignoreに登録しておく。

短時間で使えるコマンドだけを試して、履歴の移動や分割・結合が日常的に楽になる点を体験すると、Jujutsuの価値が実感できます。
