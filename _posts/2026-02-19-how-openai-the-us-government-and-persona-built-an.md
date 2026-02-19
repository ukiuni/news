---
layout: post
title: "how openai, the US government, and persona built an identity surveillance machine that files reports on you to the feds - OpenAI、米政府、Personaがあなたを連邦へ報告する身分監視マシンを構築した方法"
date: 2026-02-19T02:50:45.102Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vmfunc.re/blog/persona/"
source_title: "the watchers: how openai, the US government, and persona built an identity surveillance machine that files reports on you to the feds"
source_id: 715609034
excerpt: "公開情報で判明：OpenAI×Personaがセルフィーを監視し連邦へ通報"
---

# how openai, the US government, and persona built an identity surveillance machine that files reports on you to the feds - OpenAI、米政府、Personaがあなたを連邦へ報告する身分監視マシンを構築した方法
あなたのセルフィーが監視リストに載るまで：AI×政府×KYCの裏側

## 要約
海外の調査チームが、OpenAIとIDベリフィケーション企業Persona、米政府向けインフラの連携で「ウォッチリスト照合・疑わしい活動報告（SAR）」を自動化する仕組みが、公開情報から可視化できたと報告しています。ソースマップや証明書履歴などの公開データにより、設計と運用の実態が浮かび上がりました。

## この記事を読むべき理由
個人情報や生体データがクラウドでどう扱われるかは、日本でもすぐに他人事ではありません。AIサービスの利用拡大、政府向けクラウド認証（FedRAMP相当の議論）、そして国内IDベンダーの導入が進むなかで、実務・法務・セキュリティの両面で示唆に富む事例だからです。

## 詳細解説
- 発端：調査はShodanや証明書透明性（CT）ログなど公開情報から。特定のホスト名（例：openai-watchlistdb.withpersona.com）やGCP上の専用インスタンスがCTログで追跡できた点が鍵。
- 公開アーティファクト：未保護のソースマップやHTTP応答、APIドキュメントなどから、ID検証APIが返す「詳細な身元情報（氏名、生年月日、住所、ID画像/セルフィー、動画、信頼度等）」や、顔認証による類似度スコア、ウォッチリスト照合、SAR作成のロジックが読み取れたとされています。
- インフラの分離：通常のドメイン（Cloudflare背後）とは別に、専用のGCPインスタンスでデータを隔離している痕跡があること。これはデータ感度やコンプライアンス要件に起因している可能性がある一方、誤設定や情報露出があれば大きなリスクに。
- 透明性のタイムライン：CTログでサービス稼働開始が公記録化されており、公開ポリシーの変更より前からウォッチリスト機能が稼働していた可能性が示唆されています。
- サードパーティの痕跡：Content-Security-Policy等から、OpenAIのAPI接続やFingerprintJS、エラートラッキング、解析ツール、RUMなど外部サービスとの連携が読み取れ、政府向けプラットフォーム上でのサードパーティ利用が問題視されています。
- コンプライアンスと実運用：PersonaはFedRAMP Low相当の認定を取得している点が報告にあり、認証と実装差異、ログ・監査の扱いが焦点に。

## 実践ポイント
- 一般ユーザー向け：身分証やセルフィーをアップロードする際は提供先のプライバシーポリシー、第三者連携、保存・削除方針を確認する。可能なら利用を限定する。
- 開発者／インフラ担当向け：ソースマップやデバッグ情報を公開環境に置かない、CTログやDNSの監視を行い不要なホスト名を漏らさない、PⅡ／生体データに解析ツールや外部トラッキングを混ぜない。
- 管理者／法務向け：クラウド上でのID検証サービス導入時はサードパーティのデータフロー、ベンダーのセキュリティ認証の実態、再検査ポリシー（定期再スクリーニング等）を厳密にレビューする。
- 日本市場への示唆：国内IDベンダーや官民連携サービスでも同様の設計ミスや透明性欠如が起こりうる。FedRAMP相当や認証取得の表示だけで安心せず、実装監査と公開情報の定期チェックを。

（注）本稿は公開された調査報告の要約と解説です。調査チームの主張は「公開情報に基づく発見」として報告されており、ここではその内容を分かりやすく整理したものです。
