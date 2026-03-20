---
layout: post
title: "Show HN: We built a terminal-only Bluesky / AT Proto client written in Fortran - ターミナル専用のFortran製Bluesky/ATプロトコルクライアントを作った"
date: 2026-03-20T22:25:37.275Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/FormerLab/fortransky"
source_title: "GitHub - FormerLab/fortransky: We built a terminal-only Bluesky / AT Protocol client written in Fortran, with a Rust native firehose decoder for the relay-raw stream path. Yes, that Fortran. · GitHub"
source_id: 47461321
excerpt: "Fortran製ターミナルBlueskyクライアントを公開、C/Rust連携でJetstreamとrelay-rawの生ストリーム表示を実現。"
image: "https://opengraph.githubassets.com/24974a91decac040e0b90acc2f744fe9bcbadd8affc3ea89bc4adf6df3696c5c/FormerLab/fortransky"
---

# Show HN: We built a terminal-only Bluesky / AT Proto client written in Fortran - ターミナル専用のFortran製Bluesky/ATプロトコルクライアントを作った
本当にFortranで書かれた！レガシー言語×最新分散SNSプロトコルで遊ぶ技術実験

## 要約
FortranskyはFortranで実装したターミナル専用のBluesky（AT Protocol）クライアント。低レイヤはC（libcurl）とRust（firehoseデコーダ）を接ぎ木して、Jetstreamとraw relay両対応のストリーム表示を実現している。

## この記事を読むべき理由
- 「意外な言語でモダンなプロトコルを扱う」アーキテクチャ設計の妙を学べる。  
- Fortran／C／Rust／Pythonの混成プロジェクトでの実運用ノウハウ（ビルド、FFI、ストリーム処理）が得られる。  
- 日本でも分散SNSや低レイヤ実装に関心が高まっており、学習／実験素材として有益。

## 詳細解説
- アーキテクチャ概要  
  - フロントエンド：Fortran製TUI（コマンド入力型、行ベース）  
  - HTTPブリッジ：Cでlibcurlを使うラッパー（cshim）→ Fortranのiso_c_binding経由で利用  
  - Firehose（relay-raw）経路：Rust製ネイティブデコーダ（staticlib）で envelope → CAR → DAG-CBOR → 正規化JSON に変換。Pythonのcbor2/websocketsはフォールバック。  
  - セッションは ~/.fortransky/session.json に保存。ログインはアプリ用パスワード推奨（本アプリ用のApp Passwordを作る）。  

- ストリームモード  
  - jetstream：BlueskyのWebSocket（JSON主体、低帯域）  
  - relay-raw：AT Protocolの生フレーム（CBOR）を受け取りRustデコーダで展開。デコーダは環境変数かビルド出力を検出して使用。  

- ビルド／依存関係（概要）  
  - 必須：gfortran, cmake, pkg-config, libcurl-dev, Rust toolchain (rustc >= 1.70)  
  - relay-raw補助：Pythonで cbor2, websockets が必要（relay_raw_tail.py を使う場合）。  
  - ビルドは ./scripts/build.sh がRust→CMakeを順に実行する。  

- 現状の制限・注意点  
  - JSONパーサは軽量な自前実装（スキーマ完全対応ではない）  
  - relay-rawは現在 app.bsky.feed.post のcreate opsのみ正規化している  
  - ストリームではDIDが表示され、ハンドル解決（DID→ハンドル）は未実装  
  - TUIは生のキーイベントではなくコマンド入力方式（Enterで実行）

## 実践ポイント
1. 必要ツールを入れる（例: Ubuntu）
```bash
sudo apt install -y gfortran cmake pkg-config libcurl4-openssl-dev
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
2. リポジトリをビルドして実行
```bash
./scripts/build.sh
./build/fortransky
```
3. ログインはFortransky用のアプリパスワードを作成して使用する。セッションは ~/.fortransky/session.json に保存。  
4. live relay を使う（デフォルトは組み込みフィクスチャ）
```bash
FORTRANSKY_RELAY_FIXTURE=0 ./build/fortransky
```
5. ネイティブRustデコーダを優先させる場合は環境変数を確認／設定（FORTRANSKY_FIREHOSE_DECODER）か、ビルド済の firehose_bridge_cli を配置する。  
6. 学習用途の提案：Fortran⇄C⇄Rust のFFI実装や、CBOR→DAG-CBOR→JSONのパイプラインを読むと、低レイヤ実装の実践知が得られる。

リポジトリ: https://github.com/FormerLab/fortransky — 好奇心を刺激する実験プロジェクトなので、まずはビルドして動かしてみることをおすすめします。
