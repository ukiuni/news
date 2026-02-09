---
layout: post
title: "Actually Static: When WordPress Stops Being the Enemy - WordPressが「敵」じゃなくなるとき"
date: 2026-02-09T14:23:55.947Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/pascal_cescato_692b7a8a20/actually-static-when-wordpress-stops-being-the-enemy-37h5"
source_title: "Actually Static: When WordPress Stops Being the Enemy - DEV Community"
source_id: 3239954
excerpt: "WordPressのまま執筆→Markdown＋画像最適化でGitHub経由で即静的公開"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fvi87xptrx7q33iad0szb.png"
---

# Actually Static: When WordPress Stops Being the Enemy - WordPressが「敵」じゃなくなるとき
WordPressはそのままに、公開だけを高速で安全な静的サイトにする魔法 — 書くことを止めずにデプロイを自動化するプラグインの話

## 要約
WordPressを執筆環境のまま残し、公開だけをMarkdown＋最適化画像でGitHubリポジトリに自動同期してHugo（GitHub Pages）で静的デプロイするプラグインを紹介する記事です。非同期同期、アトミックコミット、ローカル画像最適化などで実運用の課題をクリアしています。

## この記事を読むべき理由
日本でも企業ブログや技術記事の多くはWordPressで書かれています。編集体験を犠牲にせず、表示速度・セキュリティ・運用コストを下げたい人に直接役立つ実践的ソリューションだからです。

## 詳細解説
- 解決したい問題：WordPressは編集が快適だが公開をそのままにするとホスティング、プラグイン、パフォーマンス、保守の負担が大きい。静的サイトは速く安全だが、執筆→デプロイの摩擦がある。
- 提案アーキテクチャ：WordPressプラグインが公開時に記事をHugo互換のMarkdown＋フロントマターに変換し、AVIF/WebPを含む最適化画像とともにGitHubのTrees APIで「一括（アトミック）コミット」。GitHub Actionsが静的サイト生成とGitHub Pagesへのデプロイを担当。
- 主要技術：WordPress 6.9+/PHP 8.1+, GitHub API（Trees）、Action Scheduler（非同期処理）、Intervention Image（画像最適化）、Hugo、GitHub Actions。
- 実務で直面した課題と対策：Hugoバージョン固定、production用baseURLのハードコード、PHPメモリ制限対策（memory_limit 512M、逐次処理）、保存フックのデバウンス（重複コミット防止）、例外ハンドリングでロック解放、.gitattributesでLF統一など。
- 設計ポイント：
  - ローカル（WP側）で画像をAVIF/WebPに変換→CIで処理を省くことでランナー時間とコストを削減。
  - 画像はWordPress IDベースの固定パスに保存し、URL切れを防止。
  - フロントマターテンプレートを設定で変更可能にし、Hugo以外のSSG（Jekyll/Eleventy/Astro等）にも対応できるアダプタ構成。
  - プラグインはWPネイティブAPIのみで実装し、WordPress.org準拠を意識。
- 現状の制限（MVP）：下書きは同期しない、リビジョン履歴は同期されない、複雑なGutenbergブロックやショートコードはHTML化して保存、ACF等の拡張は別アダプタ必要、Git→WPの双方向同期はしない（意図的）。

## 実践ポイント
- 必須設定：PHP 8.1+、memory_limit を最大512Mへ（画像処理するなら必須）、GitHub Personal Access Tokenを用意。
- CI対策：HugoバージョンはCIワークフローで明示的にピン留め。baseURLは本番用URLをワークフローで設定。
- 運用Tips：.gitattributesでLFを強制、WP-CLI（例: wp jamstack sync --all）で一括再同期、フロントマターテンプレートを用意してテーマ/SSG変更を簡単に。
- 検討事項：編集体験を維持したいチームはこの方法で「書く場所」と「公開場所」を分離すると効果大。まずはテスト用リポジトリでプラグインを試し、画像処理の負荷とメモリ設定を確認すること。

元記事の実装はデモとリポジトリ（Hugoワークフロー、content構成、static/images）を公開しており、WordPressをそのまま編集環境に残しつつ静的公開に移行したい日本の現場でも即試せる実践的アプローチです。
