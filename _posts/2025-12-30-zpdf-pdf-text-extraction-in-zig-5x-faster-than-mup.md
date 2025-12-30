---
layout: post
title: "Zpdf: PDF text extraction in Zig – 5x faster than MuPDF - Zpdf：ZigでのPDFテキスト抽出 — MuPDFより5倍高速"
date: 2025-12-30T21:36:52.187Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Lulzx/zpdf"
source_title: "Zpdf: PDF text extraction in Zig – 5x faster than MuPDF"
source_id: 46437288
excerpt: "Zig製のゼロコピーPDF抽出器でMuPDFより5倍高速、数万ページのバッチ処理を劇的に短縮"
---

# Zpdf: PDF text extraction in Zig – 5x faster than MuPDF - Zpdf：ZigでのPDFテキスト抽出 — MuPDFより5倍高速
魅力タイトル：Zigで“ゼロコピー”PDF抽出。高速・軽量で大量ドキュメント処理が変わる

## 要約
ZpdfはZigで書かれたゼロコピーPDFテキスト抽出ライブラリ。メモリマップ、SIMD最適化、ページ単位の並列処理でMuPDFより数倍高速にテキストを取り出せる。

## この記事を読むべき理由
大量のPDFを扱う検索インデックス作成、ログ的な文書解析、法務・アーカイブ処理など、日本の現場でも「高速でメモリ効率の良いテキスト抽出」は直接的な時間・コスト削減につながる。特に数万〜数十万ページ単位でのバッチ処理やCIパイプラインに有用。

## 詳細解説
- アーキテクチャの肝
  - ゼロコピー: ファイルをメモリマップして直接パースするため不要なバッファ複製を避ける。
  - ストリーミング抽出: 中間割当てを極力行わずにテキストを書き出す設計でGC/ヒープ負荷が小さい。
  - SIMD加速: 文字列操作のホットパスをSIMDで高速化している（高速なバイト列処理）。
  - 並列化: ページ単位で並列抽出を実行。mutool のテキスト変換がシングルスレッドであるのに対し、zpdfはマルチスレッドで大幅なスループット向上を実現。

- サポート技術
  - ストリーム解凍: FlateDecode, ASCII85, ASCIIHex, LZW, RunLength を実装。
  - フォント・エンコーディング: WinAnsi, MacRoman, ToUnicode CMap、CID (Type0) などを扱い、UTF-16BEの処理もサポート。
  - PDF内部: XRefテーブル／ストリーム（PDF 1.5+）、増分更新の追跡（/Prevチェーン）を解析可能。
  - コンテンツ解釈: Tj, TJ, Tm, Td 等のテキストオペレータを解釈してテキストを復元。

- ベンチマーク（README抜粋）
  - 順次抽出で概ね 2.7–4.4x、並列抽出だと最大 18x（Intel SDM）の速度向上。ピークスループットは約 41,000 pages/sec（並列）。
  - 再現のためには Zig 0.15.2 以上、リリース最適化（zig build -Doptimize=ReleaseFast）が推奨。

- 実行例（ライブラリ呼び出し）
```zig
const std = @import("std");
const zpdf = @import("zpdf");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    const doc = try zpdf.Document.open(allocator, "file.pdf");
    defer doc.close();
    var buf: [4096]u8 = undefined;
    var writer = std.fs.File.stdout().writer(&buf);
    defer writer.interface.flush() catch {};
    for (0 .. doc.pages.items.len) |page_num| {
        try doc.extractText(page_num, &writer.interface);
    }
}
```

## 実践ポイント
- いつ使うか：テキスト抽出だけが目的で、レンダリング不要なバッチ処理や検索インデックス作成に最適。
- 日本語PDFへの注意点：CJKフォントはToUnicode / CMap の有無で結果が大きく変わるため、日本語PDFでの抽出精度は必ず実ファイルで検証すること。CID フォント処理を確認する。
- パフォーマンスTips：必ず ReleaseFast ビルド、メモリマップが可能な環境で動かす。大量ページの処理では並列モードが有効。
- 安定性・採用判断：MITライセンスで導入しやすいが、リポジトリはまだ小規模（スター数など）なので、プロダクション採用時は耐障害性とエッジケース（特殊フォント・壊れたPDF）を自前で検証・補完すること。

## 引用元
- タイトル: Zpdf: PDF text extraction in Zig – 5x faster than MuPDF
- URL: https://github.com/Lulzx/zpdf
