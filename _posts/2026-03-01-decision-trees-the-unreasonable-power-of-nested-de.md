---
layout: post
title: "Decision trees – the unreasonable power of nested decision rules - 決定木 — ネストされた決定ルールの不合理なほどの力"
date: 2026-03-01T09:55:33.959Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mlu-explain.github.io/decision-tree/"
source_title: "Decision Trees"
source_id: 47204964
excerpt: "可視化できる決定木の直感と精度、枝刈りやランダムフォレストで実務的に安定させる方法を解説"
image: "https://mlu-explain.github.io/assets/ogimages/ogimage-decision-tree.png"
---

# Decision trees – the unreasonable power of nested decision rules - 決定木 — ネストされた決定ルールの不合理なほどの力

魅力的な日本語タイトル: 「なぜ“木”がわかりやすく強いのか？決定木で学ぶ直感×精度の秘密」

## 要約
決定木は特徴を順に分割することで直感的に分類／回帰を行う一方、深くしすぎると過学習と不安定性（高分散）に悩まされる。情報利得（エントロピー）や簡単な制約でそのバランスを取るのが肝心。

## この記事を読むべき理由
解釈性が求められる日本の業務（製造ラインの異常検知、与信判定、顧客セグメント）で決定木は強力な武器。だが適切な枝刈りやアンサンブル（例：ランダムフォレスト）を知らないと現場で使えない結果を招くため、基礎と実践の両方を押さえる価値があります。

## 詳細解説
- 基本動作：ルートから特徴に対する条件（if-then）で空間を分割し、葉で予測を返す。直感的で前処理が少ない点が利点。
- 分割基準：エントロピーで「純度」を測り、情報利得（Information Gain）を最大化する分割を選ぶ。エントロピーは
  $$H(S) = -\sum_i p_i \log_2 p_i$$
  情報利得は親ノードのエントロピーから子ノードの重み付き平均を引いて定義される：
  $$IG = H(\text{parent}) - \sum_k \frac{|S_k|}{|S|} H(S_k)$$
  Gini不純度は代替指標で、計算が速く実務でよく使われる。
- 学習アルゴリズム：ID3のように貪欲にトップダウンで最良分割を選び再帰的に構築する。停止条件（最大深さ、葉の最小サンプル数など）で枝刈りする。
- 問題点：訓練データの小さな摂動で構造が大きく変わる「不安定性」と、過度に深くすると訓練データのノイズを覚えてしまう「過学習」。これらを防ぐには枝刈りやアンサンブル（ランダムフォレスト）が有効。
- アンサンブルへの橋渡し：訓練データをランダム化して多数の木を作り予測を平均するランダムフォレストは、分散を下げて汎化性能を大きく改善する。

## 実践ポイント
- まずは見える化：小さなデータで木を可視化して分割ルールを理解する。
- 必須ハイパラ：max_depth（過学習防止）、min_samples_leaf（極端な分割防止）、criterion（"entropy"または"gini"）。
- 不均衡データ：class_weight='balanced' やサンプリングで対応。エントロピーは不均衡で慎重に振る舞う傾向あり。
- 安定化のためにランダムフォレストや勾配ブースティングを検討する。
- モデル確認：交差検証で汎化性能を評価し、特徴重要度と木のルールを業務担当者と照合する。

簡単な実例（scikit-learn）:
```python
# python
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

dt = DecisionTreeClassifier(max_depth=6, min_samples_leaf=10, criterion='entropy')
rf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=0)
dt.fit(X_train, y_train)
rf.fit(X_train, y_train)
```

以上を押さえれば、「見える」モデルとしての決定木を実務で安全に使い始められます。
