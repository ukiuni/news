---
layout: post
title: "Modetc: Move your dotfiles from kernel space - Modetc: ドットファイルをカーネル空間から移動する"
date: 2026-01-24T10:42:05.358Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://maxwell.eurofusion.eu/git/rnhmjoj/modetc"
source_title: "Modetc: Move your dotfiles from kernel space"
source_id: 46741929
excerpt: "カーネルでパスを書き換え、古いアプリのドットファイルを安全に移動する方法"
---

# Modetc: Move your dotfiles from kernel space - Modetc: ドットファイルをカーネル空間から移動する
ホームディレクトリをすっきりさせる“核オプション”──カーネルでパスを書き換えるmodetc

## 要約
modetcはLinuxカーネルモジュールで、VFSレイヤーのパス引数を書き換えてプログラムから見えるファイル位置を任意に差し替えるツール。XDG非準拠の古いアプリのドットファイルをホームから安全に移動できます。

## この記事を読むべき理由
- 日本でも未だにホーム直下に設定ファイルを置く古いアプリは多く、バックアップやストレージ管理で困る場面があるため実務的価値が高い。
- LD_PRELOADやFUSEベースの代替よりも静的バイナリや高性能が求められる環境で使える可能性がある。

## 詳細解説
- 動作原理：kprobesを使ってVFSや関連システムコール（do_symlinkat, do_rmdirなど）にブレークポイントを挿入し、カーネル側の名前キャッシュ(names_cachep)内のパス文字列をインプレースで書き換える。呼び出したプロセスは変更に気付かない。
- 設定方法：カーネルモジュールパラメータで homedir, default_rule, rules_file, debug を指定（modprobe時や /etc/modprobe.conf に記述）。
- ルール仕様：単純なテキストの検索置換のみ（正規表現不可）。ルールは1行に1つ、タブで "<match>\t<replacement>" を区切る。先にマッチしたルールが適用され、最大16ルールまで。対象は
  - 絶対パスで homedir プレフィックス + '/' の場合
  - カレントディレクトリが homedir のとき先頭が '.' の相対パス
- ランタイム制御：/proc/modetc にコマンドを書き込んでルール再読み込みや一時停止が可能（例：echo pause | sudo tee /proc/modetc）。
- 比較：LD_PRELOAD（libetc）は静的バイナリやglibcを使わないプロセスに効かない。rewritefs（FUSE）はIO性能が下がるがファイルシステム層で解決。modetcはカーネル内で動き低オーバーヘッドだが、カーネルモジュールである分リスクと注意が必要。
- ビルド/導入：Nixでのビルドが推奨だが、通常のmakeでビルドしてinsmod/installも可能。NixOS用の設定例も用意。

## 実践ポイント
- まずVMで動作確認：カーネルモジュールなので本番環境で直接試すのは危険。必ず仮想環境でテストする。
- ルールファイルの書式に注意：タブ区切り、行末の#はコメント、空行無視、最大16ルール。
- 常にバックアップを取り、/proc/modetc で動作を一時停止・再読み込みして安全に検証する。
- 競合やセキュリティ面を社内で評価すること（カーネルモジュールの挿入は監査対象になる）。
- 例：modprobeオプションとルール例
```bash
# bash
sudo modprobe modetc homedir=/home/alice default_rule=var/lib/
```
```text
# text (rules file format: <match><TAB><replacement>)
.config/	etc/
.cache/	var/cache/
.ssh	var/lib/ssh
```
