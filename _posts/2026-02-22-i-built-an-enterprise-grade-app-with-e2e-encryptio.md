---
layout: post
title: "I built an enterprise-grade app with E2E encryption for 1 user (me) — then realized mobile-first eliminates the entire problem - 自分用にE2E暗号化のエンタープライズ級アプリを作ったら、モバイルファーストが問題を丸ごと消した話"
date: 2026-02-22T08:00:52.852Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.vitaliihonchar.com/insights/what-changed-in-the-personal-application-development-in-the-vibe-coding-era"
source_title: "What changed in the personal application development in the Vibe Coding era? | Vitalii Honchar&#x27;s Blog"
source_id: 399573950
excerpt: "自分用E2Eアプリ構築から学んだ、端末ローカル＋生体認証でサーバ不要にする最短戦略"
image: "https://vitaliihonchar.com/blog/what-changed-in-the-personal-application-development-in-the-vibe-coding-era/what-changed-logo.png"
---

# I built an enterprise-grade app with E2E encryption for 1 user (me) — then realized mobile-first eliminates the entire problem - 自分用にE2E暗号化のエンタープライズ級アプリを作ったら、モバイルファーストが問題を丸ごと消した話
サーバー運用ゼロで個人アプリを安全に運用するための現実的な選択肢 — 「余計なインフラ」を捨てて機能に集中する方法

## 要約
著者はWebでエンドツーエンド（E2E）暗号化・CI/CD・監視まで備えた個人用家計アプリを作ったが、開発・運用コストと攻撃リスクを考え、最終的にモバイルファースト（端末ローカル保存＋デバイス認証）へ移行する判断をした。

## この記事を読むべき理由
日本でもエンジニア兼個人ユーザーが「自分だけのツール」を作る機会が増えています。サーバーを立てる前に、労力・セキュリティ・コストの現実を知り、より安全で手軽な選択肢を理解することは実務にも役立ちます。

## 詳細解説
- 作った構成（元のアプローチ）
  - フロントエンドでユーザー秘密鍵を保持し、サーバーには暗号化済データのみ保存（E2E暗号化）。
  - DDDで設計し、ユニット／E2Eテストを充実させ、GitHub ActionsでCI/CD、Go＋Svelteで高速ビルド。
- 問題点（個人用途での非機能要件）
  - 認証・アクセス制御、監視、CI/CD設定、ホスティング運用（Hetzner 等）、データベース運用（Postgres）…これらは1人分のアプリに対して過剰で、脆弱性や運用ミスのリスクが残る。
  - セキュリティはテストしても完全にはならない。公開サーバーはボットや自動攻撃の対象になりやすい。
- モバイルファーストへの切替理由
  - iOS/Android端末にローカル（SQLite等）でデータを保存すればホスティングや監視が不要。
  - Face ID/生体認証が認証と暗号鍵保護を代替し、多くの攻撃パターンを排除。
  - 単一端末利用なら同期やサーバー要件を放棄して機能実装に集中できる。
- ツール的追い風：Vibe Coding / Claude Code
  - AI支援でモバイル開発の知識が薄くてもアプリ移行や生成が容易になり、バックエンド開発者でも短期間でモバイル版を作れる可能性がある。
- トレードオフ
  - デバイス紛失や機種変更時のデータ移行・バックアップ設計は必要（暗号化されたバックアップ、鍵管理）。
  - マルチデバイス同期が必要なら再びサーバーとE2E設計が必要になる。

## 実践ポイント
- 単一ユーザー・個人用途ならまず「モバイルローカル」を検討する（SQLite + デバイス生体認証）。
- マルチデバイス同期が不要ならサーバーを立てない方がセキュリティ負債を減らせる。
- データ紛失対策として「暗号化バックアップ（ユーザー鍵で暗号化）」を用意する。
- サーバーを使う場合は最小構成で始め、外部監査や自動化に頼りすぎない（簡単な攻撃シナリオでの検証を実施）。
- AI支援ツールを活用してモバイル移行の初期コストを下げ、機能に集中する。

以上。
