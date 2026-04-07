---
layout: post
title: "How Linux executes binaries: ELF and dynamic linking explained - Linuxはバイナリをどう実行するか：ELFと動的リンクの仕組み"
date: 2026-04-07T11:17:39.757Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://fmdlc.github.io/tty0/Linux_ELF_Dynamic_linking_EN.html"
source_title: "Redirecting…"
source_id: 368869183
excerpt: "ELFヘッダから動的リンカ・PLT/GOTまで起動処理を一気に図解"
---

# How Linux executes binaries: ELF and dynamic linking explained - Linuxはバイナリをどう実行するか：ELFと動的リンクの仕組み
Linux実行の裏側 — ELFヘッダから動的リンカ、PLT/GOTまで一気に理解する

## 要約
Linuxがプログラムを起動する際は、カーネルがELFヘッダを読み取りメモリにセグメントをマップし、必要なら動的リンカ（ld‑linux）が共有ライブラリを解決して実行環境を組み立てます。動的リンクの要所は「.dynamic」「PLT/GOT」「遅延結合（lazy binding）」です。

## この記事を読むべき理由
サーバ、組み込み、Android、コンテナ運用など日本の開発現場でLinuxバイナリやライブラリの問題（起動失敗、依存解決、パフォーマンス、セキュリティ）に直面することは多いです。ELFと動的リンクの基本を知れば、原因追跡や対策が格段に速くなります。

## 詳細解説
- ELFとは：Executable and Linkable Formatの略。ファイル先頭のELFヘッダで種別（実行ファイル／共有ライブラリ）、アーキテクチャ、エントリーポイント、プログラムヘッダの位置などを示します。
- カーネル側の処理：ユーザーがexecveを呼ぶとカーネルがELFヘッダを検査し、Program Header（PT_LOAD等）に基づきファイルの区間をmmapでメモリにマップします。PT_INTERPがあれば、そのパスの動的リンカを最初に読み込みます。
- 動的リンカ(ld‑linux)：共有ライブラリのロードとシンボル解決を担当します。ELFの.dynamicセクションからDT_NEEDED（依存ライブラリ）、DT_RPATH/DT_RUNPATH、DT_DEBUGなどの情報を読み取り、ライブラリを検索・マップします。検索順はLD_LIBRARY_PATH → DT_RUNPATH/DT_RPATH → /etc/ld.so.cache → /lib /usr/lib等（細かい挙動はバージョンで異なる）。
- シンボル解決とリロケーション：実行時に必要なアドレス調整（リロケーション）が行われます。PLT（Procedure Linkage Table）とGOT（Global Offset Table）は関数呼び出しの遅延結合に使われ、最初の呼び出し時に動的リンカが実際の関数アドレスを解決してGOTに書き込みます（lazy binding）。一方、グローバル変数などは起動時に即時解決されることがあります（rela/relタイプによる）。
- PIEとASLR：実行ファイルを位置非依存（PIE）で作ると、カーネルはそのイメージをランダム化してマップでき、ASLRによるセキュリティ効果が高まります。共有ライブラリは通常fPICでビルドします。
- 初期化・終了処理：DT_INIT / DT_INIT_ARRAYでコンストラクタが呼ばれ、DT_FINI / DT_FINI_ARRAYで終了処理が行われます。これらはライブラリがマップされた後、実行開始前に呼ばれます。
- セキュリティ・実運用上の注意：setuidバイナリは環境変数に依るライブラリ検索（LD_PRELOAD/LD_LIBRARY_PATH）を無視します。RPATHに外部ディレクトリを入れると依存注入リスクがあるため注意が必要です。

## 実践ポイント
- まずファイルを確認：readelf/objdump/lddで構成を調べる。
```bash
# bash
readelf -hS -l -d ./your_binary
ldd ./your_binary
objdump -T ./your_binary
```
- 起動時のライブラリ検索を追う：LD_DEBUG=libs ./your_binary で動的リンカの挙動を可視化。
- シンボル解決トラブル：PLT/GOTやR_*のリロケーション問題を確認する（readelf -r）。
- 依存関係を固定化する：必要ならpatchelfでinterpreterやRPATHを修正、または静的リンク（注意：サイズと互換性）を検討。
- セキュリティ対策：PIE/RELRO/Stack Canaryなどビルド時フラグを有効化し、不要なRPATHやLD_PRELOAD使用を避ける。
- コンテナや組み込みでの運用：最小イメージに必要なLD_SOや依存を含める、ld.so.cache更新（ldconfig）を忘れない。

短くまとめれば、ELFの構造（ヘッダ・Program Header・dynamicセクション）と動的リンカの役割（ライブラリ検索・リロケーション・遅延結合）を押さえれば、起動問題の95%は原因が把握できます。実務ではreadelf/ldd/LD_DEBUGをまず使ってみてください。
