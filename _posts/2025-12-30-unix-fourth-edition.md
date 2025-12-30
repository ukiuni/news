---
layout: post
title: "UNIX Fourth Edition - UNIX 第4版"
date: 2025-12-30T08:18:03.523Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://squoze.net/UNIX/v4/README"
source_title: "UNIX Fourth Edition"
source_id: 46364136
excerpt: "SIMHでPDP-11にUNIX第4版を復元し、生のソースでカーネル再構築を体験できる"
---

# UNIX Fourth Edition - UNIX 第4版
PDP-11で「動くUNIX」を再現する──テープイメージから第4版カーネルをビルドして起動するまで

## 要約
UNIX v4のテープイメージとRK05ディスクイメージ、シミュレータ用のINIファイルが公開されており、SIMHで実機と同様にインストール／起動してカーネルを再構築できる。

## この記事を読むべき理由
古典UNIXの実動環境を手元で再現できるのは教育・研究・レガシー理解に極めて有益。日本のOS教育やレトロコンピューティング、組込み／カーネル入門者にとって、生のソースと当時のビルド手順を追う経験は貴重だ。

## 詳細解説
- 配布物の中身
  - unix_v4.tap：SIMH形式のオリジナルテープイメージ（ブロック付き）。このままSIMHに読ませて使うのが手っ取り早い。
  - bootstrap：テープの先頭 38400 バイト（ブート用）。
  - disk.rk：残りのRK05ディスクイメージ部分。
  - unix_v4.tar：ファイルシステムを取り出したtar。
  - install.ini / boot.ini：SIMH（pdp11）用のインストール／起動用設定ファイル。

- インストールの流れ（概略）
  1. SIMHのpdp11エミュレータでinstall.iniを読ませ、テープからRK05イメージへダンプする。
  2. 生成されたディスクイメージからuboot等をロードしてUNIXを起動。
  3. 一度ディスクから起動可能になればテープ不要で起動できる。

  代表的な操作（簡略化）:
  ```bash
  # SIMHを使い install.ini を実行（テープ→RK05へ展開）
  pdp11 install.ini

  # 生成されたRK05から起動（初回はubootをテープからロードしてから）
  pdp11 boot.ini
  ```

- カーネル再構築
  /usr/sys 以下にビルドスクリプト（run）があり、当時の流儀でCファイルをコンパイル→アセンブル→ライブラリ(ar)→リンク(ld)してカーネルを作る。lib1/lib2をmklibで作成し、最終的に a.out を /nunix 等に配置してブートする流れ。現代の環境と異なる点（アセンブラ/リンカの挙動、デバイスドライバの扱い）に注意。

  例（薄めたイメージ）:
  ```sh
  # /usr/sys/run の要旨
  cc -c *.c
  sh mklib      # ../lib1 ../lib2 を ar で作る
  as conf/low.s
  ld -x low.o mch.o conf.o lib1 lib2 -o a.out
  mv a.out /nunix
  ```

- 注意点と未解決項目
  - テープイメージはブロック付きなので生データを取り出す場合は整形が必要だが、SIMHにそのまま読ませるのが簡単。
  - デバイスファイルやmanページ、/dev/memなど環境依存の設定が不足している場合があり、手作業で補う必要がある。
  - 自動インストール（expectでの自動化）や別ディスク（rp, rf）の検証、古いカーネル（pre-v4）との互換性回復など改善余地がある。

## 実践ポイント
- まずはSIMH（pdp11）を準備し、配布されているinstall.ini / boot.ini をそのまま動かしてみる。問題の切り分けが早い。
- カーネルビルドは当時のツールチェーンに依存するため、SIMH上の環境でビルドするのが安定する。ホスト側で無理に変換しないこと。
- ドライバやデバイスファイルが抜けている場合は /dev を手作業で作り、mountやswapの設定を確認すること。ログイン直後のroot権限で試すと復旧が速い。
- 教材利用なら、ソースを追って「ファイルシステム」「プロセス」「デバイスドライバ」の実装差分を学ぶと学習効率が高い。

## 引用元
- タイトル: UNIX Fourth Edition
- URL: http://squoze.net/UNIX/v4/README
