---
layout: post
title: "Rescuing old printers with an in-browser Linux VM bridged to WebUSB over USB/IP - ブラウザ内Linux VMとUSB/IP経由のWebUSBで古いプリンターを救う"
date: 2026-04-07T18:29:54.543Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://printervention.app/details"
source_title: "printervention: the backstory"
source_id: 47677885
excerpt: "ブラウザだけで古い写真プリンターを復活、USB/IP経由でドライバ不要にする実践ガイド"
---

# Rescuing old printers with an in-browser Linux VM bridged to WebUSB over USB/IP - ブラウザ内Linux VMとUSB/IP経由のWebUSBで古いプリンターを救う
魅力的な日本語タイトル: 「もう捨てないで！ブラウザだけで古い写真プリンターを復活させる方法」

## 要約
ブラウザ上で動く軽量Linux（v86）にCUPS/Gutenprintを組み込み、WebUSB→USB/IPの双方向ブリッジでUSBプリンターを直接扱うことで、ドライバ非対応になった古いプリンターを手間なく再利用できる仕組みを作った話。

## この記事を読むべき理由
macOSやWindowsでサポートが切れたプリンターを「安く・手軽に」復活させられる実用的な手法は、日本の家庭や中小事業者にとって写真印刷や保守コスト削減の現実的な選択肢になるから。

## 詳細解説
- 基礎構成：v86でx86エミュレーションを行い、Alpine Linux上にCUPS＋Gutenprintを入れてプリントサーバを仮想化。ブラウザ側はWebUSBで物理プリンターにアクセスする。
- 直接プリントの初期試行：CUPSのカスタムバックエンドを使い、エミュマシンのTTY経由でバイナリをブラウザに流してUSBに送る方式を試行。TTYの改行問題はstty rawで解決。9p経由で大きなチャンクを渡す実装も試したが、いずれも一方向通信の限界があった。
- 双方向ブリッジの決定打：Linux側でusbipを動かし（USBをTCPでカプセル化）、ブラウザ側でtcpip.js（lwIPをWASM化）を使ってエミュマシンのL2フレームをTCP/IPに戻す方式を採用。これによりCUPSはあたかも通常のUSBプリンターに接続しているように振る舞い、ステータスやエラー情報も双方向で扱える。
- 画像処理周りの工夫：プリンター側の自動縮小を避けるためJPEGを用紙サイズに合わせたPDFに埋め込み、EXIF向き情報やICCプロファイルを引き継ぐ。HEICはlibheif-js＋wasm-mozjpegでメモリ効率よく変換。
- 拡張性：SANEでスキャナを試すプロトタイプも作成。将来的には他のPPD（brlaser, splix等）追加で対応機種拡大が可能。
- 運用面：ブラウザアプリなのでインストール不要でクロスプラットフォーム。簡易テレメトリ（Neon Postgres）や消耗品への導線も実装している点が現実運用を見越した設計。

## 実践ポイント
- ユーザー向け：まともなChrome系ブラウザでprintervention.appを開き、WebUSBでプリンターを許可すれば試せる。Raspberry Pi設置より手軽にファミリー向け写真印刷を提供可能。
- 開発者向け：注目コンポーネントは v86（ブラウザ内x86）、usbip（Linux側）、tcpip.js（WASMでのTCP/IP復元）、CUPS＋Gutenprint。実装時の教訓：TTYはrawに、ファイルはLinux側でsyncしてからJSで読み出すこと。
- 日本市場への提案：ドライバ切れで廃棄候補のプリンターを低コストで再利用可能。祖父母向けの「写真印刷サービス」やプリント消耗品販売サイトとの連携でビジネス化しやすい。

元記事のアイデアは、古いハードを“ソフトウェアだけで蘇らせる”好例で、家庭ユースにも実用的です。興味があれば試してみてください（元記事詳細: https://printervention.app/details）。
