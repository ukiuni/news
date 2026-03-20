---
layout: post
title: "Is the Strategy Pattern an ultimate solution for low coupling? - ストラテジーパターンは低結合の究極解か？"
date: 2026-03-20T10:33:16.475Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://event-driven.io/en/is_strategy_pattern_an_ultimate_solution_for_low_coupling/"
source_title: "Is the Strategy Pattern an ultimate solution for low coupling? - Event-Driven.io"
source_id: 378734690
excerpt: "ストラテジーパターンは強力だが、検証の位置次第で低結合が崩れる危険と回避策を具体的に解説する。"
image: "https://event-driven.io/static/e1764ada3a11425bce8089e83509e760/2a4de/2023-10-01-cover.png"
---

# Is the Strategy Pattern an ultimate solution for low coupling? - ストラテジーパターンは低結合の究極解か？
「設計の魔法か、それとも隠れた設計臭？ストラテジーパターンで低結合を狙うときに注意すべきこと」

## 要約
ストラテジーパターンは検証や差し替え可能なロジックを切り出して結合を下げられるが、「ただ検証するだけ」の戦略は結合や抽象の漏れを招く可能性がある、という検討。

## この記事を読むべき理由
実務ではルール（バリデーションやビジネス条件）が頻繁に変わるため、戦略的に実装を分離することが多い。日本の業務系システム（金融、EC、基幹）でも同じ課題が発生しやすく、誤った分離は保守性を下げるため、適切な設計判断が重要です。

## 詳細解説
- 元記事はNBAのトレード処理を例に、トレード対象の選定・契約更新・給与上限・選手の拒否権などルールが増える実装を提示。
- 単純化した実装だとバリデーションがAggregate（TeamRoster）の内部で肥大化するため、ICheckTradeのようなインターフェースで検証ロジックを注入（Strategy）する案を示す。
- しかし問題は「検証だけして結果をAggregateが使わない」ケース。Aggregateが外部世界（選手の拒否設定やパラメータ）に依存したままなら、結合は完全に解けていない。
- 代替案として:
  - アプリケーションサービス側で tradeChecker.CanTradeTo(...) を呼んでから aggregate.TradePlayers(...) を呼ぶ（検証を外に出す）。
  - aggregate の読み取り専用プロパティ（例: CurrentContracts）を公開して検証に必要な状態を渡す。
  - proxy（拡張メソッド）を使って検証＋操作を明示的にまとめる（TradeCheckProxy）。
- こうすることで責務が明確になり、テストもしやすくなる。逆に「voidで何もしない戦略」「Aggregateに知られず裏で状態を書き換える戦略」は設計臭（smell）になりうる。

簡単なコード例（アプリサービス側で検証するパターン）:

```csharp
// csharp
var teamRoster = await database.GetById(teamId, ct);
var check = tradeChecker.CanTradeTo(teamId, teamRoster.CurrentContracts, tradeOffer);
if (check != ICheckTrade.Result.Ok) throw new InvalidOperationException(check.ToString());
teamRoster.TradePlayers(tradeOffer);
await database.Store(teamId, teamRoster, ct);
```

## 実践ポイント
1. 戦略（Strategy）は「結果を返してビジネスに使われる」ように設計する：単なる副作用だけに頼らない。  
2. 検証ロジックは可能ならアプリケーション層で実行し、Aggregateはコア状態の更新に集中させる。  
3. Aggregateから読み取り専用プロパティを公開して検証に必要な情報を渡す（mutableな公開は避ける）。  
4. 変更頻度の高いルールは独立した戦略／サービスに切り出し、差し替えと単体テストを容易にする。  
5. 「戦略を注入したらそれでOK」と安易に結論付けず、結果的に結合が残っていないかを確認する。  

短く言えば：ストラテジーは強力だが使い方次第で設計臭に変わる。責務の境界を明確にしてから使おう。
