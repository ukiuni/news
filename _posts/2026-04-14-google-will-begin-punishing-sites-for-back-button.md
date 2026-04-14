---
layout: post
title: "Google will begin punishing sites for back button hijacking starting in June - Googleが「戻る」改ざんサイトを6月から制裁へ"
date: 2026-04-14T17:03:51.967Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/gadgets/2026/04/websites-that-hijack-your-back-button-must-stop-by-june-15-or-face-googles-wrath/"
source_title: "Google will begin punishing sites for back button hijacking in June - Ars Technica"
source_id: 361799840
excerpt: "Googleが6月15日から「戻る」ハイジャックを制裁、検索流入依存サイトは即点検"
image: "https://cdn.arstechnica.net/wp-content/uploads/2025/05/google-logo-green-terminal-1152x648.jpg"
---

# Google will begin punishing sites for back button hijacking starting in June - Googleが「戻る」改ざんサイトを6月から制裁へ
「ブラウザの“戻る”が効かない」サイトに制裁──検索流入頼みのサイトは今すぐチェックを

## 要約
Googleは2026年6月15日から「戻るボタンのハイジャック」を悪質な行為とみなし、違反サイトに自動／手動のペナルティ（検索順位下落など）を適用すると発表しました。

## この記事を読むべき理由
検索流入に依存する日本のニュース・ブログ・EC・アフィリエイトサイトは、突然のトラフィック激減でビジネスリスクを負います。SPAや広告ライブラリ経由で知らぬ間に改ざんが入ることも多く、開発・運用者は早急な対応が必要です。

## 詳細解説
- 何が問題か：ユーザーがブラウザの「戻る」を押しても意図した前のページに戻らず、別の“ファントム”ページ（関連記事一覧やポップアップ等）を差し挟む手口を指します。目的はページビュー増加や広告クリック誘導です。  
- 技術的手法：history.pushState/replaceState や onpopstate ハンドリング、リダイレクトループ、ハッシュ操作などでブラウザ履歴を書き換え、正常な戻り挙動を妨げます。  
- Googleの対応：新たなルールではなく、既存の「悪質な行為（malicious practices）」ポリシーの適用を徹底。6/15以降は自動・手動のアンチスパム処置が入り得ます。結果として検索順位の大幅低下やインデックス影響が起きます。  
- 事例言及：LinkedInなど、大手でもユーザーをフィードに戻す実装が問題視されてきました。問題は自サイト実装だけでなく、サードパーティの広告・ライブラリに起因することも多い点です。

## 実践ポイント
- 緊急監査：開発環境・本番でブラウザの戻る操作を手動・自動テストし、期待通りに前のページへ戻るか確認する。  
- コードチェック：history API（pushState/replaceState/onpopstate）の利用箇所を洗い出し、不要な履歴挿入・阻害を除去する。SPAはルーティング設計を見直す。  
- サードパーティ確認：広告ネットワーク、ウィジェット、トラッキングライブラリをアップデート／無効化して挙動を確認。ベンダーへ改善を要求。  
- モニタリング：Google Search Consoleのメッセージと手動対策通知を監視し、流入・CTRをAnalyticsでウォッチ。問題が疑われたら即対応ログを残す。  
- 期限を意識：Googleは2026年6月15日から適用開始。余裕をもって今すぐ対応を始めること。

以上。問題箇所が特定できれば短期間で修正可能です。必要なら技術的な調査手順や簡単なテストスクリプト例も提供します。
