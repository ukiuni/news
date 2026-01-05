---
  layout: post
  title: "Should a bilateral filter library automatically match blur across RGB and CIELAB, or just document the difference? - バイラテラルフィルタライブラリはRGBとCIELABでぼかし量を自動で一致させるべきか、それとも差分をドキュメントするだけか？"
  date: 2026-01-05T02:17:54.805Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/Ryan-Millard/Img2Num/discussions/195"
  source_title: "Bilateral Filter: Should `sigma_range` produce identical blur in RGB vs CIELAB, or should the difference be documented? · Ryan-Millard/Img2Num · Discussion #195 · GitHub"
  source_id: 472092902
  excerpt: "バイラテラルフィルタでCIELABが過度にぼける理由と実践的な設計解決を明かす"
  image: "https://opengraph.githubassets.com/04ddc9723b8b3791e9b5c7330de411242754d72a8b94b89f831ffb6067c2ea4b/Ryan-Millard/Img2Num/discussions/195"
---

# Should a bilateral filter library automatically match blur across RGB and CIELAB, or just document the difference? - バイラテラルフィルタライブラリはRGBとCIELABでぼかし量を自動で一致させるべきか、それとも差分をドキュメントするだけか？

画像が突然「CIELABでぼける」理由と、ライブラリ設計で避けるべき落とし穴

## 要約
同じ `sigma_range` を使っても、RGB と CIELAB（Lab）で視覚的なぼかし量が変わる。Labでは隣接ピクセルの色差が小さく表現されやすく、そのままにするとLab側がより「ぼけて」見える問題が起きる。

## この記事を読むべき理由
画像処理ライブラリやフィルタを作る／使う日本のエンジニアは、色空間による数値と「見た目」のずれでユーザーやクオリティチェックに悩みやすい。既定値の扱いでユーザー体験を壊さないための設計判断と実践的対処法が得られる。

## 詳細解説
バイラテラルフィルタは「空間距離を重み付けする sigma_spatial」と「色差に対するガウス重みでエッジを保つ sigma_range」の2つが主要パラメータ。ここでの問題は sigma_range が色差の大きさに依存する点に起因する。

- RGB の各チャンネルは典型的に $[0,255]$。3チャンネルの最大ユークリッド距離は
  $$
  \sqrt{255^2 \times 3} \approx 442
  $$
- CIELAB（L: $[0,100]$, a/b: $[-128,127]$）だと最大は
  $$
  \sqrt{100^2 + 255^2 + 255^2} \approx 374
  $$

単純な最大値比（$442/374 \approx 1.18$）だけでは説明しきれず、実画像の隣接画素差分布（perceptual compression により Lab の隣接差が小さくなる傾向）が効いてくる。結果として、同じ `sigma_range` を与えるとLab側の出力が見た目でより滑らか（＝ぼけ）になりやすい。実験的には RGB の `sigma_range` を約 $4.18$ 倍にすると自然画像で視覚的に近い結果になったという報告がある（例: $4.18 \times 50 = 209$）。

設計上の選択肢は主に三つ：
1. ライブラリ内部で自動スケーリングして視覚的に一致させる（ユーザに透明）。
2. 数値をそのまま尊重し、差をドキュメントに明示する（ユーザに調整を任せる）。
3. デフォルトは「数値を尊重」しつつ、オプションで自動スケーリングや変換ヘルパーを提供する。

自動スケーリングは初心者には便利だが、数値に敏感な上級者を混乱させる可能性がある（「sigma=50 が突然違う見た目に」という不一致）。一方で未説明だと多くのユーザが理由不明の結果に悩む。

## 実践ポイント
- ライブラリ推奨方針：デフォルトは sigma を「数値通り」に扱い、README と API ドキュメントで色空間差を明示する。加えて opt-in の自動補正オプション（例: `match_visual_range=True`）か、変換ヘルパーを提供するのが現実的。
- ドキュメントに含める情報：色空間の既定、代表的な差（例：Labがぼけやすい）、簡単な換算例（経験則として $4.18$ 倍など）と注意書き。
- 実装の提案：ユーザが簡単に使えるヘルパーを用意する。例えば（最小限の例）：

```python
# python
# Labのsigma_rangeを与えてRGBで同等にしたいとき（経験的係数）
def sigma_lab_to_rgb(sigma_lab, factor=4.18):
    """経験的に得られた係数でLab->RGBのsigma_rangeを換算する簡易関数"""
    return sigma_lab * factor
```

- より堅牢な方法：使用する画像群から隣接ピクセルの色差分布（例：95パーセンタイル）をサンプリングして、実測比を採る関数を提供すると環境差を吸収できる。
- テストと例：サンプル画像で RGB と Lab の出力を並べて示すユニットテスト・ビジュアル例をドキュメントに含める（CI に画像差分チェックを入れると親切）。

結論：ユーザーを驚かせないために「数値の厳密さを保ちつつ、明確にドキュメントし、必要ならオプションで視覚一致モードを提供する」設計が現実的で推奨される。
