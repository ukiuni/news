---
layout: post
title: "150 MB Minimal FreeBSD Installation - 150MBで動く最小FreeBSDインストール"
date: 2026-02-05T17:05:43.776Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vermaden.wordpress.com/2026/02/01/150-mb-minimal-freebsd-installation/"
source_title: "150 MB Minimal FreeBSD Installation | 𝚟𝚎𝚛𝚖𝚊𝚍𝚎𝚗"
source_id: 46841897
excerpt: "ZFS＋zstd-19でFreeBSDを約150MBに圧縮する最小化手順をVMで安全に試す方法"
image: "https://vermaden.wordpress.com/wp-content/uploads/2026/01/sqlite-pkg-database-relations.png"
---

# 150 MB Minimal FreeBSD Installation - 150MBで動く最小FreeBSDインストール
魅力的タイトル: 「FreeBSDをたった150MBに圧縮する裏ワザ — テスト環境で試すスリム化手順」

## 要約
FreeBSD 15.0 を PKGBASE（パッケージベース）で最小化し、ZFS＋zstd-19 圧縮を使って実働サイズを約150MBまで削減する手順と注意点を紹介します。実運用では非推奨なので、検証用VMでのみ実行してください。

## この記事を読むべき理由
- 日本でも組み込み機器やリソース制約のあるVMで「軽いOS」が求められます。FreeBSDを極限まで小さくする手法は、学習やプロトタイプ、検証環境として即役立ちます。  
- pkg（パッケージ管理）とZFSの組合せでどこまで削れるかを理解すると、システム設計と運用判断がより正確になります。

## 詳細解説
- ベースは FreeBSD 15.0-RELEASE を bsdinstall で「Packages (Tech Preview)」→「Offline (Limited Packages)」→「Auto (ZFS)」→ZFS オプションで `-O compression=zstd-19` を選択してインストールします。これによりディスクの物理使用量を大きく削減できます。  
- デフォルトで入るセット（base/devel/minimal/optional 等）を削り、pkg 自体が動くために必要な最小パッケージ群だけを残すのが狙いです。実際に残すべき主要パッケージ例：FreeBSD-libarchive, FreeBSD-openssl-lib, FreeBSD-xz-lib, FreeBSD-libucl, FreeBSD-libcasper 等。  
- 手順の要点：
  1. まず重要なライブラリ類をロックして誤削除を防ぐ。
  2. FreeBSD-set-*（devel/optional 等）に含まれる不要パッケージを削除して容量を削る。
  3. pkg の依存情報（/var/db/pkg/local.sqlite）を書き換え、base の set 依存を取り除くことで次回 upgrade 時に再インストールされるのを防ぐ（ただしリスクあり）。  
- 失敗例：依存ライブラリを削ると pkg が共有ライブラリ不足で動かなくなることがあり、その場合は pkg-static が救いになります。必ず ZFS のブート環境（bectl create backup）や /var/db/pkg/local.sqlite のバックアップを取ってから実行してください。  
- pkg upgrade はデフォルトで多くの base パッケージを再インストールしに来ます。これを回避するために pkg の SQLite データベースから特定の deps エントリを削除する手法が使われますが、パッケージ整合性を壊す可能性があるため慎重に。

## 実践ポイント
- 必須の事前準備（テスト環境で必ず行う）:
```bash
# ZFS BE を作る（バックアップ）
bectl create backup

# pkg データベースのバックアップ
cp /var/db/pkg/local.sqlite /var/db/pkg/local.sqlite.BACKUP
```
- ロックしておくパッケージ例:
```bash
pkg lock -y FreeBSD-libarchive FreeBSD-openssl-lib FreeBSD-xz-lib FreeBSD-libucl FreeBSD-libcasper
```
- 不要セット内のパッケージ一括削除（例）:
```bash
pkg info -d FreeBSD-set-devel-15.0 | tr ':' ' ' | while read PKG; do pkg delete -fy ${PKG}; done
pkg info -d FreeBSD-set-optional-15.0 | tr ':' ' ' | while read PKG; do pkg delete -fy ${PKG}; done
```
- pkg が将来再インストールしないよう deps を編集する（リスク有り）:
```bash
echo 'delete from deps where origin = "base/FreeBSD-set-devel";' | pkg shell
```
- 注意点（必読）:
  - これらの変更は「サポート外／非推奨」です。実機での運用には向きません。  
  - pkg の整合性が崩れると自動更新やパッケージ管理に問題が残ります。復旧手順（BE 切替、local.sqlite の復元）を必ず確認してください。

以上を踏まえ、まずはクリーンな VM で手順をなぞって挙動を観察することをおすすめします。
