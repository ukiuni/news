---
layout: post
title: "Never Buy A .online Domain - .onlineドメインを買うな"
date: 2026-02-25T14:11:59.837Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.0xsid.com/blog/online-tld-is-pain"
source_title: "Never Buy A .online Domain | Sid's Blog"
source_id: 47151233
excerpt: "無料プロモの.onlineが検証ループで公開不能に陥る実例の警告"
---

# Never Buy A .online Domain - .onlineドメインを買うな
魅惑的な「無料ドメイン」に騙されるな──たった20セントが招いた公開停止の悪夢

## 要約
Namecheapのプロモで取得した「.online」ドメインが突然Googleの安全性フィルタでブロックされ、registryとGoogleの間で“確認の負のループ”に陥って公開不能になった事例を解説する。

## この記事を読むべき理由
日本のスタートアップや個人開発者も格安プロモでTLDを手に入れがち。通知や復旧手順を知らないと、サービス停止・流入ゼロ・ブランド毀損につながる実例として学べる。

## 詳細解説
- きっかけ：Namecheapの「1アカウントにつき1つ無料(.online/.site)」プロモで取得。CloudflareとGitHubでホスティングしていたため一見問題なしに見えた。  
- 発覚：アクセス解析で訪問ゼロを確認し、実際に開くとGoogleの「このサイトは安全ではない」全画面表示。さらに直接アクセスすると「サイトが見つかりません」。  
- 技術的診断：digでNSが返らず、WHOISを確認するとregistry側で付与される「serverHold」ステータスが設定されていた。nameserver設定は正しく、Cloudflare側も有効だったため混乱が生じる。  
- 根本原因（検証の捕虜状態）：
  - GoogleのSafe Browsing/Safe Searchが該当ドメインをブロック。
  - Googleに解除審査を申し込むにはサイト所有の検証（Search ConsoleでDNS TXTやCNAME追加）が必要。
  - しかしドメインは解決せずDNS変更が外部から確認できないため検証不可能。
  - registryはserverHoldを解除する際にGoogle側のフラグ解除を条件にするケースがあり、結果として「registryは解除しない→Googleは検証できない→解除されない」のループに陥る。  
- 関係者の対応：registry（Radix）やレジストラ（Namecheap）に連絡したが、通知が届いておらず手続きとタイムラインが不明瞭だった。Googleの自動応答や「提出ページが有効でない」といったメッセージにより復旧が長引いた。

## 実践ポイント
- ドメイン取得直後にやるべきこと
  1. Google Search Consoleへ即登録し、所有権検証（DNS TXT/CNAME）を済ませる。  
  2. 監視を入れる（uptime監視・外部の被検出チェック）。  
  3. WHOIS連絡先とメール通知を確実に受け取れるようにする。  
- 運用上の注意
  - プロダクション用途は信頼できるTLD（企業なら.comや国別TLD）を優先検討する。  
  - プロモ系・マイナーTLDはリスクと運用コスト（復旧手順）を見積もる。  
  - registryやレジストラと連絡を取る際は、事前にサポート手順とエスカレーション窓口を確認しておく。  
- トラブル時の対処法
  - registryへ一時的な解除（temporary release）を依頼し、Googleに中身を確認してもらう手続きを試す。  
  - GoogleのSearch ConsoleとSafe Browsingの申請フォーム両方に並行して申請する。  
  - 重要ならすぐに代替ドメイン（サブドメインではなく別TLD）へ切替えて被害拡大を防ぐ。

短い結論：無料・格安の魅力に飛びつく前に、ドメイン検証と監視の基本を押さえること。小さな手間が復旧不能なダウンタイムを防ぐ。
