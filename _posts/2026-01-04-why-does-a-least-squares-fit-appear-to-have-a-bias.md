---
  layout: post
  title: "Why does a least squares fit appear to have a bias when applied to simple data? - 単純なデータに最小二乗フィットを当てると「バイアス」が見えるのはなぜか"
  date: 2026-01-04T20:55:24.774Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://stats.stackexchange.com/questions/674129/why-does-a-linear-least-squares-fit-appear-to-have-a-bias-when-applied-to-simple"
  source_title: "regression - Why does a linear least squares fit appear to have a bias when applied to simple test data? - Cross Validated"
  source_id: 46491821
  excerpt: "直感と違う回帰線の正体—OLSとPCA/TLSの違いと適切な選び方"
  image: "https://stats.stackexchange.com/Content/Sites/stats/Img/apple-touch-icon@2.png?v=344f57aa10cc"
---

# Why does a least squares fit appear to have a bias when applied to simple data? - 単純なデータに最小二乗フィットを当てると「バイアス」が見えるのはなぜか

誰もが直感で想像する「データの主軸」と回帰線がズレる理由を、OLS（普通最小二乗）とPCA／TLS（直交最小二乗）の違いでスパッと解説する

## 要約
普通最小二乗（OLS）は縦方向の誤差だけを最小化するため、データ群の「主軸」（分散最大方向、PCAで得られる方向）とは一般に一致しない。PCA/TLSは点と直線の垂直距離を小さくするため、人間の直感に近い向きになる。

## この記事を読むべき理由
- 可視化や予測で回帰線の向きに違和感を覚えた経験があるなら、その原因がすぐに分かる。
- センサーデータ、製造業の品質データ、金融・計測データなどで「Xにも測定誤差がある」場合、誤った手法選択は予測や解釈を歪める可能性がある。
- scikit-learn / numpy 等のツールで何を使えば良いかが分かる。

## 詳細解説
問題の核心は「誤差モデルの仮定」にある。主要な違いを整理する。

- OLS（Ordinary Least Squares）  
  - 目的：$y$ の観測値とモデル $y=\beta x+\alpha$ の縦（$y$方向）誤差の二乗和を最小化。  
  - 仮定：$x$ は誤差なし（固定）で、ノイズは $y$ 側のみ。  
  - 解（中心化した場合）：$$\beta_{OLS}=\frac{\sigma_{xy}}{\sigma_x^2}$$  
  - 特徴：回帰線は必ず点 $(\bar x,\bar y)$ を通るが、点群の「主軸」とは異なる向きになることが多い。

- PCA / TLS（Total Least Squares, orthogonal regression）  
  - 目的：点から直線への垂直（直交）距離の二乗和を最小化、または共分散行列の最大固有値に対応する固有ベクトルを主軸として取る。  
  - 仮定：$x,y$ 双方に誤差がある場合に自然。  
  - PCAから得られる主軸の傾きは共分散の固有ベクトルから算出され、一般に OLS の傾きとは異なる。実際の式の一つ（固有値を使った形）は：  
    $$\beta_{PCA}=\frac{\sigma_y^2-\sigma_x^2+\sqrt{(\sigma_y^2-\sigma_x^2)^2+4\sigma_{xy}^2}}{2\sigma_{xy}}$$  
  - 特徴：点群の長軸（分布の方向）を表現するため、視覚的に「データの中心を通る主方向」に見える。

人間の視覚直感は通常「点から直線までの最短距離（直交距離）を小さくしたい」と考えるため、PCA/TLS の結果を「正しい」と感じる。だが統計的に予測を行う場合、Xが誤差を持たないという仮定が妥当なら OLS が適切である。

## 実践ポイント
- X に測定誤差が明らかな場合：TLS（直交回帰）や Deming 回帰を検討する。Python では scipy.odr か SVD を使って実装可能。  
- 予測が目的で「Xを観測値として固定」しているなら OLS が適切。  
- 可視化で違和感があるときは、OLS（y~x）と逆回帰（x~y）とPCAの主軸を同時にプロットして比較すると理解が早い。  
- 手早く確認するPythonコード（OLS vs PCA vs TLSの傾き比較）:

```python
# python
import numpy as np

# データ生成（例）
np.random.seed(0)
x = np.random.randn(20000)
y = 0.5*x + np.random.randn(20000)*2

# OLS
ols_slope, _ = np.polyfit(x, y, 1)

# PCA（共分散の最大固有ベクトル）
cov = np.cov(x, y)
eigvals, eigvecs = np.linalg.eig(cov)
v = eigvecs[:, np.argmax(eigvals)]
pca_slope = v[1] / v[0]

# TLS（SVDによる直交回帰方向）
X = np.column_stack((x - x.mean(), y - y.mean()))
_, _, Vt = np.linalg.svd(X, full_matrices=False)
tls_dir = Vt[0]
tls_slope = tls_dir[1] / tls_dir[0]

print("OLS:", ols_slope, "PCA:", pca_slope, "TLS:", tls_slope)
```

- 実務的判断基準：  
  - センサ／計測でXにも誤差 → TLS/Deming。  
  - 実験でXを意図的に制御（誤差小） → OLS。  
  - 可視化は必ず複数手法で重ねて確認する。

以上を踏まえれば、「回帰線が傾いている」ことはバグではなく、手法の仮定に基づく必然的な違いであることが理解できる。適切な誤差モデルを選べば、可視化と推定の齟齬は解消される。
