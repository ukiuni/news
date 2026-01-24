---
layout: post
title: "cURL Gets Rid of Its Bug Bounty Program Over AI Slop Overrun - cURL、AI生成の“ゴミ報告”氾濫でバグバウンティを終了"
date: 2026-01-24T10:40:54.733Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://itsfoss.com/news/curl-closes-bug-bounty-program/"
source_title: "cURL Gets Rid of Its Bug Bounty Program Over AI Slop Overrun"
source_id: 418870967
excerpt: "cURLがAI生成の大量無価値報告に嫌気、現金バグ報奨を停止へ—広範なサービスに影響"
image: "https://itsfoss.com/content/images/2026/01/curl-bug-bounty-program-discontinued.png"
---

# cURL Gets Rid of Its Bug Bounty Program Over AI Slop Overrun - cURL、AI生成の“ゴミ報告”氾濫でバグバウンティを終了
驚きの決断：世界で最も広く使われるcURLが、AI生成の質の低い脆弱性報告に業を煮やして現金報酬を停止

## 要約
cURLプロジェクトは、AIが生成した大量の“中身のない”報告でセキュリティ対応チームが疲弊したため、2026年1月31日をもってバグバウンティを廃止すると発表しました。以後は報告は受け付けるが報酬は支払われません。

## この記事を読むべき理由
cURLは多くのサーバー、組み込み機器、アプリで基盤的に使われており、報告文化の変化は日本の製品やサービスのセキュリティ運用にも影響します。AIツールの利用が進む今、正しい脆弱性報告の作法を知ることは必須です。

## 詳細解説
- 背景：cURLはコマンドラインやライブラリとして世界中で広く採用されているため、脆弱性報告が頻繁に寄せられます。最近はAI生成ツールによる「再現性のない」「根拠の薄い」報告（記事は“AI slop”と表現）が大量に届き、HackerOne上で対応負荷が急増しました。  
- 対応：プロジェクト創始者の判断で、公式ドキュメントからバグバウンティの案内を削除し、security.txtも方針を明確化。現金報酬は終了し、報告はGitHubやメーリングリスト経由で受け付けるが報奨金は付かない方針です。  
- 意図：金銭的インセンティブをなくすことで、質の低い自動生成レポートや未確認の投げ込みを減らし、限られた維持者の時間を守る狙いです。作者は「バグを報告するなら理解して再現できることが前提」と強く主張しています。

## 実践ポイント
- 報告者向け：問題を報告する前に必ず環境、再現手順、ログ、最小再現例を用意する。AIを使って草案を作る場合でも人間が検証し、誤検知を排除する。  
- 企業/OSS運営者向け：バグ報奨金制度はメリットとコストがあるため、スパム対策（レート制限、事前フィルタ、明確なsecurity.txt）や人的トリアージ体制を整備する。  
- 日本市場への示唆：組込み機器やクラウドサービスでcURLを使う事業者は、外部からのノイズ増加に備えた脆弱性対応フローと、内部での再現・検証責任者を明確にしておくと安心です。
