---
layout: post
title: "Gentoo on Codeberg - Codeberg上のGentoo"
date: 2026-02-17T18:59:12.182Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.gentoo.org/news/2026/02/16/codeberg.html"
source_title: "Gentoo on Codeberg – Gentoo Linux"
source_id: 47050067
excerpt: "GentooがCodebergミラー化、AGitでフォーク不要なPR手順を公開"
image: "https://www.gentoo.org/assets/img/og-image.jpg"
---

# Gentoo on Codeberg - Codeberg上のGentoo
魅力的なタイトル: 「GitHub離れの波に乗るGentoo──Codebergへ移行して何が変わるのか？」

## 要約
Gentooが公式リポジトリのミラーをCodebergに公開しました。今後徐々にGitHub依存を減らす施策の一環で、Codeberg経由でのコントリビュート方法（AGitベースのPR手順）も案内されています。

## この記事を読むべき理由
オープンソースのホスティング移行は、開発ワークフローやコントリビューションの敷居に直結します。日本の個人開発者や企業OSS担当者が今後どのプラットフォームで活動すべきか判断する材料になります。

## 詳細解説
- 背景：Gentooは2025年の年末レビューで示した通り、GitHubから段階的にミラーを移行しています。今回のCodeberg追加は非営利組織運営（Forgejoベース、ベルリン拠点）のプラットフォームを選ぶ動きの一例です。  
- 何が変わるか：Gentooは引き続き自前のリポジトリをホストしますが、Codebergミラーを通じてGitHubに代わる貢献経路を提供します。プライバシーや運営の独立性を重視するプロジェクトにとって意味があります。  
- 技術的ポイント：Codeberg上でのPRは「AGitアプローチ」を推奨。フォークを自分のCodebergアカウントに保持する必要がなく、topicベースのrefs/for/masterプッシュでPRが自動作成されます。コミット追加や強制プッシュ（コミット修正時）のオプションも指定可能。

例：リポジトリ追加とPR作成の流れ
```bash
# 上流をクローンしてCodebergリモートを追加
git clone git@git.gentoo.org:repo/gentoo.git
cd gentoo
git remote add codeberg ssh://git@codeberg.org/gentoo/gentoo

# ブランチ作成、作業
git checkout -b my-new-fixes

# PR作成（topicで自動作成）
git push codeberg HEAD:refs/for/master -o topic="短いタイトル"

# 修正を上げるときは同じtopicで繰り返す
# amendして強制更新する場合：
git push codeberg HEAD:refs/for/master -o topic="短いタイトル" -o force-push=true
```

## 実践ポイント
- まずはミラーURL（https://codeberg.org/gentoo/gentoo）を確認し、既存ワークフローに影響がないか試す。  
- フォーク管理を減らしたければAGit流（refs/for/master + topic）を試す。  
- 企業や団体での採用検討時は、Codebergの運営形態（非営利、EU拠点）と自社ポリシーを照らし合わせる。  
- 公式WikiやGentooの連絡窓口で追加ドキュメントを確認してから本番運用へ移行する。
