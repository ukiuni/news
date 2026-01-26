---
layout: post
title: "I built a 2x faster lexer, then discovered I/O was the real bottleneck - 2倍速の字句解析器を作ったら、真のボトルネックはI/Oだった"
date: 2026-01-26T00:19:24.440Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://modulovalue.com/blog/syscall-overhead-tar-gz-io-performance/"
source_title: "I built a 2x faster lexer, then discovered I/O was the real bottleneck | modulovalue"
source_id: 417458388
excerpt: "2倍速レキサーでも104kファイルのI/Oが支配—tar.gz化で総合2.3x高速化の裏技"
---

# I built a 2x faster lexer, then discovered I/O was the real bottleneck - 2倍速の字句解析器を作ったら、真のボトルネックはI/Oだった
2倍速のレキサーを作っても遅いまま？「ファイル数」が性能を食う意外な真実

## 要約
ARM64で2x速い字句解析器を作ったが、104,000ファイルの実データで走らせるとI/O（ファイル読み書き）が支配的で総速改善は僅か。tar.gzでパッケージ化するとI/Oが劇的に速くなり総合で約2.3xの改善に。

## この記事を読むべき理由
日本でも大規模モノレポ、CI、パッケージキャッシュ、ビルドシステムなど「多数の小ファイル」を扱う場面は多い。コード最適化だけでなく「ファイルアクセスの設計」が性能を左右する実例と具体対策が得られる。

## 詳細解説
- ベンチ概要：pubキャッシュ相当の104,000ファイル＝1.13GBを対象に、各ファイルをディスクから読み字句解析。ASMレキサーは字句解析自体は約2.17x高速（Lex: 2,807ms vs 6,087ms）が、I/O時間は双方で約14秒と変わらず、総合は1.22xの改善にとどまった。
- なぜ遅いか：多数の小ファイルは open/read/close をファイルごとに実行するため、100kファイルで300k超のシステムコールとファイルメタデータ参照が発生。システムコールごとのコンテキストスイッチやVFSの作業、ランダム読みのレイテンシが積み重なりI/Oが支配的になる。
- 試した改善：mmapや直接FFIでのsyscallはほとんど効果なし。根本は「ファイル数の多さ」。
- アーカイブ戦略：キャッシュをパッケージ単位で tar.gz にまとめ（104k→1,351アーカイブ、1.13GB→169MB）、I/O時間が14.5s→0.339sに（I/Oで約42.8x速く）、ただし解凍に約4.5sかかる結果に。結果として総合は約2.27x向上。解凍が新たなボトルネックに。
- その他の選択肢：zstd（高速・良圧縮）、uncompressed tar（ローカルキャッシュなら解凍不要でsyscall削減）、SQLiteストアやSquashFS、OSレベルのpackagefs的アプローチも有効。Linuxならio_uringやgetdents64でstat回避、macOSはkqueueやFD制限に注意。ワンショット処理ではclose/freeを省くトリックもあるがFD上限に注意。

## 実践ポイント
- 少数の大きなファイルで扱う：可能なら複数ファイルをアーカイブ（tar/zstd）して読み書き回数を減らす。  
- 圧縮方式は検討する：zstdはgzipより高速解凍＋良好な比率。ローカルキャッシュなら非圧縮tarも選択肢。  
- Linuxではio_uring/getdents64を検討：syscallバッチやstat回避で効果大。  
- SQLiteやSquashFSを検討：大量小ファイルを単一ファイルで扱う別解。  
- 計測を先に：CPU最適化をする前に「I/O vs CPU」を分離測定してボトルネックを確認する。  
- CI/ビルド設計の見直し：多数小ファイルに依存するワークフローはアーカイブやキャッシュ方針で大幅改善が見込める。

短く言えば、「コードを速くするだけでは不十分。ファイルの見せ方（まとまり・圧縮・アクセス方法）を変えれば、桁違いの改善が得られる」。
