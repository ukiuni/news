---
layout: post
title: "Arrow's Either: The Kotlin Chapter of our Scary Words Saga - ArrowのEither：Kotlin編（怖い言葉の正体をやさしく解説）"
date: 2026-01-16T12:23:04.290Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cekrem.github.io/posts/arrow-either-kotlin-functors-monads/"
source_title: "Arrow's Either: The Kotlin Chapter of our Scary Words Saga · cekrem.github.io"
source_id: 425502209
excerpt: "Kotlinで業務エラーを型で扱い、全バリデーションの失敗をまとめて返すArrow Either入門"
image: "https://cekrem.github.io/images/banner.jpg"
---

# Arrow's Either: The Kotlin Chapter of our Scary Words Saga - ArrowのEither：Kotlin編（怖い言葉の正体をやさしく解説）
Kotlinで使いこなす「Either」──エラーと成功をスマートに扱う実践テクニック

## 要約
ArrowのEitherは「失敗か成功か」を型で明示する結果型で、map/flatMap/zip系の操作で関数型パターン（functor/applicative/monad）を自然に使えます。Kotlinらしい可読性（eitherブロック）と、エラーを一括収集する選択肢が特徴です。

## この記事を読むべき理由
AndroidやKotlinバックエンドでエラー処理や入力検証を堅牢にしたい開発者に有益です。例外ベースのResultと違い、ビジネスエラーを自由に扱えるため、ドメイン設計・ユーザー向けバリデーションで実装が明確になります。

## 詳細解説
- Eitherとは  
  Either<E, A>は左側(Left)にエラー、右側(Right)に成功値を持つコンテナ。Kotlin標準のResultは例外向けにThrowableを固定するのに対し、Eitherはエラー型を任意に定義できるため業務ロジックの表現力が高い。

- Functor（map）  
  Rightなら関数が適用され、Leftならそのまま通り抜ける。エラー側を変換したければ mapLeft を使う。

  ```kotlin
  // kotlin
  "hello".right().map { it.uppercase() }   // Right("HELLO")
  "oops".left().mapLeft { "Error: $it" }   // Left("Error: oops")
  ```

- Applicative（複数のEitherを組み合わせる）  
  複数の検証を組み合わせてデータクラスを作るパターン。eitherブロック内でbind()すると最初の失敗で短絡します（短絡方式）。一方で Arrow は zipOrAccumulate を用意し、すべての失敗を収集する（バリデーションで有用）操作も可能です。

  - 短絡（最初のエラーで終了）: 実用的でシンプル。
  - 収集（すべてのエラーを集める）: フォーム検証などで一度に複数の問題をユーザーに返せる。

- Monad（flatMap / bind）  
  flatMap や either { ... bind() } によって、ネストした Either を避けつつ連鎖的な検証・変換が書けます。eitherブロックはコルーチン機構を利用し、命令形の読みやすさを保ちながらモナディックな短絡を実現します。

- Arrowの設計判断  
  かつての型クラス風APIは削除され、現在は拡張関数群で提供。Kotlinの型システム制約に合わせた実用重視の設計です。

## 実践ポイント
- ドメインエラーは sealed class で定義して Either<DomainError, T> を使うと型安全で保守的。
- 例外捕捉が目的なら Kotlin.Result、業務ロジックの失敗を表現するなら Arrow.Either を選ぶ。
- フォームや複数フィールドのバリデーションでは zipOrAccumulate を検討し、ユーザーに全エラーを返すUXを実現する。
- 可読性を優先するなら either { ... bind() } ブロックを活用。テストもしやすくなる。
- エラー翻訳は mapLeft でレイヤー間の責務を分離する（例：インフラエラー→ユーザ向けメッセージ）。

短く言えば、「怖い"functor/applicative/monad"は既にあなたが使っている操作の名前に過ぎない」。ArrowのEitherはKotlinの現場で即戦力になるツールなので、まずは小さなバリデーションから取り入れてみてください。
