---
layout: post
title: "/e/OS is a complete \"deGoogled\", mobile ecosystem - /e/OSは完全な「DeGoogled」モバイルエコシステム"
date: 2026-03-02T10:04:40.452Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://e.foundation/e-os/"
source_title: "/e/OS - e Foundation - deGoogled unGoogled smartphone operating systems and online services - your data is your data"
source_id: 47215489
excerpt: "トラッカー可視化や無料1GB搭載、/e/OSで脱Google端末を実現"
---

# /e/OS is a complete "deGoogled", mobile ecosystem - /e/OSは完全な「DeGoogled」モバイルエコシステム
脱Googleでプライバシー重視の“使える”スマホ体験を手に入れる——/e/OSとMurenaが目指す新しいモバイル環境

## 要約
/e/OSはGoogleのサービスを排したオープンソースのAndroid系OSと、Murenaが提供するクラウド／アカウントを組み合わせた「deGoogled」なモバイルエコシステムで、アプリ互換性やトラッカー可視化、無料のMurena Workspaceなど実用機能を備える。

## この記事を読むべき理由
日本でも個人情報保護や企業のデータ漏洩対策が強まる中、Google依存を減らした端末運用は個人・法人問わず現実的な選択肢になりつつあります。既存のAndroidアプリ資産を維持しつつプライバシーを高めたい読者に有益です。

## 詳細解説
- コア設計：AOSPベースでGoogleアプリ／サービスを排除。GoogleのNTP/DNSや接続チェックを使わず、代替実装（microGやBeaconDBなど）で機能を置換。  
- アプリ互換性：多くのAndroidアプリが動作する設計。デフォルトでオープンソース系アプリを選定し、UI改善を施す。  
- プライバシー可視化：アプリごとのトラッカー数や要求パーミッションをスコア表示し、インストール前にリスク評価が可能。ブラウザは広告ブロックを初期有効化。  
- Murena Workspace：@murena.ioアカウントで1GB無料ストレージ、E2E暗号化のVault、メールやオンラインドキュメントを提供。自主管理（セルフホスティング）も選択可。  
- 家族向け／運用機能：ペアレンタルコントロール、端末追跡、Account Managerによる複数アカウント同期など、実用的な管理機能を用意。  
- 導入手段：Murena端末購入、Webベースの/ e/OS Installer（WebUSB対応）、あるいはGitLabからの手動インストール。コミュニティサポートと開発リソースが公開されている。

## 実践ポイント
- まず互換端末を確認：公式の対応端末リストとInstallerの対応状況をチェック。  
- テスト導入：既存端末でInstallerを使って試し、重要アプリの動作とトラッカー表示を確認。  
- Murena Workspaceを試す：無料1GBアカウントでメールやVaultを体験して運用感を把握。  
- 法人利用はPoCから：社内でのデータフローや認証連携（Google/Yahoo等）影響を小規模で検証。  
- 自主管理が必要なら：セルフホスティングの可否と運用コストを評価してから移行を検討。  

興味があれば公式ドキュメントとコミュニティフォーラムで最新の対応端末・導入手順を確認してください。
