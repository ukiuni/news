---
layout: post
title: "Everything Should Be Typed: Scalar Types Are Not Enough - すべてに型を付けるべきだ：スカラー型だけでは不十分"
date: 2026-04-13T20:42:28.052Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sot.dev/everything-should-be-typed.html"
source_title: "Everything Should Be Typed: Scalar Types Are Not Enough"
source_id: 362664722
excerpt: "IDや金額をドメイン型で厳密化し致命的バグを防ぐ実践法"
image: "https://sot.dev/assets/images/everything-should-be-typed.png"
---

# Everything Should Be Typed: Scalar Types Are Not Enough - すべてに型を付けるべきだ：スカラー型だけでは不十分
クリックせずにはいられないタイトル案：型が「意味」を守る時代へ――ただの string/int からドメイン型への脱却で致命的バグを防ぐ方法

## 要約
スカラー型(string/int/float)だけに頼ると「意味の取り違え」による致命的なバグが発生する。識別子や金額、サニタイズ済み文字列などドメインごとに新しい型（newtype／branded type）を導入すると、コンパイラが意味のミスを検出してくれる。

## この記事を読むべき理由
日本のサービス（決済・マーケットプレイス・地図・セキュリティ系）が扱うID、通貨、単位、入力データは「型の間違い」で大きな事故につながる。小さなチームやレガシー混在のコードベースほど導入効果が大きく、運用コストと信頼性が劇的に上がる。

## 詳細解説
- 問題の本質：コンパイラは「形（shape）」しか見ない。String や i64 は同一扱いで、shopId と customerId を取り違えても検出できない。
- 位置引数の危険：パラメータが多い関数における引数の順序ミスはテストやコンパイルで見つからないことがある。
- struct/object 化は改善するが不十分：名前付きフィールドで位置ミスは防げるが、フィールドに誤った意味の値を代入しても型は通る。
- 解決策：ドメイン意味を型に埋め込む（newtypes / branded types / defined types）。以下の効果が得られる。
  - 意味的に異なる値の混入をコンパイル時に拒否
  - コンストラクタでバリデーションを一箇所に集約（不変条件を保証）
  - 型名がドキュメントとなり可読性向上
  - セキュリティ（未サニタイズ vs サニタイズ済み）を型で強制

簡単な例（抜粋）：

Rust:
```rust
struct ShopId(String);
struct CustomerId(String);

struct OrderPayoutParams {
    shop_id: ShopId,
    customer_id: CustomerId,
    // ...
}
```

Go:
```go
type ShopID string
type CustomerID string

type OrderPayoutParams struct {
    ShopID     ShopID
    CustomerID CustomerID
    // ...
}
```

TypeScript (branded type):
```ts
type ShopId = string & { readonly __brand: "ShopId" };
type CustomerId = string & { readonly __brand: "CustomerId" };

interface OrderPayoutParams {
  shopId: ShopId;
  customerId: CustomerId;
  // ...
}
```

- 実務上の工夫：Rust の Deref/From/Display で利便性を担保、Go は基底型のメソッドを利用、TS はコンパイル時だけブランドを付ける。コンストラクタで検証を行えば、その型が存在するだけで不変条件が成立する。

## 実践ポイント
- 優先度高：ID（ユーザー/注文/店舗）、金額（金額単位の違い）、外部入力（生/サニタイズ済）、単位（m/km/秒/分）を最初に型化する。
- 言語別導入案：
  - Rust：newtype を作り Deref/From/Display と constructor を実装
  - Go：type T underlying で distinct type を定義しメソッドで Validate
  - TypeScript：branded types または nominal typing のヘルパーを採用
- 工程：まずライブラリ層・API境界から導入し、徐々にコアロジックへ拡張する（レガシーとの橋渡しを忘れずに）。
- 自動化：コードジェネレータ・テンプレートで newtype 定義を簡略化し、CI で未ラップのスカラーを検出する静的解析ルールを追加する。

型は「形」ではなく「意味」を守る道具。小さな型の投資が将来の数千万円の事故を防ぐことが多い――まずは ID と金額から新しい型習慣を始めよう。
