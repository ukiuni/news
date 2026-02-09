---
layout: post
title: "I built a CRUD Web API using .NET Minimal APIs + EF Core (No Controllers) - .NET Minimal API + EF Coreで作るCRUD Web API（コントローラー不要）"
date: 2026-02-09T04:46:19.179Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://youtu.be/qV-lKUIfQ3g"
source_title: "How To Build CRUD APIs Using .NET Minimal API + EF Core | No Controllers - YouTube"
source_id: 405685034
excerpt: "Minimal APIとEF Coreでコントローラー不要の超高速CRUDを最短で構築する方法"
image: "https://i.ytimg.com/vi/qV-lKUIfQ3g/maxresdefault.jpg"
---

# I built a CRUD Web API using .NET Minimal APIs + EF Core (No Controllers) - .NET Minimal API + EF Coreで作るCRUD Web API（コントローラー不要）
驚くほどシンプル：コントローラーを使わずに最短で動くCRUD APIを作る方法

## 要約
.NETのMinimal APIsとEF Coreを組み合わせることで、コントローラー不要でシンプルかつ速く動くCRUD Web APIを短時間で実装できます。

## この記事を読むべき理由
日本のスタートアップや組み込みチーム、社内PoCを行うエンジニアにとって、開発スピードと運用コストを下げられる手法は魅力的です。Azureやオンプレの既存.NET資産とも親和性が高く、まず試す価値があります。

## 詳細解説
- Minimal APIsの本質  
  .NET 6以降で導入された「Minimal APIs」は、Program.csに直接エンドポイントを定義できる軽量モデル。MapGet/MapPost等でルートを登録し、コントローラー・属性に依存しない設計が可能です。

- EF Coreとの組み合わせ  
  DbContextをDIコンテナに登録して、エンドポイントのパラメータとして受け取るだけでDBアクセスが行えます。非同期メソッド（ToListAsync/FindAsync/SaveChangesAsync）を用いるのが標準的です。

- 典型的なCRUD構成（ポイント）
  - モデル（Entity）
  - DbContext（DbSet<T>）
  - マイグレーション（dotnet ef migrations add / dotnet ef database update）
  - エンドポイント（MapGet/MapPost/MapPut/MapDelete）
  - DTO/バリデーション（必要に応じて）

- 長所・短所
  - 長所: コード量削減、素早いプロトタイピング、学習コスト低め
  - 短所: 大規模アプリでは構造化が必要、慣習的なコントローラー層の分離が無いと保守性低下の恐れ

簡単な実装例（概念を掴むための最小コード）:

```csharp
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AppDbContext>(opt => opt.UseSqlServer(builder.Configuration.GetConnectionString("Default")));
var app = builder.Build();

app.MapGet("/items", async (AppDbContext db) => await db.Items.ToListAsync());
app.MapGet("/items/{id}", async (int id, AppDbContext db) => await db.Items.FindAsync(id) is Item item ? Results.Ok(item) : Results.NotFound());
app.MapPost("/items", async (Item item, AppDbContext db) => { db.Items.Add(item); await db.SaveChangesAsync(); return Results.Created($"/items/{item.Id}", item); });
app.MapPut("/items/{id}", async (int id, Item input, AppDbContext db) => { var item = await db.Items.FindAsync(id); if (item is null) return Results.NotFound(); item.Name = input.Name; await db.SaveChangesAsync(); return Results.NoContent(); });
app.MapDelete("/items/{id}", async (int id, AppDbContext db) => { var item = await db.Items.FindAsync(id); if (item is null) return Results.NotFound(); db.Items.Remove(item); await db.SaveChangesAsync(); return Results.NoContent(); });

app.Run();

class Item { public int Id { get; set; } public string Name { get; set; } }
class AppDbContext : DbContext { public AppDbContext(DbContextOptions<AppDbContext> opts) : base(opts) {} public DbSet<Item> Items => Set<Item>(); }
```

## 実践ポイント
- まずはローカルで「dotnet new web」→ EF Coreパッケージ追加 → DbContext登録→上記のMapXXXを貼って動かす。
- マイグレーションは必須：dotnet ef migrations add Init / dotnet ef database update。
- 開発はVS Code＋C#拡張、Postman/curlでテスト。Azureにデプロイする場合はWeb Appかコンテナ化を検討。
- 本番を見据えるならDTO・バリデーション・ログ・認証（JWT）を早めに導入して構造化する。

以上を踏まえ、まずは1エンドポイントから試して「速さ」を体感してみてください。
