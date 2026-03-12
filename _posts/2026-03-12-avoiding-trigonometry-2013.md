---
layout: post
title: "Avoiding Trigonometry (2013) - 三角法を避ける"
date: 2026-03-12T14:22:35.507Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://iquilezles.org/articles/noacos/"
source_title: "Inigo Quilez :: computer graphics, maths, shaders, fractals, demoscene"
source_id: 47348192
excerpt: "sin/cosを使わずdot/crossで高速かつ安定に3D回転行列を構築する実践手法"
image: "https://iquilezles.org/logo.jpg"
---

# Avoiding Trigonometry (2013) - 三角法を避ける
回転処理を三角関数なしでシンプルかつ高速にする方法

## 要約
三角関数（sin, cos, acos など）を中核に使うと、3D 回転処理は冗長で不安定になりがち。内積・外積だけで同じ回転を正確かつ高速に表現できる。

## この記事を読むべき理由
ゲームやレンダラー、WebGL/VR など日本の開発現場でも、性能・数値安定性・コードの簡潔さは重要。三角関数を避ける手法はモバイルやリアルタイム処理で特に有効。

## 詳細解説
- 基本観点：内積(dot)は cos、外積(cross)は sin を幾何学的に持つ。具体的には $|a\times b|=|a||b|\sin\theta$、$a\cdot b=|a||b|\cos\theta$。
- 問題の例：軸と角度を計算して回転行列を作る典型的な実装は、まず角度を acos で求めてから再び cos/sin を使う（結果的に cos(acos(x)) = x）。無駄な計算と丸め誤差の温床になる。
- 解決策：目標ベクトル d と基準軸 z に対して
  - 軸ベクトルを $v = z \times d$、
  - cos 値を $c = z \cdot d$、
  - 定数 $k = \dfrac{1}{1+c}$
  を使うと、三角関数や正規化・平方根を使わずに回転行列を構成できる（ただし $c \approx -1$（反対方向）では特別処理が必要）。
- 結果的に得られる回転行列（要点のみ）：

```cpp
// C++
mat3 rotationAlign(const vec3& d, const vec3& z){
    vec3 v = cross(z, d);
    float c = dot(z, d);
    float k = 1.0f / (1.0f + c); // c == -1 は要ハンドリング
    return mat3(
        v.x*v.x*k + c,  v.y*v.x*k - v.z,  v.z*v.x*k + v.y,
        v.x*v.y*k + v.z, v.y*v.y*k + c,   v.z*v.y*k - v.x,
        v.x*v.z*k - v.y, v.y*v.z*k + v.x, v.z*v.z*k + c
    );
}
```

## 実践ポイント
- 内部ループやホットパスで acos/sin/cos を避け、dot/cross ベースの実装を検討する。
- $c = z\cdot d \approx -1$（ベクトルがほぼ反対）の場合は、任意の直交軸で 180° 回転するフォールバックを用意する。
- サンプル実装を小さなユニットで置き換え、パフォーマンスと数値安定性をベンチマークする。
- 外部 API（axis-angle を返すなど）をそのまま受け入れず、可能ならベクトル表現で扱う設計にする。

以上。
