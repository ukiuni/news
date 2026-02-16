---
layout: post
title: "Error payloads in Zig - Zigにおけるエラー・ペイロード"
date: 2026-02-16T00:33:16.134Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://srcreigh.ca/posts/error-payloads-in-zig/"
source_title: "Error payloads in Zig"
source_id: 47028705
excerpt: "Zigでエラーに任意ペイロードを持たせ自動伝搬し冗長を削減する実践テクニック（SQLite例あり）"
---

# Error payloads in Zig - Zigにおけるエラー・ペイロード
Zigでエラーに“中身”（ペイロード）を持たせ、呼び出し側で簡潔に受け渡すテクニック

## 要約
Zigで関数ごとにunion(enum)ベースのDiagnostics型を作り、エラーに任意のペイロードを紐付けて呼び出し側で自動的にコピー／伝搬する手法を紹介する。これによりコールサイトの冗長なボイラープレートを減らせる。

## この記事を読むべき理由
システムプログラミングや組込系・DB周りの処理で「エラーの種類」と「追加情報（例：SQLiteのエラーメッセージ）」を一緒に扱いたい場面が多く、日本の現場でも可読性とバイナリサイズの改善に直結する実用的なテクニックだから。

## 詳細解説
- アイデア：各関数に対して
  union(enum) で可能なエラーとそれぞれのペイロード型を列挙し、これをラップする Diagnostics 型を作る。ラッパーは内部に optional ペイロードを持ち、enum からエラーセット型を生成する。
- 型生成（要点）：
```zig
pub fn FromUnion(comptime _Payload: type) type {
    return struct {
        pub const Payload = _Payload;
        pub const Error = ErrorSetFromEnum(std.meta.FieldEnum(Payload));
        payload: ?Payload = null;
        // ...withContext, get, call 等のメソッド...
    };
}
```
- withContext：エラーを返す際にペイロードをセットして返す。例：sqliteの500バイトのエラーメッセージを保存して返す。
```zig
catch |err| return switch (err) {
    error.SqliteError => diag.withContext(error.SqliteError, .init(db)),
    error.OutOfMemory => error.OutOfMemory,
};
```
- call メソッド：ある関数を呼び出す際、その関数が期待する Diagnostics 型を推論して一時的な diag を渡し、エラー時にペイロードを呼び出し側の Diagnostics にコピーして返す。結果的にコールサイトは1行でペイロード伝搬を実現できる。
```zig
const n_rows = try diag.call(countRows, .{ alloc, db, opts });
```
- エッジ処理：最終的にログ出力や詳細処理を行う場所で diag.get(errorType) でペイロードを取り出して使う。
- 補足：ZLS（エディタの補完）は diag.call の戻り型を推論できないことがあるため、明示的な型注釈を入れると便利。

## 実践ポイント
- 各モジュール／関数に対して union(enum) でエラー＋ペイロードを定義して Diagnostics を作る。
- エラーを返す箇所では withContext を使ってペイロードを添える。
- 呼び出し側では diag.call を使ってペイロードを自動伝搬させ、必要なら最終処理で diag.get してログや詳細表示に使う。
- ZLSや型推論が怪しい場合は明示的な Diagnostics 型注釈を付ける。

このパターンは、エラー情報を豊かに保ちながらコールサイトのコード量を減らしたい場面に特に有効です。
