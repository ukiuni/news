---
layout: post
title: "Are Two Heads Better Than One?"
date: 2025-12-26T04:07:01.135Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://eieio.games/blog/two-heads-arent-better-than-one/"
source_title: "Are Two Heads Better Than One?"
source_id: 1586274099
---

# [2人より1人？嘘つき2人が語る「増やしても意味がない」確率の罠]

## 要約
コイントスを見て20%嘘をつく友人が1人いると信頼して80%の正答率。もう1人を独立に追加しても、最良戦略では正答率は依然として$80\%$のまま変わらない、という逆説的な話。

## この記事を読むべき理由
センサー融合やアンサンブル学習、バイアスのある人間の報告を扱う設計では「情報を増やせば改善する」は常識だが、条件次第で期待が裏切られる。本稿は直感に反する簡潔な確率論と実践的示唆を日本のエンジニア向けに整理する。

## 詳細解説
設定：コインは表裏同確率、Alice と Bob は独立にそれぞれ嘘をつく確率 $p=0.2$（真実を言う確率 $q=1-p=0.8$）。Alice だけ聞いて「そのまま信じる」戦略で正答率は $q=0.8$。

Bob を追加して「観測パターンごとに最もありそうな結果を推定する（MAP）」戦略を採るとどうなるか。

観測パターンと確率（コインが表だった場合）：
- 両方が表と言う：$q^2 = 0.8^2 = 0.64$
- 両方が裏と言う：$(1-q)^2 = 0.04$
- 意見が割れる：$2q(1-q) = 0.32$

同様にコインが裏のときは表と裏が入れ替わる。両者が一致する場合（確率 $0.68$）は一致側が正しい可能性が高く、実際にそのときに正解となる確率は
$$
\frac{0.64}{0.64+0.04}=0.94.
$$
一方で意見が割れた場合は完全に無情報で確率 $0.5$ に戻る。

期待正答率は
$$
0.68\times 0.94 + 0.32\times 0.5 \approx 0.8.
$$
したがって、Bob を追加してもMAP による精度は変わらない。直感的には「同意した時は強い情報だが、割れた時は無情報になり、その平均が元と等しくなる」ため。

補足：3人目を入れて多数決にすれば改善する（$q=0.8$ のとき3人では約 $0.896$）――偶数人数で生じる「引き分け」が2人の場合にちょうど効いている。

## 実践ポイント
- センサー／アノテータが独立かつ同品質（対称ノイズ）で、事前が均等なケースでは偶数個の情報源が“無効化”することがある。設計時に偶数・奇数やタイブレーク戦略を意識する。
- 意見が割れたケースを別途扱う（追加質問、信頼度取得、外部情報参照）ことで、情報追加の効果を取り戻せる。
- 実務では独立性や誤報確率が均一でないことが多い。事前分布や個々の信頼度を使うベイズ融合が有効。

簡単なシミュレーション（Python）：
```python
# python
import random
def trial(n_friends=2, p_lie=0.2, trials=200_000):
    correct=0
    for _ in range(trials):
        is_head = random.random() > 0.5
        reports = []
        for _ in range(n_friends):
            lied = random.random() < p_lie
            report = (not is_head) if lied else is_head
            reports.append(report)
        # MAP: pick majority if decisive, else random
        heads = sum(reports)
        if heads > n_friends/2:
            guess = True
        elif heads < n_friends/2:
            guess = False
        else:
            guess = random.choice([True, False])
        if guess == is_head:
            correct += 1
    return correct / trials

print("1 friend:", trial(1))
print("2 friends:", trial(2))
print("3 friends:", trial(3))
```

## 引用元
- タイトル: Are Two Heads Better Than One?
- URL: https://eieio.games/blog/two-heads-arent-better-than-one/
