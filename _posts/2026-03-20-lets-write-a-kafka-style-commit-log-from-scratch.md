---
layout: post
title: "Let's write a Kafka-style commit log from scratch. - Kafka風コミットログをゼロから作る"
date: 2026-03-20T12:56:09.561Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sushantdhiman.dev/kafka-like-commit-log/"
source_title: "Building a Kafka-style commit log from scratch."
source_id: 377922603
excerpt: "GoでKafka風コミットログを実装し、store/index/mmapで高速耐久性を体験"
image: "https://static.ghost.org/v5.0.0/images/publication-cover.jpg"
---

# Let's write a Kafka-style commit log from scratch. - Kafka風コミットログをゼロから作る
Kafkaの「中身」を手で触って学ぶ──Goで実装するシンプルなコミットログ

## 要約
Kafkaは本質的に「追記専用のコミットログ」。この記事はGoで最小限のコミットログ（store + index + segment + mmap）を作り、仕組みを実践的に解説します。

## この記事を読むべき理由
Kafkaやイベントソーシング、耐久性が必要なメッセージ基盤の内部動作を理解すると、障害設計・パフォーマンス改善・自作軽量ストレージ設計で即戦力になります。日本のスタートアップや金融系で低レイテンシかつ耐久性のある設計が求められる場面で特に役立ちます。

## 詳細解説
- コミットログとは  
  追記専用（append-only）で不変なレコード列。DBのWALやメッセージブローカー、イベントソーシングのソース・オブ・トゥルースになる。

- storeファイル（*.store）のフォーマット  
  各レコードはまず長さを8バイトで書き、その後にデータ本体を続ける。長さは常に8バイト（lenWidth = 8）で、エンディアンはネットワーク標準のbig-endianを使用（enc = binary.BigEndian）。これにより読み取りは「先頭8バイト→長さN→Nバイト読取」で確定的に行える。Append時はバッファ（bufio.Writer）へ書き、sizeで現在のファイル末尾位置を保持。Readではbuf.Flush()してから ReadAt で直接読み取る（OSキャッシュ対策）。並行処理対策に mutex を使う。

  例（要点抜粋）:
  ```go
  // go
  binary.Write(buf, binary.BigEndian, uint64(len(data)))
  buf.Write(data)
  ```

- indexファイル（*.index）のフォーマット  
  各インデックスエントリは 4バイト（offset）+ 8バイト（store内のposition）で合計12バイト（completeWidth = 12）。オフセットは自動増分なので任意の offset に対して位置は
  $byte\_pos = offset \times 12$
  で計算できる（例：$5 \times 12 = 60$ → バイト60〜71が5番目のエントリ）。

- メモリマップ（mmap）による高速化  
  gommap を使い index ファイルをメモリにマップすると、システムコールを減らして配列アクセス感覚で読み書きできる。ただし mmap する前にファイルを最大サイズへ Truncate（ゼロ埋め）しておく必要がある。理由は mmap 後のサイズ変更が困難なため。書き込み時は mmap 上のバイト領域に enc.PutUint32/PutUint64 で直接書き、Close 時に mmap.Sync → file.Sync → 実データ長に再トランケートして余分なゼロを取り除く（再起動時の誤読防止）。

- セグメント化（Segment）  
  ファイルが大きくなりすぎないよう、複数のセグメント（例: 00000000.store / 00000000.index, 00010000.*）で区切る。セグメントごとに初期オフセット、最大store/indexサイズを持たせる。

- 実装上の注意点
  - Endiannessは揃える（big-endian推奨）。
  - Read前の buf.Flush() を忘れない（メモリ上に留まっているデータが読み出せない）。
  - mmapは高速だが事前割当とトランケートの手順が必須。
  - 並列Append/Readはロックで整合性確保。
  - 再起動時は index の実サイズに合わせてファイルを復元する。

## 実践ポイント
- まず小さなPoCを書いて、storeに書いて読み出せることを確認する（len-prefix + data の読み書き）。
- indexは最初は単純なファイルアクセスで実装し、動作確認後に mmap 化する。mmap化前に必ず Truncate を行うこと。
- Read実装では常に buffered writer を Flush してから ReadAt を行う。
- セグメントの閾値（MaxStoreBytes, MaxIndexBytes）を運用想定で決め、古いセグメントの削除/圧縮戦略を用意する。
- 再起動テスト：クラッシュ相当でプロセスを止め、index と store が整合しているか確認する（Close時の truncate/Sync 処理が鍵）。

以上を踏まえれば、Kafkaの「速さ」「耐久性」「シーケンシャル書き込み」などの本質を自分の手で体験できます。興味があれば、実装の小さなサンプルを付けて続編を書きますか？
