---
layout: post
title: "Date is out, Temporal is in - Dateは終わり、Temporalが来た"
date: 2026-01-12T16:08:24.856Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://piccalil.li/blog/date-is-out-and-temporal-is-in/"
source_title: "Date is out, Temporal is in  - Piccalilli"
source_id: 46589658
excerpt: "Dateの曖昧さと副作用を解消し、バグ激減を実現するTemporalの導入法"
image: "https://piccalil.b-cdn.net/api/og-image?slug=date-is-out-and-temporal-is-in/"
---

# Date is out, Temporal is in - Dateは終わり、Temporalが来た
もうDateで悩まない。Temporalでバグを減らし、時刻処理を安全にする方法

## 要約
JavaScriptの組み込みDateはパースやタイムゾーン、可変性で事故を誘発するため非推奨の流れにあり、代わりに設計し直されたTemporal API（不変で時差対応）への移行が推奨されるという話。

## この記事を読むべき理由
日本でもサーバー・フロント双方で時刻処理は頻出（スケジュール、請求、ログ、国際サービス）。Dateに起因する微妙なバグは見つけにくくコストになるため、より堅牢で明示的なTemporalの基本を知っておくと実務で役立つ。

## 詳細解説
- Dateの問題点（抜粋）
  - 文字列パースの挙動が不統一（例："2026-01-02" が UTC として扱われローカル表示で前日になるなど）。
  - monthは0始まりだが year/dayはそうではないなどAPI設計が混乱を招く。
  - Dateは内部的にミリ秒のタイムスタンプ（時刻）を持つ「可変オブジェクト」で、参照渡しによる意図しない副作用を生む（例：関数内で日付を増やすと元の変数も変わる）。
  - タイムゾーンと夏時間（DST）についての表現力が弱く、グローバル対応で多くの外部ライブラリが必要になりがち（パフォーマンス問題にもつながる）。

- Temporalの設計
  - Temporalはコンストラクタではなく「名前空間オブジェクト」（Mathに近い）で、PlainDate/PlainDateTime/ZonedDateTime/Instant/Durationなど用途別の型を提供する。
  - 重要な点は「不変（immutable）」であること。値を操作すると新しいインスタンスが返るため、参照による意図せぬ副作用が減る。
  - タイムゾーンや暦（Gregorianに限らない拡張余地）を明示的に扱える。Temporal.Nowなどで現在時刻を用途に応じて取得できる。
  - 例：日付だけを扱いたいときは PlainDate（タイムゾーン無視）、タイムゾーン込みで瞬間を扱いたければ ZonedDateTime を使う。

- 比較コード（抜粋）
```javascript
// JavaScript (Date) の副作用例
const today = new Date();
const addDay = d => { d.setDate(d.getDate() + 1); return d; };
console.log(`Tomorrow is ${addDay(today).toLocaleDateString()}. Today is ${today.toLocaleDateString()}.`);
// -> 両方とも翌日になってしまう（副作用）
```

```javascript
// JavaScript (Temporal) の例
const { PlainDate } = Temporal;
const today = Temporal.Now.plainDateISO(); // 例: 2026-01-01
const tomorrow = today.add({ days: 1 });
console.log(today.toString(), tomorrow.toString());
// -> today は不変、明示的に新しい値が得られる
```

## 実践ポイント
- まずはランタイムのサポート状況を確認する（ブラウザやNodeのバージョン、もしくは @js-temporal/polyfill を導入）。
- 使い分けルールを決める：
  - 日付のみ（カレンダー日）→ PlainDate / PlainYearMonth
  - 時刻のみ → PlainTime
  - タイムゾーンを考慮した瞬間 → ZonedDateTime / Instant
  - 期間計算 → Duration
- 既存コードでは「Dateを直接渡して関数内で変更する」パターンを見直す。Temporalでは不変性を前提に書くことでバグを減らせる。
- 重いサードパーティ（moment.js等）からの移行を検討すると、バンドルサイズやパフォーマンス改善につながる。
- 日本向けにはJST固定の表示や会計期などのローカルルールを明示的に扱い、国際化が必要な部分だけZonedDateTimeを用いると実装が単純になる。

短く言えば：日付と時刻は「曖昧さ」と「副作用」の温床。Temporalを取り入れれば意図的で安全な時間処理が書けるようになり、バグもコストも減る。まずはpolyfillで試して、小さなモジュールから移行してみることを薦める。
