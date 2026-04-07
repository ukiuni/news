---
layout: post
title: "German police name alleged leaders of GandCrab and REvil ransomware groups - ドイツがGandCrab/REvilの実質的リーダーを特定"
date: 2026-04-06T23:55:47.347Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://krebsonsecurity.com/2026/04/germany-doxes-unkn-head-of-ru-ransomware-gangs-revil-gandcrab/"
source_title: "Germany Doxes &#8220;UNKN,&#8221; Head of RU Ransomware Gangs REvil, GandCrab &#8211; Krebs on Security"
source_id: 47660954
excerpt: "BKAがGandCrab/REvil首謀者「UNKN」を実名公表、企業の防御見直しを急げ"
image: "https://krebsonsecurity.com/wp-content/uploads/2026/04/shchukin-kravchuk.png"
---

# German police name alleged leaders of GandCrab and REvil ransomware groups - ドイツがGandCrab/REvilの実質的リーダーを特定
世界を震撼させた「UNKN」ついに実名公開 — 日本企業が今すぐ確認すべき防御策

## 要約
ドイツ連邦刑事局（BKA）が、GandCrabとREvilを率いたとされるハッカー「UNKN」の実名を公表。捜査は、世界的なランサムウェアの商業化と被害拡大の実態を改めて浮き彫りにしました。

## この記事を読むべき理由
ランサムウェアの手口はますます組織化・ビジネス化しており、日本の企業やMSP（マネージドサービス事業者）も大口被害のターゲットになり得ます。今回の公表は攻撃者の構造理解と対策見直しの重要な契機です。

## 詳細解説
- BKAの発表では、31歳のDaniil Shchukin（別名UNKN）がGandCrabとREvilの中心人物とされ、別のロシア人とともに多数の標的で金銭を要求、数千万ユーロの経済損失を引き起こしたとされます。米司法省の文書ではShchukinに紐づく暗号通貨ウォレットから数十万ドル相当が押収対象になっています。  
- GandCrabは2018年にアフィリエイト（加盟型）プログラムで台頭し、攻撃成功報酬を分配するモデルで急成長。開発陣はマルウェアを複数回アップデートし検知回避機能を強化しました。  
- REvilはGandCrabの継承的存在で、身代金要求に「二重恐喝（double extortion）」を組み合わせ、身代金とデータ公開抑止の二重請求で高額を狙う手口を確立。初期アクセスブローカー、暗号資産洗浄サービス、検知回避ツールなどの“サプライチェーン”が形成され、犯罪のプロ化が進みました。  
- 2021年のKaseya被害はREvilの「ビッグゲームハンティング」手法の象徴で、MSP経由で大量被害を引き起こした事件です。FBIの介入や復号鍵の配布でREvilは大打撃を受けましたが、手口自体は継続的に進化しています。  
- BKAの公表は、フォーラム投稿、インテリジェンス解析、顔認証ツール等を組み合わせた「ドクシング（実名・顔写真の公開）」で、追跡と抑止を狙う動きです。ただし「容疑者と特定のフォーラムアカウントの直接的結びつきは限定的」との評価もあり、法的手続きや証拠精査が今後の焦点になります。

## 実践ポイント
- 重要データの定期バックアップをオフライン／物理隔離で保持し、復元手順を定期検証する。  
- 管理用ポート（RDP等）の公開停止、ゼロトラスト原則・セグメンテーションを導入する。  
- 多要素認証（MFA）と最小権限でアカウントを管理する。  
- EDR/ログ収集とSIEMで初期アクセスの兆候（異常なログイン、横展開の痕跡）を監視する。  
- サプライチェーン対策：取引先・MSPのセキュリティ基準を審査し、契約で対応要件を明確化する。  
- インシデント対応訓練（テーブルトップ）とランサムウェア対応プレイブックを整備する。  

（注）BKA発表は「容疑」としての公表であり、法的手続きや追加情報を注視してください。
