---
layout: post
title: "Chrome extensions spying on 37M users' browsing data - Chrome拡張が3700万ユーザーの閲覧データを盗聴"
date: 2026-02-11T12:11:29.088Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://qcontinuum.substack.com/p/spying-chrome-extensions-287-extensions-495"
source_title: "Spying Chrome Extensions: 287 Extensions spying on 37M users"
source_id: 46973083
excerpt: "287のChrome拡張が閲覧履歴やクッキーを外部送信、計3740万件影響の調査"
image: "https://substackcdn.com/image/fetch/$s_!kI0A!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4bc7ba4b-4d4d-48cd-8ba7-b8cbec20887f_2896x1947.jpeg"
---

# Chrome extensions spying on 37M users' browsing data - Chrome拡張が3700万ユーザーの閲覧データを盗聴
あなたのブラウザ履歴が勝手に売買されているかもしれない — 287の拡張機能、約3,740万インストールを検出した調査

## 要約
自動化スキャンで「URL長と送信バイト量の相関」を指標に287のChrome拡張が閲覧履歴を外部送信していると判定され、合計で約37.4Mのインストールが確認された。

## この記事を読むべき理由
無料で便利に見える拡張機能が、無自覚にブラウザ履歴やクッキーを外部ブローカー（Similarweb 等）へ流し、広告プロファイリングや企業機密漏洩のリスクを高めている可能性があるため。日本の個人・企業ユーザーにも現実的な脅威です。

## 詳細解説
- スキャン手法：Docker上でChromiumを動かし、MITMプロキシで全トラフィックをキャプチャ。合成ブラウジングで訪問URLの長さを変え、外向け通信の増分と相関があるか回帰分析で判定。
- 漏洩指標：送信バイト量を $payload\_size$（URL長等）で回帰して
  $bytes\_out = R \times payload\_size + b$
  とし、$R \ge 1.0$ を「確実な漏洩」、$0.1 \le R < 1.0$ を「疑わしい漏洩」と分類。
- 規模とコスト：240k近いストア中で287件が該当、スキャンには約930 CPU日を要したためスケール運用の難しさも指摘。
- アクターと流通：Similarweb、Curly Doggo、Offidocs、Kontera など複数のデータブローカー／スクレイパーが関与。調査で設定したハニーポットに複数のIPレンジ/サービスからアクセスが確認された。
- 技術的な隠匿手法：ROT47やLZ-string圧縮、AES-GCMでの一時キー生成＋RSA-OAEPでのキーラッピング（ハイブリッド暗号）などでペイロードを隠蔽していたが、送信量の増加自体が判定に有効だった。
- 例：ポップアップブロッカーや「Stylish」系の拡張が、変形した／暗号化されたペイロードで閲覧URLを送信している実例がある。

## 実践ポイント
- すぐやるべきこと：
  - chrome://extensions で不要な拡張を削除、履歴やクッキーへのアクセス権がある拡張を優先して確認。
  - 開発者・プライバシーポリシーが不明瞭な拡張は避ける。
- 技術者向け対策：
  - エンタープライズはforce‑installホワイトリスト運用や拡張の検証プロセスを導入。
  - ネットワーク側で疑わしい外部エンドポイントの通信を監視・遮断（プロキシ／IDSルール）。
  - 高リスク環境では拡張を使わない専用ブラウザプロファイルやサンドボックス運用。
- 調査を深めたい場合：
  - 拡張のソースやService Workerの挙動を確認、疑わしいPOSTやカスタムヘッダ（例：x‑uuid 等）を追う。

短くまとめると、便利さの裏で拡張が「あなたを商品化」している可能性があるため、日常的な拡張の棚卸しと組織レベルの導入ポリシーが必要です。
