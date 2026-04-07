---
layout: post
title: "Parse, Don't Validate — In a Language That Doesn't Want You To · cekrem.github.io - 「検証ではなくパースを — 言語があなたの味方でないときに」"
date: 2026-04-07T11:27:08.750Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cekrem.github.io/posts/parse-dont-validate-typescript/"
source_title: "Parse, Don't Validate — In a Language That Doesn't Want You To · cekrem.github.io"
source_id: 367808359
excerpt: "TypeScriptで外部入力をパースして型に検証の証明を刻む方法"
image: "https://cekrem.github.io/images/banner.jpg"
---

# Parse, Don't Validate — In a Language That Doesn't Want You To · cekrem.github.io - 「検証ではなくパースを — 言語があなたの味方でないときに」
TypeScriptで「バリデーションを散らす」悪習を断ち切り、型に「信頼の証明」を持たせる方法

## 要約
TypeScriptでよくある「ifでチェックして終わり」の検証は型情報を捨ててしまう。代わりにパーサーを使って外部データをきちんと型化（branded types + discriminated union）すると、安全で追跡可能なドメインモデルが得られる、という話です。

## この記事を読むべき理由
日本のプロダクトでもAPIやフロントで外部データを扱う機会は多く、検証漏れがバグやセキュリティ問題に直結します。TypeScriptを使うなら「検証を型に刻む」設計に変えるだけでバグを減らし、コードの読みやすさと信頼性が劇的に上がります。

## 詳細解説
- 問題点：if (user.email) のような「バリデータ」は実行時に値をチェックしても、関数が戻ると型は元のまま（string/number）。呼び出し元はその検証結果を知れず、再検証や防御的コードが増える。
- 目標：Parserが生データ（unknown）を受け取り、成功なら「ブランド付きの型（Email, Age, UserId など）」を返す。以降のコードはその型があることで検証済みと扱える。
- TypeScriptでの実装テクニック：
  - ブランド（unique symbol）で疑似的な名義型を作る（runtimeでは何も追加されない）。
  - Parsed<T> のような判別共用体で成功/失敗を明示する（例：{ kind: "ok"; value: T } | { kind: "err"; error: {...} }）。
  - JSON.parseの戻り値は any ではなく即座に unknown にして、パーサーに渡す。
  - パーサーだけが as Brand を使って型を与える（キャスト散在を防ぐためモジュール分割＋ESLintルール推奨）。
- ライブラリ：Zod / io-ts / valibot などはこの考え方を楽にする。スキーマからパーサーと型を同時に作れるため導入価値大。ただしライブラリがあっても「境界で必ずパースする」という設計上の規律は必要。

簡単な例（要点のみ）：

```typescript
// TypeScript
declare const EmailBrand: unique symbol;
type Email = string & { readonly [EmailBrand]: true };

type ParseError = { message: string };
type Parsed<T> = { kind: "ok"; value: T } | { kind: "err"; error: ParseError };

function parseEmail(raw: string): Parsed<Email> {
  if (!raw.includes("@")) return { kind: "err", error: { message: "missing @" } };
  return { kind: "ok", value: raw as Email }; // キャストはパーサーだけが使う
}
```

## 実践ポイント
- APIや外部入力はすべて unknown で受け、必ずパーサーを通す（JSON.parse → const raw: unknown = JSON.parse(...)）。
- 生データ型（UnvalidatedUser）と信頼済み型（ValidUser）を明確に分ける。
- ブランドはパーサーモジュール内だけで生成・付与する。外部での as Brand を禁止するESLintルールを検討する。
- 小さなプロジェクトでも Zod 等を導入してスキーマ駆動でパース→型生成を行うと手間が減る。
- 「型が証明を持つ」設計をチームルールにして、レビューで境界の漏れを防ぐ。

このアプローチはTypeScriptの構造型の制約を工夫で補うものです。言語が完全に強制しない以上、設計と習慣で安全性を担保しましょう。
