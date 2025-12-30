---
layout: "post"
title: "I was wrong about typescript part 1 - TypeScriptについて私は間違っていた 第1部"
date: "2025-12-28 19:19:09.874000+00:00"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://chefama.blog/blog/posts/i-was-wrong-about-typescript-1"
source_title: "Amadu's and Don'ts"
source_id: "1658036199"
excerpt: "TypeScriptの落とし穴と即効対策を実務視点で具体解説"
---
# I was wrong about typescript part 1 - TypeScriptについて私は間違っていた 第1部

## 要約
TypeScriptは完璧ではないが、設定とパターン次第で実用的な型安全性を実現できる。本稿は「問題点の整理」と「日本の現場で使える即効対策」を中心に解説する（元記事は前編）。

## この記事を読むべき理由
TypeScriptは日本のフロント／フルスタック開発で広く採用されている。だがデフォルト設定や誤った使い方で型の恩恵を失いやすく、バグや設計上の誤解を招く。実務で事故を減らすための具体策を知っておく価値がある。

## 詳細解説
以下は元記事で指摘された代表的な問題点とその技術的背景。

1. 例外・エラー情報が型に現れない
   - fetchやJSON.parseなどが投げる例外は型システムに反映されない。TypeScriptの型はコンパイル時のみで、関数が例外を投げる事実を型で表現する仕組み（checked exceptions）は無い。
   - 結果: 呼び出し側で「この呼び出しが失敗する可能性がある」ことが明示されず、実行時エラーにつながる。

2. any／型逃げの容易さ
   - any によるキャストはコンパイラチェックを回避する。ある型から別型へどうしても変換したい場合、`as any as T` といった抜け道があり得るため安全性が崩れやすい。
   - 対象: 大規模コードベースでの一箇所の any が引き金で型情報が広がる。

3. デフォルトで厳格ではない
   - tsconfig の既定値では型の抜け穴（implicit any、strict null checks 無効など）が残るため、型の利点が得られにくい。
   - 例: `!!`（non-null assertion）や `as any` によって安全策を明示的に破るコードが書きやすい。

4. 返り値型の「保証」が実行時にない（構造的型付け）
   - TypeScriptは構造的型システムのため、関数のシグネチャに「User -> SafeUser」と書いても、ランタイムで余分なプロパティが残っていてもコンパイルを通る。
   - 対照: Rustのようにコンパイラが静的にすべてを保証する仕組みとは異なる（TypeScriptの型はランタイムに残らない）。

短いコード例（問題のイメージ）:
```typescript
// TypeScript
type User = { name: string; age: number; password: string };
type SafeUser = { id: string; email: string };

function toSafe(user: User): SafeUser {
  return user as any as SafeUser; // 型が通るが実行時に問題が出る可能性あり
}
```

## 実践ポイント
すぐ導入できる現場向け対策を簡潔にまとめる。

- tsconfig を厳格化する
  - まずは tsconfig.json に:
    - "strict": true
    - "noImplicitAny": true
    - "strictNullChecks": true
    - "noUncheckedIndexedAccess": true
  - 段階的にオンにしてコードベースを修正する。

- any を禁止・代替する
  - ESLint で `@typescript-eslint/no-explicit-any` を有効化し、例外はレビューで許可制にする。
  - 代替: unknown を使い、型ガードで安全に narow する。

- ランタイムバリデーションの導入
  - API境界には zod / io-ts / runtypes などでスキーマバリデーションを入れる（型情報をランタイムで検証）。
  - 例: 外部JSONを受け取る箇所は `zod.parse()` を通す。

- エラー表現を型にする（Result パターン）
  - 例外を型で表現するには Result/Either 型を使う（fp-ts / ts-results など）:
```typescript
// TypeScript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

async function fetchData(): Promise<Result<Data, Error>> {
  try {
    const r = await fetch(url);
    const j = await r.json();
    return { ok: true, value: parseData(j) };
  } catch (e) {
    return { ok: false, error: e as Error };
  }
}
```
  - 呼び出し側でエラーパスを明示的に扱うことができる。

- レビューと自動化
  - CIで型チェック（tsc --noEmit）と ESLint を必須にする。
  - 重大箇所はインテグレーションテスト／型付きユニットテストで検証。

- 設計上の注意
  - API の返却型は「必要なプロパティのみを返す」ように明確に実装する（例えばサニタイズ関数を作る）。
  - `as` キャストは最小限に抑え、使う場合はコメントで根拠を残す。

