---
layout: post
title: "The end of the curl bug-bounty - curlのバグバウンティ終了"
date: 2026-01-26T09:52:52.289Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/"
source_title: "The end of the curl bug-bounty | daniel.haxx.se"
source_id: 886383397
excerpt: "cURLがバグバウンティ終了、AI報告増で日本企業の脆弱性対応に影響"
image: "https://daniel.haxx.se/blog/wp-content/uploads/2025/12/no-more.jpg"
---

# The end of the curl bug-bounty - curlのバグバウンティ終了
cURLがバグバウンティを打ち切った理由と、日本の現場が取るべき対策

## 要約
cURLプロジェクトは2026年1月31日で公式のバグバウンティを終了。AI生成の低品質報告（“AIスロップ”）や悪意ある重複報告が増え、維持コストと精神的負担が大きくなったための決断です。

## この記事を読むべき理由
cURLはLinuxディストリ・組み込み機器・サーバー通信ライブラリとして日本の多くのプロダクトの根幹にあるため、報告フローや脆弱性対応の変化は日本企業や開発者に直接影響します。

## 詳細解説
- 経緯：本格的なバグバウンティは2019年4月にHackerOneで開始。これまでに87件の確定脆弱性と約10万米ドルの支払いがあった。  
- 背景問題：2024後半〜2025年にかけて、AI生成レポートが爆発的に増加。以前は提出の15%以上が有効だったが、2025年は5%未満に低下。人手での精査が増え、メンテナーの疲弊を招いた。  
- 取った措置：  
  - すべてのセキュリティ報告に対する金銭的報酬を停止（2026-01-31以降）。  
  - HackerOneを推奨チャネルから外し、今後はGitHubのPrivate vulnerability reportingか security@curl.se 宛のメールでの非公開報告へ移行。  
  - 明らかなAI生成の低品質報告は即時禁止・公表して排除する方針。  
- 備考：PR（修正提案）はCIとテストでふるいにかけやすく、AIノイズの影響が比較的小さいと評価。curlは今後もGitHubで開発を継続し、透明性ある公開報告の仕組みを模索する意向。

## 実践ポイント
- 脆弱性を見つけたら：GitHubのPrivate vulnerability reportingを使うか、security@curl.se に完全なレポート（再現手順、影響範囲、PoC、可能なら修正案）を送る。  
- 報告の品質：AIに頼り切った断片的な指摘は避け、必ず手で検証した再現手順と根拠を付ける。低品質報告はプロジェクトの信頼を損なう。  
- 貢献の仕方：単なる問題指摘だけでなく、パッチやテストを添えてPRを出すと効果的。curlはCIでの自動検証が強いので、テストを通すPRは歓迎される。  
- 企業向け提案：curlのような基盤OSSはメンテナーの負担が直接セキュリティ影響につながる。スポンサーや技術支援、社内での脆弱性トリアージ体制の整備を検討すること。  
- 情報収集：プロジェクトの今後の方針や議論はDaniel Stenbergの発表（FOSDEM 2026など）やGitHubのissueをフォローする。

以上。需要の高いライブラリの保守方針変更は、品質とセキュリティ運用の見直し機会でもあります。
