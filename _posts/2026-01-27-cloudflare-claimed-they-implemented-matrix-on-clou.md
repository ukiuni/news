---
layout: post
title: "Cloudflare claimed they implemented Matrix on Cloudflare workers. They didn't - CloudflareがCloudflare Workers上でMatrixを実装したと主張したが、実際は違った"
date: 2026-01-27T16:27:21.859Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tech.lgbt/@JadedBlueEyes/115967791152135761"
source_title: "Jade: &quot;Cloudflare just published a vibe coded blog post …&quot; - LGBTQIA+ and Tech"
source_id: 46781516
excerpt: "CloudflareのWorkers上でのMatrix実装は実運用に耐えうるか？制約を検証すべき"
---

# Cloudflare claimed they implemented Matrix on Cloudflare workers. They didn't - CloudflareがCloudflare Workers上でMatrixを実装したと主張したが、実際は違った

魅力的タイトル: 「Cloudflareが“サーバーレスMatrix”を宣言。でも実運用で本当に動くの？」

## 要約
海外の投稿は、Cloudflareの発表が「Workers上でMatrixプロトコルを実装した」と主張したが、実際の要件を満たす完全実装には至っていないと指摘しています。

## この記事を読むべき理由
Matrixは分散チャット（Fediverseの一員）として注目度が高く、日本の企業やOSSコミュニティでも導入検討が進んでいます。クラウドベンダーの「サーバーレスで実装可能」という主張は運用コストや設計に直結するため、エンジニアはその限界を理解しておくべきです。

## 詳細解説
元投稿の論点を一般的な技術観点で整理すると次の通りです。

- Matrixの要件: クライアント—サーバAPI、サーバ—サーバ（フェデレーション）API、長時間接続やリアルタイム配信、イベント履歴の永続化、メディア配信、エンドツーエンド暗号化（Olm/Megolm）など多面的な機能を必要とします。
- サーバーレス/Workersの制約: Cloudflare Workersはリクエスト/レスポンス中心の短時間実行モデルで、長期的なTCP接続や常駐プロセス、任意のバックグラウンドタスクが得意ではありません（ただしDurable ObjectsやKV/R2で状態管理はある程度補えます）。これらの制約は、フェデレーションの安定した接続維持やE2E鍵管理、メディア配信の処理といった部分で問題になります。
- 実用上の意味: 「Workers上で動くデモ」や「一部APIをプロキシで扱う」程度なら可能でも、他のMatrixサーバ（Synapse等）と完全に互換・同等の運用（スケール、レイテンシ、暗号鍵ローテーション、監査やバックアップ）を実現するには追加のインフラや設計上の工夫が必要です。
- セキュリティとプライバシー: E2E暗号化や鍵管理をクラウドの短命な実行環境に任せると、鍵の可用性・バックアップ・監査面で課題が生じます。

## 実践ポイント
- ベンダー発表は「何がデモで、何が運用レベルか」を確認する。フェデレーションやE2E暗号化が本当に動くか検証すること。  
- テスト項目例: 他のMatrixサーバとのフェデレーション接続、長時間接続（プッシュ／受信）の耐久試験、メディアアップロード／配信、鍵のバックアップ・復元。  
- 選択肢: 本番性が要るなら既存の成熟したhomeserver（SynapseやDendrite等）やマネージドサービスを検討。サーバーレスは特定ユースケースで有効だが万能ではない。  
- 日本企業向け注意点: 個人情報や企業内の会話を扱う場合は、鍵管理とログ保持ポリシー、データ主権（国内リージョン）を重視する。

短くまとめると、Cloudflareの主張が「技術デモ」レベルだった可能性が高く、実運用を目指すなら仕様・制約を自ら検証してから採用判断をするのが安全です。
