---
layout: post
title: "How the Lobsters front page works - Lobstersのフロントページはどう動くのか"
date: 2026-01-18T18:08:13.410Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://atharvaraykar.com/lobsters/"
source_title: "How the Lobsters front page works"
source_id: 46669996
excerpt: "投票・タグ・コメント・経過時間で決まるLobstersの「hotness」仕組みを噛み砕いて解説"
image: "https://atharvaraykar.com/content/images/2026/01/lobster-vintage-illustration-1.png"
---

# How the Lobsters front page works - Lobstersのフロントページはどう動くのか
前ページを制するのは何か？Lobstersの「hotness」アルゴリズムをやさしく分解する

## 要約
Lobstersのフロントページは投稿の「hotness」を計算して昇順で並べるシンプルかつ効果的な仕組みです。投票（ログスケール）、タグや自己投稿のボーナス、コメントの扱い、そして時間経過（年齢）が合わさって順位が決まります。

## この記事を読むべき理由
キュレーションやコミュニティ運営に関心がある日本の開発者やモデレーターにとって、このアルゴリズムは「どうして良い投稿が上がるのか／悪い議論が目立つのか」を理解する良い教科書です。Qiitaやはてなブックマーク、SNSでの露出設計にも応用できる考え方が詰まっています。

## 詳細解説
Lobstersはオープンソースで、フロントページ順位は次の式で決まります（数式はKaTeXで表記します）:

$$\textbf{hotness} = -1 \times (\text{base} + \text{order} \times \text{sign} + \text{age})$$

- hotnessが小さい（より負）ほど上位に来ます。ページはhotnessの昇順でソートされます。

各項の意味：
- base：タグごとの「hotness modifier」を合計した値（各タグは-10〜+10の範囲）。自己投稿には小さなブースト +0.25。
  $$\textbf{base} = \sum_{t \in \text{tags}} \text{hotness\_mod}_t + \begin{cases}0.25 & \text{if self-authored} \\ 0 & \text{otherwise}\end{cases}$$
  一部タグ（例：culture, rant）は初期ランクを下げるように負の修正が付く。

- order：投稿のエンゲージメントを表す項で、スコアとコメントの影響をログで表現。
  $$\textbf{order} = \log_{10}\left(\max\left(|\text{score} + 1| + \text{cpoints}, 1\right)\right)$$
  増加が対数的なので、0→100票の効果は1000→1100票の効果よりずっと大きい。

- cpoints（コメントポイント）：コメントのアップボートを考慮。ただしbaseが負の場合はコメントは無視され、かつcpointsは投稿スコアを超えないように制限される。
  $$
  \text{comment\_points} = \begin{cases}
  0 & \text{if } \text{base} < 0 \\
  \frac{1}{2}\sum(\text{comment\_scores} + 1) & \text{otherwise}
  \end{cases}
  $$
  $$\textbf{cpoints} = \min(\text{comment\_points}, \text{story\_score})$$
  これにより「低スコアだがコメントだけ多い炎上投稿」が不当に昇格するのを防ぐ設計。

- sign：投稿スコアの符号で、コメントやorderの影響を反転させる。
  $$\textbf{sign} = \begin{cases} -1 & \text{if score} < 0 \\ +1 & \text{if score} > 0 \\ 0 & \text{otherwise} \end{cases}$$

- age：投稿作成時のタイムスタンプをホットネス窓（hotness_window、既定22時間）で割った値。新しい投稿によって線形的に増える。
  $$\textbf{age} = \frac{\text{created\_at\_timestamp}}{\text{hotness\_window}}$$
  ageは線形成長、orderは対数成長なので、時間が経つと年齢が必ず勝つ設計です（永遠にフロントに残らない）。

設計上の狙い：
- 新着が一定時間チャンスを得られる。
- コメントだけで順位を不正に上げられない。
- 低品質で議論を煽る投稿を抑制しつつ、良質な高評価投稿は上がりやすい。
- しかしコミュニティの性質（モデレーションや参加者文化）がサイトの雰囲気を決めるとも著者は述べています。

## 実践ポイント
開発者・コミュニティ運営者向け：
- 露出アルゴリズム設計で「対数スケーリング」「コメント上限」「タグ修正」「時間窓」は有効な要素。炎上やゲリラ的な操作を抑える手段になる。
- hotness_window（例：22時間）を短くすると新着回転が速く、長くすると投稿が長居する。

一般ユーザー向け：
- 早い段階での良質なアップボートと建設的なコメントは投稿の命運を分ける。見かけた良記事には初動でリアクションを。
- タグ選びは意外に重要。ネガティブ修正があるタグは初動ハードルが上がる。
- 炎上狙いのコメントで順位を上げさせないために、健全な議論を心がけることがコミュニティを良くする近道。

Lobstersはアルゴリズムだけでなく、モデレーション方針と招待制で独自の文化を作っています。仕組みを理解すると、参加の仕方や自分の見せ方が変わり、結果的にコミュニティをより良くできるかもしれません。
