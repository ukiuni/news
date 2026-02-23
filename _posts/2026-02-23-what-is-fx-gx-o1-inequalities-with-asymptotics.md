---
layout: post
title: "What is f(x) ≤ g(x) + O(1)? Inequalities With Asymptotics - f(x) ≤ g(x) + O(1) とは何か？"
date: 2026-02-23T23:47:16.725Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jamesoswald.dev/posts/bigoinequality/"
source_title: "What is f(x) ≤ g(x) + O(1)? Inequalities With Asymptotics · James Oswald"
source_id: 47088076
excerpt: "$+O(1)$は差の上下を区別する重要表記、片側不等式の誤解を具体例で解説"
---

# What is f(x) ≤ g(x) + O(1)? Inequalities With Asymptotics - f(x) ≤ g(x) + O(1) とは何か？
思わず読みたくなるタイトル: 「“+ O(1)” の本当の意味：片側不等式 f(x) ≤ g(x) + O(1) を初級者にもすっきり解説」

## 要約
$f(x)=g(x)+O(1)$ は差が定数で抑えられることを意味し、$f(x)\le g(x)+O(1)$ はその「上側」だけを抑える一方通行の意味を持つ。片側不等式は等式表示より弱く、しばしば誤解されやすい。

## この記事を読むべき理由
理論計算機科学や圧縮・Kolmogorov複雑性の文献でこの表記は頻出。日本の学生やエンジニアが論文や教科書を正確に読み解くために、この違いを押さえておくと誤解を避けられる。

## 詳細解説
まず標準の Big‑O の定義：
$$
f(x)=O(g(x)) \iff \exists C>0,\ \exists x_0,\ \forall x>x_0,\ |f(x)| \le C|g(x)|.
$$
これを差分で使うと
$$
f(x)=g(x)+O(1)
$$
は
$$
\exists C>0,\ \exists x_0,\ \forall x>x_0,\ |f(x)-g(x)|\le C
$$
すなわち $f(x)$ と $g(x)$ の差が上にも下にも定数で抑えられることを意味します（絶対値が重要）。一方で
$$
f(x)\le g(x)+O(1)
$$
は「一方の不等式」だけを主張します。形式的には
$$
\exists C>0,\ \exists x_0,\ \forall x>x_0,\ f(x)\le g(x)+C.
$$
このため $f(x)=g(x)+O(1)$ が成り立てば自動的に $f(x)\le g(x)+O(1)$ も成り立ちますが、逆は必ずしも真ではありません。簡単な例：

- 等式成立の例: $f(x)=\sin x,\ g(x)=0$ は $|f(x)-g(x)|\le1$ なので $f(x)=g(x)+O(1)$。
- 片側のみ成立する例: $f(x)=-x,\ g(x)=0$ は若い $x$ でも $-x\le C$ が成り立つため $f(x)\le g(x)+O(1)$ だが、差 $f-g=-x$ は下に発散するので $f(x)=g(x)+O(1)$ ではない。

議論は $O(1)$ を任意の関数 $O(h(x))$ に置き換えても同様で、片側／両側の区別が同じように重要になります。

## 実践ポイント
- 論文や教科書で $+\!O(1)$ が出てきたら、「絶対値（両側）か片側か」をまず確認する。
- 証明を書くときは不等式を差として書き換え、必要なら絶対値で上下を明示する。
- アルゴリズム解析やKolmogorov複雑性の境界（定数項の扱い）で結果の強さを判定するとき、この違いで主張の可否が変わることを意識する。
