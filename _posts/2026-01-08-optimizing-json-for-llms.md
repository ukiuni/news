---
layout: post
title: "Optimizing JSON for LLMs - LLM向けJSON最適化"
date: 2026-01-08T16:14:19.876Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/mattlewandowski93/optimizing-json-for-llms-1dgf"
source_title: "Optimizing JSON for LLMs - DEV Community"
source_id: 3156698
excerpt: "短ID・キー短縮・ミニファイでLLM向けJSONを大幅圧縮しコストと遅延を削減"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F33v6vo8it4lqbiw6ne2n.png"
---

# Optimizing JSON for LLMs - LLM向けJSON最適化
LLM APIのトークンとレスポンスタイムを劇的に下げる、実用的なJSON最適化ガイド

## 要約
大量の構造化データをLLMに投げるとトークン消費とレイテンシが膨らむ。キー短縮・不要フィールド削除・IDマッピングなど、手軽に実装できる手法で実効的にサイズを削減できる。

## この記事を読むべき理由
日本の開発チームでも、レトロスペクティブやスタンドアップの自動要約、社内チャットボットなどで同様の課題に直面することが多い。API課金・レスポンス速度・プライバシー観点で即効性のある改善策が欲しいなら必読。

## 詳細解説
以下は使いやすく効果の出る主要テクニック（元記事の実践例を日本向けに整理）。

1. 長いID（UUID等）を短いIDに置換  
   - 同一エンティティに対して一意な短ID（u-1, q-1等）を割り当てて使い回す。モデルは繰り返し出現する短IDで関係性を学べる。  
   - 実装はストリーム処理やバッチの前処理でマップを作るだけ。

```javascript
// JavaScript: UUIDを短IDに変換するイメージ
const map = new Map();
let counter = 1;
function shortId(uuid, prefix) {
  if (!map.has(uuid)) map.set(uuid, `${prefix}-${counter++}`);
  return map.get(uuid);
}
```

2. フォーマット（空白・改行）を除去  
   - JSON.stringify(data) でミニファイ。LLMは整形を必要としないため余分な空白は無駄。

3. キー名を短くする  
   - odQuestionId → qid、answerText → text 等。可読性を損なわない範囲で短縮する。

4. null・空配列・空文字列を削除  
   - 存在しない値を送らない。例えば blocker: null を省くとトークン節約＋誤解の減少になる。

```typescript
// TypeScript: 空値削除の例
function removeEmpty<T extends object>(obj: T): Partial<T> {
  return Object.fromEntries(
    Object.entries(obj).filter(([_, v]) => v !== null && v !== undefined && v !== "" && !(Array.isArray(v) && v.length === 0))
  ) as Partial<T>;
}
```

5. ネストを平坦化  
   - 深いプロパティをトップレベルに上げられる場合は上げる。構造トークンが減る。

6. 繰り返しオブジェクトは配列の行列形式に変換  
   - 各要素が同じ形の大量データは cols/rows 形式にするとキーの繰り返しを抑えられる（可読性とのトレードオフ）。

7. メタデータ（タイムスタンプ、監査用フィールド等）を削る  
   - サマリ生成用途で不要なら送らない。プライバシー保護にも有利。

8. ブールは存在性で表す／フラグ配列を使う  
   - false を大量に送るより、true のものだけを列挙するか flags: ["verified","active"] のようにする。

補足：TOONのような標準仕様もあるが、自前のプリプロセッサで運用する利点は柔軟性と依存排除。重要なのはモデル精度を保ちながらコストを下げること。実運用では最適化前後の精度・レイテンシ・コストを必ず計測する。

## 実践ポイント
- 適用対象を選ぶ：小さなリクエストには不要。大量データを定期的に送るパイプラインに有効。  
- まずは短ID・キー短縮・ミニファイの3点を導入し、削減率と精度を計測する。  
- マッピング（UUID→短ID）は必ず一貫して保持し、デバッグ用に復元ロジックを用意する。  
- 過度の最適化は可読性と将来の拡張性を損なうため、チームで命名規約と変換ルールを合意する。  
- 標準化を検討する場合はTOON等を評価。自前運用は柔軟性と説明責任が得られる。  

すぐに試せるチェックリスト：JSONをミニファイ／キー短縮ルール作成／UUID短IDマッパー実装／空値除去関数導入／最適化前後でモデル出力差とコストを比較。
