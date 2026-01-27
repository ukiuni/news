---
layout: post
title: "Designing Error Types in Rust Applications - Rustアプリにおけるエラー型設計"
date: 2026-01-27T18:40:02.736Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://home.expurple.me/posts/designing-error-types-in-rust-applications/"
source_title: "Designing Error Types in Rust Applications &#183; Dmitrii Aleksandrov"
source_id: 416274480
excerpt: "関数単位の小さなエラー型で保守性とデバッグ効率を実例付きで劇的改善"
---

# Designing Error Types in Rust Applications - Rustアプリにおけるエラー型設計
もう大きな「全局Error」はやめよう：Rustアプリで保守性と可読性を両立するエラー設計

## 要約
アプリケーション内では「関数（あるいは機能）ごとに小さなエラー型」を使い、グローバルな巨大enumを避けると保守性・意図の明確化が得られる。flat（葉）型とnested（呼び出し単位）型のトレードオフを理解して使い分けるのが肝。

## この記事を読むべき理由
日本の開発現場でも、IO多用・サービス連携・複数チームでの改修が増える中、エラー設計が雑だとデバッグやリファクタが爆発的に難しくなる。小さく意味のあるエラー型を使うことで、コードの安全性と運用性が向上します。

## 詳細解説
- ライブラリとアプリの違い  
  ライブラリは呼び出し側が不特定で後方互換性を重視するため幅広いエラー公開が必要。一方アプリは呼び出し元が分かっており、安易に互換性を気にせず内部を最適化できる。

- なぜ「1つの大きな enum」はダメか  
  大きなcatch-all enumはモジュール性を壊し、関数シグネチャが返し得るエラーを正確に表さない。ドキュメントや実装を参照しないと挙動が分かりにくくなる。

- 小さな型に分けるメリット（精密なシグネチャ）  
  共通の葉（leaf）エラーを独立型に抽出すれば、関数ごとの戻り型が実際に出るエラーを正確に示し、コンパイラで安全に扱える。

- Flat vs Nested の対比（簡潔なコード例）

  Flat（葉を列挙）
  ```rust
  enum FoobarError {
      A(AError),
      B(BError),
      C(CError),
  }
  ```

  Nested（呼び出し単位）
  ```rust
  enum FoobarError {
      Foo(#[from] FooError),
      Bar(#[from] BarError),
  }
  ```

  - Flat は呼び出し側で特定の葉エラーを簡単にマッチできるが、リファクタに弱く冗長になりがち。  
  - Nested は呼び出しの文脈（どの呼び出しが失敗したか）を保ち、リファクタに強く、エラーにコンテキストを付けやすい。アプリでは nested を好むケースが多い。

- 必要に応じた「葉エラー」抽出  
  複数箇所で同じ低レベルエラーを扱うなら、共通の型にまとめるとDRYで安全。

- パターンマッチで特定の葉を捕まえたいときの手段  
  - 深いネストを直接パターンマッチする（単純だが将来脆弱）  
  - エラーメッセージで判定（脆弱）  
  - TryFrom/TryInto を実装して安全に抽出する（冗長だが堅牢）

- その他の実務的注意
  - モジュールごと／関数近傍にエラー型を置く（global error.rs は避ける）  
  - 1バリアントだけのenumは不要。必要になったらリファクタでenumを導入する。  
  - アプリでは #[non_exhaustive] は基本不要。  
  - 命名は簡潔に（FooErr::Bar など）。フィールドの可視性も設計で制御。

## 実践ポイント
- まずは「関数（または機能）ごとにenum or error型を用意」する癖をつける。  
- モジュール内で共通の低レベルエラーがあれば独立型にまとめる。  
- 呼び出しレベルでは nested enums を基本とし、特殊に葉マッチが必要な箇所だけ TryFrom などで抽出する。  
- エラー型は関数の直近に置き、ドキュメントでは「どのvariantが返るか」を短く明記する。  

これらを踏まえれば、リファクタやデバッグが楽になり、大規模化した日本のプロダクトでも安定したエラー設計が可能になります。
