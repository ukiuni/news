---
layout: post
title: "Microsoft suspends dev accounts for high-profile open source projects - マイクロソフトが有名オープンソースプロジェクトの開発者アカウントを停止"
date: 2026-04-10T12:37:16.151Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.bleepingcomputer.com/news/microsoft/microsoft-suspends-dev-accounts-for-high-profile-open-source-projects/"
source_title: "Microsoft suspends dev accounts for high-profile open source projects"
source_id: 47716412
excerpt: "Microsoftの自動停止でWireGuard等のWindows更新が不能、脆弱性対応に危機"
image: "https://www.bleepstatic.com/content/hl-images/2025/08/07/Microsoft.jpg"
---

# Microsoft suspends dev accounts for high-profile open source projects - マイクロソフトが有名オープンソースプロジェクトの開発者アカウントを停止
「Windows向けアップデートが突如止まる」──WireGuardやVeraCryptなど主要OSSの配布経路に潜む単一点障害を暴いた事件

## 要約
MicrosoftがWindows向け配布に紐づく開発者アカウントを自動で停止し、WireGuard、VeraCrypt、MemTest86、Windscribe等のプロジェクトがWindows用ビルドや修正を公開できなくなった。マイクロソフトは「Windows Hardware Programの必須認証未完了による自動停止」と説明するが、開発者側は事前通知や迅速な復旧窓口がなかったと訴えている。

## この記事を読むべき理由
Windows利用が多い日本の企業・個人に直接影響するツール（VPN、ディスク暗号化、メモリ診断等）がアップデート不能になると、脆弱性修正やドライバ署名の配布が滞り、大規模なセキュリティリスクや運用問題を招く可能性があるため。

## 詳細解説
- 何が起きたか：複数の高プロファイルなOSS保守者のMicrosoft Partner/Developerアカウントが、事前の個別通知なしに停止され、Windows向けの署名・配布・アップデート提出ができなくなった。Linux/macOS向けは継続できた例が多い。
- 影響項目：Windowsドライバ署名、ブートローダー署名、セットアップEXE／インストーラの新バージョン配布、緊急パッチの即時公開（RCE等の緊急対応が困難に）。
- Microsoftの説明：Windows Hardware Programで義務化されたアカウント認証を完了していないパートナーに対し、自動で停止処理が走る仕様で、一定期間の通知後に「Rejected」扱いなら停止されると公表。運用側はメールやバナーで告知したと主張するが、当該開発者らは個別連絡を受けていないと述べる。
- 運用上の問題点：自動停止・人手対応の乏しさ、復旧の遅さ、サプライチェーンとしての透明性欠如。メディア露出やSNSでの発信がなければ復旧が進まなかったケースも報告されている。
- リスクシナリオ：もしWireGuard等にゼロデイのリモート実行脆弱性が発見されていたら、Windowsユーザー向けの迅速な修正版配布が妨げられ、被害拡大の要因になり得る。

## 実践ポイント
- 開発者（OSS保守者）向け
  - Windows関連の公式アカウントは必ず事前に認証・二段階確認を完了する。複数の連絡先（組織メール、代替管理者）を登録する。
  - Windows向け配布に依存しすぎない：GitHub Releases、流通ミラー、パッケージ署名の多重化を用意する。
  - 緊急時の連絡フロー（別の公開チャネルや法務窓口、スポンサー経由）を整備する。
- ユーザー／企業向け
  - 重要ツールは複数の入手経路を確保し、信頼できる署名・ハッシュを検証する習慣を持つ。
  - サプライチェーン障害を想定した脆弱性対応計画を作る（代替ツールや一時的な緩和策）。
  - 主要OSSのセキュリティ通知（メールリスト、GitHubのSecurity Advisories）を購読する。

短期的には、関係開発者はアカウント確認を優先し、利用者側は配布停止のアナウンスを逐次チェックしてください。
