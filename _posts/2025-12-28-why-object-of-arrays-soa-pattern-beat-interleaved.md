---
layout: post
title: "Why Object of Arrays (SoA pattern) beat interleaved arrays: a JavaScript performance rabbit hole"
date: 2025-12-28T15:05:53.600Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.royalbhati.com/posts/js-array-vs-typedarray"
source_title: "Why Object of Arrays (SoA pattern) beat interleaved arrays: a JavaScript performance rabbit hole"
source_id: 436117482
excerpt: "数百万件の数値処理がTypedArrayを使ったSoAで大幅高速化する理由と実践法を解説"
---

# JSで処理が劇的に速くなることも？SoA（Object of Arrays）がAoS（Interleaved Array）を打ち負かす理由

## 要約
JavaScriptで数百万件の数値データを扱うとき、配列の「構造（Array of Structures, AoS）」よりも各フィールドを別々の配列にした「Object of Arrays / Structure of Arrays（SoA）」とTypedArrayを組み合わせると、メモリ局所性・JIT最適化・GC負荷の観点から大きく高速化することがある。

## この記事を読むべき理由
ブラウザやNodeで高頻度に数値ループを回す開発（ゲーム、物理シミュレーション、金融データ処理、WebGLバッファ操作など）をしているなら、配列データのレイアウトを変えるだけで実行速度とメモリ効率が改善する可能性があります。特に日本のモバイル中心のユーザー層では、CPUキャパ・メモリが限られるため効果が大きく出ます。

## 詳細解説
問題の本質
- AoS（例: [{x,y,z}, ...]）は各要素がオブジェクトで、フィールドアクセスはオブジェクトのプロパティ読み書きになる。各オブジェクトはヘッダやポインタを持ち、メモリ上で散らばりやすい。
- SoAは各フィールドを別の配列で管理（例: xs = Float32Array(n), ys = Float32Array(n)、...）。数値が連続した領域に並び、CPUキャッシュにやさしい。

なぜSoAが速くなるのか（技術的要因）
- メモリ局所性: 連続したメモリを順次アクセスするパターンはキャッシュミスを減らす。
- JITと型安定性: JSエンジン（V8等）は均一な数値配列やTypedArrayをより効率的に最適化できる。AoSではオブジェクトの内部表現や隠れクラス（hidden class）が変化すると最適化が外れることがある。
- GC負荷の低減: TypedArrayはヒープ外の連続バッファ（ArrayBuffer）を使えるため、オブジェクトを大量に生成するAoSに比べGCコストが下がる。
- SIMD/ベクトル化の恩恵: 低レベルで連続した数値列は将来的に自動ベクトル化やWebAssemblyでの最適化と相性が良い。

実践的なコード例（概念）
JavaScriptで位置ベクトルを更新する単純な例を示す。実際にはベンチマークで環境差が出るので必ずターゲットで測ること。

```javascript
// JavaScript

// AoS（配列の要素がオブジェクト）
const n = 1e6;
const ptsA = new Array(n);
for (let i = 0; i < n; i++) ptsA[i] = { x: Math.random(), y: Math.random() };
function updateAoS(dt) {
  for (let i = 0; i < n; i++) {
    const p = ptsA[i];
    p.x += p.y * dt; // 複数プロパティへアクセス
  }
}

// SoA（各フィールドをTypedArrayで管理）
const xs = new Float32Array(n);
const ys = new Float32Array(n);
for (let i = 0; i < n; i++) { xs[i] = Math.random(); ys[i] = Math.random(); }
function updateSoA(dt) {
  for (let i = 0; i < n; i++) {
    xs[i] += ys[i] * dt; // 連続メモリアクセス
  }
}
```

典型的な結果（概念的）
- 小さなnやランダムアクセスが支配的なケースでは差が小さい。
- 大きなnで連続走査するホットループではSoA + TypedArrayの方が高いスループットを示すことが多い。

注意点と落とし穴
- 可読性と保守性: SoAはコードが分散しがちで扱いづらい。抽象化レイヤーを作ると良い。
- アクセスパターンに依存: ランダムに単一要素の複数フィールドを頻繁に読むならAoSの方が扱いやすい場合もある。
- エンジン依存: 最適化のしやすさはエンジン（V8, SpiderMonkey, JavaScriptCore）やバージョンで変わる。必ず実機で測定する。
- 型の選択: Float32Array vs Float64Arrayはメモリと精度のトレードオフ。GPU/WebGL用バッファと連携するならFloat32が自然。

代替と発展
- WebAssemblyやGPU処理（WebGPU）を使えば、さらに低レイヤで効率を引き出せる。数値集約処理はそちらに移すのが有効な場合が多い。
- データ構造の抽象化（例: accessor 関数やビューオブジェクト）でSoAの可読性を保てる。

## 実践ポイント
- まずはプロファイル：実際のホットパスに対してperformance.now()やブラウザのプロファイラで計測する。
- アクセスパターンを観察：連続走査が多ければSoA + TypedArrayを検討する。
- 小さなPoCを作る：AoSとSoAの小さなベンチマークを実機で比較する。
- 変更は段階的に：読みやすさと保守性を損なわない範囲で最適化する。必要ならWebAssemblyに移行する判断も視野に。
- モバイルを忘れずに：日本ではモバイル比率が高く、SoAの恩恵が顕著に出ることが多い。

