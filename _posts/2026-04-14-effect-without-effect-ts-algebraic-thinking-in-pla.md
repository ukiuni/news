---
layout: post
title: "Effect Without Effect-TS: Algebraic Thinking in Plain TypeScript - Effect-TSなしで実装する：プレーンなTypeScriptでの代数的思考"
date: 2026-04-14T09:16:42.058Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cekrem.github.io/posts/effect-without-effect-ts/"
source_title: "Effect Without Effect-TS: Algebraic Thinking in Plain TypeScript · cekrem.github.io"
source_id: 363266262
excerpt: "TypeScriptだけで副作用を型で扱い、可読性とテスト性を高める"
image: "https://cekrem.github.io/images/banner.jpg"
---

# Effect Without Effect-TS: Algebraic Thinking in Plain TypeScript - Effect-TSなしで実装する：プレーンなTypeScriptでの代数的思考

魅力的なタイトル: Effect-TSに頼らない「型で誠実に」―TypeScriptだけで副作用とエラーを見える化する実践法

## 要約
Effect-TSの考え方（型付きエラー、明示的依存、合成）はライブラリに頼らずTypeScriptの標準機能だけでかなり再現できる。日常的なサービス実装の可読性・テスト性が劇的に上がる。

## この記事を読むべき理由
日本の開発現場でも、try/catchでエラーを握りつぶしたり、モジュールレベルの依存に悩むケースが多い。ライブラリ導入前に「型で証明する」基本パターンを押さえておくと導入判断や設計がブレません。

## 詳細解説
ポイントは3つ。

1) エラーを投げず値として返す（typed errors）
- Result型を使い、失敗を型で表現することで呼び出し側に「何が起きうるか」を明示する。

```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

type SignupError =
  | { _tag: "InvalidEmail" }
  | { _tag: "EmailTaken"; email: string }
  | { _tag: "DbError"; cause: unknown }
  | { _tag: "EmailServiceDown" };
```

2) 依存をシグネチャに置く（明示的DI）
- DBやメール送信などの副作用依存を関数引数に置くと、型が必要な能力を表現し、テストや差し替えが容易になる。

```typescript
type SignupDeps = {
  findUserByEmail: (email: string) => Promise<Result<User | null, DbError>>;
  createUser: (input: CreateUserInput) => Promise<Result<User, DbError>>;
  sendWelcomeEmail: (email: string) => Promise<Result<void, EmailError>>;
  trackEvent: (name: string, props: Record<string,string>) => Promise<void>;
};

async function signupUser(
  deps: SignupDeps,
  email: string,
  password: string
): Promise<Result<User, SignupError>> { /* ... */ }
```

3) 合成パターンと限界
- 逐次処理は「成功なら次へ」を繰り返す形になりがち。andThen（flatMap）ヘルパーでボイラープレートを削減できるが、ステップが増えると可読性が辛くなる。並列・キャンセル・構造化同時実行などはEffect系ライブラリが得意領域。

```typescript
async function andThen<T,U,E1,E2>(
  result: Promise<Result<T,E1>>,
  f: (v: T) => Promise<Result<U,E2>>
): Promise<Result<U, E1|E2>> { /* ... */ }
```

日本のプロダクトでは、レガシーDBや外部API依存が多く、まずは「型付きResult」と「依存を引数に出す」だけでバグ低減・テスト容易化の効果が大きいです。

## 実践ポイント
- 小さく始める：Result<T,E>型を導入し、まずは1〜2関数を変えてみる。
- 依存注入は単純に引数オブジェクトにするだけで十分。テストはフェイク関数で済む。
- andThen等でボイラープレートを減らすが、複雑な並列制御はEffect系ライブラリを検討する。
- ライブラリ導入は「なぜ必要か」を理解した上で：Effect-TSは便利だが概念は先に手で理解しておくと選定が早い。

この記事の考え方を取り入れると、型が「設計ドキュメント」として振る舞い、チーム内での認識合わせや自動化テストが格段に楽になります。
