---
layout: post
title: "Flutter ECS: Performance Optimization & Profiling - Flutter ECS: パフォーマンス最適化とプロファイリング"
date: 2026-01-21T04:53:55.444Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@dr.e.rashidi/flutter-ecs-performance-optimization-profiling-e75e89099203"
source_title: "Flutter ECS: Performance Optimization &amp; Profiling"
source_id: 421509549
excerpt: "FlutterでECSを導入し単一責務と更新制御で描画遅延を確実に削減"
---

# Flutter ECS: Performance Optimization & Profiling - Flutter ECS: パフォーマンス最適化とプロファイリング
Flutterで「速い」を設計する：システムを小さく、責務を絞ればパフォーマンスは勝手に良くなる

## 要約
Flutter向けのECS（Event‑Component‑System）を使うと、システムを「単一責務」に保ち、コンポーネントの更新を明示的に制御するだけで、再描画や不要な処理を大幅に減らせる。

## この記事を読むべき理由
日本のモバイルアプリやEC／業務アプリは、端末のスペック差や多機能化でパフォーマンス管理が重要です。ECS設計を学べば、Flutterアプリの遅延原因が構造的に見え、確実な改善アクションが取れます。

## 詳細解説
ポイントは「1システム＝1振る舞い」。以下の設計要素を厳密に分けることで、無駄な実行や再レンダリングを防げます。

- Single‑Responsibility Systems  
  各Systemは一文で説明できる責務だけ持つ。複数の仕事が混ざると、どこが頻繁に走るか分からなくなる。

- reactsTo / interactsWith / reactsIf (or executesIf)  
  - reactsTo：どのコンポーネントの変化で起動するか（トリガ）  
  - interactsWith：そのシステムが実際に「変更する」コンポーネントだけを列挙（読むだけのものは含めない）  
  - reactsIf / executesIf：実行前の前提条件（認可フラグやオン/オフ）をここで判断する  
  これらを正しく宣言すると、実行頻度を仕組みとして抑えられる。

- コンポーネント更新の細かな制御 (force / notify)  
  - force: true — 値が同じでも変更として扱い、リスナーや他システムを起動する（例：同じエラーを再表示したい時）  
  - notify: false — 値を更新するが通知は行わない（バッチ更新や内部整備用）  
  中間更新をnotify:falseで行い、最後に1回だけ通知するパターンが有効。

- UI側は必要なものだけwatchする  
  大きなWidgetが複数コンポーネントを監視すると、どれかが変わるたびに全体が再構築される。小さなECS対応ウィジェットに分割して、各Widgetが本当に使うコンポーネントだけwatchする。

- 高コスト計算はWidgetでやらない、システムでやる  
  派生値や重い要約はSystemで計算して専用コンポーネントに保存。Widgetはその結果だけを読めば良い。

短いコード例（要点のみ）:

```dart
// dart
class ValidateEmailSystem extends ReactiveSystem {
  @override Set<Type> get reactsTo => {EmailComponent};
  @override Set<Type> get interactsWith => {EmailValidationComponent};

  @override bool get reactsIf {
    final cfg = getEntity<FormValidationConfigComponent>();
    return cfg.value.validateEmail; // read-only precondition
  }

  @override void react() {
    final email = getEntity<EmailComponent>();
    final validation = getEntity<EmailValidationComponent>();
    validation.update(validateEmail(email.value));
  }
}
```

コンポーネント更新例:

```dart
// dart
// 同じ値でも再通知させたい（force）
errorComponent.update(currentError, force: true);

// 中間処理は黙って更新し、最後に通知
cartComponent.update(itemsPartial, notify: false);
// ...他の内部更新...
cartComponent.update(itemsFinal); // 通知される
```

UIのアンチパターンと改善例:

```dart
// dart - NG: ページ全体が無駄に再構築される
final notifications = ecs.watch<NotificationListComponent>();
final analytics = ecs.watch<AnalyticsSummaryComponent>();
// ...UIはuserしか使っていない...

// dart - OK: 小さなウィジェットに責務分離
final user = ecs.watch<UserComponent>();
NotificationIcon(); // ここだけが通知を受け取る
```

日本の現場で効く点：
- 中小スマホや古めの端末が多い環境では再描画の削減がUXに直結する。  
- ECや認証など「レイテンシと状態が重要」な機能は、ECSの分離でテスト／プロファイルしやすくなる。  
- チームでも「どのSystemが何を変えるか」が明確だとバグ追跡やコードレビューが速くなる。

## 実践ポイント
1. まず1機能を選ぶ（例：ログイン or カートの追加）  
2. その機能のSystemを一覧化して、各Systemを「一文」で説明する。分けられるなら分割する。  
3. interactsWithには「本当に変更するコンポーネントだけ」を列挙する。読み取りだけは除外。  
4. reactIf / executesIf に前提条件を移し、条件判定で不要実行を防ぐ。  
5. コンポーネント更新で force / notify を使い分け、バッチ更新を導入する。  
6. Widgetを分割して、各Widgetがwatchするコンポーネントを最小化する。  
7. 計測は必須：Flutter DevToolsのTimeline・RebuildCountsでbefore/afterを比較する。  

チャレンジ：1つのユーザー操作（例：ログイン）を取り、Before/Afterのプロファイルとリビルド数を比較して効果を確認・共有すること。成果が計測できればチーム導入が進みやすい。
