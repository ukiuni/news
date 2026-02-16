---
layout: post
title: "Testing Postgres race conditions with synchronization barriers - Postgresの競合状態を同期バリアでテストする"
date: 2026-02-16T21:44:00.594Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.lirbank.com/harnessing-postgres-race-conditions"
source_title: "Harnessing Postgres race conditions"
source_id: 47039834
excerpt: "同期バリアでPostgresの書き込み競合を確実に再現し、ロック対策の有効性をCIで検証する方法"
image: "https://www.lirbank.com/og/harnessing-postgres-race-conditions.png"
---

# Testing Postgres race conditions with synchronization barriers - Postgresの競合状態を同期バリアでテストする
テストで「消えるお金」を防ぐ：同期バリアでPostgresの書き込み競合を確実に再現する方法

## 要約
同時実行の書き込み競合はテストでは再現しづらいが、同期バリアを使えば「必ず同じタイミングで読む」状況を作り出せる。これによりロックやトランザクションの有無が正しく動くかを決定的に検証できる。

## この記事を読むべき理由
金融系や在庫管理など、データの整合性が命の日本のプロダクトでは、レース条件が本番で致命的になる。 flaky な再試行や運任せのテストに頼らず、CIで確実に検出できる方法を知っておくべきだから。

## 詳細解説
- 問題の本質：2つの同時処理が同じ古い値を読み、両方がそれを基に書き戻すと片方の更新が消える。例：残高 $100$ に $50$ を2回同時適用すべきところが最終 $150$ になる。
- ナイーブ実装（例）:

```typescript
// javascript / typescript
const credit = async (accountId: number, amount: number) => {
  const [row] = await db.execute(sql`SELECT balance FROM accounts WHERE id = ${accountId}`);
  const newBalance = row.balance + amount;
  await db.execute(sql`UPDATE accounts SET balance = ${newBalance} WHERE id = ${accountId}`);
};
```

- 同期バリア（createBarrier）のアイデア：期待するタスク数を渡し、その数が揃うまで待機させ、最後の到着で一斉開放する。これを「読みの直後」や「BEGINの直後」などに差し込むと、特定のインタリーブを決定的に再現できる。

```typescript
// javascript / typescript
function createBarrier(count: number) {
  let arrived = 0;
  const waiters: (() => void)[] = [];
  return async () => {
    arrived++;
    if (arrived === count) {
      waiters.forEach(resolve => resolve());
    } else {
      await new Promise<void>(resolve => waiters.push(resolve));
    }
  };
}
```

- 検証パターン（要点）
  1. 生のSELECT/UPDATEにバリアを挟むと期待通り失敗（deterministicにレースが再現）。
  2. トランザクション（READ COMMITTED）にしても失敗：トランザクションは「ステートメント単位の一貫性」だが書き込みロックを保証しない。
  3. SELECT ... FOR UPDATE を使うと読み時に行ロックがかかるため、バリアを「読みと書きの間」に置くとデッドロックする（片方がロックで止まり、もう片方がバリアで待つ形になる）。
  4. 対処法：バリアを BEGIN の直後（SELECT の前）に置くと、両トランザクションが開始された状態で FOR UPDATE が作用し、シリアライズされ期待通りの結果（$200$）になる。
  5. 良いテストは「ロックありでパス」「ロックなしで失敗」の両方を確認すること。両方でパスするならテストが無意味になっている可能性が高い（vanity test）。

- テスト実行環境：モックではなく実際のPostgresが必要（ロックやトランザクション動作を模倣できない）。Neon Testingなどの一時的なPostgresサービスが便利。

- フックによる注入：本番コードにバリアを置かないよう、トランザクション開始直後に任意のテストフックを受け取る設計にする。例：

```typescript
// javascript / typescript
async function credit(
  accountId: number,
  amount: number,
  hooks?: { onTxBegin?: () => Promise<void> | void },
) {
  await db.transaction(async (tx) => {
    if (hooks?.onTxBegin) await hooks.onTxBegin();
    const [row] = await tx.execute(sql`SELECT balance FROM accounts WHERE id = ${accountId} FOR UPDATE`);
    const newBalance = row.balance + amount;
    await tx.execute(sql`UPDATE accounts SET balance = ${newBalance} WHERE id = ${accountId}`);
  });
}
```

## 実践ポイント
- 実DBでテストする：ローカル/CIでPostgresを起動（コンテナ、Neon Testing等）。
- バリアはテストのみ：本番コードには残さず、テストフック経由で注入する。
- テストは双方向チェック：LOCKありでパス、LOCKなしで失敗することを確認して初めて意味あるテスト。
- デッドロックに注意：バリアの位置を調整し、BEGIN直後に置くのが安全なケースが多い。
- CIで回す：一度書けば、将来のリファクタでロックを失う回帰を早期検出できる。

以上を導入すれば、$100 + 50 + 50 = 200$ になるべき処理が「いつの間にか150になる」悲劇をCIで未然に防げる。
