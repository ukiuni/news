---
layout: post
title: "Show HN: Mastra 1.0, open-source JavaScript agent framework from the Gatsby devs - Show HN: Mastra 1.0、Gatsby開発者によるオープンソースJavaScriptエージェントフレームワーク"
date: 2026-01-20T21:25:19.450Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mastra-ai/mastra"
source_title: "GitHub - mastra-ai/mastra: From the team behind Gatsby, Mastra is a framework for building AI-powered applications and agents with a modern TypeScript stack."
source_id: 46693959
excerpt: "TypeScript製Mastraで複数モデル統合の本番向けAIエージェントを即構築"
image: "https://opengraph.githubassets.com/3d42513905e7c5326295ffd485eb1ef22e682e83dc6f69e149382cdc34abe300/mastra-ai/mastra"
---

# Show HN: Mastra 1.0, open-source JavaScript agent framework from the Gatsby devs - Show HN: Mastra 1.0、Gatsby開発者によるオープンソースJavaScriptエージェントフレームワーク
Gatsbyチーム発、TypeScriptで作る「実運用向けAIエージェント基盤」Mastraを試す理由

## 要約
MastraはGatsby開発チーム発のオープンソースフレームワークで、TypeScriptベースでエージェント＋ワークフローを素早くプロトタイプから本番へ移行できる設計（モデルルーティング、エージェント、グラフ型ワークフロー、監視・評価など）を提供する。

## この記事を読むべき理由
日本のスタートアップや企業が、既存のWebスタック（React/Next.js/Node）に安全・拡張性のあるAI機能を統合したい場面で、Mastraは「現場で使える」選択肢になる。TypeScript中心で導入障壁が低く、複数のモデルプロバイダを1つのインタフェースで切替えられる点は、日本のデータポリシーやプロバイダ多様化にも有利。

## 詳細解説
- コア設計
  - TypeScriptファースト：パッケージ群が整理され、フロント〜サーバーまで統一的に扱える。
  - オープンソースかつ活発（GitHub: 約19.5k★、1.4k fork、多数のコントリビュータ）。
- モデルルーティング
  - 40以上のプロバイダを単一のインタフェースで利用可能。OpenAI, Anthropic, Google Gemini等を切替えて評価・運用できる。
- エージェント
  - LLMに「目的」を与え、必要なツールを呼び出しながら自己判断でタスクを完遂するエージェントを構築可能。内部で複数の推論・反復を行い、最終出力や停止条件を管理する。
- ワークフローエンジン
  - グラフベースで明示的な制御が可能。.then(), .branch(), .parallel() のような直感的APIでステップを繋げられるため、複雑なビジネスロジックを表現しやすい。
- Human-in-the-loop と状態管理
  - 実行状態を永続化して、ユーザ承認や入力待ちで処理を一時停止・再開できる。長期の承認フローや審査ワークフローに適合。
- コンテキスト管理
  - 会話履歴、外部データベース/API/ファイルからの情報取り込み、意味記憶（semantic memory）や作業記憶で一貫性のある応答を実現。
- 統合と運用
  - React/Next.js/Nodeに容易に組み込み可能。観測（observability）や自動評価（evals）機能でモデルの挙動を監視し継続的に改善できる。MCP（Model Context Protocol）サーバーを介して他システムと連携可能。
- セキュリティとサポート
  - OSSライセンス、セキュリティ報告窓口（security@mastra.ai）、テンプレ・チュートリアル・Discordコミュニティあり。

## 実践ポイント
- まず試す
  - CLIでテンプレから素早く開始:
    ```bash
    npm create mastra@latest
    ```
- 最低限の検証フロー
  1. 公式テンプレートでサンプルエージェントを起動し、OpenAI等と接続して挙動を確認。
  2. モデルルーティングで同一プロンプトを複数プロバイダに投げ、応答品質とコストを比較。
  3. .then() / .branch() を使ったワークフローで、承認ありのHuman-in-the-loopを実装して動作確認。
- 日本向けの注意点
  - データ所在（国内リージョン要件）がある場合は、プロバイダ選定やオンプレモデルの組合せを検討する。
  - 個人情報や業務機密を扱うワークフローでは、ストレージ・アクセス制御・監査ログの設計を優先。
- 本番運用準備
  - builtin evals と observability を必ず組み込み、モデル挙動のモニタリングと継続改善ループを作る。
  - ライセンスとセキュリティ連絡先（security@mastra.ai）を確認し、社内ポリシーに合わせた審査を行う。
- コミュニティ活用
  - ドキュメント、YouTubeチュートリアル、Discordで疑問解消やテンプレ拡張を行う。

短時間でプロトタイプを挙げ、本番に必要な観測・評価ループをすぐに組み込みたい場合、Mastraは現実的な選択肢となる。日本の要件（データ駐在、オンプレ事情、プロバイダ多様化）を考慮しつつ、まずはテンプレで手を動かすことが最短の理解手段。
