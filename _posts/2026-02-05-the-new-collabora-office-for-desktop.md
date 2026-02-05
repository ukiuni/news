---
layout: post
title: "The New Collabora Office for Desktop - 新しい Collabora Office（デスクトップ版）"
date: 2026-02-05T15:09:27.647Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.collaboraonline.com/collabora-office/"
source_title: "Collabora Office - Collabora Online and Collabora Office"
source_id: 46899591
excerpt: "クラウド不要・高互換、オフラインで使えるCollabora Office登場"
image: "https://www.collaboraonline.com/wp-content/uploads/2025/11/Impress-Apple-1-1024x666.png"
---

# The New Collabora Office for Desktop - 新しい Collabora Office（デスクトップ版）
自分の端末で動く「Collabora Online」の体験をそのままデスクトップへ — クラウドに依存しないオープンソースのオフィスが登場

## 要約
Collabora Online のUIとコードをそのままデスクトップ用に移植した「Collabora Office」が、Windows・macOS・Linux向けにリリース。ODFやDOCXなど主要フォーマット互換で、オフラインでもオンラインと同じ編集体験を提供します。

## この記事を読むべき理由
日本でもプライバシー重視やクラウド依存を避けたい自治体・教育機関、Nextcloudなど自前インフラ利用者が増えています。CollaboraはLibreOfficeの主要貢献者でもあり、Microsoft 365依存からの代替や既存環境への統合を検討する価値が高いです。

## 詳細解説
- コードとUI: Collabora Online のコードベースと同等の編集エンジンをローカルで動かす形。見た目・操作感が統一され、オンライン版との切替が容易。
- 対応アプリ: Writer（文書）、Calc（表計算）、Impress（プレゼン）、Draw（図形）をサポート。各アプリは.odt/.docx/.pdf/.ods/.xlsx/.odp など主要フォーマットを扱えます。
- 技術的特徴:
  - Calcは最大16k列まで扱えるなど大規模スプレッドシート対応。
  - ピボットテーブル、条件付き書式、HTML式入力、複数ソート・フィルタなど高度な表計算機能を提供。
  - 共同編集はオンライン版と同様のモデルを想定し、ローカル編集→オンライン同期のワークフローが可能。
  - 開発向けにCODE（開発版）を用意。プロダクション向けは安定版／LTSサポートを提供予定。
- 製品ライン: Collabora Office（新デスクトップ）、Collabora Office Classic（LibreOfficeベースのLTS製品）、Collabora Online（ブラウザ版）、モバイルアプリ、Chromebook対応など。
- 統合性: API/SDKや管理コンソールによる監視、既存インフラ（Nextcloud等）との統合が容易で、カスタム展開や企業向けサポートも用意。

## 実践ポイント
- まずはデスクトップ版をダウンロードして、手元のDOCX/ODTファイルで互換性を検証する。
- Nextcloudなど既存のファイルサーバと組み合わせて、オフライン→オンラインの同期ワークフローを試す。
- 大規模スプレッドシートやマクロ（.xlsm）を含むファイルで表示・計算結果を確認し、移行リスクを評価する。
- 開発・テスト用途にはCODEを、業務導入はLTSサポートや見積もり相談を検討する。
- セキュリティ／データ所在地の要件がある組織は、オンプレでの導入プランを早めに相談する。

--- 
公式発表のポイントを日本向けに整理しました。導入検討や互換性チェックをまず手元で試すのがおすすめです。
