---
layout: post
title: "Brat, a parallel TAP testing harness for the POSIX shell - Brat：POSIXシェル向け並列TAPテストハーネス"
date: 2026-02-20T18:24:54.437Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://codeberg.org/sstephenson/brat"
source_title: "Brat, a parallel TAP testing harness for the POSIX shell"
source_id: 776777563
excerpt: "POSIXシェルだけで並列実行する軽量TAPハーネスBrat、CIやレガシ環境へ簡単導入。"
---

# Brat, a parallel TAP testing harness for the POSIX shell - Brat：POSIXシェル向け並列TAPテストハーネス
Shellだけで並列実行もこなす、埋め込み型テストランナー「Brat」の魅力を短く解説

## 魚拓タイトル
Shellテストの新定番？POSIXだけで動く並列TAPハーネス「Brat」を使ってみたくなる理由

## 要約
BratはPOSIXシェル＋awkだけで動く軽量なTAP（Test Anything Protocol）テストハーネスで、並列実行・端末色付け・失敗時のxtrace出力などを備え、プロジェクトにそのまま埋め込めます。

## この記事を読むべき理由
日本のプロジェクトでは「最小限の依存でCIや組み込み環境でテストしたい」という要望が多く、Bratはその条件を満たします。Batsと似た開発体験を保ちながらPOSIX準拠で互換性が高く、社内ツールや古いUnix環境でも使いやすい点が魅力です。

## 詳細解説
- 基本思想：Bratは「brutal（露出した内部）」「POSIX（依存ゼロ）」を標榜し、約1000行のシェル＋awkで実装。外部依存が不要でそのままプロジェクトにベンダリング可能。
- テスト記法：.bratファイル内で @test "説明" { ... } という構文を使い、プリプロセッサが各テストを set -eu の関数に変換。各行がアサーションとして機能します。
- 実行と出力：出力は常にTAP（例：TAP version 14）で、端末接続時は色付きの「pretty」表示も可能。失敗時は set -x 相当のトレースと stdout/stderr を表示して原因特定が容易。
- 並列実行：-j または環境変数 BRAT_JOBS（デフォルトでCPU数）で並列実行が可能。各テストはバックグラウンドプロセスで走り、prettyフォーマッタが結果をバッファして順序を整えつつ表示します。
- run/match/compare：runはコマンド実行結果をファイルに捕捉し、$status / $stdout / $stderr を提供。matchは引数が /.../ ならERE（拡張正規表現）として評価、そうでなければ部分文字列一致。大きな出力をメモリに読まない設計はCIや大規模テストで有利。
- ポータビリティ：POSIX.1-2024準拠を目指し、Alpine/Debian/Fedora/FreeBSD/macOS上でCIテスト済み。シェル実装やawk差異を吸収する設計。

## 実践ポイント
- すぐ試す（プロジェクトに埋め込む例）:
```sh
# gitでベンダリングして直接実行
git clone https://codeberg.org/sstephenson/brat.git vendor/brat
vendor/brat/bin/brat test/*.brat
```
- 典型的なテスト例（.brat）:
```sh
@test "captures exit status and output" {
  run ls /nonexistent
  [ $status -eq 1 ]
  match "$stderr" 'No such file'
}
```
- 並列実行: 小規模なら `brat -j 4 test/*.brat`、CIでは `BRAT_JOBS=$(nproc)` を利用。
- 運用上のTip: 大きな出力を扱うテストは run を使ってファイルで処理するとCIメモリ負荷を抑えられる。リポジトリに vendor/brat を置けばビルド環境が厳しい現場でも安定。

元記事／プロジェクト：Brat (sstephenson/brat) — https://codeberg.org/sstephenson/brat
