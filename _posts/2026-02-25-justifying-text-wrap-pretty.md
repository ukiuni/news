---
layout: post
title: "Justifying Text-Wrap: Pretty - text-wrap: pretty と段落整形の落とし穴"
date: 2026-02-25T02:41:55.257Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://matklad.github.io/2026/02/14/justifying-text-wrap-pretty.html"
source_title: "Justifying text-wrap: pretty"
source_id: 47077215
excerpt: "Safariのtext-wrap: prettyとjustify併用で単語間が異様に広がる原因と対処"
---

# Justifying Text-Wrap: Pretty - text-wrap: pretty と段落整形の落とし穴
Safariが実装した“綺麗な折り返し”なのに、なぜ単語間スペースが大きくなるのか？

## 要約
2025年、SafariがCSSの新機能 text-wrap: pretty をまともに実装したが、text-align: justify と組み合わせると単語間の空白が異様に広がる問題がある。原因は行割り当ての「賢い」アルゴリズムと整列処理の相互作用にある。

## この記事を読むべき理由
ブラウザの行割り（wrap）挙動は読みやすさに直結します。日本語ページは英語混在や見出し・キャプションで欧文の扱いが必要になる場面が多く、今回の問題を知っておくと見栄えの不具合を未然に防げます。

## 詳細解説
- 貪欲法 vs 最適化  
  典型的な折り返しは「次の単語が入れば同じ行に入れる（貪欲）」だが、これだと行長のバラつきが目立つ。TeX の Knuth–Plass は動的計画法で行割りを最適化し、美しい段組を実現した。
- ブラウザ特有の課題（オンライン変動）  
  印刷は固定幅で一度最適化すれば良いが、ブラウザはウィンドウ幅が変わる「オンライン」環境。これを動的に扱う必要があるため実装が難しい。
- Safari の text-wrap: pretty の挙動  
  実装は各行が目標幅に近づくようスコアリングして行割りを選ぶ。安定性のため「目標幅を段落幅よりわずかに狭く」設定し、行がやや短めに終わる余地を作る設計にしている。
- 問題の本質：整列（justify）との食い違い  
  text-align: justify は行を段落幅いっぱいまで伸ばして余白を均等化する。動的計画法が「意図的に短め」に割った結果を justify で伸ばすと、各行の余白が大きく膨らんでしまう。つまり「スマートな折り返し」が justify と組むと逆効果になるケースがある。

## 実践ポイント
- 当面の回避策  
  - 英文段落で text-wrap: pretty を使うときは text-align: justify を避け、text-align: left/start にする。  
  - どうしても両立させたいなら Safari での見え方を個別に調整（メディアクエリやベンダープレフィックスで振り分け）する。  
- レイアウト設計上の注意  
  - 最大幅（max-width）を調整して行数が変わらない幅で表示を固定すると、折り返しの影響を抑えられる場合がある。  
  - 英語長文はハイフネーション（hyphens）や word-spacing の調整で余白挙動を改善できることがある。  
- 日本語特有の観点  
  - 日本語は単語間スペースを基本としないため justify の問題は直接発生しにくいが、英語混在ページやコード・引用ブロックがある場合は影響を受けやすい。混在コンテンツは個別にスタイルを分けるのが堅実。  
- 今後の対応  
  - WebKit 側での修正を待つ（既報のバグ報告に注目）か、必要なら自分のサイトでフォールバック（justify を切る等）を用意する。

短く言えば：text-wrap: pretty は段落の「見た目」を良くする可能性があるが、text-align: justify と組み合わせると現状では単語間スペースが大きくなりやすい。サイトの表示をチェックして、必要なら justify をオフにするのが現実的な対応です。
