---
layout: post
title: "Lilush: A static LuaJIT runtime with batteries - Lilush：バッテリー同梱の静的LuaJITランタイム"
date: 2026-02-19T15:14:31.966Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lilush.link/"
source_title: "Lilush: A static LuaJIT runtime with batteries"
source_id: 848810999
excerpt: "3MB未満の単一バイナリで依存ゼロ、ネット/暗号/TUI内蔵のLuaJITランタイム"
---

# Lilush: A static LuaJIT runtime with batteries - Lilush：バッテリー同梱の静的LuaJITランタイム
驚きの3MB以下・依存なしで動く「持ち運べるLuaJIT環境」——サーバもコンテナもこれ1本でOK

## 要約
Lilushは静的にコンパイルされたLuaJIT実行ファイルで、ネットワーク、暗号、ファイル操作、ターミナルUIなどを一つのバイナリに詰め込み、依存関係ゼロでx86_64 Linux上で動きます。

## この記事を読むべき理由
小さく安全にツールを配布したい開発者や、軽量コンテナ／組込み系でスクリプト実行環境を手早く用意したい日本のエンジニアにとって、依存を気にせず「そのまま動く」実行環境は即戦力になります。

## 詳細解説
- 単一バイナリかつ3MB未満：インストール不要でそのまま配布・実行でき、FROM scratchのDockerイメージやbusybox代替として利用可能。  
- 静的リンクされたLuaJIT：高速なJITエンジンをそのままパッケージ化しているため、Luaで書いたスクリプトを高パフォーマンスで動かせる。  
- 同梱ライブラリ（抜粋）：  
  - ネットワーキング：TCP/UDP、SSL対応、HTTP/1.1サーバとHTTP(S)クライアント（WolfSSL組み込み）。  
  - 暗号：現代的な暗号プリミティブを利用可能。  
  - ファイル・プロセス操作：システムスクリプトに必要な基本機能をサポート。  
  - ターミナルUI：UTF-8対応入出力、TSS（Terminal Style Sheets）でのスタイリング、ウィジェット群。  
  - その他：Markdown処理、Redisプロトコル、JSON/Base64、WireGuard埋め込み、ACMEv2クライアント、ランタイム内ドキュメント等。  
- Lilush Shell：シェルとしても充実。ホスト・ユーザ・カレントディレクトリ・gitブランチ・Kubernetesコンテキストなどを表示するスマートプロンプト、タブ補完・履歴検索・ディレクトリナビゲーション機能、kat/ktl/netstat/dig/wgcli等の組み込みツールを備える。Kittyのキーボードプロトコルに依存するため、kitty/foot/alacritty/konsole等互換端末推奨。  
- 拡張性：プラグイン追加やTSSでのスタイル調整が可能。  
- セキュリティと配布：リリースバイナリはSSH鍵で署名されており、ソースからのビルドや検証手順が公開されている。

## 実践ポイント
- まず試す（ダウンロード＋実行権限付与）:
```bash
# bash
curl -fLO "https://codeberg.org/latimar/lilush/releases/download/latest/lilush"
chmod +x lilush
./lilush --help
```
- 軽量コンテナのベースに：FROM scratchコンテナにバイナリだけ入れて配布すれば依存ゼロのランタイムが完成。  
- シェル置き換え：既存の開発環境で端末互換があれば、Lilush Shellを試してCLIワークフローを簡素化。  
- 日本での用途例：IoTゲートウェイの簡易管理ツール、コンテナCIのテストランナー、ネットワーク診断ツールの単一バイナリ配布など。  
- ソース検証：配布物の署名検証や必要ならソースからビルドして導入することを推奨。

元記事とリポジトリで更に詳細なモジュール一覧やビルド方法が公開されています。興味があればまずは上のダウンロード手順で触ってみてください。
