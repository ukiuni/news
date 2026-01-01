---
layout: post
title: "Sorting with Fibonacci Numbers and a Knuth Reward Check - フィボナッチ数でソートしてKnuthの報奨小切手をもらった話"
date: 2026-01-01T10:37:28.619Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://orlp.net/blog/fibonacci-sort/"
source_title: "Sorting with Fibonacci Numbers and a Knuth Reward Check"
source_id: 475096830
excerpt: "短い実装のShellsortがフィボナッチギャップで性能改善しKnuthの報奨を得た経緯"
---

# Sorting with Fibonacci Numbers and a Knuth Reward Check - フィボナッチ数でソートしてKnuthの報奨小切手をもらった話
フィボナッチで加速する“超ミニ”Shellsort：なぜ単純なギャップ列で $O(n^{4/3})$ が出るのか

## 要約
極めて短い実装の Shellsort（著者は「fibonacci_sort」と命名）が、フィボナッチ数列に基づくギャップ列 $$k_i = F_i \cdot F_{i+1}$$ を使うことで最悪計算量 $O(n^{4/3})$ を達成する、という話とその背後にある数論的な証明スケッチを紹介する記事です。

## この記事を読むべき理由
- Shellsort は実装が簡潔でメモリに優しく、組み込み系や教育用途で魅力が高い。  
- フィボナッチ数の「インデックスの最大公約数が値の最大公約数になる」性質 $\gcd(F_a,F_b)=F_{\gcd(a,b)}$ がアルゴリズム性能に直結する面白い接点を示す。  
- 実務で使うアルゴリズム選定や競プロ、組み込み最適化の観点で新たな視点が得られる。

## 詳細解説
まず実装は非常に短く、Python 表記だと次のようになります。

```python
def fibonacci_sort(v):
    a, b = 1, 1
    while a * b < len(v): a, b = b, a + b
    while a > 0:
        a, b = b - a, a
        g = a * b
        for i in range(g, len(v)):
            while i >= g and v[i - g] > v[i]:
                v[i], v[i - g] = v[i - g], v[i]
                i -= g
```

ポイントを分解すると：

- これは Shellsort の一種：複数のギャップ $k$ で配列を部分的にソート（$k$-sorting）して順序を蓄積していく手法です。小さなギャップのとき、各要素は既にほぼ正しい位置にあるため挿入ソートが効率的に働きます。  
- 挿入ソートは「各要素が最終位置から最大 $m$ だけ離れている」なら $O(nm)$。Shellsort はギャップ列を工夫して $m$ を抑え、全体の最悪時コストを下げます。  
- ここで決め手になるのが数論的議論：複数のギャップ列 $\{k_i\}$ の組合せが十分に「表現力」を持てば、ある閾値以降の遠方にある要素対は正しい相対順序が保証され、挿入ソートの局所的コストが定数級に抑えられます（Frobenius/コイン問題の考え方）。  
- 著者が選んだギャップ列は $$k_i = F_i F_{i+1}$$。フィボナッチの性質から、隣接する $k_i$ の組が「独立（線形結合で表せない）」であることが示せ、Johnson/Sedgewick の既存の上界結果を適用すると最終的に $O(n^{4/3})$ の上界が得られます。  
- 技術的核はフィボナッチ数の次の性質です：まず加法公式 $$F_{n+m}=F_{n+1}F_m+F_nF_{m-1}$$ を用い、さらに $F_n \mid F_{kn}$（すなわち $F_{kn}\equiv0\pmod{F_n}$）や隣接項が互いに互除的（$\gcd(F_n,F_{n+1})=1$）であることを示します。これを Euclid の互除法の操作に沿って組み合わせると、インデックスでの $\gcd$ が値での $\gcd$ に対応すること、すなわち
$$\gcd(F_a,F_b)=F_{\gcd(a,b)}$$
が導かれます。これがギャップ列の独立性や Frobenius の境界推定に効き、計算量解析を可能にします。  
- 余談として、著者はこの解析の過程で Donald Knuth の小切手（報奨小切手）を手にするエピソードを述べています。これはアルゴリズム系の文化的トリビアとして興味深い点です。

## 実践ポイント
- 小規模でメモリ制約のある環境（組み込み、ファームウェア）では、簡潔な Shellsort の実装は有力な選択肢。フィボナッチギャップ列を試す価値あり。  
- 一方、汎用ライブラリ置き換え（std::sort 等）や並列化が必須の場面では向かない。安定性も保証しない点に注意。  
- 検証：ランダムと最悪入力（逆順など）でベンチを行い、実測での定数項やキャッシュ振る舞いを確認すること。  
- 学習用途：Shellsort と数論（Frobenius 問題、フィボナッチの $\gcd$ 性質）を結びつける教材として非常に良い題材。競技プログラミングでの洞察にも使える。

## 引用元
- タイトル: Sorting with Fibonacci Numbers and a Knuth Reward Check  
- URL: https://orlp.net/blog/fibonacci-sort/
