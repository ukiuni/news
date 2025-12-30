---
layout: "post"
title: "Building an AI agent inside a 7-year-old Rails monolith - 7年前のRailsモノリス内にAIエージェントを構築する"
date: "2025-12-26 08:11:50.550000+00:00"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://catalinionescu.dev/ai-agent/building-ai-agent-part-1/"
source_title: "Building an AI agent inside a 7-year old Rails application"
source_id: "46390055"
excerpt: "AlgoliaとPunditで権限を保ち最小変更でRailsモノリスに安全なAIを実装"
---
# Building an AI agent inside a 7-year-old Rails monolith - 7年前のRailsモノリス内にAIエージェントを構築する

## 要約
大規模Railsモノリス（マルチテナント／厳格な権限制御）に対して、既存の検索インデックス（Algolia）とPunditを使い、RubyLLMの「ツール（関数呼び出し）」機能で安全にAIエージェントを組み込んだ実践記。

## この記事を読むべき理由
日本の多くの企業システムは長年育ったモノリスで、個人情報や厳しいアクセス制御を伴います。AI導入で「データ漏洩」「権限逸脱」を恐れて踏み出せないチームに対し、最小限の変更でリスクを抑えつつAIの利便性を取り入れる実装パターンを示します。

## 詳細解説
背景
- 典型的課題：クライアント検索がDB直叩きでは遅い→検索にAlgoliaを導入。さらにAIを入れたいが、LLMに生データを与えるのは危険。
- 方針：LLMには直接データベースアクセスさせず、「許可済みの関数（ツール）」だけを通じてデータを返す。関数内でPundit等の既存の認可ロジックを適用することで、AIの行動範囲を明確に制限する。

RubyLLMの役割（概念）
- ConversationとMessageで会話の文脈を保持。
- 「ツール（function call）」を定義して、LLMが必要に応じて呼び出せるようにする。ツールは受け取るパラメータと返す構造を宣言し、LLMはその説明を見て呼び出し判断を行う。

実装の核（要点）
1. ruby_llmを導入して初期化（プロバイダAPIキーやタイムアウト設定）
2. アプリ側に「Tool」を定義（検索ツールなど）。ツールは外部検索（Algolia）を叩き、結果に対してPundit等で可視性フィルタをかけた上で返す
3. Conversationをツールと紐づけてchatするだけで、LLMは自然言語の問いに対して安全にツールを呼べる

おさえておくべき注意点
- ツールは「読み取り専用」に限定する。初期は更新系を与えない。
- ロギング／監査：ツール呼び出し・返却データは必ず監査ログに残す（誰がいつ何を聞いたか）。
- 最小権限：ツール内でPunditを適用し、結果集合をユーザーの権限で絞る。
- コストとレイテンシ：LLM呼び出し・外部検索で合計レイテンシが増えるためタイムアウトやリトライ戦略を設定。

簡潔なサンプル（イメージ）
```ruby
# Ruby
# 初期化（概念）
RubyLLM.configure do |c|
  c.openai_api_key = Rails.application.credentials.dig(:openai_api_key)
  c.request_timeout = 600
end

# ツールの骨子
class ClientSearchTool < BaseTool
  description "クライアントを検索して、呼び出し元ユーザーが見られる結果のみ返す"
  param :query, desc: "名前／ID／メールなど", type: :string

  def execute(query:)
    hits = Algolia::SearchClient.create(app_id, search_key)
                    .search_single_index(Client.index_name, { query: query.truncate(250) })
                    .hits
    ids = hits.map { |h| h["id"] }
    clients = Client.where(id: ids)
    # Punditでフィルタリング（current_userはコンテキストから取得）
    visible = Pundit.policy_scope!(context[:current_user], clients)
    visible.map { |c| { id: c.id, name: c.name, phone: c.phone } }
  end
end
```

運用イメージ
- Conversation.with_tools(ClientSearchTool).ask("山田太郎さんの電話番号は？")
- LLMは返答前にツール呼び出しを行い、ツールがPunditでフィルタ済みデータを返す→安全な回答が得られる。

## 実践ポイント
- まずは「検索（読み取り）」ツールだけでPoC：ユーザーの問い合わせに対して正しい結果が返るか確認する。
- Punditのポリシーを網羅的にテスト：ツール実行単位での単体テスト（権限がない場合は結果が空になる等）を整備する。
- ログと監査UIを早期に用意：不正利用や誤回答のトレーサビリティを確保する。
- 日本法令・ガイドライン対応：個人情報はAPPIや社内ルールに従って扱う。外部LLM利用時は送信するデータを最小化・匿名化する。
- 段階的導入：まずは非本番データで検証→許可されたユーザーのみ→限定機能→本番展開。

