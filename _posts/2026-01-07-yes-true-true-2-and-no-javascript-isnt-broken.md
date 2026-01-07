---
  layout: post
  title: "Yes, true + true === 2. And No, JavaScript Isn’t Broken - はい、true + true === 2。いいえ、JavaScriptは壊れていません"
  date: 2026-01-07T12:50:39.659Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://dev.to/sylwia-lask/yes-true-true-2-and-no-javascript-isnt-broken-37p7"
  source_title: "Yes, true + true === 2. And No, JavaScript Isn’t Broken - DEV Community"
  source_id: 3146913
  excerpt: "true + true === 2は仕様です—暗黙の型変換を理解してバグを防ぐ方法を学べる"
  image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fpod1y92llxdnck3pxoav.png"
---

# Yes, true + true === 2. And No, JavaScript Isn’t Broken - はい、true + true === 2。いいえ、JavaScriptは壊れていません
JSの「謎」を知れば、もはや笑い話にならない — 実務で役立つ型変換の正しい見方

## 要約
JavaScriptでtrue + trueが2になるのはバグではなく、演算子の動作と型変換（ToNumber）の仕様によるもの。歴史的な設計方針を理解すれば奇妙さは合理的に見える。

## この記事を読むべき理由
日本のフロント/バックエンド開発現場でもJSは依然主流。意図せぬ型変換はバグの温床になるため、短時間で本質を押さえて日常のコーディングやレビューでミスを減らしたいエンジニアに必読。

## 詳細解説
- 演算子 + は2モード動作：いずれかが文字列なら文字列連結、そうでなければ数値加算を行う。  
- ブール値は内部で数値に変換される（ToNumber）：true → $1$、false → $0$。したがって
```javascript
true + true // 1 + 1 => 2
```
は仕様どおりの結果。これはJS固有の奇行ではなく、多くの言語で見られる慣例（PythonやC系でも同様の扱いがある）。

- 他の例：
```javascript
true * 10  // 10
false * 10 // 0
true - 1   // 0
```

- 背景：JSは90年代にブラウザ向けに短期間で設計され、エラーを厳格に出すより「動く」ことを優先する哲学が根底にある。これが暗黙的な型変換やNaNの伝播などの挙動につながる。

- NaNや==の挙動なども同様に「設計上のトレードオフ」で説明できる（IEEE浮動小数点標準に由来する部分もあり、NaNは演算の失敗を静かに伝播する）。

## 実践ポイント
- 暗黙の型変換を避ける：
  - 明示的に数値に変換する（Number(x) や 単項 +x）を使う。
  - 文字列連結と数値加算を混在させない。
```javascript
+value        // 明示的に数値にする
String(value) // 明示的に文字列にする
```
- 比較は厳格比較を基本に：== を避けて === を使う。
- NaN判定は Number.isNaN を使う（グローバルの isNaN は曖昧）。
- TypeScriptを導入して型境界を明確にする（strictモード推奨）。ただし as や any の多用は禁物。
- ESLintルールで防ぐ：eqeqeq, no-implicit-coercion 等を有効化。
- 入力処理では input.valueAsNumber や明示的パースを使い、未検証の文字列をそのまま計算に回さない。
- 小さなテストで挙動を確認：ユニットテストに型変換の境界条件を含める。

短いまとめ：true + true === 2 はバグではなく仕様。JSの「寛容さ」を理解し、明示的な変換とツールで守れば、類似のトラブルは回避できる。
