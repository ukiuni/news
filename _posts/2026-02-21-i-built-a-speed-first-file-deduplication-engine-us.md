---
layout: post
title: "I built a speed-first file deduplication engine using tiered BLAKE3 hashing and CoW reflinks - Tiered BLAKE3ハッシュとCoW reflinkで作った“速度重視”ファイル重複排除エンジン"
date: 2026-02-21T14:17:07.599Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://crates.io/crates/bdstorage"
source_title: "I built a speed-first file deduplication engine using tiered BLAKE3 hashing and CoW reflinks"
source_id: 400141710
excerpt: "Tiered BLAKE3とCoW reflinkで数TBを瞬時重複削除"
---

# I built a speed-first file deduplication engine using tiered BLAKE3 hashing and CoW reflinks - Tiered BLAKE3ハッシュとCoW reflinkで作った“速度重視”ファイル重複排除エンジン
一瞬で重複を片付ける：Linux向け高速ファイル重複排除ツール bdstorage の中身

## 要約
bdstorage は、Tiered BLAKE3 ハッシュ＋Copy-on-Write (reflink) を使い、I/O を最小化して高速にローカルファイルの重複を検出・置換する Rust 製エンジンです。

## この記事を読むべき理由
大量の写真・動画やバックアップ、NAS を運用する日本のエンジニアにとって、ディスク読み込みを抑えつつ安全に重複を削減できるツールは運用コストとパフォーマンス改善に直結します。

## 詳細解説
- 基本方針：全ファイルをフル読みするのではなく「速度優先」で候補を絞り込む階層化ハッシュ処理を採用。
- Tiered Hashing：
  - サイズでグループ化（I/O なし）。サイズが唯一なら終了。
  - スパースハッシュ（最小 I/O）：12KB をサンプル（先頭4KB・中央4KB・末尾4KB）読み、差があれば除外。Linux では sparse ファイルを fiemap で扱う。
  - フル BLAKE3 ハッシュ：候補のみ 128KB バッファで高速にフルハッシュして確定。
- 同一と判定したら CAS（Content-Addressable Storage）ボールトへ「マスター」を移動し、そのハッシュ名で保存。
- リンク戦略：
  - 優先：CoW reflink（瞬時でディスク領域を共有、推奨ファイルシステム：Btrfs/XFS）。
  - 非対応時：ハードリンクにフォールバック。
- 状態管理：組み込みの低レイテンシ DB（redb）でメタデータと参照カウントを管理し、誤削除を防止。
- 安全設計の要点：ボールト保存成功確認→リンク作成、処理途中で中断しても未処理ファイルはそのまま、--paranoid でバイト単位検証が可能。
- 要件：Linux 必須（fiemap 最適化のため）。ソースは Rust（stable）。

## 実践ポイント
- まずは read-only な scan を実行して候補を確認：
```bash
bdstorage scan /path/to/directory
```
- 実行は dry-run から。実運用では --paranoid を付けると安全性がさらに高まる：
```bash
bdstorage dedupe /path/to/directory -n    # シミュレーション
bdstorage dedupe /path/to/directory --paranoid
```
- リストア：
```bash
bdstorage restore /path/to/directory -n
```
- インストール：
```bash
cargo install bdstorage
# またはソースから
git clone https://github.com/Rakshat28/bdstorage
cd bdstorage
cargo build --release
```
- 運用上の注意：
  - 実行前に必ず scan と dry-run を行う。
  - reflink 対応ファイルシステム（Btrfs/XFS）を推奨。未対応だとハードリンクになる。
  - ボールト（~/.bdstorage/store/）と state.redb を監視・バックアップしておく。
  - 大量データ／業務データで使う場合はまずテスト領域で検証すること。

短く言えば、bdstorage は「読み込みを減らして速く、安全に重複を共有する」ことに特化したツールで、特に媒体多めの日本の現場で即戦力になり得ます。
