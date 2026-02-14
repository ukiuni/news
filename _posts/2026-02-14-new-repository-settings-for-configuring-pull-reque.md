---
layout: post
title: "New repository settings for configuring pull request access - プルリクエストアクセスを設定するための新しいリポジトリ設定"
date: 2026-02-14T18:13:13.034Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.blog/changelog/2026-02-13-new-repository-settings-for-configuring-pull-request-access/"
source_title: "New repository settings for configuring pull request access - GitHub Changelog"
source_id: 1179610344
excerpt: "GitHubがPRを完全無効化や協力者限定で外部PRを封じる新設定を追加"
image: "https://github.blog/wp-content/uploads/2026/02/548515957-56ddc14a-9f83-4ddc-b19f-b5177c1925f8.jpeg"
---

# New repository settings for configuring pull request access - プルリクエストアクセスを設定するための新しいリポジトリ設定

## 魅力的タイトル
PRを受け付けない選択肢と協力者限定PR──GitHubが「応募の窓口」を細かく制御できる新設定を導入

## 要約
GitHubがリポジトリごとに「プルリクエストを完全無効化」または「協力者のみ作成可」にする新しい設定を追加。公開・非公開問わずすぐ利用可能で、ミラーや読み取り専用、重要フェーズでの貢献管理に有効。

## この記事を読むべき理由
オープンソース運営や社内リポジトリの運用ポリシーが厳格化する中、誰がどのように変更を送れるかをUIレベルで制御できる意味は大きい。日本のOSSプロジェクトや企業開発でも、雑多な外部PRやリスクを減らしつつ公開のメリットを残せる運用に直結します。

## 詳細解説
- 追加された2つの設定（リポジトリ → Settings → General → Features）
  1. Disable pull requests entirely（プルリクエストを完全に無効化）  
     - PRタブが非表示になり、既存のPRも含めて閲覧・作成ができなくなる。  
     - ミラーリポジトリや読み取り専用の公開コードで有用。
  2. Restrict pull requests to collaborators（協力者のみプルリク作成可）  
     - PRタブは表示され、全員が閲覧・コメント可能だが、新規PRを作成できるのは collaborators（書き込み権限を持つユーザー）のみ。  
     - リリース前や品質管理が必要なフェーズで、提出者を限定してレビュー負荷や品質を保つ用途に向く。  
- 設定の適用範囲：すべてのパブリック・プライベートリポジトリで利用可能。  
- モバイルアプリの差異：フルUIは順次対応中。現状、PRを無効化してもモバイルではタブが表示されるが作成は不可。  
- 補足：一時的に特定ユーザーからの活動を制限したい場合は「一時的なインタラクション制限（temporary interaction limits）」を併用可。

## 実践ポイント
- ミラーや配布用リポジトリ：Settings → General → Features で「Disable pull requests entirely」を有効化して外部貢献を遮断。READMEに明記して誤解を防ぐ。  
- 開発中の重要ブランチやリリース期間：一時的に「Restrict pull requests to collaborators」を使い、外部PRの流入を防ぎつつレビューは公開にして透明性を確保。  
- コラボレーター管理：Collaboratorsタブで書き込み権限を調整し、誰がPRを作成できるかを運用ポリシーに合わせて管理。  
- モバイル利用者へ注意喚起：モバイルUIの制約があるため、外部コントリビュータにはWebでの挙動を案内する。
