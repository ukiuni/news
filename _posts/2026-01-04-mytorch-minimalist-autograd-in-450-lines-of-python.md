---
  layout: post
  title: "MyTorch – Minimalist autograd in 450 lines of Python - MyTorch（450行で実装した最小限の自動微分）"
  date: 2026-01-04T02:20:39.735Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/obround/mytorch"
  source_title: "GitHub - obround/mytorch: Automatic differentiation implemented in python, inspired by Pytorch (easily extensible)"
  source_id: 46483776
  excerpt: "450行のシンプル実装で自動微分の仕組みを丸ごと理解できる教材"
  image: "https://opengraph.githubassets.com/2288c72cf8628d8afd98485ab5e29d03d3debbd7b57f6d088c39f24e81bc540b/obround/mytorch"
---

# MyTorch – Minimalist autograd in 450 lines of Python - MyTorch（450行で実装した最小限の自動微分）
450行で学ぶ自動微分の本質 — PyTorchに触発された軽量実装で「仕組み」を丸ごと理解する

## 要約
MyTorchはPyTorch風のAPIを模した、約450行のPython実装による自動微分ライブラリ。NumPyを裏で使い、逆モード（reverse‑mode）自動微分をシンプルに再現しているため、教育・実験用途に最適。

## この記事を読むべき理由
自動微分は深層学習の根幹だが、フルスペックのフレームワークはブラックボックスになりがち。MyTorchはコード量が小さく拡張しやすいため、微分の挙動、高階導関数、ブロードキャスト時の勾配伝播などの“なぜ”を手でトレースして学べます。日本の研究者やエンジニアが理論と実装を結びつけるには格好の教材です。

## 詳細解説
- 実装の核：MyTorchは「グラフベースの逆モード自動微分」を採用。演算ごとにノードを作り、後向きに連鎖律で勾配を累積します。これによりスカラー・非スカラーともに任意の階数の導関数が計算可能です。
- API：PyTorchと似たインターフェースを持ち、`tensor(..., requires_grad=True)`、`backward()`、`autograd.grad()`が使えます。`autograd.grad`は高階導関数計算にも対応しており、元記事の例ではPyTorchなら`create_graph=True`が必要な場面でもMyTorchは簡潔に計算できます。
- ブロードキャスト対応：NumPy準拠のブロードキャストを考慮して勾配をまとめてくれるため、行列演算やベクトルを含む演算でも期待通りの勾配が得られます。
- 実装規模と拡張性：全体が約450行に収まり、拡張して `torch.nn` 相当のモジュールや、CuPy/NumbaによるGPU対応に拡張する足がかりを提供します。教育的に読み解きやすく、低レイヤ（BLAS利用）へ移植する良い出発点でもあります。
- 注意点：NumPyベースなのでデフォルトはCPU実行。プロダクション用途や大規模モデルの高速化には追加実装（GPUバックエンド、最適化された演算子など）が必要です。ライセンスはUnlicense（パブリックドメイン相当）で試しやすい。

自動微分の基本的な連鎖律を逆方向でまとめると、ノードxに対する損失Lの勾配は次の形で表現されます：
$$
\frac{dL}{dx} = \sum_{y \in \text{children}(x)} \frac{dL}{dy}\,\frac{\partial y}{\partial x}
$$

簡単な使用例（READMEより抜粋）:
```python
# python
import mytorch as torch

a = torch.tensor(3., dtype=torch.float32, requires_grad=True)
b = torch.tensor(10., dtype=torch.float32, requires_grad=True)
c = 2 + (a + b**2) / (a + b + a*b)

dc_da, dc_db = torch.autograd.grad(c, [a, b])
d2c_da2 = torch.autograd.grad(dc_da, [a])[0]

print(f"∂c/∂a = {dc_da}")
print(f"∂²c/∂a² = {d2c_da2}")
```

## 実践ポイント
- ローカルで試す：GitHubリポジトリをクローンして、examples.pyを動かして挙動を追う（`pip install numpy`だけでOK）。
- 「なぜ」トレース：任意の演算を入れて計算グラフを手で辿ると、連鎖律の流れが理解しやすい。勾配がどこで累積されるかを確認しよう。
- 高階導関数の実験：PyTorchで`create_graph=True`が必要なケースをMyTorchで比較し、内部の違い（グラフ保持の扱い）を学ぶ。
- 拡張ワークショップ案：`torch.nn`風の簡易レイヤを実装し、小さな訓練ループを作る。次のステップはCuPyやNumbaで演算部分を差し替えGPU対応を試すこと。
- 教材化：大学や社内の勉強会で「自動微分の仕組みを実装してみる」教材として使うと効果的。

リポジトリは軽量で読みやすく、理論と実装を結びつけたい日本の開発者にとってすぐに取り組める入門素材です。興味があればまずはコードを動かして、1つずつ演算ノードの振る舞いを確認してみてください。
