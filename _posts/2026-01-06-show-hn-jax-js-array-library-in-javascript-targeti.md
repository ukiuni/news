---
  layout: post
  title: "Show HN: Jax-JS, array library in JavaScript targeting WebGPU - WebGPUをターゲットにしたJavaScript配列ライブラリ「jax-js」"
  date: 2026-01-06T18:50:31.890Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://ss.ekzhang.com/p/jax-js-an-ml-library-for-the-web"
  source_title: "Announcing jax-js: an ML library for the web"
  source_id: 46516267
  excerpt: "ブラウザでGPU直結、JAX風の高速自動微分と数値計算を純JSで実現"
  image: "https://substackcdn.com/image/fetch/$s_!7bb1!,w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1466b600-4dc2-4a2c-9639-843f5a1c700a_1196x450.png"
---

# Show HN: Jax-JS, array library in JavaScript targeting WebGPU - WebGPUをターゲットにしたJavaScript配列ライブラリ「jax-js」

ブラウザだけでJAXっぽい高性能な数値計算と自動微分ができる時代が来た — jax-jsでGPUをフロントエンドに直結する

## 要約
jax-jsはGoogleのJAXを「純粋なJavaScript」で再実装し、WebAssembly／WebGPUにJITでカーネルを生成してブラウザ上で高速な数値計算と自動微分を可能にするライブラリです。

## この記事を読むべき理由
ブラウザがそのまま実行環境（GPU含む）になれば、プライバシー重視のクライアント推論、オフライン対応のインタラクティブなML開発、プロトタイピングの高速化など日本のプロダクト開発・研究現場に直結するメリットが大きいためです。特にWeb技術に強い日本のスタートアップや研究チームは、サーバ負荷やデータ転送コストを下げる新たな選択肢として注目すべきです。

## 詳細解説
- 基本コンセプト  
  jax-jsはJAXの設計を踏襲しつつ、カーネル生成をJavaScriptで行いWebAssembly／WebGPUに変換して実行します。JSのインタプリタ負荷を回避し、GPUやWASMでほぼネイティブに近い速度を目指します。

- 実行環境とパフォーマンス  
  WebGPU（とWASM）を使うことでブラウザ上で行列演算や畳み込みを効率的に実行。著者のベンチではM1/M4系でmatmulが数TFLOP、実用デモではCLIP埋め込みが500 GFLOP/s程度を記録しています。ただし conv2d など最適化余地は残ります。

- APIと特徴  
  - npmパッケージは依存なしの純粋JS: @jax-js/jax  
  - APIはJAXに近く、grad、vmap、jitなどをサポート  
  - JavaScriptに演算子オーバーロードがないため ar.mul(10) のようなメソッド呼び出しが必要  
  - メモリは参照カウント（move semantics）で管理。.ref() で参照を増やし、.js() で通常の配列に戻す

- バックエンド設計（概略）  
  Backendインタフェースでメモリ確保/参照管理、カーネルのprepare/dispatchを定義。カーネル表現は「AluExp」ツリーと28種類ほどのAluOpで構成され、ポイントワイズと還元（reduction）を組み合わせてGPUカーネルを自動生成します。生成されるWGSL（WebGPUシェーダ）例は大規模行列乗算用にループのアンローリング・タイル化が施されています。

- 実用デモ例  
  - ブラウザでMNISTを学習して99%超の精度を数秒で達成するデモ  
  - 全文検索（Great Expectations全文）をCLIP埋め込み→セマンティック検索でリアルタイム実行

## 実践ポイント
- まずは試す（インストールと最小例）
```bash
npm install @jax-js/jax
```

```javascript
// javascript
import { numpy as np } from "@jax-js/jax";
const ar = np.array([1,5,6,7]);
console.log(ar.mul(10).js()); // -> [10,50,60,70]
```

- WebGPUを使う場合（初期化）
```javascript
// javascript
import { init, setDevice } from "@jax-js/jax";
await init("webgpu");
setDevice("webgpu");
```

- 自動微分とJITの使い方（簡単例）
```javascript
// javascript
import { grad, jit, numpy as np } from "@jax-js/jax";

const f = (x) => np.sqrt(x.ref.mul(x).sum());
const df = grad(f);

const g = jit((x) => np.sqrt(x.add(2).mul(Math.PI)).sum());
```

- 製品化での注意点と応用案
  - ブラウザでの推論は通信とプライバシー面で有利（顧客データをサーバに送らない設計が可能）。  
  - 既製モデルを使うならONNX等の「モデルランタイム」と組み合わせる設計も実用的。  
  - 最適化余地（conv2dやトランスフォーマー推論）あり：日本のハードウェア特性（Apple Silicon普及率など）を踏まえたチューニングが勝負どころ。  
  - 開発体験（ホットリロードで学習中にコード編集できる）を活かしたインタラクティブな研究・教育ツールに最適。

参考リンク：GitHub（ekzhang/jax-js）、REPL／APIリファレンス。まずはREPLで手元のブラウザで動かしてみることを強くおすすめします。
