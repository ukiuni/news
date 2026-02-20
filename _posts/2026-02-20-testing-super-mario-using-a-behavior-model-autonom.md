---
layout: post
title: "Testing Super Mario Using a Behavior Model Autonomously - 振る舞いモデルでスーパーマリオを自律的にテスト"
date: 2026-02-20T19:29:02.846Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://testflows.com/blog/testing-super-mario-using-a-behavior-model-autonomously-part1/"
source_title: "Testing Super Mario Using a Behavior Model Autonomously (Part 1) | TestFlows"
source_id: 47092348
excerpt: "AIが無人で発見的にマリオを攻略、遺伝的探索で膨大な状態空間を効率探索する手法"
image: "https://testflows.com/images/testing-super-mario-using-a-behavior-model-autonomously-part1.png"
---

# Testing Super Mario Using a Behavior Model Autonomously - 振る舞いモデルでスーパーマリオを自律的にテスト
AIが無人でマリオを“発見的に”クリアする──遺伝的探索で巨大な状態空間を効率的に探る方法

## 要約
ランダム変異で入力列を生成し、ゲームの決定性を利用して「再生→変異→評価」を繰り返すことで、スーパーマリオのレベルを自律的に攻略する手法を紹介する。これは事実上の遺伝的アルゴリズム（GA）で、少ないルールで広大な状態空間を探索する。

## この記事を読むべき理由
自動化テストやゲームAI、組み込みソフトの検証で「人手では追い切れない状態」をどう探索するかは日本の開発現場でも重要な課題。この記事で紹介する単純かつ再現可能な手法は、ゲームQAだけでなく、決定性のあるシステム検証やファジングにも応用可能だ。

## 詳細解説
- 入力表現と変異  
  ゲーム操作（右・左・ジャンプなど）を1バイトのビットで表し、各フレームごとに低確率でビットを反転（XOR）することで入力列を生成する。典型的な反転確率は約 $10\%$（あるいは探索用に$5\%$）で、現在押しているキーが次フレームでも維持される挙動を自然に模倣する。

  ```python
  # Python
  import random
  def generate_input(starting_byte, flip_prob, length):
      inputs = []
      next_byte = starting_byte
      for _ in range(length):
          for j in range(8):
              if random.random() < flip_prob:
                  next_byte ^= (1 << j)
          inputs.append(next_byte)
      return inputs
  ```

- パス（入力列）の保存と再生  
  ゲームが決定性であるため、同じ入力列を再生すれば必ず同じ状態に到達する。したがって「到達した入力列＝状態への道筋」を保存し、そこから変異を加えて延長することで探索を継続できる。

- 選択とスコアリング  
  単純な評価指標はx座標の進行量（右方向）。ただし常に最高スコアを選ぶと行き止まりにハマるため、多様性を保つ確率的選択が必要。指数重み付け（softmax）で確率を作るのが有効：
  $$
  P_i = \frac{e^{\alpha s_i}}{\sum_j e^{\alpha s_j}}
  $$
  ここで $\alpha$ を大きくすると有望パスを強く優先する。

- 世代ループ（選択→再生→変異→評価）  
  探索は「間隔（epoch）ごとに最良候補を選び、ある停止点まで再生してそこから複数回変異を試す」サイクルで進む。死に至ったパスは除去し、冗長なパスは定期的にクリーンすることで探索効率を維持する。

- GAとしての位置付け  
  - 個体＝入力列（パス）  
  - 適応度＝進行量（スコア）  
  - 変異＝ビット反転ベースの入力生成  
  - 交叉は使わない実装が多いが、交叉を導入すれば探索多様性をさらに高められる。  
  決定性があるため、再現性の高い進化実験が可能という利点もある。

## 実践ポイント
- リポジトリをクローンして動かす（元実装は Examples/SuperMario）。まずは手元で再現して挙動を観察する。  
  git clone --branch v2.0 --single-branch https://github.com/testflows/Examples.git && cd Examples/SuperMario
- 変異率（flip_prob）は $5\%-10\%$ 程度で調整。探索（fuzzy）と定型動作（move library）を混ぜると効率が上がる。  
- スコアはまずは x 進行量だけで十分。必要に応じて生存時間や得点も階層的に加える。  
- 選択は「ベスト優先だが確率的に他も試す」方式（指数重み付け）を採用する。  
- 実運用では「行き止まりの検出」「パスの冗長除去」「切り替え頻度（epoch）」のチューニングが鍵。  
- 発展案：交叉の導入、行動モデル（Part 2で示唆）によるリアルタイム検証や、日本のゲームQAワークフローへの組み込み。

短くまとめると、この手法は「単純な変異＋決定性の再生」で巨大な状態空間を体系的に探索する強力で実用的なアプローチであり、マリオ実験はその分かりやすいデモンストレーションである。
