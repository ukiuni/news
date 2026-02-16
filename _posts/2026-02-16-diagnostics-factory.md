---
layout: post
title: "Diagnostics Factory - 診断ファクトリ"
date: 2026-02-16T18:36:40.834Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://matklad.github.io/2026/02/16/diagnostics-factory.html"
source_title: "Diagnostics Factory"
source_id: 829581228
excerpt: "Zig流診断ファクトリでエラー報告と表示を分離し、テストを容易化"
---

# Diagnostics Factory - 診断ファクトリ
エラー処理は「型」だけで終わらせない──Zig流「エラーを作る関数」で、報告（reporting）を分離する賢い設計

## 要約
Zigコミュニティの提案は「エラーを列挙する大きなenumを作らない」代わりに、エラーを生成・報告する関数群（＝Diagnostics Factory）を用意して、発生側と表示側を分離する設計です。これによりテストしやすく、出力先やフォーマットを後から柔軟に切り替えられます。

## この記事を読むべき理由
日本の開発現場でも、リンターやCLIツール、CIの診断メッセージは頻出の課題です。エラーの「扱い」と「見せ方」を分けるだけで、テストや国際化、IDE連携（行番号・カラム変換）などの運用がグッと楽になります。

## 詳細解説
基本アイデアは単純です。エラーを「データとして返す（enum/union）」ではなく、「エラーを作って報告する関数群」を定義する。呼び出し側は自分の持っている情報（ファイル、オフセット、禁止語など）をそのまま渡すだけで良く、実際の表示ロジックは中央のfactoryが受け取って処理します。

例（Zig風の擬似コード）:
```zig
const Errors = struct {
    pub fn add_long_line(errors: *Errors, file: SourceFile, line_index: usize) void { ... }
    pub fn add_banned(errors: *Errors, file: SourceFile, offset: usize, banned: []const u8, replacement: []const u8) void { ... }
    pub fn emit(errors: *Errors, comptime fmt: []const u8, args: anytype) void { ... }
};
```

呼び出し側は単に:
```zig
if (line_length > 100) {
    errors.add_long_line(file, line_index);
}
```
と使うだけ。重要なポイントは emit の実装で、実行時は stderr に直接出し、テスト時はメモリに収集するといった切り替えが容易なことです。emit はオフセット→行番号や列の変換、ANSI色付け、フォーマット統一などを一箇所に集約します。

利点まとめ:
- 発生側は余計な型設計を不要にできる（生データを渡すだけ）
- 表示側を自由に差し替え可能（テスト収集、ファイル出力、IDE用フォーマット）
- grep で全エラー箇所が探しやすい（errors.add_ などの命名規約）
- enum で発生側と表示側を結びつけないため進化しやすい

注意点:
- 全エラーが一箇所に列挙されるため、規模次第では肥大化する可能性あり
- 複雑なエラー表現が必要な場面では、工夫が必要

## 実践ポイント
- 小さなツールやリンターならまず関数ベースのDiagnostics Factoryを導入してみる
- emit 関数に「capture（テスト用バッファ）」と「直接出力（実行時）」のスイッチを用意する
- ファイル内位置は内部は0-based、ユーザー表示は1-basedに変換して一元管理する
- 命名規約（errors.add_...）でgrep可能にしてエラー箇所を簡単に把握する
- 将来ANSI色付けやスパン（範囲）、IDE連携へ拡張できる設計にしておく

以上を取り入れると、日本の現場でもツールの品質向上・テスト容易性・運用負荷低減が期待できます。
