---
layout: post
title: "Hackers claim to have Target source code for sale following cyberattack - ハッカーがサイバー攻撃後にTargetのソースコードを販売と主張"
date: 2026-01-19T06:39:50.953Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.techradar.com/pro/security/hackers-claim-to-have-target-source-code-for-sale-following-recent-cyberattack"
source_title: "Hackers claim to have Target source code for sale following recent cyberattack | TechRadar"
source_id: 423114192
excerpt: "Targetの約860GBの内部コード流出が決済設計の脆弱性を暴露"
image: "https://cdn.mos.cms.futurecdn.net/EZ7Q5Kg74zh3jfdr4jRyNA-1920-80.jpeg"
---

# Hackers claim to have Target source code for sale following cyberattack - ハッカーがサイバー攻撃後にTargetのソースコードを販売と主張
なぜ日本の小売・決済担当者が震えるべきか：Targetの「860GB」流出と内部コード流出リスクの教訓

## 要約
海外メディアによれば、不明のハッカー集団がTargetの内部ソースコードや設定、開発ドキュメント約860GBを入手して販売すると主張。リポジトリの一部が公開され、Targetは該当サーバーをロックダウンしたが、真偽はまだ完全には確認されていない。

## この記事を読むべき理由
- 日本の小売・決済サービスやシステム開発に携わる人にとって、内部コードが流出すると決済・認証・ギフトカード等の設計情報が第三者に渡り、二次被害（不正利用・脆弱性の悪用）につながる可能性があるため。  
- 海外大手の事例は、国内企業が取り組むべき対策（コード管理、秘密管理、公開設定の確認）を具体的に示す教科書的事件になり得る。

## 詳細解説
- 主張される内容：攻撃者はGitea上に複数のリポジトリを作成し、wallet（ウォレット／決済系）、identity（認証）、gift-card（ギフトカード）、ストアネットワーク、Secrets管理などを示すファイル名やドキュメントをサンプルとしてアップした。合計で約57,000行に及ぶインデックスがあり、総容量は約860GBと報告されている。  
- 証拠の手がかり：コミットメタデータやドキュメント内に内部開発サーバーや内部URL（例：confluence.target.com）や、Targetの現職エンジニア名が記載されていた点が指摘されている。検索エンジンのキャッシュから一部が過去に公開されていた可能性もある。  
- 対応と現状：報道後、該当のGiteaレポは削除され、Targetは内部Gitサーバーをロックダウン。だが攻撃の全容や流出経路、実データの範囲は外部からはまだ完全に検証できない状況。  
- リスクの本質：ソースコード自体は個人情報ではないが、仕様や認証フロー、暗号鍵の取り扱い、APIエンドポイントや内部運用手順が分かれば攻撃者による侵入・不正操作や、決済不正の効率化につながる。さらに、公開履歴に含まれるトークンや秘密情報の漏洩は直ちに深刻な被害を招く。

## 実践ポイント
- まず前提確認：自社で使っているGit系サービス（GitHub/GitLab/Gitea等）やConfluence、ストレージの公開設定とアクセスログを即点検する。外部にインデックスされていないか確認。  
- シークレットの洗い出しとローテーション：コードや履歴に含まれるAPIキー/シークレット/TLS証明書が漏れていないかスキャン（git-secrets、truffleHogなど）し、該当あれば即ローテーション。  
- アクセス制御と多要素認証：開発アカウント、CI/CD、内部管理画面にMFAを必須化し、最小権限原則を見直す。  
- 監査と検出体制：リポジトリの変更追跡、外部ダークウェブやフォーラムの監視、SIEMでの異常検出ルール整備。  
- インシデント対応計画：誰が通知するか（法務・広報・個人情報保護委員会等）、どの情報をいつ公開するか、復旧手順を文書化しておく。  
- 開発プロセスの改善：機密情報は環境変数やシークレットマネージャで管理、CIに平文を残さない、公開前に自動スキャンを組み込む。

短くまとめると、今回の報道は「コードやドキュメントの管理不備が企業の事業リスクに直結する」ことを示す警鐘です。日本企業も同種の設計情報漏洩に備え、リポジトリ設定・シークレット管理・アクセス制御の見直しを急いでください。
