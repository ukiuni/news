---
layout: post
title: "Everything as Code: How We Manage Our Company in One Monorepo - すべてをコード化：1つのモノレポで会社を運用する方法"
date: 2025-12-30T20:38:27.421Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.kasava.dev/blog/everything-as-code-monorepo"
source_title: "Everything as Code: How We Manage Our Company in One Monorepo"
source_id: 46437381
excerpt: "プロダクト・ドキュメント・運用を1つのモノレポで一括管理しAI支援で変更を自動反映する実践法"
---

# Everything as Code: How We Manage Our Company in One Monorepo - すべてをコード化：1つのモノレポで会社を運用する方法
モノレポで“会社ごと”運用する──AIと一緒に動く開発体験を手に入れる方法

## 要約
1つのモノレポにプロダクト、ウェブサイト、ドキュメント、メール、拡張機能まで全部入れて運用することで、変更の原子性・一貫性・AIとの親和性を得て、開発・運用の速度と信頼性を高める実践例。

## この記事を読むべき理由
日本のプロダクト開発でも、複数ツールやCMSにまたがる運用は頻繁に同期ミスや調整コストを生む。本記事は「コードで全てを扱う」実装パターンと運用ルールを具体例とともに示し、AI支援が自然に機能する開発基盤を作るヒントを与える。

## 詳細解説
- モノレポの範囲  
  Kasavaの例では、frontend（Next.js + React）、backend（Cloudflare Workers + Hono）、website（マーケティング）、docs、emailテンプレート、Chrome拡張、Google Apps Script、Tree‑sitterサービス、テスト用モックまで一つのリポジトリに収めている。これにより「1コミットでフロント・バック・サイト・ドキュメントが同期する」ことが可能になる。

- AIネイティブな利点  
  AIアシスタント（例: Claude）がコードベースとドキュメントを同じコンテキストで読めるため、料金変更や仕様追加を「話しかけるだけ」で横断的に反映・検証できる。単一のソースオブトゥルースはAIによる自動チェックやドキュメント提案の精度を上げる。

- 一貫したワークフロー  
  コード、ブログ、メール、投資家向け資料までGitで管理し、PR→CI→デプロイの流れで全てレビューされる。結果としてローリングアップデートやロールバックがgit操作で完結する。

- 技術的な運用ルール（抜粋）  
  - 各サブディレクトリは独立したnpmプロジェクトにして、依存関係のホイスティングや複雑なワークスペース運用を避ける。  
  - パスベースのGitHub Actionsで影響範囲に応じたSelective CIを走らせる（例：frontend/** に変更があればフロント用テストのみ）。  
  - 各ディレクトリにCLAUDE.mdのような「プロジェクトのメタ情報」を置き、AIや新任者が環境を理解しやすくする。  
  - ローカル開発用のモック（github-simulatorなど）や統合テストハーネスを同梱し、外部依存を減らす。

- 実例：料金設定の単一管理  
  billing-plans.json のような共通設定ファイルをバックエンド・フロントエンド・マーケティングで共有することで、「ウェブは50件、アプリは25件」といった不整合を排除する。

json
```json
{
  "plans": {
    "free": { "limits": { "repositories": 1, "aiChatMessagesPerDay": 10 } },
    "starter": { "limits": { "repositories": 10, "aiChatMessagesPerDay": 100 } },
    "professional": { "limits": { "repositories": 50, "aiChatMessagesPerDay": 1000 } }
  }
}
```

- 運用上の課題と対策  
  リポジトリ肥大化、CIの実行コスト、権限分離の運用負荷などは避けられない。Kasavaはクローン時間が短く、パスベースCIやプロジェクト分割で影響を限定する方針を取っている。

## 実践ポイント
- まずは「設定とドキュメント」をモノレポに移す：料金・フィーチャーフラグ・メールテンプレートなどをGitで管理してみる。  
- パスベースのCIを導入して、変更ごとに必要なテストだけを走らせる。  
- 各サブプロジェクトにCLAUDE.md相当のREADMEを置き、ツールチェインや起動手順を明文化する（AIにも読みやすい形式で）。  
- 外部サービス依存はモックを同梱してローカルで完結させる。  
- 最終的に「コンテンツもコードでレビューする」文化を育てる（マーケとエンジニアが同じPRフローで協業）。

