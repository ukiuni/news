---
layout: post
title: "Simulation of \"The Ladybird Clock Puzzle\" - 「てんとう虫の時計パズル」のシミュレーション"
date: 2026-01-19T13:00:10.199Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://navendu.me/posts/ladybug-clock-puzzle/"
source_title: "The Ladybug Clock Puzzle | Navendu Pottekkat - The Open Source Absolutist"
source_id: 424234336
excerpt: "てんとう虫の時計で最後に塗られる数字が全て1/11になる理由を賭博者の破産で直感的に解説"
image: "https://navendu.me/images/the-ladybug-clock-puzzle/ladybug-banner.jpg"
---

# Simulation of "The Ladybird Clock Puzzle" - 「てんとう虫の時計パズル」のシミュレーション
直感を覆す確率のトリック：てんとう虫が12時からランダムに歩くと、最後に塗られる番号はなぜどれも同じ確率になるのか？

## 要約
てんとう虫が12の位置から隣接番号へランダムに移動していくと、最終的に最後まで残って塗られる番号（12を除く）はどの番号でも等しい確率で起こり、その値は $1/11$（約9.09%）になる。

## この記事を読むべき理由
直観に反する結果を、確率論（ランダムウォーク）と賭博者の破産問題（Gambler’s Ruin）の簡潔な考え方で理解できる。日本の学生やエンジニアが確率的思考、シミュレーション、面接問や授業ネタとして使える好例。

## 詳細解説
設定：12マスの時計を循環するグラフと考える。てんとう虫は12（位置0）から始まり、毎秒ランダムに隣の番号（時計回りか反時計回り）へ移動する。訪れたマスは赤で塗る。問題は「最後に赤くなるマスが6である確率は？」。

鍵は「最後に残るための必須経路」を観察すること：
- ある番号kが最後になるためには、まずkのどちらかの隣（k−1またはk+1）に初めて到達する必要がある（このときk自体はまだ未訪問）。
- その後、到達した隣から“反対側を長く回って”もう一方の隣に到達し、やっとkに戻ってくる。短い距離（1ステップ）でkに行ってはいけない。

これを賭博者の破産問題に対応させる。公平コインで1ドルずつ増減する賭けを、始値$x$から上下限$0$か$n$に到達するまで続けるとき、
$$
P(\text{reach } n \text{ before } 0 \mid \text{start at } x) = \frac{x}{n}
$$
となる。てんとう虫の場合、隣から「長い方へ回ってもう一方の隣に先に到達する確率」は、始点が「1」で目標が「11」に相当するため $\frac{1}{11}$ になる。最初にどちらの隣に行くかは同確率なので、合成しても
$$
P(k\ \text{is last})=\frac12\cdot\frac{1}{11}+\frac12\cdot\frac{1}{11}=\frac{1}{11}.
$$
この議論はどの番号$k\in\{1,\dots,11\}$にも同じ形で適用できるため、12を除く全ての番号が等確率で最後になる。一般化すれば、nマスの円環でスタート地点を1つ固定すると、残りの各マスの確率は
$$
P = \frac{1}{n-1}
$$
となる。

元記事はインタラクティブなシミュレーションも示しており、数万回の試行でこの理論値が収束する様子を視覚的に確認できる。

## 実践ポイント
- 手を動かして理解する：小さなシミュレーションを動かしてみると直感と結果のズレがよく分かる。以下は簡単な Python シミュレーション例（参考）。
```python
# python
import random, collections

def trial(n=12):
    pos=0
    visited=[False]*n
    visited[pos]=True
    remain=n-1
    while remain>0:
        pos = (pos + random.choice([-1,1]))%n
        if not visited[pos]:
            visited[pos]=True
            remain-=1
    return pos  # 最後に訪れた位置

def run(N=20000):
    c=collections.Counter(trial() for _ in range(N))
    for k in range(1,12):
        print(k, c[k]/N)
run()
```
- 教材・面接ネタに最適：ランダムウォーク、境界到達確率、対称性の考え方を説明する良い題材。視覚的なアニメーションと組み合わせると理解が深まる。
- 応用観点：同様の考え方はネットワーク上のカバータイムや探索アルゴリズム、ランダムサンプリングの直観検証に役立つ。

短くまとめると、このパズルは「遠い＝最後になりやすい」という直観を覆し、ランダムウォークの構造的対称性と賭博者の破産問題のシンプルな公式で簡潔に説明できる。日本の教育現場や技術コミュニティで取り上げる価値が高い良問である。
