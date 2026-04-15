---
layout: post
title: "It's NOT OK to compare floating-points using epsilons - 浮動小数点をεで比較するのはダメだ"
date: 2026-04-15T00:12:16.132Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lisyarus.github.io/blog/posts/its-ok-to-compare-floating-points-for-equality.html"
source_title: "It's OK to compare floating-points for equality | lisyarus blog"
source_id: 1150140974
excerpt: "ε比較は安易な対処でバグを招く、ゲームやグラフィックスでは設計や閾値で根本解決を図れ"
image: "/blog/media/compare-floating-points/cover.png"
---

# It's NOT OK to compare floating-points using epsilons - 浮動小数点をεで比較するのはダメだ

魅力的なタイトル: 「ε信仰はもうやめよう：浮動小数点の比較、’==’で良い場合が多い理由」

## 要約
一般的な「浮動小数点は等号で比較してはいけない、εを使え」という教えは万能ではなく、多くの場合は設計や境界処理を見直す方が正解になる。

## この記事を読むべき理由
日本のゲーム開発や組込み、グラフィックス、シミュレーション開発では浮動小数点を大量に扱う。無意味なε比較はバグの温床になりやすく、開発コストやデバッグ地獄を招くため、代替手法を知る価値が高い。

## 詳細解説
- 浮動小数点はランダムではなく決定論的で標準化された表現。各演算は「最も近い表現値」に丸められるため、挙動は予測可能だが数学的性質（例：結合法則）は壊れることがある。
- 問題点（ε比較の欠陥）:
  - 多くは「場当たり的」で一次的な修正に留まりがち。
  - プログラム全体で異なるεが混在すると非推移的な比較になり、アルゴリズムが破綻する（整合性の喪失、難解なバグ）。
  - εはたいてい経験則で決められ、正当化が難しい。
- 事例1 — グリッド移動（ゲーム）
  - 表示の補間で位置が厳密に等しくならず、`if (pos != target)` が期待通り動かない場面がある。
  - 一見 ε を入れると直るが、本質は「表示（レンダリング）と内部状態の混同」。解決策は内部モデルでセル遷移を完了扱いにする、または受け入れ半径（意味に基づくしきい値）やアニメーションキューを使う設計。
  - 悪い例:
```cpp
// C++
if (distance(selectedUnit.position, targetCell.center) > 1e-4) return;
```
- 事例2 — Slerp（球面線形補間）
  - 公式：
$$
\text{slerp}(a,b,t)=\frac{\sin((1-t)\theta)\,a+\sin(t\theta)\,b}{\sin\theta},\quad \theta=\arccos(a\cdot b)
$$
  - NaN が発生する原因：
    1. acos の引数が $[-1,1]$ を超える（丸めで1.0000001など）。
    2. $\theta=0$ により $\sin\theta=0$ で 0/0 発生。
  - 対処法：acos の引数を clamp し、$a\cdot b \ge 1$ の場合は単純な線形補間にフォールバックする。FLTEPSILON を無条件に投げるのは十分な理由にならない（$\sin(\acos(x))=\sqrt{1-x^2}$ で小さな誤差の振る舞いが理解できるため）。具体例：
```cpp
// C++
vec3 slerp(vec3 a, vec3 b, float t) {
    float d = dot(a, b);
    if (d >= 1.f) return lerp(a, b, t); // 完全一致なら線形でOK
    float angle = acos(clamp(d, -1.f, 1.f));
    return (sin((1 - t) * angle) * a + sin(t * angle) * b) / sin(angle);
}
```

## 実践ポイント
- 「まず考える」：なぜ比較しているのか（表示同期？状態遷移？入力検証？）を明確にする。
- 設計で解く：表示と内部状態を分離し、意味に基づくしきい値（受け入れ半径）や状態フラグで扱う。
- 境界処理を明示的に扱う：acos の引数は clamp、ゼロ割りの可能性は特殊ケースで明示的にフォールバックする。
- グローバルな ε は避ける：コンテキストに応じた閾値をドメイン知識で決める。
- テストを充実させる：端点や極端な入力（正規化ベクトル、ほぼ一致、反対方向）をユニットテストに含める。

短く言えば、εは便利なツールだが安易に使うと長期的には害になる。まず問題の本質を設計で解決できないかを検討する習慣をつけよう。
