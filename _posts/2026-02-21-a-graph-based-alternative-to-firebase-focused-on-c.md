---
layout: post
title: "A graph-based alternative to Firebase focused on collaborative SaaS apps - コラボ向けSaaSに特化した、Firebaseの代替となるグラフ型プラットフォーム"
date: 2026-02-21T14:16:25.846Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://linkedrecords.com/getting-started/"
source_title: "Getting Started"
source_id: 400154953
excerpt: "Factベースで共有語彙と細かな権限をほぼサーバーコード不要で実現するLinkedRecords"
---

# A graph-based alternative to Firebase focused on collaborative SaaS apps - コラボ向けSaaSに特化した、Firebaseの代替となるグラフ型プラットフォーム
Firebaseっぽい手軽さ×「グラフ（事実／トリプル）」で共有と権限管理を自然に扱えるLinkedRecordsの概観と導入ガイド

## 要約
LinkedRecordsは「事実（Fact）/トリプル」と属性を中心にしたグラフ型バックエンドで、認証・権限・共有・永続化をほぼサーバーコード無しで提供し、複数ユーザーが共同作業するSaaSに向く。

## この記事を読むべき理由
日本のスタートアップやプロダクトチームが、素早く共同編集や細かい参照権限を伴う機能を試作・実装する際、従来のFirebaseやREST設計より自然に表現できる選択肢だから。プロトタイプからチーム向け機能まで短期間で実現できます。

## 詳細解説
- アーキテクチャの核  
  - データは「Fact（トリプル）」と「Attribute（属性）」で表現。Factは [主語, 述語, 目的語] の形で、用語（Term）は事前宣言して共有語彙にする。属性はKey-Valueでオブジェクトを保管する想定。  
  - 用語（例: "Archived"）は $isATermFor で宣言する必要があり、宣言済みの用語のみオブジェクトとして参照可能。これにより共有語彙と権限モデルが両立する。

- 認証と権限  
  - OIDCベース（開発用はモックのOIDCでワンクリックログイン）。サービスは「誰が何を参照・参照可能か」「誰が主語を拡張できるか」など細かい権限チェックを自動で行う（例: $canRefine, $canReferTo）。  
  - ユーザー単位でスコープされたデータ管理がデフォルトで効くため、個人データと共有データの境界が扱いやすい。

- 開発フロー（公式チュートリアルの要点）  
  - ローカル起動は Docker Compose 一行で（開発用モックOIDC付き、6543番ポート）。  
  - フロントは Vite + React（もちろん任意）で、linkedrecords-react パッケージの Provider をルートに置くだけで API が使える。  
  - 主要メソッド例（概念）:  
    - Attribute.createKeyValue(...)：Key-Value属性の作成（Todoの本文など）  
    - Fact.createAll([...])：用語宣言や状態遷移（Archived/Active 等）を一括登録  
    - useKeyValueAttributes(query)：クエリに合致する属性群をリアクティブに取得  
    - lr.isAuthenticated()/lr.login()/lr.getCurrentUserEmail()：認証フローと現在ユーザー取得  
  - 実例：Todoアプリを短時間で作成でき、ユーザー毎の永続化・ログイン切替・アーカイブ／復元・共有（招待）をサポート。

- 共同作業における利点  
  - 「用語を宣言する」仕組みで、状態やカテゴリなどの共有語彙を安全に管理。  
  - ファクトベースの履歴や参照性により、誰が何を参照・変更したかを追いやすく、細かいコラボ権限設計が可能。

## 実践ポイント
- まずはローカルで動かす：公式の docker-compose（開発用モックOIDC）で backend を起動（ポート6543）。  
- フロントは Vite + React で素早くプロトタイプ。linkedrecords-react を Provider でラップすればすぐ使える。  
- 用語（Terms）は必ず事前宣言（$isATermFor）する — 省くと参照や状態遷移が失敗する。  
- ユーザー単位の可視性や共有を試すには、別ブラウザ／シークレットで別ユーザーでログインして動作を確認。  
- 日本のプロダクトでの活用例：チームで共有するタスク管理、ドキュメントのアクセス権管理、カスタム分類の共通語彙化など。既存の認証（OIDC）と統合すれば本番移行も視野に入る。

興味があれば、ローカルでの起動コマンドやReactの最小実装例を短くまとめます。どれを知りたいですか？
