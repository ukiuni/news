---
layout: post
title: "Show HN: CLI to order groceries via reverse-engineered REWE API (Haskell) - 逆解析したREWE APIで食料品を注文するCLI（Haskell）"
date: 2026-04-01T08:13:07.458Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/yannick-cw/korb"
source_title: "GitHub - yannick-cw/korb: REWE delivery CLI · GitHub"
source_id: 47571183
excerpt: "Haskell製CLIで逆解析REWE APIを使い、エージェント連携で買物を完全自動化"
image: "https://opengraph.githubassets.com/bae0703d5845383409b865698110eacec5a04912e981a0a2e3a525acd25bd773/yannick-cw/korb"
---

# Show HN: CLI to order groceries via reverse-engineered REWE API (Haskell) - 逆解析したREWE APIで食料品を注文するCLI（Haskell）
AIエージェントに「買い物を全部任せる」── Haskell製CLI「korb」で作る自動買い出しワークフロー

## 要約
Haskellで書かれたCLI「korb」は、逆解析したREWE（ドイツのスーパー）モバイルAPIを使ってバスケット作成〜受け取り注文までを自動化するツール。出力はJSONで、エージェントとの連携を前提に設計されています。

## この記事を読むべき理由
- 音声アシスタントや自動エージェントと連携して買い物を自動化する実例は、日本のスマートホーム / 自動化ニーズにも応用できるため学びが大きいです。
- 逆解析・mTLS認証・PKCEログイン・Leanによる形式検証といった技術スタックの実務的組合せは、セキュリティや信頼性を重視する開発者にとって興味深い実装例です。

## 詳細解説
- アーキテクチャ／機能
  - korbはREWEのモバイルAPIを逆解析して利用。主な機能は店舗設定、商品検索、バスケット操作、受け取り日時選択、注文、注文キャンセル、デジタルレシート取得など。
  - すべての出力がJSONになっており、外部エージェント（例：Claude）から呼び出してフローを自動化する想定です。
- 認証と証明書
  - REWEのクライアント用mTLS証明書が必要（リポジトリに手順へのリンクあり）。ブラウザPKCEフローでログインしアクセストークンを取得します。
- 実装と検証
  - コアはHaskell（GHC 9.12+、Cabal）で実装。提案エンジン（free-pickup閾値を満たすアイテム選定）はLean 4で形式仕様を証明し、Differential Random TestingでHaskell実装と一致することを検証しています。形式証明を実運用コードに紐づけた稀有な例です。
- 制約とリスク
  - 非公式でありAPIは予告なく変わる。利用は自己責任で、利用規約・法的側面に注意が必要です。

## 実践ポイント
- まず試す手順（要約）
  1. GitHub Releasesからバイナリを入手（macOS/linux）。あるいはGHC+Cabalでビルド。
  2. REWEモバイルのmTLS証明書を抽出して certs/mobile-clients-api.rewe.de/{private.pem,private.key} に配置（逆解析ドキュメント参照）。
  3. korb login → korb store set → korb search / korb basket add → korb checkout create → korb checkout order の流れで動作確認。
- 日本での応用アイデア
  - ローカルのECやスーパーAPI（公式／非公式）を同様にラップして、Siri／Google Assistantや自動化エージェントと連携した「買い物代理」ワークフローを作る。
  - 形式検証を導入して、提案ロジックや割引計算の精度保証を高める設計は、金融や医療系の自動化でも有用。
- 注意点
  - 逆解析や非公式APIの利用は規約違反やサービス停止のリスクがあるため、商用化や大量自動化は避けるか事前確認を。
