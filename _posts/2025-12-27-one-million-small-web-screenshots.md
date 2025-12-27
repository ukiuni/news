---
layout: post
title: "One million (small web) screenshots"
date: 2025-12-27T02:07:38.939Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nry.me/posts/2025-10-09/small-web-screenshots/"
source_title: "One million (small web) screenshots"
source_id: 46354492
excerpt: "スクリーンショット×SOMで未発掘の小規模良サイトを視覚発見、デザインや知見を得る"
---

# 小さなウェブを可視化する：100万枚スクリーンショットで見つける“質のある”サイト群

## 要約
人気順だけでは見つからない「良い小規模サイト」を、スクリーンショットの視覚埋め込みと自己組織化マップ（SOM）で可視化した試みを紹介。派手な人気サイトを避け、意外な良サイトを発見するための実装と考え方を解説する。

## この記事を読むべき理由
日本でも個人運営の技術ブログ、地元コミュニティ、趣味プロジェクトなど“small web”は健在で、探索手法を知れば新しい情報源やデザインのインスピレーションを得られる。人気指標に偏らない発見の方法はプロダクト探索やキュレーションにも使える。

## 詳細解説
- 背景：一般に「人気＝良さ」ではない。Common Crawl やトップランキングは大量のトラフィックを示すが、本当にユニークで質の高いコンテンツは小規模なドメインやニッチなページに多い。この記事の狙いはその「small web」を効率的に可視化・探索すること。

- ワークフロー（概観）：
  1. ドメイン集合の収集（著者は別途収集ロジックを持つ）。
  2. 各サイトのスクリーンショットを撮影（ヘッドレスブラウザで自動化）。
  3. 画像から視覚埋め込み（embedding）を生成。
  4. 次元削減とクラスタ割当て。ここで自己組織化マップ（SOM）を採用して「レイアウト的な近接性」を保ちながら配置する。

- 技術的ポイント：
  - 埋め込み選択：最新の大規模自己教師ありモデル（例：DinoV3）は高次元で多くの情報を持つが、ウェブの「美的/レイアウト」特徴だけを取り出したい場合は過学習気味。そこで小さめのエンコーダにトリプレット損失を適用して64次元程度に圧縮すると、色・レイアウトなどの高レベルな違いを効率よく表現できる。
  - SOMの利点：SOMは局所的な近接性（Best Matching Unit を中心に近傍のノードを同時に更新）を保ちながら配置するため、視覚的に連続した地図が得られる。SOM の基本は学習率と近傍関数の減衰を持つ反復更新であり、実装は極めてシンプル。
  - 近傍（theta）関数の例：$$\theta = \exp\left(-\left(\frac{\mathrm{dists}}{\sigma}\right)^2\right)$$
  - 実装スニペット（PyTorch風、概念の短縮版）：

```python
# python
@torch.no_grad()
def som_step(alpha, sigma):
    # ランダムにサンプルを選択
    idx = np.random.randint(0, x.shape[0])
    sample = torch.from_numpy(x[idx]).to(DEVICE)  # 埋め込みベクトル

    # 全ノードとコサイン類似度で比較してBMUを選択
    bmu_flat = torch.argmax(torch.nn.CosineSimilarity(dim=2)(sample, W).flatten())

    # flat index -> 2D座標
    ui = bmu_flat // W.shape[1]
    uj = bmu_flat % W.shape[1]

    # BMUから全ノードへの格子距離を計算
    dists = torch.sqrt((W_i - ui)**2 + (W_j - uj)**2)

    # 近傍影響度（theta）を適用して重み更新
    theta = torch.exp(-(dists / sigma)**2)
    W.add_((theta * alpha).unsqueeze(2) * (sample - W))
```

- 実務上の注意点：
  - スクリーンショット取得は Playwright / Puppeteer / Selenium が実用的。動的要素や遅延読み込みをどう扱うかで見た目が大きく変わるため待機戦略が重要。
  - 埋め込み学習はトリプレットの正/負サンプル設計が肝。色やレイアウトを強めに学習させたいなら、色差を考慮したサンプル生成や別途色ヒストグラムの損失追加が有効。
  - SOM のサイズ（ノード数）と格子形状は可視化目的に合わせて調整。縦長・横長の地図で発見しやすさが変わる。

## 実践ポイント
- 今すぐ試す流れ（優先度順）：
  1. 小規模なドメインリスト（日本語ブログ、技術ノート、同人/ローカルサイト）を手作業で数千件集める。
  2. Playwright でスクリーンショットを一括取得（レスポンスの待機や viewport を固定）。
  3. ResNet など軽量エンコーダに triplet loss を適用して 64 次元へ圧縮。
  4. PyTorch で SOM を実装してマップ上に埋め込みを配置。得られた地図を眺めて、視覚的に興味深い領域をピックアップする。
- 運用上のヒント：
  - 「人気でフィルタしない」ために、被リンク数やトラフィック指標を使わずに候補を選ぶか、意図的に低指標のサイトを混ぜる。
  - 日本市場向けにはローカル文字フォント・文字列の見え方（文字サイズ・行間）も視覚特徴に影響するため、スクリーンショットのフォントレンダリングを統一すると比較が楽になる。

## 引用元
- タイトル: One million (small web) screenshots
- URL: https://nry.me/posts/2025-10-09/small-web-screenshots/
