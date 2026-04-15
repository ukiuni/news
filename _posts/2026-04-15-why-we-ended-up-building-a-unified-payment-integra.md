---
layout: post
title: "Why we ended up building a Unified Payment Integration Library? - なぜ統一された決済統合ライブラリを作ることになったのか？"
date: 2026-04-15T14:39:27.419Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/juspay/hyperswitch-prism/wiki/How-we-ended-up-building-a-Unified-Payment-Integration-Library%3F"
source_title: "How we ended up building a Unified Payment Integration Library? · juspay/hyperswitch-prism Wiki · GitHub"
source_id: 362315155
excerpt: "決済プロバイダー差分を一括解消、Rust×protobufで即導入できるPrismの全貌"
image: "https://repository-images.githubusercontent.com/975510733/4b7c010b-e1f9-4ff2-9db4-be9df3b504f4"
---

# Why we ended up building a Unified Payment Integration Library? - なぜ統一された決済統合ライブラリを作ることになったのか？
決済連携の「面倒」をゼロにする――StripeもAdyenも同じように扱えるライブラリ、Prism誕生の理由と仕組み

## 要約
決済プロバイダーごとの差分に毎回苦しむ開発者のため、Hyperswitchの接続層を切り出して「Prism」という多言語で使える統一ライブラリにした話。protobufで契約を定義し、RustをコアにしてFFI／gRPCの両モードで動きます。

## この記事を読むべき理由
日本は多様な決済サービス（PayPay、LINE Pay、楽天ペイなど）や海外決済の併用が増え、プロバイダー切替や並列運用が現実的課題です。決済連携を一度しっかり組めば、切替・追加が設定変更で済むようになり、開発コストと運用リスクが大幅に下がります。

## 詳細解説
問題点
- 各決済プロバイダーはAPI仕様やエラーハンドリングがバラバラ。資料が古かったり、微妙に意味が違う「decline code」などで手戻りが発生。
- 多くのプロジェクトでは「プラットフォーム丸ごと導入」でしか良い接続を得られないことが多い。

Prismでのアプローチ
- 接続ロジックをHyperswitchのオーケストレーターから切り出し、汎用ライブラリ（Prism）として公開。
- ライブラリは「統一されたプロトコル（protobuf）」を契約にしており、支払いライフサイクルを9つのサービス（Authorize, Capture, Refund, Webhookなど）で型安全に定義。
- すべての入出力は厳密なproto型。自由形式JSONや文字列ステータスは排除され、実装が契約に縛られる。

なぜprotobufか
- マルチランゲージでのクライアント生成が必須：Python/Java/TypeScript/Rustなどで型付きAPIを自動生成できる成熟したエコシステムがあるため。
- 同じprotoがgRPCインターフェイスにも使えるため、埋め込みSDKとネットワークサービスの両方を自然にサポートできる。

なぜRustコアか
- 既存実装が多く、ネイティブ共有ライブラリ（.so/.dylib）として各言語に組み込める利点があるため。GCを持たないコンパクトなバイナリを配布でき、メモリ安全も確保できる。
- コードは小さなクレートに分割（connector-integration, domain_types, grpc-api-types, interfaces 等）されている。

設計の肝：二相変換（Two-phase transformer）
- ライブラリは自分でHTTPを投げない。各フローは2つの純粋関数に分かれる：
  1. req_transformer：統一リクエスト(proto) → コネクタ固有のHTTP情報(URL, headers, body)
  2. res_transformer：生のHTTPレスポンス(bytes) + 元リクエスト → 統一レスポンス(proto)
- 利点：ステートレスでトランスポート非依存、テストが容易、TLS/リトライ/接続プールなどの責任を呼び出し側に残せる。

実装支援
- Rustマクロでフロー登録やボイラープレートを自動生成。新しいフロー追加は実装とマクロ呼び出し1ペアで済む。
- 全言語向けにSDKを生成。データはシリアライズ済みのprotobufバイト列でやり取りするため言語中立。

2つの使用モード
1. 埋め込みSDK（FFI／UniFFI）
   - Rustをネイティブライブラリにビルドし、UniFFIでPython/JS/Javaなどのバインディングを生成。
   - 同一プロセス内で呼び出すためネットワーク遅延ゼロ。サーバーレスやエッジ、単一言語サービスに向く。
   - 開発時はRustビルドが必要。配布はプラットフォーム別バイナリ入りのwheel/jarで簡単。

2. gRPCサーバ（Tonic）
   - Rust製の独立したgRPCサービスを立て、言語別に生成したgRPCスタブから利用。
   - ポリグロット環境やプロセス分離（セキュリティ・運用上の理由）に適する。

## 実践ポイント
- 小規模・単一言語の環境なら埋め込みSDKを先に試す（サーバーレスやファンクションに最適）。
- 複数言語・複数サービスで共通化したいならgRPCサーバ化して全社で共有。
- Transformerをユニットテストして外部ネットワークを持ち込まずに接続ロジックを検証する運用フローを作る。
- 日本市場では国内決済やOCR／請求連携など固有要件があるため、まずはよく使うコネクタをPrism側で実装・確認すると迅速に効果が出る。
- 興味があればprotobuf定義と既存のRustコネクタを確認して、まずはローカルでEmbed SDKをビルドし試すと理解が早い。

以上を踏まえると、Prismは「決済ごとの差分で開発が止まる」問題を工学的に切り分けた実用的な解です。日本の事業者や決済を多用するスタートアップにとって導入の価値は高いでしょう。
