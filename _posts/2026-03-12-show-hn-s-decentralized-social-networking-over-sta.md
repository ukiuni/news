---
layout: post
title: "Show HN: s@: decentralized social networking over static sites - s@: 静的サイトで動く分散型ソーシャルネットワーキング"
date: 2026-03-12T14:17:30.640Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://satproto.org/"
source_title: "s@: social networking over static sites | sAT Protocol"
source_id: 47344548
excerpt: "自分のドメインで動く暗号化静的SNS、s@で友達限定の安全なフィードを即導入"
---

# Show HN: s@: decentralized social networking over static sites - s@: 静的サイトで動く分散型ソーシャルネットワーキング
サーバ不要で「友だちだけ」が見られるSNS——静的サイト×暗号で実現するs@プロトコル入門

## 要約
s@（sAT Protocol）は、各ユーザーが自分の静的サイトに暗号化されたJSONデータを置き、ブラウザクライアントがそれを集約してフィードを表示する「サーバレス／分散型」SNSプロトコル。フォロー相互承認型でスケールを追わない小さなコミュニティ向け設計。

## この記事を読むべき理由
- 日本の開発者やコミュニティ運営者にとって、広告や中央サーバに依存しない“クローズドなSNS”を手早く試せる手段だから。
- GitHub Pagesなど既存の静的ホスティングで公開でき、個人ドメインをそのまま身分に使える点は法人やローカルコミュニティに有用。

## 詳細解説
- 身元と公開鍵: ユーザーIDはドメイン名。HTTPSでコンテンツを取得することでドメイン所有が証明される。各サイトは /satellite/satproto.json に公開鍵などのディスカバリ情報を置く。
- データ配置: {domain}/satellite/ 以下に posts/（個別投稿は暗号化ファイル）、follows/index.json（フォローリストは平文）、keys/（各フォロワー向けに暗号化されたコンテンツ鍵）などを置く静的構造。
- 暗号モデル: 各ユーザーはX25519鍵ペアを生成。投稿はランダムな256ビットのコンテンツ鍵で XChaCha20-Poly1305 によって暗号化。コンテンツ鍵は libsodium の sealed box（受信者の公開鍵で暗号化）で各フォロワー向けに格納される。
- 自己鍵（keys/_self.json）: 自分用のコンテンツ鍵や発行に必要なトークンは自身の公開鍵で封印して保存。ブラウザのローカルストレージに秘密鍵を置くことで別端末で復元可能。
- フォローと鍵回転: 誰かのフォローを外すと新しいコンテンツ鍵を発行し既存投稿を再暗号化、残ったフォロワー向けに鍵を再作成。外した相手は古い鍵で復号不可。
- フィード構築: クライアントは自分の follows を読み、各フォロー先の satproto.json を解決、各フォロー先の keys/自分のドメイン.json を使ってコンテンツ鍵を開き、posts/index.json → 個別投稿を取得してマージする。
- UI/UXの制約: 返信はトップレベル投稿への平坦スレッドのみ。相互フォローでしか投稿が見られないため「フォロワー数で拡張する」用途には向かない。
- ホスティングと公開: GitHub Pagesで簡単に始められるが、カスタムドメインや自ホストする場合はCORS設定や公開トークン管理に注意。

## 実践ポイント
- まずはフォークして GitHub Pages を有効化し、公開URL（例: https://username.github.io/satellite/）を確認する。
- 自ドメインで運用する場合は /satellite/satproto.json と必要な静的ファイル群を配置。既存のパスがあれば satproto_root.json でルートを指定。
- 秘密鍵はローカルで厳重にバックアップ（ブラウザ消去や端末変更時の復元に必須）。
- 小さなクローズドコミュニティ（チーム、趣味のグループ、地域コミュニティ）で試すのに最適。インフルエンサーや大規模公開を目的にしないこと。
- 自ホストする場合は CORS と GitHub（等）のアクセストークンを keys/_self.json に正しく封印してから使う。

元プロジェクト: http://satproto.org/ — 小規模でプライベートな分散SNSを自分のドメインで試したい人にお勧め。
