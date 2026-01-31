---
layout: post
title: "The dumbest performance fix ever - 愚かなほどシンプルだったパフォーマンス改善"
date: 2026-01-31T10:39:52.524Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://computergoblin.com/blog/the-story-of-a-5-minute-endpoint/"
source_title: "Nef's Professional Showcase"
source_id: 412865713
excerpt: "数千件の逐次INSERTをAddRangeに置換し、処理が5分→約300msに激変した話"
---

# The dumbest performance fix ever - 愚かなほどシンプルだったパフォーマンス改善
5分かかっていたエンドポイントが、たった2行で300msになった話 — 「やらない」ことで賢く見える方法

## 要約
数千件のユーザーを一件ずつ await でINSERTしていた旧コードを、EF Core の AddRange + SaveChangesAsync を使う単純なリポジトリ実装に置き換えたら、処理が5分超→約300msになった話。

## この記事を読むべき理由
同様の課題（レガシーなフレームワーク、外注で積み上がった無駄な実装、逐次DB操作）が日本のプロダクトでも頻発します。初歩的な非効率を見逃さないことで、顧客体験と運用コストを劇的に改善できます。

## 詳細解説
- 問題の本質：foreach の中で await レスポンスを待ちながら1レコードずつ InsertAsync を呼ぶ実装は「逐次（シリアル）」にDB往復を行うため、データ件数が増えると遅延が線形に増大する。  
- なぜ起きたか：採用していたABPフレームワークの古いバージョンに InsertMany/UpdateMany の便利関数が無く、チームは手作業で一件ずつ登録するワークアラウンドを選んでいた。技術的負債や「とにかく機能を出す」文化が背景にある。  
- 正しい方向性：EF Core は集合挿入/更新をサポートしており、AddRange と SaveChangesAsync を使えば単一のトランザクションでバルク的に処理できる。これにより往復回数が減り、IO待ちが激減する。  
- 結果：簡単な InsertManyAsync を実装しただけで、エンドポイントの応答時間が数分→数百ミリ秒へ激変。

例：今回実装した InsertManyAsync（概念コード）

```csharp
public Task InsertManyAsync(ICollection<T> entities)
{
    context.Set<T>().AddRange(entities);
    return context.SaveChangesAsync();
}
```

## 実践ポイント
- まずコードベースで「foreach (var x in items) await InsertAsync(x)」のような逐次DB呼び出しを検索する。  
- EF Core の AddRange / SaveChangesAsync や、可能なら DB バルクインサート（BulkInsert ライブラリ等）を検討する。  
- フレームワークの古いバージョンが原因なら、段階的に自前の薄いラッパー実装で不足機能を補う。  
- パフォーマンス改善は測定（プロファイラ／ログ／APM）→小さな安全な置換→ロールアウトの順で行う。  
- マネジメント向けには「機能優先の開発が運用コストを生む」点を数値で示して改善提案する。

短い結論：ときに最も効果的な最適化は「非常に愚かな実装をやめる」こと。
