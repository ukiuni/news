---
layout: post
title: "VisualJJ – Jujutsu in Visual Studio Code - Visual Studio Codeで使うVisualJJ（Jujutsu対応）"
date: 2026-02-01T12:39:31.501Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.visualjj.com/"
source_title: "VisualJJ – Jujutsu in Visual Studio Code"
source_id: 46799435
excerpt: "VS Codeで履歴を可視化・安全に編集しPR管理や衝突解消まで完結"
---

# VisualJJ – Jujutsu in Visual Studio Code - Visual Studio Codeで使うVisualJJ（Jujutsu対応）
VS Codeで「履歴が見える・安全に直せる」Git体験を実現するVisualJJ

## 要約
VisualJJはVS Code拡張で、Jujutsu（JJ）とGitの上に直感的な変更ツリーを表示し、履歴編集やリベース、コンフリクト解消、GitHub連携をエディタ内でシームレスに行えるツールです。

## この記事を読むべき理由
Gitの履歴操作やリベース、コンフリクトで時間を浪費している日本の開発者にとって、VS Codeだけで安全に履歴を可視化・編集できることは生産性向上とミス削減に直結します。

## 詳細解説
- コア機能: JujutsuとGitの上に「変更ツリー」を可視化。どのコミットがどの差分を持つかがツリーで分かるので履歴の全体像が把握しやすい。  
- 安全な履歴編集: コミットの並べ替え・編集をドラッグ＆ドロップやガイドに従って行え、履歴をきれいに保ちながら作業できる。特にbusyなmainブランチへのリベース時に有用。  
- リベースと衝突対処: コンフリクトは変更ツリーの一部として扱われ、作業を「ドラフト状態」で保ちながら段階的に解決可能。途中で止めて検査・巻き戻しができるためデプロイの安全性が高まる。  
- GitHub統合: プルリクエストの状態をツリー上で追跡し、エディタから数クリックでPRを作成／管理できるため、エディタからレビュー〜マージまでの流れが滑らかになる。  
- 導入形態: VS Code拡張として配布。既存のGitワークフローに自然に組み込める設計。

## 実践ポイント
- まずVS Codeに拡張を入れて、既存リポジトリで変更ツリーを確認してみる。  
- 小さなブランチでドラッグ＆ドロップによるコミット再配置や履歴編集を試し、挙動を把握する。  
- コンフリクト発生時は「ドラフト」で一時保存→段階的解消をして、安全性を体験する。  
- GitHub連携でPR作成→レビューの流れをエディタ内で完結させ、チームのワークフローに組み込む。  

VisualJJは「履歴を怖がらない」開発習慣を促進します。まずは小さな変更で試して、日常的なGit操作をより快適にしてみてください。
