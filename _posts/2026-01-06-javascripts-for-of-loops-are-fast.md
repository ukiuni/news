---
  layout: post
  title: "JavaScript's For-Of Loops Are Fast - JavaScriptのfor-ofループは実は高速"
  date: 2026-01-06T08:21:57.410Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://waspdev.com/articles/2026-01-01/javascript-for-of-loops-are-actually-fast"
  source_title: "JavaScript&#39;s for-of loops are actually fast | WaspDev Blog"
  source_id: 46477306
  excerpt: "V8の最適化でfor-ofが古典ループと遜色ない速度に、実測と最適化指針を解説"
  image: "https://waspdev.com/static/images/2026-01-01/500000-1500-repeats.webp"
---

# JavaScript's For-Of Loops Are Fast - JavaScriptのfor-ofループは実は高速
魅力的タイトル: for-ofで悩んでる人へ──可読性と速度、どちらも諦める必要はない話

## 要約
V8の最適化により、for-ofは従来のインデックスループ（特に「i++と長さをキャッシュ」する書き方）と遜色ない速度を出すことが多い。ただし大規模データやウォームアップ状況では差が出るため、実環境でのベンチが必須。

## この記事を読むべき理由
日本のフロントエンド／Node.jsエンジニアは、可読性を犠牲にせずにパフォーマンスを出せるかどうかを日常的に判断する必要がある。この記事は最新のベンチ結果と最適化の実務的示唆を端的に示す。

## 詳細解説
元記事はChrome（V8）上で複数種類の配列（整数、浮動小数点、文字列、オブジェクト、混在）と3つの要素数（5k、50k、500k）を使い、以下のループを比較した。

- 古典的for（i++）
- 古典的for（長さをキャッシュ）
- 逆順for（i--）
- for-of（イテレーションプロトコル）
- for-in（配列に非推奨）
- arr.forEach

for-ofの内部はイテレーションプロトコル（iterator.next()が{value, done}を返す）に基づくため一見オーバーヘッドがありそうだが、現代のV8はこのパターンをかなり最適化する。ベンチ結果の要点：

- 小〜中サイズ（5k〜50k）：長さキャッシュ版forとfor-ofが最速付近。forEachはやや遅め、for-inは最悪。
- 大規模（500k）：初回実行ではfor-ofが遅く見えることがあったが、JITのウォームアップ（繰り返し実行）でfor-ofは長さキャッシュ版forとほぼ同等に追いつく。forEachはウォームアップの恩恵が少ない傾向。
- 逆順forが期待通り高速化するとは限らない（CPUキャッシュやJITの挙動による）。
- 結論として、エンジン最適化が進んでおり、for-ofは実用上十分高速。ただし極端に大きい配列や特殊なデータ形状では振る舞いが不安定なこともあり、測定が重要。

参考となるコード例（要点のみ）:

```javascript
// javascript
// 安全で高速な古典ループ（長さをキャッシュ）
const len = arr.length;
for (let i = 0; i < len; i++) {
  doSomething(arr[i]);
}

// 読みやすい for-of
for (const x of arr) {
  doSomething(x);
}
```

## 実践ポイント
- まずは計測する：プロダクションに入れる前に、実際のデータ形状とサイズでベンチを取る。
- 可読性優先でまずはfor-of：パフォーマンスホットスポットでなければfor-ofを使って可読性を保つ。
- ホットパスでは長さキャッシュ版forを検討：再現性の高い高速性を欲するならこれが最も安定。
- for-inは配列走査には使わない：プロパティ列挙のため非推奨、遅い。
- ウォームアップを意識する：長時間動作するコード（サーバープロセス等）はJITのウォームアップ後の挙動を見る。
- データ形状を揃える：同じ型の要素が続く「モノタイプ」配列はJITに好まれる。混在配列は最適化の足枷になる。
- モバイル／旧ブラウザでの違いに注意：日本のユーザー環境は多様。ターゲット実行環境で必ず確認を。

以上を踏まえれば、for-ofは「可読性を維持しつつ十分な性能を得られる選択肢」として現実的である。性能が気になる箇所だけプロファイルして最適化するのが実務的なアプローチ。
