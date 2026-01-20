---
layout: post
title: "Why ALTER TABLE is such a problem for SQLite - なぜSQLiteのALTER TABLEは厄介なのか"
date: 2026-01-20T14:56:24.853Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.sqlite.org/lang_altertable.html#why_alter_table_is_such_a_problem_for_sqlite"
source_title: "ALTER TABLE"
source_id: 1036278500
excerpt: "SQLiteのALTER TABLE操作の落とし穴と安全な対処法を具体的に提示"
---

# Why ALTER TABLE is such a problem for SQLite - なぜSQLiteのALTER TABLEは厄介なのか
魅力的タイトル: 「SQLiteでテーブル変更が怖くなる理由 — ALTER TABLEの落とし穴と安全な対処法」

## 要約
SQLiteのALTER TABLEは表面上は簡潔だが、実装は制約だらけで意図せぬ破壊や互換性問題を招きやすい。安全にスキーマを変えるには仕組みの理解と慎重な手順が必須。

## この記事を読むべき理由
SQLiteはモバイルアプリ、組み込み機器、デスクトップツールなど日本のプロダクトでも幅広く使われている。スキーマ変更でアプリが壊れたり古い端末で読めなくなる事故を防ぐため、ALTER TABLEの制約と安全なやり方を知っておく価値が高い。

## 詳細解説
- サポートされるALTER TABLE操作は限られる：テーブル名の変更、カラム名の変更、カラムの追加、カラムの削除のみ。これらも条件付きで動作する。
- スキーマはsqlite_schema（旧sqlite_master）にSQLテキストとして保持され、ALTER TABLEはそのSQL文字列を書き換えて再解析する方式。つまり見た目は「コマンド1発」でも内部はテキスト編集であり、関係するトリガー・ビュー・外部キーなどに残る参照によって失敗する。
- バージョン差に注意：3.25〜3.26でリネーム時のトリガー/ビュー/外部キーの扱いが改善されたが、互換性オプション（PRAGMA legacy_alter_table）や外部キーのON/OFFによって挙動が変わる。
- ADD COLUMNの制約：追加列は末尾にしか付けられず、PRIMARY KEYやUNIQUEは付けられない。デフォルト値としてCURRENT_TIMESTAMP等の特殊式や括弧内式は不可。NOT NULLを付けるならNULLでないデフォルトが必要。チェック制約や生成列のNOT NULLは既存行に対して検査する（失敗すると中止）。
- DROP COLUMNはテーブルを書き換える（データを書き出し・再作成）ため、インデックス、制約、トリガー、ビュー、外部キーで使用されていたり、主キー/一意制約に含まれると失敗する。
- writable_schemaの活用：3.38以降はPRAGMA writable_schema=ONで解析エラーを無視してスキーマ直接編集が可能だが、誤るとデータベースを壊す危険がある。
- 汎用的な安全手順（推奨）：新テーブルを作りデータを移して古いテーブルを削除・リネーム、インデックスやトリガー・ビューを再作成する12ステップ。短縮手順もあるがリスクが高い場面がある。

## 実践ポイント
- まずバージョン確認：SQLiteのバージョンやターゲット端末（古いAndroid等）で機能差異がある。3.25/3.26/3.37/3.38で挙動が変わるため要確認。
- 安全第一の手順（簡易チェックリスト）
  1. バックアップを取る。
  2. PRAGMA foreign_keys を必要に応じて OFF にする（再検証を忘れずに）。
  3. トランザクションを開始する。
  4. CREATE TABLE new_X (...desired schema...);
  5. INSERT INTO new_X SELECT ... FROM X; （列マッピングを明示）
  6. DROP TABLE X;
  7. ALTER TABLE new_X RENAME TO X;
  8. 再作成：CREATE INDEX / CREATE TRIGGER / CREATE VIEW。
  9. PRAGMA foreign_key_check とテストで整合性確認。
 10. コミットしてバックアップを保存。
- 単純な追加（制約なしのADD COLUMN）は高速で安全だが、NOT NULLやCHECKなどを伴う場合は既存データ検査で時間がかかる。
- テスト環境で事前検証：ローカルコピーでschema編集手順を繰り返し検証すること。PRAGMA writable_schemaを使う場合は特に慎重に。
- マイグレーションはアプリ側で順次実行可能なものにする（段階的ロールアウト）と互換性管理が楽。
- ツールの活用：複雑なスキーマ変更はsqitchや独自マイグレーションスクリプトで管理すると事故が減る。

短く言えば、SQLiteのALTER TABLEは「簡単そうに見えて注意が必要」。影響範囲（トリガー・ビュー・外部キー・古いクライアント）を把握して、上記の安全手順を守ればトラブルを避けられる。
