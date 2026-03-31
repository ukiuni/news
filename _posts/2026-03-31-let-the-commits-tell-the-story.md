---
layout: post
title: "Let the commits tell the story - コミットに物語を語らせよう"
date: 2026-03-31T08:18:25.583Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://chrismaiorana.com/git-commits-tell-the-story/"
source_title: "Let the commits tell the story - Chris Maiorana"
source_id: 956237314
excerpt: "一行の丁寧なコミットで、作業履歴が物語化され将来のレビューや引継ぎで価値を生む"
image: "https://chrismaiorana.com/wp-content/uploads/2026/03/girl-thinking-yellow_matix.jpg"
---

# Let the commits tell the story - コミットに物語を語らせよう
あなたのGit履歴を“作業日誌”に変える──一行のメッセージがプロジェクトの過程を可視化する方法

## 要約
コミットメッセージを丁寧に書くだけで、作業の流れや決断の履歴が見える化され、将来の自分やチームに大きな価値を残せる。

## この記事を読むべき理由
日本の現場でも、コードレビューや引き継ぎ、品質管理で「いつ」「なぜ」「どう変わったか」を追う必要が増えています。良いコミット習慣は小さな手間でその可視化を実現します。

## 詳細解説
- コミットは「固定された判定」ではなく、作業を記録するスナップショット（ledgerの記入）のようなもの。短いWIPだけのメッセージより、何をしたかを一行で書くことで後から履歴が物語になる。  
- コマンドで履歴の見方を変えると情報量が違う：
```bash
# 要点を一覧で見る
git log --oneline

# 各コミットの差分量（挿入/削除）を確認
git log --oneline --stat

# 単語差分を見て、何が変わったか精査する
git diff --word-diff HEAD~1
```
- Emacs + Magitを使うと、ログ表示（l l）やハンク単位での分割・ステージが簡単（ステージ分割で関連する変更だけを一つのコミットにまとめられる）。Magitの差分表示はword-diffが見やすい（statusバッファで d r）。
- コミットメッセージは創作行為でもある：問題を解いた、構造を切った、フローに入った等、感情や判断を書き残すと後で役立つ。
- コミットのメタデータ（日時・追加/削除行数）も第二の物語を語る。ドラフト期は挿入が多く、推敲期は削除が増えるといった傾向が見える。

## 実践ポイント
- 自然な区切りでコミットする（毎段落は多すぎ、週1回は少なすぎ）。目安は編集で約250語単位（プロジェクトに応じて500–1000も可）。  
- コミット前に差分を単語単位で確認：`git diff --word-diff HEAD~1`（Magitなら d r）。  
- その場で率直な一行メッセージを書く（できれば何を達成したか）。  
- 重要な節目はタグを付ける：  
```bash
git tag -a rough_draft -m "Rough draft finished, 62,000 words"
```
- ハンク分割で関連変更をまとめる（Magitの分割ステージが便利）。  
- 定期的に `git log --oneline --stat` を見て、自分の作業パターン（ドラフト vs 推敲）を把握する。

短い手間で履歴は劇的に有益になります。特にチーム開発や将来の振り返りで差が出るので、今日から一行を丁寧に。
