---
layout: post
title: "(Open) Widevine support added to the chromium port - （Open）Widevine サポートが chromium ポートに追加されました"
date: 2026-01-24T00:34:25.971Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://undeadly.org/cgi?action=article;sid=20260118112808"
source_title: "(Open) Widevine support added to the chromium port"
source_id: 920246966
excerpt: "OpenBSDのChromiumでOpenWV実装、.wvd用意でDisney+視聴可能に"
---

# (Open) Widevine support added to the chromium port - （Open）Widevine サポートが chromium ポートに追加されました
OpenWVでOpenBSDのChromiumがストリーミング再生に近づく — ただし「鍵」は自分で用意する必要あり

## 要約
OpenBSDのportsにOpenWV（Widevine CDMを再実装したOSS）が追加され、chromiumポートで利用できるようになりました。動作確認例としてDisney+の再生が報告されていますが、動作にはデバイスID（`.wvd`ファイル）の準備が必須です。

## この記事を読むべき理由
日本でもNetflixやDisney+などストリーミング利用は一般的。OpenBSDで公式プロプライエタリCDMを使わずに視聴環境を整えたい開発者や技術好きにとって、オープンソースで代替できる動きは注目に値します。ただし法的・運用上の注意点があります。

## 詳細解説
- OpenWVとは：GoogleのWidevineのCDM（Content Decryption Module）をオープンに再実装したプロジェクトで、共有ライブラリ形式のCDMと互換を目指しています。OpenWVはproprietaryなGoogle CDMの「置き換え」として動作します。
- portsへの追加内容：ports/multimedia/openwv として openwv-1.1.3 がインポートされ、chromiumポートで利用可能になりました。パッケージ構成やパッチ類も用意されています。
- 実際の動作報告：投稿ではDisney+で動作確認が取れている旨が報告されています（環境依存の可能性あり）。
- 重要な制約：OpenWV自体にはデバイスIDが含まれません。Widevineクライアントを認証するためのメタデータ＋秘密鍵を格納した`.wvd`ファイルが必要で、正しく配置しないと動作しません。パスの例：/etc/openwv/widevine_device.wvd
- セキュリティと信頼性：READMEやportsの説明で外部リンクや配布元を確認すること。記事のコメントではpkg-readmeのリンクが不正リダイレクトする問題が指摘されています。公式リポジトリ（例：OpenBSDのports GitHubミラー）やプロジェクトの公式ページを参照してください。
- 法的・利用上の注意：デバイスIDの入手方法や配布には権利者の制約がある場合があります。正規ルートでの利用を心掛けてください。

## 実践ポイント
- 環境：OpenBSDでportsツリーを最新にしておく。
- インストール候補：ports/multimedia/openwv と www/chromium をビルド・インストールする。
- デバイスIDの用意：OpenWVは`.wvd`ファイルを必要とする。入手は正規ルートを確認し、配置先は /etc/openwv/widevine_device.wvd のようにする。
- 検証：ブラウザで対象のストリーミングサイトを開き、再生可否を確認する。動作しない場合はportsのREADMEやログ、Chromiumのコンソール出力を確認。
- 情報源の確認：portsのREADMEや公式リポジトリで最新情報やセキュリティ注意事項を確認する（pkg-readmeリンクの不具合報告あり）。

この記事はOpenWV導入の「可能性」と「現実的な準備事項」を短くまとめたものです。導入前に公式ドキュメントと法的条件を必ずご確認ください。
