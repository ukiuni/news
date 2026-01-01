---
layout: post
title: "I built DevBench – an offline-first developer desktop tool with API client, planner, notes, diagrams & Git sync - オフライン重視の開発デスクトップ「DevBench」を作った：APIクライアント、プランナー、ノート、図、Git同期を一つに"
date: 2026-01-01T08:38:38.430Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://devbench.in/"
source_title: "I built DevBench – an offline-first developer desktop tool with API client, planner, notes, diagrams &amp; Git sync"
source_id: 473823185
excerpt: "オフラインで動くAPIクライアントやノート、図をGit同期で一本化する開発デスクトップツール"
---

# I built DevBench – an offline-first developer desktop tool with API client, planner, notes, diagrams & Git sync - オフライン重視の開発デスクトップ「DevBench」を作った：APIクライアント、プランナー、ノート、図、Git同期を一つに

魅力的な日本語タイトル: ローカルで完結する「全部入り」開発デスクトップ — DevBenchが仕事をどう変えるか

## 要約
DevBenchはAPIクライアント、ノート、図、日次プランナー、JS実行環境、Docker/K8sツールなどを一つにまとめたオフラインファーストなデスクトップアプリで、個別ファイル＋Gitベースで同期・自動保存するのが特徴。

## この記事を読むべき理由
日本の開発現場ではセキュリティ、オフライン作業（出張やセキュア環境）、ドキュメントのバージョン管理が重要。DevBenchは「ローカル優先」「Gitでの差分管理」「ツール集約」により、ツールチェーンの簡素化とデータ管理の透明化を同時に実現します。

## 詳細解説
- オフライン第一設計
  - 全機能がネット無しで動作。接続時にGitで同期するワークフローを採用しており、ネットワーク制約のある環境や移動中の作業に強い。
- Gitベースの個別ファイル同期
  - ノートやAPIリクエスト、図などを個別ファイルとして保存するため、差分管理やマージが扱いやすく、従来のバイナリblobに比べ競合解消が容易。
- APIクライアント
  - GET/POST/PUT/PATCH/DELETEなど多様なHTTPメソッド対応、cURLやPostman/Swaggerコレクションのインポート、レスポンスのRaw/Preview/Headers表示。APIテストとドキュメントを同じリポジトリで管理できる。
- ドキュメント & 図
  - BlockNoteベースのリッチノート、Excalidraw統合でスケッチやUI図の保存、Mermaid文法でUMLやフローチャートを記述しMonacoエディタでプレビュー可能。全て個別ファイルでGit追跡。
- 実行環境とコンテナ管理
  - サンドボックス化されたJavaScript実行（npmモジュールサポート）、Docker/Kubernetesのログやシェルアクセス機能で、ローカル検証からコンテナ操作まで一貫して行える。
- UX/実装
  - Electron + Reactでクロスプラットフォーム（macOS/Windows/Linux）、オープンソース（MIT）、自動保存・プライバシー重視（データは基本ローカル、エンドツーエンド暗号化で同期）。
- 配布と要件
  - 各OS用バイナリをGitHubで提供。同期にはGitが必要。Node.jsは同梱されるため別途インストール不要。macOSはGatekeeper回避手順あり（未署名のため）。

## 実践ポイント
- まずはGitリポジトリを用意して試す：既存のドキュメント用リポジトリをリモートに用意して、DevBenchでノート／API定義／図をコミット→プッシュして動作検証。
- Postman代替として段階的導入：重要APIコレクションをインポートして既存ワークフローと比較。ファイルベースの履歴が残る点が利点。
- 図とドキュメントをコードと同じリポジトリに入れる：設計図・UMLをソースと同じ管理下に置くとレビューやCI連携が楽になる。
- オフラインでの検証環境に最適：出張やセキュアネットワーク（社内LANのみ）での作業が多いチームは恩恵大。
- セキュリティ運用の注意：アプリは未署名の配布があるため導入時に社内ポリシーとの整合を確認。エンドツーエンド暗号化の設定とバックアップ戦略は必須。
- 拡張案：既存CIやドキュメント生成ツールと組み合わせ、Mermaid→PNGやMarkdown生成をCIに組み込むことで自動化を進める。

## 引用元
- タイトル: I built DevBench – an offline-first developer desktop tool with API client, planner, notes, diagrams & Git sync
- URL: https://devbench.in/
