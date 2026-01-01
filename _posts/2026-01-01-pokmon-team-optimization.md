---
layout: post
title: "Pokémon Team Optimization - ポケモンチーム最適化"
date: 2026-01-01T08:37:22.164Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nchagnet.pages.dev/blog/pokemon-team-optimization/"
source_title: "Pokémon Team Optimization"
source_id: 46401763
excerpt: "MIPでポケモン6体の最適チームを自動生成、耐性を網羅して基礎値最大化をPuLPで実装解説"
---

# Pokémon Team Optimization - ポケモンチーム最適化
大人の“無駄なこだわり”を数理最適化でやり切る──ポケモン6体編成をMIPで自動生成する方法

## 要約
数理最適化（Mixed-Integer Programming, MIP）を使って「総合ベースステータスを最大化しつつ、すべてのタイプに対して耐性を持つポケモンをチームに含める」問題を定式化・実装した事例。PuLPでモデル化して解く流れを解説します。

## この記事を読むべき理由
日本のエンジニアにとって、この手法はゲーム趣味の延長に留まらず、物流やスケジューリングで使うORの実務技術を楽しく学べる導入教材になります。実データ（Kaggle）を使えば短時間で試作可能です。

## 詳細解説
問題設定（簡潔化）
- 目的：チームの総ベースステータスを最大化する。各ポケモン n に対しベース値 b_n。
- 制約：チームは1〜6体、各タイプ A に対して「耐性を持つポケモンが少なくとも1体いる」こと。
- 変数：選択を表す二値変数 $x_n\in\{0,1\}$（ポケモン n を選ぶか）。

基本的なMIP定式化は
$$
\max_x \sum_n b_n x_n
\quad\text{subject to}\quad
1 \le \sum_n x_n \le 6,\quad x_n\in\{0,1\}.
$$

LPの緩和とBranch-and-Bound
- 整数制約を外すと線形計画（LP）になり、単体法などで容易に解ける。整数解でなければ分枝限定（branch-and-bound）で整数性を復元するのが定石。

タイプ耐性制約と非線形性の対処
- 「ある選択されたポケモンがタイプAに耐性」を表す条件は min や論理和に相当し非線形。ここで大きな定数Mを使うビッグMトリックと補助変数で線形化する。

補助変数の役割
- $y_{An}\in\{0,1\}$：ポケモン n がタイプAに耐性条件を満たす「候補」とするフラグ（耐性判定を満たすなら1になるよう制約）。
- ビッグM式（例）：
  $$
  x_n t_{An} + M(y_{An}-1) \le 0.5
  $$
  ここで $t_{An}$ はタイプAがポケモンnに与えるダメージ倍率（≤0.5 なら耐性）。
- しかし $y_{An}=1$ が選ばれてもそのポケモンがチームに入っていない可能性があるため、論理積を表す $z_{An}$ を導入：
  $$
  z_{An}\le x_n,\quad z_{An}\le y_{An},\quad z_{An}\ge x_n+y_{An}-1.
  $$
  これにより $z_{An}=x_n\land y_{An}$ が実現され、タイプAに対してチーム内に耐性を持つポケモンがいることを
  $$
  \sum_n z_{An} \ge 1
  $$
  で保証できます。

実装ポイント（PuLP）
- 変数定義は二値変数の辞書として作り、目的関数と制約を prob += ... で追加する。
- 解は pulp.value(var) で参照。

簡易的なPuLPスニペット（要点のみ）:

```python
# python
import pulp

def solve_pokemon_team(number_pkmn, number_types, types_matrix, pkmn_base_stat, team_size=6):
    prob = pulp.LpProblem("Pokemon_Team_Optimization", pulp.LpMaximize)
    x = pulp.LpVariable.dicts("x", range(number_pkmn), cat="Binary")
    y = pulp.LpVariable.dicts("y", (range(number_types), range(number_pkmn)), cat="Binary")
    z = pulp.LpVariable.dicts("z", (range(number_types), range(number_pkmn)), cat="Binary")

    # 目的
    prob += pulp.lpSum(pkmn_base_stat[i] * x[i] for i in range(number_pkmn))

    # チームサイズ制約
    prob += pulp.lpSum(x[i] for i in range(number_pkmn)) == team_size

    # タイプ耐性（ビッグMは十分大きく）
    M = 1000
    for a in range(number_types):
        for i in range(number_pkmn):
            prob += x[i] * types_matrix[a][i] + M * (y[a][i] - 1) <= 0.5
            prob += z[a][i] <= x[i]
            prob += z[a][i] <= y[a][i]
            prob += z[a][i] >= x[i] + y[a][i] - 1
        prob += pulp.lpSum(z[a][i] for i in range(number_pkmn)) >= 1

    prob.solve()
    return [i for i in range(number_pkmn) if pulp.value(x[i]) == 1]
```

制約簡略化の影響と拡張案
- 元記事は「ベースステータスのみ」「技の可用性・STAB・物理/特殊の分離等は無視」といった簡略化を行っている。これらを取り込むと実務的により現実的なチーム設計が可能だが、変数・制約が増え計算負荷が上がる。
- 実運用ではOR-Toolsや商用ソルバー（CPLEX/Gurobi）も選択肢。

## 実践ポイント
- まずはデータを整える：種族値とタイプ耐性行列があれば同様のMIPモデルをすぐ試せる（Kaggleのデータセットが実用的）。
- モデルは段階的に複雑化する：まずはベースステで検証 → 技や相手タイプ分布、重みづけ（対戦でよく見る相手に強くする）を追加。
- 計算負荷が増えたら：LP緩和で上界を確認、ヒューリスティックで初期解を与える、ソルバーの切り替えを検討。
- 教育用途として有用：ゲーム題材でORの基本（LP、MIP、ビッグM、分枝限定）を学ぶのは非常に効果的。

## 引用元
- タイトル: Pokémon Team Optimization
- URL: https://nchagnet.pages.dev/blog/pokemon-team-optimization/
