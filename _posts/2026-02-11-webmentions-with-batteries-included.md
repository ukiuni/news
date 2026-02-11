---
layout: post
title: "Webmentions with batteries included - 機能満載のWebmentions"
date: 2026-02-11T14:37:43.245Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.fabiomanganiello.com/article/webmentions-with-batteries-included"
source_title: "Webmentions with batteries included"
source_id: 760277827
excerpt: "外部サービス不要でコメント／いいねを自前受信、Pythonライブラリで即導入可"
image: "https://s3.fabiomanganiello.com/fabio/img/webmentions-banner.png"
---

# Webmentions with batteries included - 機能満載のWebmentions
コメント欄もSNSも不要にする「自前で受け取る反応」の作り方 — プライバシーと分散性を両立する実装ライブラリの紹介

## 要約
Webmentionは、サイト間で「誰がどの記事を参照したか／反応したか」を直接やり取りするシンプルな分散プロトコルで、作者は著者のサイトにコメントやいいねを直接送れる。この記事はその実装を簡単にするPythonライブラリ（FastAPI/Flaskバインディング、DB保存、ファイル監視など）を紹介する。

## この記事を読むべき理由
日本でも個人ブロガーや企業ブログが増える中、外部サービスに頼らずにコメントや反応を受け取れる仕組みは、プライバシー確保・ブランド統制・運用コスト削減に直結するため、実務で役立つ選択肢になります。

## 詳細解説
- 基本概念：作者Aが自サイトの投稿（source）から他者Bの記事（target）を参照すると、A側がBの /webmentions エンドポイントへ POST（source, target）を送り、Bがそのソースにtargetが含まれるか検証して受理・表示する。中継サービス不要のピアツーピア設計。
- Microformats連携：ソースHTMLを解析して author・content・type・添付などを抽出。semanticなHTML（h-entry, p-name, e-content, u-url など）を用意すると表示が豊かになる。
- ActivityPubとの違い：ActivityPubは連合的で機能豊富だが複雑。Webmentionはシンプルで既存HTTP/HTMLに馴染む補完的手段。
- 紹介ライブラリ（Python）：  
  - FastAPI/Flask用バインディングあり（/webmentions の登録、Linkヘッダ／<link>でエンドポイント広告、GET /webmentionsで一覧）  
  - 保存はSQLAlchemy既定。独自ストレージを実装して差し替え可能（store/retrieve/delete）  
  - FileSystemMonitorで静的ファイルの変更を監視し、ターゲット発見時に自動で送信  
  - 動的サイトでは publish/update/delete 時に process_outgoing_webmentions を呼ぶ運用が可能  
  - on_mention_processed / on_mention_deleted コールバックで通知・自動承認・モデレーションを実装可能  
  - 既定は受信を CONFIRMED にするが、初期を PENDING にして管理者承認フローを入れる設定も可能
- 実例：作者は madblog 等で稼働させており、既に実運用されている。

## 実践ポイント
- 最初にやること：
  - サイトに Webmention エンドポイントを宣言する（Link ヘッダ or <link rel="webmention" href="https://example.com/webmentions">）。
  - ソースページに Microformats（h-entry, p-name, e-content, u-url 等）を付与する。
- ライブラリ導入（例）：
```bash
# FastAPI 用
pip install "webmentions[db,file,fastapi]"
# Flask 用
pip install "webmentions[db,file,flask]"
```
- 動的サイト：記事やコメント公開時に WebmentionsHandler.process_outgoing_webmentions を呼ぶ。  
- 静的サイト：FileSystemMonitor を有効にしてビルド／ファイル更新で自動送信。  
- モデレーション：初期ステータスを PENDING にして on_mention_processed で承認通知や自動基準を実装する。  
- 表示：受信データをテンプレートでレンダリング（作者名、本文、種類、添付）するためのMicroformatsパーシング結果を利用する。

このアプローチは、日本の個人運営メディアや企業ブログで「外部に依存しないコメント／反応機能」を安全かつ軽量に導入したい場面で特に有効です。興味があれば公式記事（元記事）とドキュメントで実装例を確認してみてください。
