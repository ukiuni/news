---
layout: post
title: "Scipy.stats. Chatterjeexi - Scipy.stats.chatterjeexi（チャタージーの ξ 相関）"
date: 2026-02-25T19:35:43.823Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chatterjeexi.html"
source_title: "chatterjeexi &#8212; SciPy v1.17.0 Manual"
source_id: 47111092
excerpt: "非単調関係も検出できるSciPyの新指標$\xi$で未知の依存性を発見しよう"
---

# Scipy.stats. Chatterjeexi - Scipy.stats.chatterjeexi（チャタージーの ξ 相関）
非単調な関係も掴める「新しい相関指標」—SciPyで使えるChatterjeeのξを短時間で理解する

## 要約
SciPyのstats.chatterjeexiは、非単調な関係でも有効な相関係数$\xi$（xi）を計算し、独立性の検定を行う関数です。統計量とp値を返し、漸近解やパーミュテーションによる検定を選べます。

## この記事を読むべき理由
非線形・非単調な依存関係を扱う場面は増えています。日本のデータ分析・プロダクト現場でも、従来のPearson/Spearmanでは見逃しがちな関係を検出できるため実務的価値が高いです。

## 詳細解説
- 概要：Chatterjeeの$\xi$は、2変数の結びつきの強さを示す指標で、独立なら$\xi\approx0$、強い結びつきなら$\xi\approx1$になります。単調でないパターン（例：周期関数など）にも強い点が特徴です。
- 関数シグネチャ（主要引数）:
  - x, y: 観測データ（配列）。ブロードキャスト可能である必要あり。
  - axis: 統計量を計算する軸（デフォルト0）。Noneでフラット化。
  - method: 'asymptotic'（漸近分布に基づく）か PermutationMethod（パーミュテーション検定）を選択可能。
  - y_continuous: yが連続分布であると仮定するか（Trueだと高速化）。
  - nan_policy: {'propagate','omit','raise'}（NaN処理）。
  - keepdims: 結果の次元を保持するか。
- 返り値：SignificanceResult オブジェクト（.statistic に$\xi$、.pvalue にp値）。
- 実装上の注意：
  - xにおける同値（ties）は実装上ランダムに扱われます。推奨される対処は小さなノイズを加えてランダムに破る（jitter）。
  - 統計量は設計上$x$と$y$で非対称です（$Y=f(X)$かを知る目的で有利）。
- Array APIサポート：NumPy以外にCuPy/PyTorch/JAX/Daskの一部サポートあり（環境変数 SCIPY_ARRAY_API=1 で試験的利用）。

## 実践ポイント
- 非線形・非単調な関係を探すならまずxiを試す。Pearson/Spearmanと併用すると差分が分かる。
- xに同値が多い場合は小さな一様ノイズでジッターして複数回計算し平均を取ると安定化。
- 小サンプルや分布仮定を疑う場合は method にパーミュテーションを使う（より計算コストは上がる）。
- 大規模データやGPU加速を使いたいときは、バックエンド（CuPy/PyTorch/JAX）と SCIPY_ARRAY_API=1 を検討。
- 出力の p 値は「独立（帰無）」の下で観測される値以上の統計量が出る確率。閾値設定は用途に合わせて。

簡単な利用例：

```python
# python
import numpy as np
from scipy import stats

rng = np.random.default_rng()
x = rng.uniform(0, 10, size=100)
y = np.sin(x)
res = stats.chatterjeexi(x, y)
print(res.statistic, res.pvalue)
```

以上を踏まえ、単調性に依存しない相関検出が必要な場面ではscipy.stats.chatterjeexiをツールキットに加えると有用です。
