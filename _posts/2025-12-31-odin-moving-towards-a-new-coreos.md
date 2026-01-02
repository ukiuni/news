---
layout: post
title: "Odin: Moving Towards a New \"core:OS\" - Odin: 新しい core:os への移行"
date: 2025-12-31T07:37:58.386Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://odin-lang.org/news/moving-towards-a-new-core-os/"
source_title: "Odin: Moving Towards a New \"core:OS\""
source_id: 46389925
excerpt: "Odinのcore:os再設計で明示的アロケータと^os.File導入、2026Q1移行で要対応"
---

# Odin: Moving Towards a New "core:OS" - Odin: 新しい core:os への移行
Odinの基盤が刷新 — core:os再設計で何が変わる？日本の開発者が押さえるべきポイント

## 要約
Odinの基盤パッケージ core:os が全面的に再設計され、明示的なアロケータ、^os.File によるファイル抽象、os.Error の導入などで一貫したクロスプラットフォームAPIへ移行する。core:os/os2 は既に利用可能で、正式移行は2026年Q1を予定。

## この記事を読むべき理由
- システム寄りやクロスプラットフォーム開発で使う基盤APIが変わるため、既存コードの互換性対策が必要。  
- 新設計はテスト／インターセプト性を高め、OSレベルの振る舞いを明確化するため、今のうちに準備すると移行コストを下げられる。

## 詳細解説
- 背景  
  core:os と base:runtime は言語ブートストラップから残る最古のパッケージで、歴史的に寄せ集め的な設計になっていた。これを一貫性のあるコアライブラリ基準に合わせる目的で再設計が進められている。

- 移行スケジュール  
  core:os/os2 が既に提供されており、これが将来的に core:os に置き換わる。正式な切替は Q1 2026 を予定。破壊的変更が多数入るため早めの検証推奨。

- 主な技術的変更点  
  - 明示的アロケータ要求：メモリを返す手続きは明示的な allocator を受け取るように。現状の動作を模倣するには context.allocator や context.temp_allocator を渡す。  
  - エラー型の改善：真偽値や整数Errnoではなく、os.Error（enumのユニオン）を返すAPIが増える。エラー処理の判別がより表現的に。  
  - ファイル型の抽象化：生のハンドル os.Handle → ^os.File（ポインタを介した汎用インターフェース）に。バッファリングやインターセプトが容易に。  
  - パス／プロセス／ディレクトリ走査などの新APIや改良されたディレクトリウォーカー、プラットフォーム間で一貫した挙動。  
  - プラットフォーム依存APIの整理削除：get_last_error、get_page_size、get_std_handle、get_windows_version、is_windows_* などが削除または整理される。

- 設計意図（簡潔）  
  - ^os.File による抽象は、第三者コードの挙動を簡単に差し替え・監視できるようにするため。Odinの言語設計にある「暗黙のコンテキストによる介入可能性」と整合。  
  - 明示的アロケータは「誰がどこで割り当てるのか」を明確化するため。core:os は内部専用のカスタムアロケータを使い、ユーザレベルのアロケータと役割を分離する。

- 小さなコード例（旧 → 新）
```odin
// odin
// 旧 API
data, ok := os.read_entire_file("path/to/file.txt")
```

```odin
// odin
// 新 API（アロケータを渡す）
data, err := os.read_entire_file("path/to/file.txt", context.allocator)
```

```odin
// odin
// 型の違い
// 旧: fd: os.Handle
// 新: f: ^os.File
```

```odin
// odin
// エラー型の違い
// 旧: err : os.Errno
// 新: err : os.Error
```

## 実践ポイント
- まず core:os/os2 をプロジェクトで試す：互換性テストとビルドを早めに回して問題箇所を洗い出す。  
- アロケータ対応：メモリを返すAPI呼び出しを検索し、context.allocator / context.temp_allocator を渡す設計に置換。  
- ファイルAPIの差し替え準備：os.Handle を使っている箇所は ^os.File ベースへ移行できるようインターフェースを整理。テストでバッファリングやフックが正しく動くか確認。  
- エラーハンドリングを見直す：os.Error のenumをスイッチやマッチで扱うように変える。整数Errnoや真偽値の判定に依存しているロジックをリファクタ。  
- プラットフォーム固有コードの削除依存を排除：移植性を高めるため platform-specific なAPIに頼る箇所を抽象化する。  
- 依存管理：core:os の正式移行時に備え、バージョンピン／リリースノート監視で破壊的変更を見逃さない。

