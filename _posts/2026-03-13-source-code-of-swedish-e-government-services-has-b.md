---
layout: post
title: "Source code of Swedish e-government services has been leaked - スウェーデンの電子政府プラットフォームのソースコードが流出"
date: 2026-03-13T11:21:56.137Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/"
source_title: "Full Source Code of Sweden&#x27;s E-Government Platform Leaked From Compromised CGI Sverige Infrastructure"
source_id: 47362350
excerpt: "スウェーデンの電子政府コード全流出、署名鍵と個人情報が売買される危機"
image: "https://darkwebinformer.com/content/images/2026/03/35216424822626571062.png"
---

# Source code of Swedish e-government services has been leaked - スウェーデンの電子政府プラットフォームのソースコードが流出
スウェーデンの“電子政府”の全ソースコードが無料公開—サプライチェーンとCI/CDの危機が日本にも波及する理由

## 要約
スウェーデンのE‑Govプラットフォームの全ソースコードが、CGI Sverigeのインフラ侵害を通じて攻撃者「ByteToBreach」により流出・公開され、職員データや署名ドキュメントなどの追加データは別売りと報告されています。

## この記事を読むべき理由
外部ベンダーのインフラやCI/CDが破られると、国レベルのサービス全体が危険にさらされます。日本でも行政・大企業が外部委託・クラウド・コンテナを多用しており、同種のサプライチェーンリスクは現実的な脅威です。

## 詳細解説
- 攻撃概況：攻撃者はCGI Sverigeの環境を深く侵害し、E‑Govプラットフォームの「完全な」ソースコードを公開。公開は無料だが、市民の個人情報や電子署名ドキュメントは別途販売していると報告されています。  
- 流出した資産：フルソースコード、スタッフDB、API署名システム、RCE（テスト）エンドポイント、初期侵入・脱獄（jailbreak）痕跡、JenkinsのSSHクレデンシャルなど。  
- 攻撃で利用された問題点（概要）：Jenkinsの完全侵害／JenkinsユーザーがDockerグループに所属していたことに伴うコンテナ脱出の可能性／SSH秘密鍵の横展開／ローカルの .hprof（ヒープダンプ）解析による情報収集／SQLから外部プログラムへの経路を使った権限昇格の痕跡。  
- 意味合い：CI/CDやビルドサーバーが突破されると、ソースの窃取だけでなく署名鍵やリリースパイプラインの改ざん、バックドア挿入まで懸念される。攻撃者が「第三者の責任」とする言説への反論も明記されており、ベンダー管理の重要性が強調されています。

## 実践ポイント
- 直ちに：JenkinsやCI/CDのアカウント、SSHキー、APIキーをローテーション／無効化。重要なクレデンシャルは即時回収。  
- CI/CDとビルド環境の隔離：ビルドユーザーに不要なDockerグループ権限を与えない。ビルド環境は最小権限で実行。  
- 検査と監査：ヒープダンプやビルドアーティファクトに機密情報が含まれていないか検査。ログとアクセス履歴を遡って不審な横展開を確認。  
- サプライチェーン管理：外部ベンダーのセキュリティ評価・SLAs・侵害時対応手順を見直す。ソースコードや署名鍵の扱いルールを明確化。  
- 監視と対応準備：ソース流出後のリスク（脆弱性発見・エクスプロイト、ソーシャルエンジニアリング）に備え、侵害検知、通知、法務・広報の連携プランを整備。

短く言えば、「CI/CDと委託先のインフラ管理が破られるとソフトウェア供給網そのものが崩れる」ため、構成管理・鍵管理・最小権限・監査ログの整備が不可欠です。
