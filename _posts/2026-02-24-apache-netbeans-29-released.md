---
layout: post
title: "Apache NetBeans 29 released. - Apache NetBeans 29 がリリースされました"
date: 2026-02-24T04:54:03.140Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://netbeans.apache.org/front/main/download/nb29/"
source_title: "Downloading Apache NetBeans 29"
source_id: 399229084
excerpt: "NetBeans 29登場：JDK25/21対応、同梱版で即試用可—検証とWindows注意"
---

# Apache NetBeans 29 released. - Apache NetBeans 29 がリリースされました
NetBeans 29到来：JDK最新世代に対応、まず押さえるべき変更点と導入のコツ

## 要約
Apache NetBeans 29（2026-02-23リリース）は、JDK 25/21/17をサポート（JDK 26は初期対応）し、複数のプラットフォーム向けバイナリとパッケージが提供されます。ダウンロード検証や既知の問題点（String Templates廃止、Windows関連の注意点）を導入前に確認するのが重要です。

## この記事を読むべき理由
国内でもOpenJDK/Temurin採用が広がる中、IDEのランタイム互換性や配布形態（.deb/.rpm、snap、Bundled JDK）の違いは導入・運用コストに直結します。NetBeansユーザーや軽量IDEを検討する日本の開発者は本リリースの影響を早めに把握すべきです。

## 詳細解説
- リリース情報
  - リリース日：2026-02-23
  - バイナリ：netbeans-29-bin.zip、ソース：netbeans-29-source.zip（それぞれ SHA-512 と PGP署名あり）
  - 検証：ダウンロード後は .asc（PGP）または .sha512 による整合性確認を推奨
- パッケージ/インストーラ
  - Codelerity提供のインストーラ（Windows/macOS/Linux .deb/.rpm）にはローカルTemurin JDKを同梱した「自己完結」パッケージあり
  - Linux向けにsnapパッケージも提供
  - 注意：これらのパッケージはApache財団の公式リリースとは別で、追加ライセンスや同梱物がある場合あり
- 対応JDK
  - 実行 JDK：JDK 25 / 21 / 17 をサポート（JDK 26 は初期サポート）
  - 補足：IDEが使うランタイムJDKはプロジェクトが使えるJDKレンジに影響しないため、開発中のプロジェクトJDKは別途確認
- 既知の問題
  - NetBeans 23+ で String Templates のサポートが無くなっています
  - Windows の RDP セッションや UNC パスでの問題（#8236, #8611）は最新の JDK 21 で改善する場合あり
  - Windows/ARM はまだ完全サポートではない
- ビルド/コミュニティ
  - ソースからのビルドは netbeans-29-source.zip を展開して README の手順に従う
  - このリリースは Apache NetBeans コミュニティの承認プロセスを経て公開

## 実践ポイント
- ダウンロード後は必ず SHA-512 と PGP (.asc) で検証する。
- 手早く試したければ、Temurin同梱のCodelerityパッケージを利用（自己完結で即起動可）が、同梱ライセンスを確認すること。
- 日本で多い Ubuntu 系なら snap、Debian/RedHat 系なら .deb/.rpm が便利。社内サーバ運用ならソースビルドも検討。
- WindowsでRDPやUNCを使う環境では、まず JDK を最新の推奨アップデート（特に JDK21）にすることで問題が改善するかを確認する。
- 問題やバグは GitHub の Issue に報告し、README のビルド手順を参照してローカルビルドで再現性を確認する。

以上を踏まえ、まずは検証用環境で既存プロジェクトとの互換性（特に使用している JDK とプラグイン）をチェックしてから本番導入してください。
