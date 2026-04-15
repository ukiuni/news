---
layout: post
title: "How to catch N+1 queries in EF Core before they hit production - EF CoreのN+1クエリを本番投入前に検出する方法"
date: 2026-04-15T14:38:44.237Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://programming.dev/post/48748878"
source_title: "I built a small library to assert EF Core SQL query counts in integration tests (catch N+1 in 3 lines) - programming.dev"
source_id: 362200615
excerpt: "CIで自動検出してEF CoreのN+1を防ぎ、DB負荷とコストを劇的に削減する実践ガイド"
image: "https://programming.dev/pictrs/image/89113675-462b-4531-8621-0b4126966d21.webp"
---

# How to catch N+1 queries in EF Core before they hit production - EF CoreのN+1クエリを本番投入前に検出する方法
本番でDB負荷に泣かない！CIで自動検出するEF Core向けN+1対策ガイド

## 要約
EF Coreで起きるN+1問題は本番の遅延・コスト増の主要因。開発段階でログ／インターセプター＋テストでクエリ数を自動検出し、Includeや投影で解消する方法を紹介する。

## この記事を読むべき理由
N+1は気付きにくく、負荷・コスト・ユーザ体験を一気に悪化させる。日本のSaaSやECのようにスケールとコスト管理が重要なプロダクトでは、CIでの自動検出が特に効果的。

## 詳細解説
- N+1とは：親レコードN件を取得した後、各親ごとに1件ずつ追加クエリが発行される問題（合計1+Nクエリ）。原因は主に遅延ロード（lazy loading）やループ内でのナビゲーション参照。
- EF Coreでの発生パターン：foreachで子コレクションやナビゲーションを参照すると簡単に発生。例：usersを取得してループ内で user.Posts を参照するとpostsごとにSQLが飛ぶ。
- 検出方法：
  - 開発環境のSQLログ（ILogger）を確認。
  - 自動化：DbCommandInterceptor を使ってテスト実行中に発行されたSQLの数を数える。CIで閾値を超えたら失敗させると確実。
  - プロファイラ（MiniProfiler 等）でリクエスト単位のクエリ数を可視化。
- 解決法：
  - Include / ThenInclude で一括取得（ただし不要な読み込みに注意）。
  - プロジェクション（Select into DTO）で必要な列だけ取得しつつN+1回避。
  - 明示的なバッチ読み込み（Where IN によるまとめ取得）やEager loadingを使う。
  - 遅延ロードを無効にして明示的に設計する。
- CI運用：特定のエンドポイント／ユースケースについて、インテグレーションテストでクエリ数の上限を決めて自動検出する。

シンプルなDbCommandInterceptor例（テストでのクエリカウント用）：

```csharp
// csharp
public class QueryCountingInterceptor : DbCommandInterceptor
{
    public int QueryCount { get; private set; }

    public override InterceptionResult<DbDataReader> ReaderExecuting(
        DbCommand command, CommandEventData eventData, InterceptionResult<DbDataReader> result)
    {
        Interlocked.Increment(ref QueryCount);
        return base.ReaderExecuting(command, eventData, result);
    }
}
```

このインターセプターをテストのDbContextに登録して、テスト後に QueryCount を検証することでN+1をCIで検出できる。

回避のコード例：Include と投影の比較

```csharp
// csharp
// N+1を招きやすいパターン（NG）
var users = await db.Users.ToListAsync();
foreach(var u in users) Console.WriteLine(u.Profile.Name); // Profileが遅延ロードだとN+1

// Eager load（OK）
var usersWithProfiles = await db.Users.Include(u => u.Profile).ToListAsync();

// 投影（必要なデータだけ取得）
var dto = await db.Users
    .Select(u => new { u.Id, ProfileName = u.Profile.Name })
    .ToListAsync();
```

## 実践ポイント
- 開発環境でSQLログを標準有効にする（ILogger）。
- CIにQueryCountingInterceptorベースのテストを組み込み、クエリ数閾値を設定する。
- 各APIで本当に必要なデータだけを投影（Select）する習慣を付ける。
- Includeで一括取得する際はSELECTの重さを意識し、必要に応じてページングや投影を併用する。
- MiniProfiler等でリクエストごとのクエリ数を可視化し、KPIとして監視する。

短い実践投資（インターセプター＋1本のCIテスト）で、本番のパフォーマンス事故を大幅に減らせます。
