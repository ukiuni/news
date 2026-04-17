---
layout: post
title: "The Maths behind Python Dictionary probing - Python辞書プロービングの数学"
date: 2026-04-17T07:46:16.076Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.akshayxml.com/blog/python-dict-probing/"
source_title: "The Maths behind Python Dictionary probing | Akshay M"
source_id: 359563785
excerpt: "Python辞書は5と右シフト5の工夫で衝突を避け高速探索する裏側を解説"
---

# The Maths behind Python Dictionary probing - Python辞書プロービングの数学
Python辞書の衝突回避は「5」とビットシフトに隠された理由

## 要約
Pythonの辞書は衝突解決に疑似乱数的なプロービング式
$i = (5 \times i) + 1 + perturb$（かつ $perturb \mathrel{>>}=5$）
を使い、高速かつメモリ効率よく全スロットを探索する工夫をしている。

## この記事を読むべき理由
辞書はあらゆるPythonプログラムの基盤。なぜ「5」や「右シフト5」が選ばれたかを知ると、ハッシュ衝突や性能問題の原因が理解でき、実装／チューニング時の判断が的確になる。

## 詳細解説
- プロービング式  
  探索は疑似乱数列（線形合同生成器）を利用して行われる：
  $$
  i_{n+1} = (5 \times i_n) + 1 + perturb,\quad perturb \mathrel{>>}=5
  $$
  最初の $i$ はハッシュ値から得た初期インデックス、$perturb$ はハッシュ値で開始し各反復で右に5ビットシフトされる。

- なぜ線形合同生成器（LCG）か  
  LCGは「見かけは乱数」の巡回列を作る。全スロットを一巡できる条件はHull–Dobellの定理で示される。一般形：
  $$
  X_{n+1} = (a X_n + c) \bmod m
  $$
  条件：cとmが互いに素、$a-1$が$m$の素因子を満たす、さらに$m$が4で割り切れれば$a-1$は4で割り切れること。Pythonのテーブルサイズは$m=2^k$なので素因子は2のみ。最小の$a$として$a=5$が選ばれる。

- +1 の役割  
  $+1$ がないと $perturb$ が0になった後に $i=0$ が固定点になり得るため、探索が停止するリスクを避ける。

- perturb と右シフト5の意味  
  同一バケットに衝突するキー群（セカンダリクラスタリング）に対して、$perturb$（初期ハッシュに依存）を加えることで各キーのプローブ列を分岐させる。一方で高ビットが早期反映されるように右シフトは「バランス」を取る。5ビットは実験的に良い折衷とされた（ソースコードの設計コメントによる）。

- Modern Python（3.6+）の注意点  
  以降の辞書は「エントリ配列（密）」と「インデックス配列（疎）」に分離され、上のプロービングは疎インデックス上で動く。これにより順序保持とメモリ効率が両立する。

## 実践ポイント
- 普通のPython開発では辞書を信頼して使うべき。だが大量の衝突が疑われる場合はキーのハッシュ分布を確認する（カスタム __hash__ の検討や別構造を検討）。
- ハッシュテーブルを自作するなら：$m$ を $2^k$ にするなら Hull–Dobell の条件を満たす $a,c$ を選ぶ（例：$a=5, c=1$ は有効）、および高ビットを取り込む工夫（perturb 相当）を入れる。
- パフォーマンス調査時はプローブ回数や辞書の負荷率（load factor）を計測し、再ハッシュ戦略を検討する。

（元記事：Akshay M「The Maths behind Python Dictionary probing」）
