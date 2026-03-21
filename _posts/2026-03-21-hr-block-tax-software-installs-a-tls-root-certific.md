---
layout: post
title: "H&R Block tax software installs a TLS root certificate with bundled private key - H&R Blockの税務ソフトが秘密鍵付きのTLSルート証明書をインストール"
date: 2026-03-21T23:53:29.624Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://news.ycombinator.com/item?id=47457162"
source_title: "Tell HN: H&amp;R Block tax software installs a TLS backdoor | Hacker News"
source_id: 1379711960
excerpt: "H&R Blockの税ソフトが秘密鍵付きルートCAを導入、TLSがMITM可能に"
---

# H&R Block tax software installs a TLS root certificate with bundled private key - H&R Blockの税務ソフトが秘密鍵付きのTLSルート証明書をインストール

税ソフトが「見えないTLSの裏口」を仕込んでいた？H&R Block Business 2025がローカルのルートCAとその秘密鍵を同梱・登録し、アンインストールしても残るという重大な問題が報告されました。

## 要約
H&R BlockのBusiness版2025は「WK ATX ServerHost 2024」というルートCAをユーザーの信頼済みルートストアに追加し、しかも秘密鍵がDLL内に含まれているため、第三者がそれを使ってTLS通信を傍受・改ざん可能という脆弱性が見つかっています。

## この記事を読むべき理由
国内の多くはH&R Blockを直接使わないにせよ、ソフトウェアがローカルのルートCAを追加する設計ミスはどの国のユーザーにも関係があります。企業や個人で使うサードパーティ製ソフトの供給者管理／信頼チェーンの監査が重要であることを再認識するために必読です。

## 詳細解説
- 発見内容：H&R Block Business 2025が「WK ATX ServerHost 2024」という自署ルート証明書を信頼済みルートに登録。証明書の有効期限は2049年。  
- 決定的な問題点：そのルート証明書の秘密鍵がDLLファイル内に同梱されており、秘密鍵が外部に出回れば誰でもそのCAで署名した偽サーバ証明書を作成できる。結果として同一ネットワーク内でDNS偽装などを使えば任意のTLS接続をMITMできる。  
- 挙動：証明書はH&R Blockの名前を示さず、アンインストール時に自動で削除されない。開発者に連絡したところ「内部の評価で類似の所見があった」との返答があるが、修正されていない模様。  
- 実証：報告者はmitmproxyを使ったデモを公開（元情報にリンクあり）し、脆弱性の再現を示した。ブラウザの警告が出ない場合は既にルートCAが信頼されている可能性が高い。

## 実践ポイント
- まず確認：Windowsなら「certlm.msc（ローカルコンピュータ）/certmgr.msc（ユーザー）」で「Trusted Root Certification Authorities」を開き、"WK ATX ServerHost 2024"のような見慣れないエントリを探す。macOSならKeychain Accessで同名を検索。  
- 見つけたら削除／信頼解除：企業環境ではIT管理者の手で集中管理しているか確認の上、不要なら削除。アンインストールだけでは残るので手動対応が必要。  
- ネットワーク運用上の対策：公衆Wi‑Fiや未検証のネットワークでの重要作業は避け、DNS保護（DNSSEC/DoH/プロバイダ信頼）やネットワーク分離を行う。  
- 監査習慣を作る：サードパーティソフト導入時に信頼チェーンとインストールスクリプトの監査を行う。特に業務用ソフトやビジネス版はOS間の差異（Windows限定など）を確認する。  
- ベンダー対応を要求：影響を受けたユーザーはベンダーへ問い合わせと早期修正を要求し、必要なら影響の公表を促す。

この事例は「ユーザーPCにルートCAを勝手に置くこと」がどれほど危険かを端的に示しています。国内のIT管理者・エンジニアは自社環境のルートストア監査を今一度行ってください。
