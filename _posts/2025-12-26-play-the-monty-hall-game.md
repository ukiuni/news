---
layout: post
title: Play the Monty Hall game - モンティ・ホール・ゲームをプレイする
date: 2025-12-26T19:30:44.059Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://monty.donk.systems"
source_title: "Play the Monty Hall game"
source_id: 1206870145
excerpt: "ブラウザで遊んで実感：ドアを替えると当選率が2倍になるモンティ・ホール実験"
---

# Play the Monty Hall game - モンティ・ホール・ゲームをプレイする

## 要約
海外のシンプルなブラウザゲーム「Play the Monty Hall game」を使って、モンティ・ホール問題の直感に反する答え——「替えると勝率が上がる」ことを体験的に確認できる。

## この記事を読むべき理由
日本でも面接問題やデータ解析の直感トレーニングとして頻出のモンティ・ホール問題。実際に操作できるデモ（AGPL-3.0）で感覚を掴み、確率的思考やA/Bテスト・意思決定設計に応用できるため、エンジニア／データサイエンティストに有益です。

## 詳細解説
モンティ・ホール問題のルールは簡単です：3つのドアのうち1つに賞品、残り2つはハズレ。プレイヤーが1つ選ぶと、司会者は賞品でない別のドアを開けてハズレを見せる。その後で「選択を替えるか？」と問われます。

直感では「残った2つで半々」と思いがちですが、数学的には替える方が有利です。理由は選択時の情報と条件付き確率にあります。

- 初回に当たりを選ぶ確率：$1/3$ → 替えると負け
- 初回に外れを選ぶ確率：$2/3$ → 司会者が別の外れを開けるので、替えると当たりを得る

したがって、
$P(\text{勝つ}|\text{替える}) = \tfrac{2}{3}$、$P(\text{勝つ}|\text{そのまま}) = \tfrac{1}{3}$

このサイト（簡易なASCII UIのインタラクション）は、繰り返し遊ぶことで上の確率が経験的に確認できるよう作られています。ソースはAGPL-3.0で公開されており、教育用途や自分で改変して挙動を観察するのにも向いています。

## 実践ポイント
- まずは何も考えずに「替える／替えない」をランダムに選んで100回以上プレイしてみると、勝率の差が実感できます。
- シミュレーションを自分で書いて検証する。小さなPythonスニペットで10000回試行すれば理論値に収束します。

```python
# python
import random
def trial(switch):
    prize = random.randrange(3)
    choice = random.randrange(3)
    # host opens a door that's not prize and not choice
    remaining = [d for d in range(3) if d!=choice and d!=prize]
    host_open = random.choice(remaining)
    # if switch, pick the other unopened door
    if switch:
        choice = [d for d in range(3) if d!=choice and d!=host_open][0]
    return choice==prize

for switch in (False, True):
    wins = sum(trial(switch) for _ in range(10000))
    print(f"switch={switch}: win_rate={wins/10000:.3f}")
```

- 教育や社内勉強会でデモとして使うと、確率・条件付き確率・ベイズ的思考の導入に適しています。UX的には「司会者が意図を持って情報を開示する」設計が、ユーザー判断に与える影響を考える良い題材になります。
- ライセンス（AGPL-3.0）と著作者（cyberia）に留意して、改変や再配布を行ってください。

