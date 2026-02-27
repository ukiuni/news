---
layout: post
title: "Google API Keys Weren't Secrets. But then Gemini Changed the Rules. - GoogleのAPIキーは秘密じゃなかった。でもGeminiがルールを変えた。"
date: 2026-02-27T12:50:56.956Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules"
source_title: "Google API Keys Weren't Secrets. But then Gemini Changed the Rules. ◆ Truffle Security Co."
source_id: 395590879
excerpt: "公開Google APIキーがGeminiで危険に—データ漏洩・課金被害の即点検を"
image: "https://framerusercontent.com/images/YDDp8rnck6rG7jTHoAV4O5bs.png?width=1024&amp;height=572"
---

# Google API Keys Weren't Secrets. But then Gemini Changed the Rules. - GoogleのAPIキーは秘密じゃなかった。でもGeminiがルールを変えた。
公開されたMaps/Firebaseキーが「いつの間にか」機密資格情報になってしまう――あなたのサイトにも起こりうる話

## 要約
Googleが長年「APIキーはクライアントに埋め込んで良い」としてきた設計で、Gemini（Generative Language API）の登場により既存の public な APIキーが機密的な権限を持つようになり、公開されたキーでデータ盗難や高額請求が発生する危険があるとTruffle Securityが報告した。

## この記事を読むべき理由
日本の多くのサービスがMaps、Firebase、YouTubeなどで同様の公開キー運用をしており、気づかないうちにGemini経由で個人情報や機密データが露出したりAI利用料を悪用されるリスクがあるため、即時点検・対策が必要。

## 詳細解説
- 問題の核心：Googleは長年「APIキー（形式: AIza...）」をプロジェクト識別・課金トークンとして扱い、クライアント埋め込みを許容してきた。一方、Geminiの有効化により同じキーが機密APIへアクセスできるようになった（レトロアクティブな権限拡張）。
- 不備の原因：
  - 単一キー形式：公開識別用と認証用が同じフォーマットで区別されない。
  - デフォルトが「Unrestricted」：新規キーは即座にプロジェクト内の全APIに対して有効。
  - 変更の通知がない：既存の公開キーの権限が裏で変わっても開発者に警告されない。
- 攻撃の手順（簡易）：
  1. Webページのソースや公開リポジトリからAIza...キーを取得。
  2. Geminiエンドポイントへリクエスト（例：/v1beta/files）を投げ、200 OKでアクセスできるか確認。
- 被害例：公開ウェブ上で2,863本の脆弱なキーを確認。Google自身の公開サイトの古いキーも利用可能だった。侵害でファイル読み出し、キャッシュ内容取得、課金悪用、クォータ枯渇などが可能。
- 開示経緯とGoogle対応：Truffleが報告→当初「意図した挙動」と判定→証拠提示でバグ扱いに変更。Googleは漏洩検知やGeminiアクセスの制限、通知強化など対策ロードマップを提示中。

## 実践ポイント
- まず確認（優先度高）
  1. GCPコンソールで組織内全プロジェクトの「APIs & Services > Enabled APIs」にて Generative Language API が有効か確認。
  2. APIキー一覧（APIs & Services > Credentials）で「Unrestricted」や Generative Language API を許可しているキーを洗い出す。
- 見つけたら即対応
  - 公開されたキーは直ちにローテーション（新しいキーを発行して古いキーを無効化）。
  - キーに対してサービス制限（許可するAPIの明示）とアプリケーション制限（HTTPリファラ、IP）を設定。
  - 必要なら該当プロジェクトのGemini無効化や課金上限・アラート設定で被害抑止。
- 検出ツール
  - TruffleHog 等でリポジトリ・公開アセットをスキャン（TruffleHogは実際にキーの有効性とGeminiアクセスを検証可能）。
  - GitHubのシークレットスキャンや自動化パイプラインに漏洩検知を組み込む。
- 運用改善
  - 公開用（publishable）キーと機密用（secret）キーを分離する設計に移行。
  - キー作成のデフォルトを絞る、キー有効化時の通知・監査ログを強化するワークフローを導入。

参考（攻撃例コマンド）
```bash
# bash
curl "https://generativelanguage.googleapis.com/v1beta/files?key=$API_KEY"
```

短期的にまず「Generative Language API の有効化状況」と「公開されているAPIキー」を全プロジェクトで確認してください。
