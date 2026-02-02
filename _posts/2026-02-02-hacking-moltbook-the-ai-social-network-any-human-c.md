---
layout: post
title: "Hacking Moltbook: The AI Social Network Any Human Can Control - Moltbookをハッキング：人間が支配するAIソーシャルネットワーク"
date: 2026-02-02T19:17:59.108Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys"
source_title: "Hacking Moltbook: AI Social Network Reveals 1.5M API Keys | Wiz Blog"
source_id: 46857615
excerpt: "公開キー露出で150万API鍵・3.5万メール流出、AI SNSの致命的ミスと対策"
image: "https://www.datocms-assets.com/75231/1769995179-image5.png?fm=webp"
---

# Hacking Moltbook: The AI Social Network Any Human Can Control - Moltbookをハッキング：人間が支配するAIソーシャルネットワーク
「1.5MのAPI鍵が丸見え」— AIだけのSNSが抱えた“致命的な初期設定ミス”

## 要約
Supabaseの公開キーがフロントエンドに埋め込まれ、RLS（Row Level Security）が未設定だったため、Moltbookのデータベースが読み書き可能になり、1.5百万のAPIトークン・3.5万のメール・エージェント間DMなど大量の機密が露出しました。修正は迅速に行われましたが、教訓は深いです。

## この記事を読むべき理由
日本でもSupabaseや「vibe coding」（AIで高速プロトタイピング）が広がっています。設定ミス一つで顧客情報やAPI鍵が漏れ、サービスの信頼が一瞬で崩れるリスクは他人事ではありません。

## 詳細解説
- 何が起きたか：Moltbookの公開サイトに含まれるクライアント側JSにSupabaseの公開APIキーがハードコードされており、RLSが無効だったためそのキーで誰でもDBへREST/GraphQL経由で読み書きできた。
- 露出内容：エージェントのapi_key、claim_token、verification_code、ユーザのメールアドレス、エージェント間のプライベートDM（中にはOpenAIキー等のサードパーティ資格情報が平文で含まれていた）など。
- 規模と実態：表層では150万エージェントとされたが、実際に鍵が紐づく「人間」オーナーは約1.7万で、1人で多数のエージェントを作れる仕組み（レート制限なし）が存在したため指標が容易に改竄可能だった。
- 攻撃のやり方（概略）：クライアントJSを解析→公開キーでPostgREST/GraphQL呼び出し→エラーやスキーマ情報からテーブル列を列挙→データ抽出・書き換え。書き込み権限が残っていれば投稿改ざんやプロンプト注入も可能。
- 技術的教訓：Supabase自体は公開キーとRLSの組合せで安全だが、デフォルトや自動生成の設定をそのまま使うと危険。vibe codingは速度を与えるがセキュリティ設定を自動化しないと脆弱性が拡大する。

参考例（イメージ）
```bash
curl https://<project>.supabase.co/rest/v1/agents?select=name,api_key \
  -H "apikey: sb_publishable_XXXXX"
```

## 実践ポイント
- Supabase導入時は必ずRLSを有効化し、最低権限のポリシーを作る。公開キーは識別子扱いにするのみ。  
- フロントに機密情報をベタ書きしない。環境変数・サーバーサイドプロキシで隠蔽する。  
- 書き込みAPIには認可チェックとレート制限を必須化する（ボット大量作成防止）。  
- 秘密情報スキャン（CIでのシークレット検出）を導入し、キー漏洩時は即時ローテーション。  
- プライベートメッセージ等は暗号化またはアクセス制御を設け、サードパーティ鍵を共有させない運用ルールを徹底する。  
- 新規サービスは初期リリース時に外部のセキュリティレビュー／ペネトレーションテストを受ける。

Moltbook事例は「速く作る」潮流が続く中での必須学習モデルです。日本のプロダクトでも同様の落とし穴があることを念頭に、設計時からセキュリティを組み込んでください。
