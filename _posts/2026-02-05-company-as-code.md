---
layout: post
title: "Company as Code - 会社をコード化する"
date: 2026-02-05T14:02:27.826Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.42futures.com/p/company-as-code"
source_title: "Company as Code - by Daniel Rothmann - 42futures"
source_id: 46899132
excerpt: "組織をGitでコード化し、ISO監査を自動化して証跡・影響分析を即時可視化する方法を紹介"
image: "https://substackcdn.com/image/fetch/$s_!XLJb!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4811476e-62d6-4158-9343-b72f542fcc87_1232x928.jpeg"
---

# Company as Code - 会社をコード化する
組織もGitで管理する時代へ：ISO監査が楽になる「Company as Code」の全体像

## 要約
組織の方針・構造をドキュメントではなくプログラム的に定義する「Company as Code」を提案。ポリシーのバージョン管理、監査自動化、影響範囲の可視化が可能になる。

## この記事を読むべき理由
クラウド/SaaS中心の業務が当たり前になった日本企業にとって、コンプライアンスや人事・権限管理の効率化は喫緊の課題。特にISOや顧客監査対応で工数を削減したい技術者・管理者は必読。

## 詳細解説
- 問題点：コードやインフラはIaC・GitOpsで管理する一方、組織情報（方針・責任者・関係性）は散在するドキュメントに依存。監査での証跡収集が非効率。
- 提案：組織を宣言的DSLで定義し、グラフ構造（ノード＝人/ポリシー/部署、エッジ＝所属/実装/依存）で扱う。これにより
  - Queryable：ポリシー→影響範囲をクエリ可能
  - Versionable：変更履歴をコードで追跡
  - Integrated：既存ツール（Azure/GitHub/Slack等）と連携して実態と同期
  - Testable：ステージ環境で組織変更を検証
  - Accessible：ローコードUIでビジネス側も利用可能
- 実装要素：DSL、グラフDB（組織モデル）、RDB（証拠データ）、イベントストア（監査トレイル）、プラグイン式インテグレーション（データ収集・検証・強制実行）。
- 期待効果：監査時にマニフェストを直接クエリして証跡を提示、ポリシー変更の自動影響分析、人員異動の事前シミュレーションなど。

例（宣言的DSLのイメージ）:
```hcl
# hcl
Role "SoftwareEngineer" {
  responsibilities = ["コードを書く","レビュー参加"]
}
Person "bob" {
  name = "Bob Johnson"
  role = Role.SoftwareEngineer
  manager = Person.alice
  email = "bob@company.jp"
}
Policy "MFARequired" {
  enforcement = "mandatory"
  owner = Person.alice
}
```

## 実践ポイント
- 小さく始める：まずは組織図と主要ポリシーだけをDSLで定義してGit管理する。
- CIで検証：プルリク→自動テスト（ポリシールール、影響範囲チェック）を導入。
- 一つの統合先から連携：最初はIDプロバイダやGitHubなど最重要システムだけ接続して証拠収集を自動化。
- 可視化を優先：経営/法務が使えるUIを用意して現場の受け入れを促進する。
- 監査対応を想定：ISOや顧客監査の頻出チェック項目を先にマッピングしておく。

以上。Company as Codeは「組織運用のコード化」によって監査・運用コストを削減し、変更の安全性を高める実践的アプローチです。
