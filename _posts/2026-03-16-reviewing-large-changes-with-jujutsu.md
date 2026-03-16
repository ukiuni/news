---
layout: post
title: "Reviewing large changes with Jujutsu - Jujutsuで大きな変更をレビューする方法"
date: 2026-03-16T16:41:46.729Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ben.gesoff.uk/posts/reviewing-large-changes-with-jj/"
source_title: "Reviewing large changes with Jujutsu"
source_id: 1703685790
excerpt: "大きなPRも怖くない—Jujutsuで見た箇所を履歴化し分割レビュー"
---

# Reviewing large changes with Jujutsu - Jujutsuで大きな変更をレビューする方法
魅力的なタイトル: 「大きなPRも怖くない――Jujutsuでレビューを“分割して記録”する新ワークフロー」

## 要約
Jujutsu（jj）を使い、相手の大きな変更をローカルで複製→空の親コミットに少しずつスクワッシュして「見た箇所」を履歴として残しながらレビューする手法を紹介する。PRを途中で中断でき、進捗をjjの履歴で把握できるのが利点。

## この記事を読むべき理由
大規模PRやエージェント生成コードが増える中で、日本のチーム（Bitbucketを使う現場やJetBrains系IDE利用者含む）にとって、レビューの「どこを見たか」を忘れずに管理する実用的な代替案になるから。

## 詳細解説
課題
- 大きなPRはファイル間を飛び回るため「どこを確認したか」を追いにくい。Web UIでの既読管理が乏しいと効率が落ちる。
- Gitで同様の運用を再現すると、stash/worktree/ステージ操作で注意力を消費する。

jjを使うメリット
- 変更を複製（immutable → mutable）し、レビュー用の「空コミット」を親に作ることで、レビュー済みのファイルをその親にスクワッシュしていけば履歴上に「見た範囲」が残る。
- jjの差分/統計コマンドで進捗が一目瞭然。IDEは通常の作業環境のままで使える（ただし完全な統合はプラグイン依存）。
- ローカルでコメントを残し、最後に interdiff で差分を出してからWebに反映する「バッチ投げ」も可能で、途中でレビューを中断・再開しても状態が保たれる。

関連する概念
- matkladの「ローカルで状態を管理する」提案や、Jane Streetの「brain」概念と親和性が高い（空コミット＝レビュー済み領域）。

注意点
- IDE統合は完全ではない（Selvejjはプレリリース）。colocatedモード等のワークアラウンドが必要なケースがある。
- チーム全体で「レビューをローカルに残す」運用に踏み切るには合意が必要。

## 実践ポイント
基本ワークフロー（要点だけ）
1. 相手ブランチを取得して複製、編集可能にする  
```bash
jj git fetch -b big-change bookmark: big-change@origin
jj duplicate big-change@origin
jj edit <duplicated-id>
```
2. 現在の編集中コミットの手前に空コミット（レビュー用）を作る  
```bash
jj new --no-edit --insert-before @ --message 'review: big-change'
```
3. ファイルを確認したらそのファイル／ハンクをレビューコミットにスクワッシュしていく  
```bash
jj squash path/to/file
# または細かいハンクを移す
```
4. 途中で中断・再開可。完了後は interdiff で差分を出してWebにコメントを反映  
```bash
jj interdiff --from big-change@origin --to <review-commit>
```

運用のヒント
- 小さな単位（ファイル単位や論理的ハンク）でスクワッシュすると可視化が有効。
- 最後にWeb UIへまとめてコメントを投げると、途中での文言修正がやりやすい。
- IDEはcolocatedモードで通常通り使えるが、別workspaceでは.gitの扱いに注意。

短く言えば：jjの「複製＋空コミット＋スクワッシュ」で、レビューの「見た・未見」を履歴化し、認知負荷を下げて効率的に大規模PRを処理できる。日本の現場でも試す価値が高い実践的テクニックです。
