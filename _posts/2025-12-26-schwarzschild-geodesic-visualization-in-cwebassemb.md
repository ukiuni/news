---
layout: "post"
title: "Schwarzschild Geodesic Visualization in C++/WebAssembly - C++/WebAssemblyによるシュヴァルツシルト測地線の可視化"
date: "2025-12-26 04:07:51.575000+00:00"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://schwarzschild-vercel.vercel.app/"
source_title: "Schwarzschild Geodesics | Advanced Simulation"
source_id: "438037009"
---
# Schwarzschild Geodesic Visualization in C++/WebAssembly - C++/WebAssemblyによるシュヴァルツシルト測地線の可視化

## 要約
C++で実装しWebAssemblyにコンパイルしたインタラクティブなシュワルツシルト空間の光線トレーサー。観測点やインパクトパラメータを変えながら、事象の地平線・光子球・降着円盤といった一般相対論的な効果をリアルタイムで可視化できる。

## この記事を読むべき理由
日本でも大学の教室、プラネタリウム、ゲームやVR表現で「重力レンズ」やブラックホールの見た目を正確に再現したい需要が高まっています。本ツールは軽量でブラウザで動き、概念理解からプロトタイプ実装まで応用しやすい点が魅力です。

## 詳細解説
このデモはシュワルツシルト計量に従う「光の経路（null geodesics）」を数値積分して、各初期光線が事象の地平線に落ちるか（捕獲）、遠方に脱出するか、あるいは光子球付近でスワールするかを判定し、ピクセルごとに色を割り当ててレンダリングします。

基本となる計量は
$$
ds^2 = -\left(1-\frac{2M}{r}\right)dt^2 + \left(1-\frac{2M}{r}\right)^{-1}dr^2 + r^2(d\theta^2+\sin^2\theta\,d\phi^2),
$$
で、光（null）の運動はエネルギー $E$、角運動量 $L$ を保存するため、影響を受けるのは有効ポテンシャル
$$
V_\mathrm{eff}(r)=\frac{L^2}{r^2}\left(1-\frac{2M}{r}\right).
$$
光子球は半径 $r=3M$ に位置し、臨界インパクトパラメータは $b_c=3\sqrt{3}\,M$ で、これを境に光が捕獲されるか回避されるかが決まります。

実装面のポイント:
- 初期条件は観測者位置（例: 観測半径 $r_{\rm obs}=25.0\,M$）と視野から生成するレイ束（theta/phi解像度）で決定。
- 各レイは逆向きに（観測者からブラックホールへ）積分して、事象の地平線 $r=2M$ に到達するか、充分大きな $r$ に復帰するかで判定。
- 数値積分は固定ステップのRK4や適応ステップのルンゲ＝クッタ系が使われる。安定化のために座標選択（例: Eddington–Finkelstein座標）やステップ制御が導入されることが多い。
- 見た目は、捕獲された光は黒、脱出した光は星背景テクスチャを反映、光子球付近で長く留まった光線を強調して「シャドウの縁」を描画するなどの表現をする。

WebAssembly化の利点:
- C++で最適化された数値積分コードをそのままブラウザで高速に動かせる（Emscripten等）。
- マウス操作で回転/ズームが可能で、視覚フィードバックが即時に得られるため教育・デモに最適。

デモにある主要パラメータ（原文のUI表現から）
- Observer Radius (r): 25.0 M（観測点）
- Ray Bundle: Impact Min 0.1 M, Impact Max 8.0 M（インパクトパラメータ範囲）
- Theta/Phi resolution: 角度分解能（例: 8×12）
- 可視化要素: Event Horizon, Photon Sphere, Accretion Disk, Starfield
- 出力: Captured / Escaped / Photon Sphere による分類表示

簡潔な擬似コード（C++）: 積分の考え方を示します。

```cpp
// cpp
Vec4 initPhoton(int i, int j, Camera cam);
void integrateNullGeodesic(Vec4 x, Vec4 k, double M) {
  for (int step=0; step<MAXSTEP; ++step) {
    rk4Step(x, k, dt, M);
    double r = radius(x);
    if (r <= 2.0*M) { markCaptured(); break; }     // event horizon
    if (r > R_ESC) { markEscaped(); break; }       // escaped to infinity
    if (nearPhotonSphere(r, 3.0*M)) { markPhotonSphere(); }
  }
}
```

## 日本市場との関連
- 教育・普及: 大学や高校の物理教育、プラネタリウムでの視覚教材として即戦力。実際のパラメータを操作できることで直感的理解が深まります。
- VR/ゲーム: ブラックホールを舞台にした没入体験やシミュレーションゲームで、見た目の正確さを求める開発者に有用。
- 研究支援: 可視化プロトタイプとして、解析結果の理解や発表資料作成の補助に活用可能。

## 実践ポイント
- まずは観測半径を大きめ（例: $r_{\rm obs}=25M$）にして、インパクトパラメータの範囲を広く取り、光の回り込みを確認する。
- 解像度（theta/phi）を上げると境界が滑らかになるが計算コストが増える。WebAssemblyなら並列化（Worker）やSIMDで改善可能。
- 数値的安定性: 事象の地平線近傍は座標特異性が出るので、座標系変換（例: Eddington–Finkelstein）や適応ステップ幅を検討する。
- 再現してみたい人はC++で書かれた積分ルーチンをEmscriptenでビルドしてブラウザへ持ち込むのが最も手早い。実装のキーは「初期光線の作り方（スクリーン座標→球面上の発射角）」と「終了判定（r<=2M / r>R_ESC / 周回検出）」です。

