---
layout: post
title: "Lean proved this program was correct; then I found a bug - Lean がこのプログラムは正しいと証明した、しかし私はバグを見つけた"
date: 2026-04-13T16:47:52.580Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kirancodes.me/posts/log-who-watches-the-watchers.html"
source_title: "Lean proved this program was correct; then I found a bug."
source_id: 774747361
excerpt: "Lean証明済み実装をファズしたら、ランタイムのバッファオーバーフローと検証外パーサのDoSが発覚"
---

# Lean proved this program was correct; then I found a bug - Lean がこのプログラムは正しいと証明した、しかし私はバグを見つけた
「証明済みだから安全」は本当か？Leanで証明されたzlib実装をファズしたら、思わぬ“守護者”の穴が見つかった

## 要約
Lean（定理証明器）で「正しい」と証明された圧縮ライブラリ lean-zip をファズしたところ、ライブラリ自身には実装バグが見つからなかった一方で、Leanランタイムのヒープバッファオーバーフローと、ライブラリの未検証部分に起因するDoSが発見された。

## この記事を読むべき理由
AI＋ファジングの進化でバグ発見コストが急低下しており、「証明」だけでは現実の攻撃面すべてを保証できないことが示されたため。日本のプロダクトでも、検証・ランタイム・入力検証の境界を再点検する必要があります。

## 詳細解説
- 背景：lean-zip はAIエージェント群が自律的に実装・証明した zlib 相当実装で、重要定理（任意の1GB未満データについて decompress(compress(data)) = data）がLeanで証明されている。  
  例（要旨）：theorem zlib_decompressSingle_compress ... : ZlibDecode.decompressSingle (ZlibEncode.compress data level) = .ok data

- 実験：著者は証明情報やドキュメント、C FFI を取り除いた「純粋に実装だけのバイナリ」を用意し、Claude（AI）をコントローラにして AFL++、AddressSanitizer、Valgrind、UBSan 等で総当たりテストを実施。約1.058億回の実行で解析した。

- 発見された問題点：
  1. Leanランタイムのヒープバッファオーバーフロー（lean_alloc_sarray）  
     - 問題点：容量計算で elem_size * capacity + header_size の加算が size_t オーバーフローを起こし、極端に大きな capacity（SIZE_MAX）で小さなバッファを割当ててしまう。呼び出し元はそのサイズ分読み書きするためオーバーフロー発生。  
     - トリガー経路：IO.FS.Handle.read 等経由で外部データサイズを直接渡す操作。5行の最小再現コード（Lean）で再現可能。
     
     ```lean
     -- lean
     def main : IO Unit := do
       IO.FS.writeFile "test.bin" "hello"
       let h ← IO.FS.Handle.mk "test.bin" .read
       let n : USize := (0 : USize) - (1 : USize) -- SIZE_MAX
       let _ ← h.read n
     ```
     
  2. lean-zip 側の DoS（未検証のアーカイブパーサ）  
     - readExact が ZIP の central directory から取った compressedSize を検証せずにそのまま読み取り要求に渡すため、膨大な大きさを主張するファイルでメモリ枯渇によりクラッシュ。

- なぜ証明で防げなかったか：  
  - 証明は圧縮/伸張ロジック（DEFLATE・Huffman・CRC32 等）に適用されており、その領域では実装バグが実際に排除されていた。  
  - しかしランタイム（C++ 実装）は証明の信頼基盤（trusted computing base）にあり、そこに欠陥があれば全体の保証は崩れる。さらに、アーカイブパーサはそもそも証明対象外だった。

## 実践ポイント
- 「証明＝完全安全」ではない：証明対象外のコード（ランタイム、FFI、入力パーサ等）が攻撃面になり得る。  
- ランタイムとTCBを最小化し、CIでランタイム更新・監査を怠らない。  
- 外部入力は常に最大値検査やファイルサイズ検証を行う（ヘッダ内サイズを鵜呑みにしない）。  
- 証明と併用でファジング＋ASan/UBSan/Valgrindを回す。検証済みコードも実行時解析を行う価値あり。  
- 日本のプロダクトへ：重要ライブラリ（圧縮、画像、フォント等）は検証の投資検討と同時に、ランタイム堅牢化・入力検証パターンの導入を優先する。

以上。
