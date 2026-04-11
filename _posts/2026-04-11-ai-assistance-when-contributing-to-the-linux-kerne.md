---
layout: post
title: "AI assistance when contributing to the Linux kernel - カーネル貢献におけるAI支援の指針"
date: 2026-04-11T00:28:25.192Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/torvalds/linux/blob/master/Documentation/process/coding-assistants.rst"
source_title: "linux/Documentation/process/coding-assistants.rst at master · torvalds/linux · GitHub"
source_id: 47721953
excerpt: "AIで効率化しながらDCO署名・GPL遵守・Assisted-by表記でカーネル貢献の安全策"
image: "https://opengraph.githubassets.com/8eb070812f45ffffa2c223efe2df1453b4cc71c27cacfd52e1f33be996b5e1d3/torvalds/linux"
---

# AI assistance when contributing to the Linux kernel - カーネル貢献におけるAI支援の指針
魅力的タイトル: AIに頼る前に知っておきたい、Linuxカーネル貢献の“守るべきルール”と実務チェックリスト

## 要約
LinuxカーネルへのAI支援利用は許容されるが、ライセンス順守・署名（DCO）・人間の最終責任など厳格なルールがある。適切な「Assisted-by」表記や手順を守ることが必須。

## この記事を読むべき理由
日本の企業や個人開発者がAIで効率化を図る際、オープンソース貢献で法務リスクやコントリビューション拒否を避けるために、最低限のルールと実務チェックを押さえておく必要があるからです。

## 詳細解説
- 開発プロセス順守：  
  AIを使っても、カーネルの既存プロセス（開発手順、コーディングスタイル、パッチ提出ルール）に従う必要があります。AIは補助であり、プロセスそのものを置き換えません。

- ライセンス要件：  
  カーネルへ追加するコードは GPL-2.0-only と互換でなければなりません。適切な SPDX ライセンス識別子を付け、ライセンス規定に抵触しないことを確認してください。

- Developer Certificate of Origin（DCO）と署名：  
  AIエージェントは Signed-off-by を付与してはいけません。DCO（開発者の署名）を付けるのは人間の貢献者のみで、最終的な責任は提出者が負います。つまり、AI生成コードは必ず人がレビュー・修正し、提出者自身が Signed-off-by を追加する必要があります。

- 帰属（Attribution）：  
  AIの関与は透明化するため、パッチ等には Assisted-by タグを追加することが推奨されています。フォーマット例は以下の通りで、使用モデルや補助的解析ツール（必要なら）を明記します。基本的な開発ツール（git/gcc/make/エディタ等）は列挙しません。

  Example:
  ```text
  Assisted-by: AGENT_NAME:MODEL_VERSION [coccinelle] [sparse]
  ```

- 解析ツールの併用：  
  coccinelle、sparse、smatch、clang-tidy 等の静的解析を併用し、AIが作った変更を自動検査することが推奨されます。

## 実践ポイント
- 提出前チェックリスト（短縮版）：
  1. AI生成コードを必ず人がレビューする。  
  2. ライセンス（GPL-2.0-only）と SPDX タグを確認する。  
  3. DCO は自分で Signed-off-by を追加する（AIは不可）。  
  4. Assisted-by 行で使用したAIモデルと補助ツールを明記する。  
  5. coccinelle/sparse/clang-tidy 等で静的解析・ビルド・テストを実行する。  
  6. カーネルのコーディングスタイルとパッチ提出手順に従う。

- 日本の現場向け注意点：  
  法務部門やOSSポリシーがある企業では、AI利用の可否やログ保存、第三者提供モデルの利用条件を事前に確認してください。組み込みや安全性が重要な分野では、人による厳格なレビューとテストが不可欠です。

短く言えば：AIは便利なアシスタントだが、ライセンス遵守・署名・最終責任は人にある――これを守れば、効率化と安全性の両立が目指せます。
