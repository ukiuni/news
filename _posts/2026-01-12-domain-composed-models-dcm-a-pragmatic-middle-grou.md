---
layout: post
title: "Domain-Composed Models (DCM): a pragmatic middle ground between Active Record and Clean DDD - ドメイン合成モデル（DCM）：Active RecordとクリーンDDDの実用的な中間"
date: 2026-01-12T11:55:08.265Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@hamza-senhajirhazi/domain-composed-models-dcm-a-pragmatic-middle-ground-between-active-record-and-clean-ddd-e44172a58246"
source_title: "Domain-Composed Models (DCM): a pragmatic middle ground between Active Record and Clean DDD"
source_id: 428744991
excerpt: "Active Recordの気軽さを残しつつ、DDDの堅牢性を実務向けに折衷するDCM入門"
---

# Domain-Composed Models (DCM): a pragmatic middle ground between Active Record and Clean DDD - ドメイン合成モデル（DCM）：Active RecordとクリーンDDDの実用的な中間
RailsやDDDで悩む開発者必見 — 実務で効く「ほどほどの設計」を提案するDCM入門

## 要約
元記事へ直接アクセスできなかったため、タイトルと一般的な設計知見をもとに「Domain‑Composed Models（DCM）」という考え方を分かりやすく再構成しました。DCMは、Active Recordの手軽さとクリーンなDDDの設計性を折衷し、現場で実用的に使える中庸なアプローチです。

## この記事を読むべき理由
日本のスタートアップや社内システム開発では、短期的な速度と長期的な保守性の両立が課題です。RailsやORM中心の開発は素早い実装が可能ですが、モデルが肥大化すると保守コストが跳ね上がります。一方で厳格なDDDは学習コストと導入コストが高く、小さなチームでは過剰設計になりがち。DCMはその「現場の落としどころ」を示します。

## 詳細解説
- Active Record（AR）の特徴
  - 長所：モデルにデータ永続化とビジネスロジックをまとめられ、素早く実装できる（Railsの典型）。
  - 短所：モデルが肥大化（God object）、単体テストが難しく、ドメインの純粋性が失われる。

- Clean DDDの特徴
  - 長所：エンティティ／値オブジェクト／ユースケース／リポジトリなど責務が明確で設計が堅牢。
  - 短所：層が多くなり、初期導入・学習コストが高い。小〜中規模プロジェクトでは過剰。

- DCM（Domain‑Composed Models）とは
  - アイデア：ドメインの「振る舞い（ビジネスルール）」はできるだけドメイン側の小さなオブジェクトに閉じ込めつつ、永続化やフレームワーク固有の操作は適切なアダプタ／コンポーネントに委ねる。
  - 実装上の工夫：Active Recordの便利さ（バリデーション、軽い検索メソッドなど）を残しつつ、複雑なビジネスロジックやトランザクションは「ドメインサービス」「ファクトリ」「リポジトリ的アダプタ」に切り出す。
  - 目的：過度な分離で生産性を落とさないまま、テストしやすく変更しやすいコードベースを維持する。

- 典型的なパターン
  - エンティティは振る舞いを持たせる（例：振る舞いメソッドは副作用を最小に）。
  - 永続化は薄いRepository/Mapperで扱い、ORMの細部に依存しないAPIを提供する。
  - ファットモデルが現れたら、まずは責務ごとにメソッドを外出しして小さなドメインオブジェクトへ委譲する。
  - トランザクションや外部サービス呼び出しはユースケース層（アプリケーションサービス）で管理する。

- 簡単な例（Ruby風の擬似コード）
```ruby
# ruby
class Order
  attr_reader :items, :status

  def initialize(items:)
    @items = items
    @status = :pending
  end

  def place!(payment_processor:)
    validate_items!
    payment_processor.charge(total_amount)
    @status = :paid
  end

  def total_amount
    items.sum(&:price)
  end
end

# Persistence adapter
class OrderRepository
  def save(order)
    # ActiveRecord を直接使うのではなく、マッピングを担当
    OrderRecord.create!(...) 
  end
end
```

- TypeScript風にオブジェクトを分ける例
```typescript
// typescript
class Order {
  constructor(private items: Item[]) {}
  totalAmount() { return this.items.reduce((s,i)=>s+i.price,0); }
}
class OrderService {
  constructor(private repo: OrderRepo, private gateway: PaymentGateway) {}
  async place(order: Order) {
    await this.gateway.charge(order.totalAmount());
    await this.repo.save(order);
  }
}
```

## 日本市場との関連
- 日本の多くの中小企業やスクラムチームでは、短納期で機能追加が求められます。完全なDDDは導入障壁が高いため、DCMのような漸進的な分離は現場受けしやすいです。
- 既存のRailsアプリやLaravelアプリを段階的に改善する際、全面リプレイスではなくDCM的方針（小さなドメインオブジェクトの抽出＋薄いリポジトリ）によりリスクを抑えつつ設計改善できます。

## 実践ポイント
- まずは「なぜモデルが肥大化したか」を特定する。データ操作とビジネスルールを分離する小さな勝ちパターンを作る。
- 重要なドメインルールは値オブジェクトかドメインオブジェクトへ移す（テスト価値が高い箇所から）。
- 永続化は薄いアダプタ／リポジトリでラップして、フレームワーク依存を局所化する。
- 全面導入は不要。機能ごと、ドメイン境界ごとに段階的に適用する。
- CIでユニットテストと統合テストを揃え、ビジネスロジックがドメイン層に正しくあることを保証する。

DCMは「現実的で段階的に改善できる設計戦略」です。まずは一箇所だけでもドメインオブジェクトを抽出して試してみてください。
