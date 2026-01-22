---
layout: post
title: "Don't Trip[wire] Yourself: Testing Error Recovery in Zig - Zigでのエラー回復テストを簡単にするTripwire"
date: 2026-01-22T06:30:47.330Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mitchellh.com/writing/tripwire"
source_title: "Don&#x27;t Trip[wire] Yourself: Testing Error Recovery in Zig – Mitchell Hashimoto"
source_id: 996342187
excerpt: "テスト時に失敗点注入でZigのerrdefer漏れを検出、本番でゼロコスト"
---

# Don't Trip[wire] Yourself: Testing Error Recovery in Zig - Zigでのエラー回復テストを簡単にするTripwire
エラー経路を“強制発火”して、見落としがちなcleanup（errdefer）を確実に検証する方法

## 要約
Zigのerrdeferで書かれたエラー回復コードはテストしづらい。Mitchell HashimotoのTripwireは、テスト時だけ失敗点を注入してerrdeferやリソース解放の不備を検出する単一ファイルのライブラリで、リリースではゼロコストになります。

## この記事を読むべき理由
errdefer周りのバグは見落とされやすく、メモリリークや破損を招きます。日本でも組込みやサーバー系で堅牢性が問われる場面が多く、実運用前に確実にエラー経路を検証したいエンジニアは必読です。

## 詳細解説
- Zigのエラー処理要点：関数はエラーを返し得る（error値／error set／error union）。tryでアンラップし、errdeferはエラーで返るときにのみ実行されるため、部分的に成功した状態の巻き戻しに使う。
- 問題点：errdeferは通常パスほど頻繁に実行されないためテストで発火させにくく、特に複数の条件付き割当や複雑な初期化があると、失敗パスの再現が脆弱になる。
- Tripwireの仕組み：
  - テスト時に「名前付きの失敗点（FailPoint）」を定義し、該当箇所でチェック（check）すると設定次第でエラーを返す。
  - テストでは errorAlways / errorAfter などでそのポイントで必ず（または回数指定で）エラーを発生させ、endで発火確認や状態検証を行う。
  - std.testing.allocatorと組み合わせると、errdeferが正しく呼ばれていなければメモリリークとしてテストが失敗する。
- ゼロコスト設計：
  - comptimeで builtin.is_test を参照して有効化を判定し、テスト以外では関数呼び出しがインライン化され実装ごと削除されるため実行時コストはゼロ。
  - callingConventionをcomptimeで切り替え、テスト無効時はインライン化して余分な関数呼び出しを残さない工夫がある。
- 実績：Ghosttyへの導入で複数のerrdeferバグを発見・修正し、修正はユニットテストで回帰防止されている。Tripwireは単一ファイルでMITライセンス。

コード例（使い方の最小イメージ）:
```zig
const init_tw = tripwire.module(enum { alloc_buffer, open_file }, init);

fn init(alloc: Allocator) !*Self {
    try init_tw.check(.alloc_buffer);
    const buf = try alloc.alloc(u8, 1024);
    errdefer alloc.free(buf);
    try init_tw.check(.open_file); // テスト時ここでエラー注入
    const file = try std.fs.cwd().openFile("config.txt", .{});
    errdefer file.close();
    return self;
}

test "init errors at open_file" {
    try init_tw.errorAlways(.open_file, error.OutOfMemory);
    try std.testing.expectError(error.OutOfMemory, init(std.testing.allocator));
    try init_tw.end(.reset); // 発火検証とリセット
}
```

## 実践ポイント
- プロジェクトに tripwire.zig を単一ファイルで追加して、重要な初期化／リソース取得ポイントの直前に check を置く。
- 各FailPointに対して errorAlways で1回ずつテストを回す（ループで網羅すると確実）。
- std.testing.allocatorを使えばメモリリーク／未解放の誤りを自動検出できる。
- 本番ビルドでのオーバーヘッドはゼロなので、テストコードとして気軽に導入できる。
- 日本語のレビュー文化と組み合わせ、PRにTripwireベースの負荷の少ないテストを追加して回帰を防ごう。
