---
layout: post
title: "libxml2 Enterprise Edition (AGPL, from the previous maintainer) - libxml2 エンタープライズ版（AGPL：前メンテナによる）"
date: 2026-03-02T13:19:58.552Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://codeberg.org/nwellnhof/libxml2-ee"
source_title: "libxml2 Enterprise Edition (AGPL, from the previous maintainer)"
source_id: 928097319
excerpt: "libxml2EEがAGPLで復活、数千コミットとASAN/fuzzで脆弱性対策強化"
---

# libxml2 Enterprise Edition (AGPL, from the previous maintainer) - libxml2 エンタープライズ版（AGPL：前メンテナによる）
libxml2が「Enterprise Edition」として復活――AGPL化と大量のセキュリティ／ビルド修正でどう変わるか？

## 要約
Codeberg上で前メンテナが公開した「libxml2-ee」は、AGPL-3.0で再公開された libxml2 の派生ブランチで、数千コミット・活発なCI（ASAN・fuzz・下流ライブラリ検証）を通してセキュリティやビルド互換性が強化されています。

## この記事を読むべき理由
日本でも多くの業務系システムやオープンソースツール（Rubyのnokogiri、Pythonのlxml、XMLStarlet、PHP拡張など）が libxml2 に依存しています。ライブラリのライセンス変更やセキュリティ修正は、採用・配布・運用に直接影響するため、エンジニアは早めに把握しておくべきです。

## 詳細解説
- ライセンス：リポジトリに AGPL-3.0 が含まれており、派生物の配布やサービス提供時の公開義務に注意が必要です。
- 活動状況：7,700++ コミット、複数ブランチ／タグで 2.16 系のコードダンプや継続的な更新が行われている点から、実質的なメンテナンス継続が確認できます。
- セキュリティ修正と品質向上：
  - relaxng のエラーハンドラ改修で UAF（Use-After-Free）緩和。
  - c14n の型混同修正など、クリティカルな修正が追加。
  - ASAN（AddressSanitizer）や各種下流（nokogiri, lxml, perl, xmlstarlet, php）向けCIで互換性と安全性を検証。
  - fuzz 用コード・テストの整備で脆弱性検出の体制を強化。
- ビルド／配布面の変更：
  - Meson / CMake / autotools 用の更新が多数。古い win32 ビルドシステムは削除、Visual Studio で内部ヘッダを表示する対応など Windows サポートの整理あり。
  - LZMA サポートの削除など、依存・ビルドオプションに影響する変更も含む。
- 下流互換性：リポジトリのCIが主要下流プロジェクトを自動で走らせているため、既存エコシステムとの互換性確認が継続的に行われています。

## 実践ポイント
- ライセンス確認：AGPL-3.0 の影響（サービス提供時のソース公開義務など）を法務と早めに確認する。
- 依存関係のテスト：プロジェクトで nokogiri / lxml / xmlstarlet / PHP拡張 等を使っているなら、このブランチで下流テストを通すか、修正点を取り込んだ公式アップデートを待つ。
- セキュリティ対応：UAF や型混同の修正は即時アップデート検討の対象。社内パッケージやコンテナイメージの libxml2 を最新にする。
- ビルド方針の見直し：Meson/CMake への対応状況や LZMA 削除の影響をビルド/配布設定で確認する。
- CI導入：ASAN・fuzz・下流テストを取り入れて、自組織の依存先で同様の検証を回す。

（参照元：Codeberg の nwellnhof/libxml2-ee リポジトリの公開情報およびコミットログ）
