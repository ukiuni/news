---
layout: post
title: "I Made Zig Compute 33 Million Satellite Positions in 3 Seconds. No GPU Required - Zigで33百万の衛星位置を3秒で計算。GPU不要の高速化手法"
date: 2026-01-21T05:58:18.075Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://atempleton.bearblog.dev/i-made-zig-compute-33-million-satellite-positions-in-3-seconds-no-gpu-required/"
source_title: "I Made Zig Compute 33 Million Satellite Positions in 3 Seconds. No GPU Required. | Anthony T&#x27;s Blog"
source_id: 1346213125
excerpt: "ZigのSIMDとcomptime最適化でGPU不要、秒間数千万のSGP4伝搬を実現"
image: "https://bear-images.sfo2.cdn.digitaloceanspaces.com/herman-1683556668-0.png"
---

# I Made Zig Compute 33 Million Satellite Positions in 3 Seconds. No GPU Required - Zigで33百万の衛星位置を3秒で計算。GPU不要の高速化手法

ZigでSGP4実装を徹底最適化し、GPUなしで数千万件級の衛星位置計算を高速化した話を、IT初級者にも分かりやすく解説します。

## 要約
Zig言語の特徴（comptime／SIMDサポート）とアルゴリズム工夫で、汎用SGP4実装「astroz」はネイティブで11–13M伝搬/秒、Pythonバインディングでも約7M/秒を実現。用途に応じた3つの並列化モードとキャッシュ配慮が勝因です。

## この記事を読むべき理由
衛星運用・追跡、パス予測、近接通過解析などで「高精度×大量時間解像度」が求められる場面は増えています。日本の衛星サービス、大学やスタートアップの観測系ツールづくりでも、実務上の計算負荷削減と応答性改善に直結するテクニックが学べます。

## 詳細解説

- なぜSGP4最適化が重要か  
  SGP4はTLEから衛星位置を求める標準アルゴリズムで、1秒刻みで1か月分を出すと1衛星あたり約$2.6\times10^{6}$回の伝搬が必要になります。典型的な実装で2–3M/sなら1衛星あたり数秒、複数衛星や反復解析では遅延が積み重なります。

- Zigで伸びた設計的理由  
  1) ブランチレスなホットパス：条件分岐を可能な限り式（branchless）にしてCPUの分岐予測ミスを避ける。  
  2) comptimeでの事前計算：重い定数や係数をコンパイル時に算出して実行時コストを削減。  
  これらだけでスカラー実行で約5.2M/sが出た（Rust実装と同等か僅かに上回る）。

- SIMD化の肝（Zigの利点）  
  Zigは@Vector(4, f64) のようにベクトル型を簡潔に扱え、@sin/@cosなどLLVMベースのベクトル化機能も使えるため、低レベルの命令を直接書かずにSIMD化が可能。幅$4$のレーンで並列計算することでスループットが2倍以上に。

  例（Zig）:
  ```zig
  const Vec4 = @Vector(4, f64);
  const twoPiVec: Vec4 = @splat(constants.twoPi);
  const mask = eccentricity < @as(Vec4, @splat(1.0e-4));
  const result = @select(f64, mask, simple_result, complex_result);
  ```

- SIMDで注意する点（分岐と収束）  
  SIMDでは各レーンが同時に実行されるため、分岐は「両方計算してマスクで選ぶ」スタイルに変換。Kepler方程式の反復収束もレーン毎の収束マスクを管理して、全レーンが終わるまでループするパターンを採る（@reduceで全員完了を判定）。

- atan2の扱い（近似で問題なし）  
  LLVMにベクトル化されたatan2が無いため、誤差許容の範囲内で多項式近似を用いることでベクトル化を維持。近似誤差は約$10^{-7}$ラジアン（LEOで位置誤差数mm相当）で、SGP4自体のモデル誤差に比べ十分小さい。

- データレイアウト：Struct of Arrays  
  衛星多数を同時に処理するには、各パラメータを「4要素ベクトルの集合」として格納するElementsV4のような構造（struct-of-arrays）が重要。定数はあらかじめ@splatしておく（pre-splat）とホットパスでのコストが下がる。

- 3つの伝搬モード（用途別）
  1) Time-batched（propagateV4）: 1衛星×複数時刻（時間列の生成が主目的） — 最もキャッシュフレンドリーで時間分解能高い処理に強い。  
  2) Satellite-batched（propagateSatellitesV4）: 複数衛星×1時刻（スナップショット向け） — 衛星多数の瞬時監視に有利。  
  3) Constellation mode: タイリング（時間方向をブロック化）してL1/L2キャッシュを活かしつつ多数衛星×多数時刻を効率化。

- ベンチマークの要点（抜粋）
  - スカラー実行: Zig ≈ 5.2M/s, Rust ≈ 5.0M/s（僅差）  
  - SIMD化: Zigで11–13M伝搬/s（2×超）  
  - Pythonバインディング: astrozで約7M/s（pipで利用可能）  
  - 比較: heyoka.pyは多数衛星の一時刻処理で高速（例：16M/s）だが、時間軸を細かく取る用途ではastrozが優位（例：8.5M/s vs 3.8M/s）

## 実践ポイント
- まず用途を明確に：時間分解能が重要ならTime-batched、スナップショット多数ならSatellite-batchedを選ぶ。  
- Zigを選ぶ場合はcomptimeで定数を前処理して無駄な初期化を減らす。  
- データレイアウトはstruct-of-arraysにしてSIMDレーンをまとめる（ElementsV4的構造）。  
- 分岐は可能な限りマスク＆@selectで置き換える。Keplerの反復はレーン別収束マスクで管理する。  
- atan2などベクトル化非対応関数は誤差許容範囲内の多項式近似で代替可能（LEO運用では実用的）。  
- Pythonから手早く試すなら pip install astroz で手元のスクリプトを高速化できる（約7M/sの現実的スループット）。  
- 大規模バッチではGPUやJIT（heyoka系）も選択肢。ただし環境依存（CUDA/LLVM/JIT）や導入コストを考慮する。

興味があれば、特定用途（例えば「日本の観測局網でのパス予測」や「LEOコンステレーションの近接解析」）に合わせた実装設計やベンチ手法のアドバイスを提供します。
