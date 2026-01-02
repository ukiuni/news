---
  layout: post
  title: "Designing type-safe sync/async mode support in TypeScript - TypeScriptで同期／非同期モードを型安全に設計する"
  date: 2026-01-02T14:19:33.250Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://hackers.pub/@hongminhee/2026/typescript-sync-async-type-safety"
  source_title: "Designing type-safe sync/async mode support in TypeScript"
  source_id: 1652910196
  excerpt: "TypeScriptで1つがasyncなら全体をasync化する型設計と実践解説"
  image: "https://hackers.pub/@hongminhee/2026/typescript-sync-async-type-safety/ogimage?l=en"
---

# Designing type-safe sync/async mode support in TypeScript - TypeScriptで同期／非同期モードを型安全に設計する

魅力的なタイトル: 「同期で速く、非同期で安全に──TypeScriptで“どれか1つがasyncなら全部async”を型で保証する方法」

## 要約
オープンソースのCLIパーサーライブラリで「1つでも非同期なパーサーがあれば合成結果は非同期になる」ルールをTypeScriptの型レベルで安全に表現する設計と、その実装上のトレードオフを解説します。著者は複数案を検証し、互換性を保ちながら明示的なモードパラメータ（既定値: "sync"）を採用しました。

## この記事を読むべき理由
- ライブラリ設計で「同期パスは速く」「非同期も扱える」を両立したい人向け。
- TypeScriptの条件型、型推論の限界、実装時に必要なカストやランタイム補助に関心がある人に有益。
- CLIやパーサー、型安全APIを作る日本のOSS/プロダクト開発者に直接役立つ実践的知見が得られます。

## 詳細解説
問題設定は単純明快：「complete() は T または Promise<T> を返し、suggest() は Iterable<T> または AsyncIterable<T> を返す。複数パーサーを組み合わせる時、任意の要素が async なら合成結果は async であるべき。既存の同期コードはそのまま動くべき。」この"any async → all async"ルールを型で表現するために著者は5案を比較検討しました。

- Option A: モード型パラメータ + 条件型（基本案）。  
  type Mode = "sync" | "async"; を導入し、Mode に応じて返り値型を変える。
- Option B: モード型パラメータを先頭に置き既定値 "sync" を与える（採用）。  
  既存コード互換を保ちつつ、型とランタイムで $mode を確認できる。
- Option C: 完全に別インターフェース（Parser / AsyncParser）に分離。シンプルだが重複が増える。
- Option D: 最小妥協。suggest() だけを非同期に許す。parse() の非同期化が必要なら不足。
- Option E: fp-ts流の HKT 模倣。最も柔軟だが学習コストが高い。

試作（プロトタイプ）で Option B が実務的に使えることを確認。主要な理由は「デフォルトを sync にして既存互換を保つ」「$mode によりランタイムでモード判定が可能」「IDE上の型情報が扱いやすい」など。

代表的な型実装（抜粋）例:

```typescript
// typescript
type Mode = "sync" | "async";
type ModeValue<M extends Mode, T> = M extends "async" ? Promise<T> : T;

interface Parser<M extends Mode = "sync", TValue = unknown, TState = unknown> {
  readonly $mode: M;
  parse(ctx: ParserContext<TState>): ModeValue<M, ParserResult<TState>>;
  // suggest なども同様にモード依存
}
```

合成時にどのフィールドが async を含むかを判定する型レベルロジック例:

```typescript
// typescript
type CombineModes<T extends readonly Mode[]> = "async" extends T[number] ? "async" : "sync";

// レコードの各パーサーからモードを抽出
type ParserMode<T> = T extends Parser<infer M, any, any> ? M : never;

type CombineObjectModes<T extends Record<string, Parser<Mode, any, any>>> =
  CombineModes<{ [K in keyof T]: ParserMode<T[K]> }[keyof T][]>;
```

ランタイム側は各パーサーに $mode を付け、合成時に走査して combinedMode を決定します。object() の実装は合成時に combinedMode を計算し、sync/async で別実装を返す（内部でロジックが二重化される）パターンです。

```typescript
// typescript (抜粋)
function object<T extends Record<string, Parser<Mode, unknown, unknown>>>(
  parsers: T
): Parser<CombineObjectModes<T>, ObjectValue<T>, ObjectState<T>> {
  const keys = Reflect.ownKeys(parsers);
  const combinedMode: Mode = keys.some(k => parsers[k as keyof T].$mode === "async") ? "async" : "sync";
  if (combinedMode === "async") {
    return { $mode: "async" as any, /* async parse implementation */ };
  } else {
    return { $mode: "sync" as any, /* sync parse implementation */ };
  }
}
```

API UX の改善点として、run()/parse()/suggest() に対して自動判定版と、明示的に同期／非同期を要求する runSync()/runAsync() などの関数を提供する方針が採られました。これにより型レベルでの誤用を防げます。

非同期を含む ValueParser の作り方では、ValueParser<"async", T> の場合すべてのメソッドが async シグネチャになるため、実装上「本来同期でも Promise.resolve() を返す」などの小さな冗長が発生します。著者は per-method granularity を避け、設計の複雑性を抑える判断をしています。

コストと学び
- すべてのコンビネータにモード伝播ロジックを追加する必要があり、実装行数は増える（例: object() が 100行 → 250行）。
- TypeScript の高度な条件型は強力だが実装はカスタムキャストや明示的注釈が必要な場合がある。
- 事前にプロトタイプで挙動を検証することが肝要。理論だけでは見えない落とし穴がある。

## 実践ポイント
- ライブラリは既存ユーザを壊さない既定値（sync）を用意するのが現実的。
- API は自動判定(run)に加え、明示的な runSync/runAsync を用意して型で誤用を防ぐ。
- 型設計時は「型レベルの決定ロジック」と「ランタイムのモード判定($mode)」を両輪にする。
- 実装複雑性を受け入れられない場合は Option C/D を検討。学習コストを抑えつつ機能を絞る選択も現実的。
- TypeScript の条件型は強力だが、IDE 補完や型推論の現実挙動を実プロトタイプで確認すること。

## 引用元
- タイトル: Designing type-safe sync/async mode support in TypeScript
- URL: https://hackers.pub/@hongminhee/2026/typescript-sync-async-type-safety

もし試してみたい場合は、Optique の pre-release（@optique/core@0.9.0-dev...）や該当 PR を参照すると実装の生データが見られます。
