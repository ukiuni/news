---
layout: post
title: "Understanding how databases store data on the disk - データベースがディスク上にデータを格納する仕組み"
date: 2026-02-21T13:10:09.520Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pradyumnachippigiri.substack.com/p/how-databases-store-data-on-the-disk"
source_title: "How databases store data on the disk  - by Pradyumna"
source_id: 400466020
excerpt: "ページやブロック、B+木インデックスでI/Oを劇的に減らすDBのディスク設計を図解解説"
image: "https://substackcdn.com/image/fetch/$s_!ns2o!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb57b976a-7a4e-4c32-9683-21bac212706e_2110x1396.png"
---

# Understanding how databases store data on the disk - データベースがディスク上にデータを格納する仕組み
魅力タイトル: ディスクの裏側を覗けばSQLの速さが見える — 「ページ」「ブロック」「インデックス」を一発理解

## 要約
データベースはOSの「ブロック(例:4KB)」とDB固有の「ページ(例:8KB)」を介してディスクとやり取りし、インデックスやB+木でアクセス回数を劇的に減らすことで高速化している。

## この記事を読むべき理由
ディスク構造とDBのページング／インデックスの関係を理解すると、クエリ最適化・インデックス設計・ストレージ選定（HDD vs SSD / NVMe）で実務的に速さとコストを改善できるから。

## 詳細解説
- ディスクの基本要素：プラッタ（磁気面）、トラック（同心円）、セクタ（円弧の切片）を組み合わせた「ブロック（OS/ファイルシステム単位）」が物理読み書きの最小単位。モーターで回り、アームがヘッドを移動するHDDの物理特性がアクセス遅延に直結する。
- OSとDBの単位差：OSは通常4KBブロック単位でI/Oを扱う。DBはそれより大きな「ページ（例:8KB,16KB）」を論理単位とし、ページは複数ブロックに跨る。例：8KBページは2つの4KBブロックを使う。
- 読み取り経路（Read Path）：DBが対象ページを特定 → OSにブロック読み出し要求 → OSキャッシュに無ければディスクから読んで返す → DBはページをバッファプール（RAM）に置き行を抽出。
- 書き込み経路（Write Path）：ページをバッファで更新 → WAL/ジャーナルに追記して永続化 → ページは後でまとめてディスクにフラッシュ（I/O削減のため遅延フラッシュする）。
- ページ内配置：ページはヘッダ／データ領域／スロットディレクトリ（行のオフセット配列）で構成。例えば行サイズ64B、利用可能データ領域8060Bなら行数は $8060 / 64 \approx 125.9$ より1ページ125行となる。
- インデックス効果：全件走査はページ数に比例してI/Oが増えるが、インデックス（キー＋レコードポインタ）を作れば索引のページだけ読み、該当データページにジャンプするため総ブロック数が大幅減。小規模なら一次インデックスで済むがデータが巨大化すると索引自体を多層化（ガイド索引）し、B-tree / B+tree 構造で探索コストを対数的に保つ。
- SSD/NVMeでは物理メカは変わるがOS→ブロックという論理層は同じ。ランダムアクセスが高速になりレイテンシ改善が期待できる。

## 実践ポイント
- ファイルシステムのブロックサイズとDBページサイズを整合させる（例: 4KBと8KBの関係を意識）。
- 重要クエリには適切なインデックスを張る（カーディナリティとカバリングを考慮）。
- バッファプール（キャッシュ）を監視しヒット率を上げることでI/O削減。
- 大規模テーブルはマルチレベル索引（B+木）を前提に設計し、フルスキャンを避ける。
- ストレージ選定はワークロード依存：大量シーケンシャルならHDDでも可、ランダム重視ならNVMe/SSDを優先。
- 実務ツール：EXPLAIN/EXPLAIN ANALYZEで物理読み取り量を確認し、fillfactor・クラスタリング・VACUUM/OPTIMIZEでページ密度を管理する。

必要なら日本のDB製品（PostgreSQL / MySQL / Oracle）での具体的な設定例も用意できます。どの製品で見たいですか？
