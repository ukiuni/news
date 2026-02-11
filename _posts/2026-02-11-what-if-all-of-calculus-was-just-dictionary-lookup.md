---
layout: post
title: "What if all of calculus was just dictionary lookups? - 微分積分は辞書引きにできる？"
date: 2026-02-11T14:35:53.613Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/tmilovan/composite-machine"
source_title: "GitHub - tmilovan/composite-machine: Composite Machine: Automatic Calculus via Dimensional Arithmetic"
source_id: 444293169
excerpt: "Composite Machineは一次評価で任意階微分・積分を係数読み出しで得る衝撃の手法だ"
image: "https://opengraph.githubassets.com/e79eadd4e11f80f35d4a089bd32be308a0a57f24f753dcbe1af69a783c8e4c97/tmilovan/composite-machine"
---

# What if all of calculus was just dictionary lookups? - 微分積分は辞書引きにできる？

計算は「評価して係数を読む」だけ──1回の数値評価で高階導関数や積分・極限まで取り出せる研究実装「Composite Machine」の衝撃

## 要約
Composite Machineは「次元付き数（dimensional number）」で関数を表現し、微分・積分・極限を係数操作として扱うことで、1回の評価から任意階の導関数や積分を得る新しい数体系を実装した研究プロジェクトです。

## この記事を読むべき理由
- 自動微分や数値解析の常識（計算グラフや差分、ルール分岐）に代わる代数的アプローチを学べる。  
- 教育・プロトタイピングや特殊ケース（0/0の扱いなど）で新しい道具として活用できる可能性がある。

## 詳細解説
- コアアイデア：数に「次元構造」を持たせ、負の次元が導関数情報を符号化する。代数演算は係数畳み込みになり、例えば
  $$ (2+h)^4 = 16 + 32h + 24h^2 + 8h^3 + h^4 $$
  の各係数が $f(2),\ f'(2)/1!,\ f''(2)/2!,\dots$ に対応する。これにより1回の評価で全階の導関数が得られる。
- 主な機能（現状）：
  - 単変数・多変数の四則演算、冪、三角・指数・対数などの超越関数。
  - 任意階導関数の抽出（d(n)、nth_derivative、all_derivatives）。
  - 極限は代入して標準部分を取るだけで代数的に解決（L'Hôpital不要）。
  - 統一的な integrate() API：1D〜3D、線積分、面積分、非有界積分に対応。誤差推定も自動。
  - 0/0 や ∞×0 といった通常は未定義な操作に対する明確な取り扱い（ライブラリ内の定義論理に基づく）。
  - 多変数（勾配、ヘッセ行列、ヤコビアン、ラプラシアン）、複素解析（留数、輪積分）、ベクトル解析まで拡張モジュールあり。
- 制約と現状：研究実装（v0.1-alpha）、性能は遅く（PyTorch比数百〜千倍遅）、APIが変わる可能性あり。ただしテストは168件すべてパス。
- 実装構成：core (composite_lib.py)、multivar、extended（複素）、vector 各モジュールで機能拡張。

## 実践ポイント
- 試す（最短）：Python3.7+ 環境で
```python
# python
git clone https://github.com/tmilovan/composite-machine
cd composite-machine
pip install -e .
```
- すぐ試せる例：
```python
# python
from composite_lib import derivative, all_derivatives, exp
derivative(lambda x: x**2, at=3)            # → 6
all_derivatives(lambda x: exp(x), at=0, up_to=5)
```
- 利用シーンの提案（日本市場向け）：
  - 教育：直感的に係数と導関数の関係を示せる教材ツールとして有用。  
  - プロトタイピング：数式処理や特異点解析を素早く試すリサーチ用途。  
  - 応用分野：ロボット制御やフィナンシャル数値実験で、極限・特異点の扱いを検証する際に便利。
- 注意点：現状は性能面で実務利用は限定的。NumPy/Numba最適化やGPUサポートが今後の鍵。興味があればリポジトリのissuesや貢献（ベンチ最適化、API安定化）を検討すると良い。
