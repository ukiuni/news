---
layout: post
title: "SOLID in FP: Single Responsibility, or How Pure Functions Solved It Already - FPにおけるSOLID：単一責任（SRP）は純粋関数ですでに解決されている"
date: 2026-02-17T13:32:47.389Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cekrem.github.io/posts/solid-in-fp-single-responsibility/"
source_title: "SOLID in FP: Single Responsibility, or How Pure Functions Solved It Already · cekrem.github.io"
source_id: 440748844
excerpt: "Elmの純粋関数とTEAがSRPを言語で実現し保守性を劇的に高める理由"
image: "https://cekrem.github.io/images/banner.jpg"
---

# SOLID in FP: Single Responsibility, or How Pure Functions Solved It Already - FPにおけるSOLID：単一責任（SRP）は純粋関数ですでに解決されている

言語が勝手にSRPを守ってくれる話 — Elmが教える「責務の分離」

## 要約
Elm の純粋関数設計とアーキテクチャ（TEA）が、開発者の「分離しなければならない」という意識に頼らずに自然とSingle Responsibility Principle（SRP）を実現する仕組みを示す話です。

## この記事を読むべき理由
日本の現場ではReact＋TypeScriptで巨大コンポーネントや副作用の混在に悩むことが多く、ElmやFP的な設計を理解することで保守性・テスト性が格段に向上します。

## 詳細解説
- SRP（単一責任原則）は「モジュールが変わる理由は一つだけ」で表現されます。命令型／副作用混在のコードでは「データ取得・状態管理・副作用・描画」が一箇所にまとまりやすい。
- Elm の設計はこれを言語仕様で強制します：view は純粋関数（Model → HTML）のみ、副作用は Cmd として記述して update が返す。結果として「何が行われるか」は説明されるが、副作用そのものは関数内で実行されない。
- 典型的な違いを示す短い例：

```typescript
// typescript
async function processOrder(order: Order) {
  const validated = validateOrder(order);
  await saveToDatabase(validated);
  await sendConfirmationEmail(validated);
  logger.info(`Order ${order.id} processed`);
}
```

```elm
-- elm
validateOrder : UnvalidatedOrder -> Result (List ValidationError) ValidOrder
processOrder : ValidOrder -> List (Cmd Msg)
processOrder order = [ saveOrder order, sendConfirmation order ]
```

- Elm ではロード状態を RemoteData のような列挙型で扱い、view はその状態に応じた純粋なレンダリングのみを行う。update は Msg を受け取り Model と Cmd を返すため、関心ごとの分離が型で見える化される。
- 大きな update を扱う際は「拡張可能レコード（extensible records）」で「関数が触ってよいフィールド」を型で制限し、コンパイラに意図を明示させる。これがSRPのドキュメントにもなる。

## 実践ポイント
- RemoteData（NotAsked/Loading/Failure/Success）で非同期状態をモデル化し、view を純粋に保つ。
- 副作用は「命令の記述（Cmd）」として切り出す設計を検討する（Elm 以外でもコマンドパターンやEffect Descriptorsを模倣）。
- TypeScript でも union 型・Result 型・fp-ts 等を使い、純粋な関数を増やして副作用を集約する。
- 大きな関数は型シグネチャでアクセス可能なフィールドを限定する（Elm の拡張レコード相当の考え方を取り入れる）。
- 小さなプロジェクトで Elm を試し、言語が「制約として与える自由」を体験してからチーム導入を検討する。

短く言うと、制約が多いほど「ミスできない」ため結果的にSRPが保たれ、保守性と安全性が上がります。日本の多人数開発でも有効な考え方です。
