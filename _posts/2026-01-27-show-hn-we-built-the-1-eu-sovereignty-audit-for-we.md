---
layout: post
title: "Show HN: We Built the 1. EU-Sovereignty Audit for Websites - EU主権性（独立性）監査ツールを作ったよ"
date: 2026-01-27T14:20:10.044Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lightwaves.io/en/eu-audit/"
source_title: "Lightwaves • EU Audit"
source_id: 46779994
excerpt: "無料ツールで自社サイトのEU外依存を瞬時に可視化し、対策箇所を特定できる"
image: "https://lightwaves.io/images/news/ship-europe-first/eu-privacy-shield.png"
---

# Show HN: We Built the 1. EU-Sovereignty Audit for Websites - EU主権性（独立性）監査ツールを作ったよ
EU依存を秒速チェック——あなたのサイトは「非EUサービス」にどれだけ頼っている？

## 要約
Lightwavesが公開した無料の「EU-Sovereignty Audit」は、ホスティング位置やフォント、解析、CDN、動画埋め込み、チャット等の外部依存を自動でスキャンし、どれだけEU外サービスに依存しているかを可視化します。将来的なEU域外データフロー規制の変化に備えるための初動ツールです。

## この記事を読むべき理由
EU向けサービスやEU市民のデータを扱う日本の事業者にとって、米国系サービスへの依存は法的・事業リスクになります。監査で「どこを替えるべきか」が分かれば、コンプライアンス強化・サービス継続性の確保に直結します。

## 詳細解説
- 何をチェックするか：ホスティングの所在地、Google/Adobeフォントの使用、Google Analytics等の解析、Cloudflare/AWS等のCDN、YouTube等の動画埋め込み、Intercom/Drift等のチャット、Facebook PixelやTwitterウィジェット、Google Maps等。
- 方法：ウェブページを解析し、外部ドメインや埋め込みを検出して依存度スコアを算出。JSオフでも動作する設計（ただしJS有効のほうが詳細を拾える）。
- 背景の重要性：EU–USデータ取引枠組み（例：Safe Harbor、Privacy Shield）の無効化は過去にも起きており、将来の枠組み変更で米国サービスが使えなくなる可能性がある。100% EUスコアはリスク低減に寄与する。
- 提供元：オーストリアのLightwavesによる無料スキャナ。実際のサイト（例：bbc.com）でのチェック例を提供。

## 実践ポイント
- まずスキャン：Lightwavesの無料ツールで自社サイトを走らせ、依存箇所を洗い出す。  
- 優先対応：個人データを送る解析・チャット・マップ・動画埋め込みを優先的に見直す。  
- 代替案：
  - フォント：Google Fontsを自己ホスティングに置き換える。
  - 解析：Google Analytics→Matomo等のセルフホスト／EUホスティング版へ移行。
  - 動画：YouTube埋め込みを控え、自己ホストやプライバシー配慮型埋め込みに変更。
  - マップ：Google Maps→OpenStreetMapベースのソリューションへ。
  - CDN/ホスティング：EU内リージョンや欧州プロバイダの利用、SCC（標準契約条項）やデータ処理契約の確認。
- ガバナンス：重要な外部依存は資産管理・リスク評価の対象にし、定期監査を実施する。

以上を踏まえ、EU向けのサービスやユーザーデータを扱うなら早めに監査を実行して影響範囲を把握することをおすすめします。
