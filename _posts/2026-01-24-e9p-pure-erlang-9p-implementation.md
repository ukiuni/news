---
layout: post
title: "e9p - pure Erlang 9p implementation - e9p：純粋Erlangによる9p実装"
date: 2026-01-24T17:40:06.704Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tangled.org/hauleth.dev/e9p"
source_title: "e9p - pure Erlang 9p implementation"
source_id: 1539349882
excerpt: "ビルド不要でErlang内部をprocfs風に公開する純Erlang製9p"
---

# e9p - pure Erlang 9p implementation - e9p：純粋Erlangによる9p実装
Erlangだけで作る「procfs風」リモートファイルシステム —— e9pでErlangランタイムを安全に覗いてみる

## 要約
e9pは9p2000プロトコルを純粋Erlangで実装したプロジェクトで、ネイティブコード（NIF／libfuse）を使わずにErlangプロセスやシステム情報をファイルシステム風に公開できます。現状は読み取り専用のERTS情報FSが中心です。

## この記事を読むべき理由
- Erlangベースのシステム（RabbitMQ、ソフトリアルタイム系など）を運用する日本のエンジニアにとって、ネイティブビルド不要で内部状態を可視化できる手段は運用負担とデプロイの複雑さを下げます。  
- クロスコンパイルや組み込み環境でlibfuse/NIFの依存を避けたい場合の有力な選択肢になります。

## 詳細解説
- プロトコル：RFC準拠の9p2000を実装。メッセージ解析、接続確立、ツリーウォーク、読み書きIO、ファイル/ディレクトリ操作などクライアント・サーバ両面を目標にしています。  
- 実装方針：純粋Erlangのみで完結するため、ネイティブコード不要でリモートアクセスも可能。fuserl（libfuse/NIF）と異なりクロスコンパイルの問題が小さい点が利点。  
- 現状の機能：基本は読み取り専用のERTS system information FS。ディレクトリ構成は主に以下の3つ。  
  - processes：基本的なプロセス情報一覧  
  - applications：ロード済みアプリケーション情報  
  - system_info：ERTS全体の情報  
  将来的には memory／statistics の追加、プロセス削除でのプロセス終了や擬似ファイル経由でメッセージ送信などを想定。  
- 互換性：Linuxのv9fsドライバが期待するためQID情報に加えてmodeフィールドも設定。現状は拡張なしの“legacy”バージョンのみを報告します。  
- サンプルFS：UnixFs（ローカルFSをマウントする実験的実装。WIPで読み書きは一部対応）とErlProcFS（procfs風にErlang内部を露出、現状は読み取り専用）。  
- ライセンス：Apache-2.0。ただしPropErテストはGPL-3.0で、実行時にGPLコードは使われないよう分離されています。

## 実践ポイント
- リポジトリをクローンして動かす（ビルド不要が魅力）：純ErlangなのでErlang/OTP環境があれば試せます。  
- 開発用途ではまずErlProcFSをマウントしてプロセス一覧やアプリ情報を観察。運用監視やデバッグに活用可能。  
- 本番で利用する前に「読み書き機能の実装状況」と「v9fs互換性（modeフィールド）」を確認すること。  
- 拡張案：memory/statisticsパスの追加、擬似ファイルでのメッセージ送信やプロセス操作を実装すれば運用効率が大きく向上。  
- ライセンスに注意：テストコードのライセンス（GPL）と実行時ライセンス（Apache-2.0）の違いを確認する。

この記事で紹介したe9pは、Erlang環境の可視化やクロス環境でのデバッグツール構築に即戦力となる選択肢です。興味があればまずリポジトリを試して、ErlProcFSを覗いてみてください。
