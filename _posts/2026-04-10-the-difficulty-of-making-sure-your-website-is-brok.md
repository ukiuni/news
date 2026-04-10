---
layout: post
title: "The difficulty of making sure your website is broken - ウェブサイトが「壊れている」ことを確認する難しさ"
date: 2026-04-10T21:28:31.978Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://letsencrypt.org/2026/04/10/test-sites.html"
source_title: "The difficulty of making sure your website is broken -  Let&#39;s Encrypt"
source_id: 1184818181
excerpt: "失効・期限切れ・有効を確実に再現する証明書テスト環境の作り方と実装"
image: "https://letsencrypt.org/images/LetsEncrypt-SocialShare.png"
---

# The difficulty of making sure your website is broken - ウェブサイトが「壊れている」ことを確認する難しさ
「本当に“失効”／“期限切れ”の証明書が出る」テストサイトを作る裏側 — Let’s Encrypt流の工夫

## 要約
Let’s Encryptが公開テスト用に「有効・期限切れ・失効」の3種類の証明書を確実に提供するために直面した技術的課題と、そのために書いたGo製ツールの設計を解説する記事。

## この記事を読むべき理由
証明書周りの不具合は復旧やテストで頻出します。日本の開発現場や組み込み／CI環境でも「失効を確実に再現できる」テスト環境は非常に有用なので、実装上の落とし穴と対策を知る価値があります。

## 詳細解説
- 目的：各ルート証明書ごとに「有効・期限切れ・失効」のサイトを公開し、クライアント実装（ブラウザやcurlなど）の挙動を検証可能にする。  
- 一見簡単な「期限切れ」は、短期間での発行→待機→切り替えで対処可能（Let’s Encryptの最短有効期間でも数日必要）。  
- 「失効」は難しい：失効済みでかつ有効期限内の証明書を確実に配信しなければならない。失効申請をしてもCRL（Certificate Revocation List）やキャッシュの反映に時間差があり、オフ・ザ・シェルフのツールでは管理しづらい。  
- 技術スタック：Goで専用サーバを実装し、LegoライブラリをACMEクライアントとして利用。TLS-ALPN-01チャレンジを組み込みで処理してドメイン検証を完了させることで追加の外部設定を避ける。  
- ワークフローの肝：証明書を「すぐに使う」のではなく「次に使う候補（next）」として保管し、CRLに反映されるまで（失効は最低24時間待つ等）や、期限切れ到来まで待ってから運用中の証明書を差し替える。これにより「誤って有効な証明書を公開してしまう」「失効が期限切れに置き換わる」問題を回避。  
- サーバ側はGoのGetCertificateコールバックでSNIに応じた証明書をメモリ上から選択。テスト用途では正しい状態を優先するため、意図せず期限切れ証明書を返すことを拒否する実装にしている。  
- ブラウザ側挙動：失効チェックはブラウザ間で大きく差があり、FirefoxのCRLiteやRustlsのupkiのような実装が先進的。curl等のCLIクライアントや組み込みデバイスのテストにも配慮し、HTML/プレーンテキストの応答切替など細かい使い勝手も用意している。  
- オープンソース：実装は https://github.com/letsencrypt/test-certs-site/ で公開。他CAでも再利用可能。

## 実践ポイント
- テスト環境を作るなら、単に証明書を発行するだけでなく「状態の反映遅延（CRL／キャッシュ）」を考慮して切替ロジックを入れる。  
- ACMEを使うならサーバ内蔵のクライアント（例：Lego＋Go）でTLS-ALPN-01を使うと追加DNS設定などを避けられる。  
- 失効確認はCRLやOCSPだけでなく、ブラウザやOSレベルの実装差を意識して複数クライアントで検証する。Firefox（CRLite）やupkiの挙動を参考にする。  
- すぐ試したい場合は Let’s Encryptのテストサイトのリポジトリ／リンクを確認し、curlやブラウザで挙動を比較してみると学びが大きい。

以上。
