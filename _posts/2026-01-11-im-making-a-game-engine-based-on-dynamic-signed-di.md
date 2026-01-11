---
layout: post
title: "I'm making a game engine based on dynamic signed distance fields (SDFs) - 動的SDFを基盤にしたゲームエンジンを作っています"
date: 2026-01-11T21:56:28.278Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=il-TXbn5iMA"
source_title: "I&#39;m making a game engine based on dynamic signed distance fields (SDFs) - YouTube"
source_id: 46539478
excerpt: "動的SDFでポリゴン不要、滑らかなブーリアン合成と破壊表現を実現するゲームエンジン"
image: "https://i.ytimg.com/vi/il-TXbn5iMA/maxresdefault.jpg"
---

# I'm making a game engine based on dynamic signed distance fields (SDFs) - 動的SDFを基盤にしたゲームエンジンを作っています
ポリゴンに頼らない世界観へ — 動的SDFで描くリアルタイムゲームエンジンの可能性

## 要約
動的な符号付き距離場（SDF）を核に据えたゲームエンジンは、形状合成や衝突判定、レイトレース的レンダリングを一貫して扱えるため、表現の自由度と実行時の柔軟性を大幅に高めます。

## この記事を読むべき理由
SDFベースの技術は、プロシージャル表現や滑らかなブーリアン操作が得意で、モバイルからコンソールまでパフォーマンスと表現のトレードオフを工夫する日本のゲーム開発者やエンジニアにとって有用です。新しい表現手法やプロトタイピングの選択肢を増やせます。

## 詳細解説
- SDFとは：点位置 $\mathbf{p}$ に対してその点から最近接表面までの符号付き距離を返す関数 $f(\mathbf{p})$。表面はゼロレベルセット $f(\mathbf{p})=0$ で表されます。例：中心 $\mathbf{c}$、半径 $r$ の球の距離は $f(\mathbf{p})=\|\mathbf{p}-\mathbf{c}\|-r$。
- 動的SDFの利点：
  - プリミティブ（球、箱、トーラス等）の解析的定義とブーリアン（union/intersection/subtract）で瞬時に形状合成が可能。
  - 形状のモーフィングや破壊表現、滑らかなブレンドが簡潔に書ける（smooth min/max 等）。
  - レンダリング：GPUでのスフィアトレース（sphere tracing）によるピクセル単位のレイトマーチングで高品質な陰影や反射が得られる。
  - 物理/衝突：距離情報から最短距離と法線（勾配）を直接得られるため、安定した衝突解決やスライディングが可能。
- 実装上のポイント：
  - データ表現：解析関数の合成だけで済む場合と、格子（ボクセル）やテクスチャとして距離値を保持する場合がある。動的更新が頻繁なら局所的な再計算（narrow band）や疎なオクツリーが有効。
  - パフォーマンス最適化：スフィアトレースはステップ数を距離で決めるため、バウンディングボリュームや階層距離フィールドで早期脱出を導入する。GPUのコンピュートシェーダで並列化するのが実用的。
  - 精度と解像度：ボクセル解像度と距離の切り捨て（truncation）によるアーティファクトに注意。必要に応じてハイブリッド（メッシュ＋SDF）戦略を採る。
- 実例的な処理フロー：
  1. 基本プリミティブを解析的SDFとして定義。
  2. ブーリアンや滑らかなブレンドで複合形状を作る。
  3. 必要箇所だけローカルで距離場をサンプリング／再構築。
  4. フラグメントでスフィアトレース→法線算出→ライティング。
- 参考技術・ツール：GPUコンピュート（OpenGL/GLSL、Vulkan、DirectX）、疎ボクセルライブラリ（OpenVDB系やNanoVDB的コンセプト）を組み合わせるとスケールしやすい。

短いGLSL風のスフィアトレース例（概念）を示します。

```glsl
// GLSL
float sceneSDF(vec3 p) {
    // 例：球と箱の合成（smooth unionは省略）
    float d1 = length(p - vec3(0.0,0.0,0.0)) - 1.0; // sphere
    float d2 = max(abs(p.x)-0.5, max(abs(p.y)-0.5, abs(p.z)-0.5)); // box
    return min(d1, d2); // union
}

vec3 rayMarch(vec3 ro, vec3 rd) {
    float t = 0.0;
    for(int i=0;i<100;i++){
        float d = sceneSDF(ro + rd * t);
        if(d < 1e-3) break;
        t += d;
        if(t > 100.0) break;
    }
    return vec3(t); // 距離を返す（簡略）
}
```

## 実践ポイント
- まずは2DのSDF（Canvas/WebGL）で基礎を体験：プリミティブ、ブレンド、スフィアトレースの感触を掴む。
- 小さなスコープで「SDFでの衝突判定」や「動的破壊表現」を試す。局所更新（narrow band）を実装すると性能改善を実感しやすい。
- GPUでの実行を前提にプロトタイプを作る（フラグメントシェーダやCompute）。ボトルネックはメモリ帯域とステップ数。
- ハイブリッド運用を検討：静的な複雑ジオメトリはメッシュ、動的かつ合成が重要な部分をSDFで担当させると現実的。
- 日本の開発現場では、モバイルや小規模チームでの高速プロトタイピング、ツール寄せ（エディタ内で形状を直感的に編集）の需要が高いので、SDFの「即時合成」「パラメトリック編集」は強みになる。

このアプローチはまだ研究・実装の余地が大きく、新規表現や小規模タイトルでの差別化に向いています。まずは小さく試して、GPU最適化とデータ構造の設計を段階的に進めてください。
