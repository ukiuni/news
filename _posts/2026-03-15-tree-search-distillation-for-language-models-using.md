---
layout: post
title: "Tree Search Distillation for Language Models Using PPO - PPOを使った言語モデルへの木探索蒸留"
date: 2026-03-15T02:20:09.565Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ayushtambde.com/blog/tree-search-distillation-for-language-models-using-ppo/"
source_title: "Tree Search Distillation for Language Models using PPO"
source_id: 47383059
excerpt: "木探索をPPOで蒸留し、小型モデルの算術推論を mean@16=11.3% に改善"
---

# Tree Search Distillation for Language Models Using PPO - PPOを使った言語モデルへの木探索蒸留
木探索で「考え方」を学ばせ、小さな言語モデルの推論精度を引き上げる手法

## 要約
木探索（Tree Search／MCTS）で見つけた強い推論経路をオンラインPPO（CISPO）で蒸留すると、単発生成時の算術的推論（Countdown）で改善が確認された（Qwen‑2.5‑1.5Bで mean@16 = 11.3%）。

## この記事を読むべき理由
言語モデルの「より良い推論」を得る手段はトークン単位の強化学習だけではない――探索で得た頑健な思考経路をモデルに教え込むことで、小型モデルでも目に見える性能向上が期待でき、日本のプロダクトや研究で計算資源を工夫して性能を稼ぎたい場面に有用です。

## 詳細解説
- 背景と目的  
  AlphaZero型の「推論時探索＋蒸留」を言語モデルに適用できるかを検証。言語はトークン単位だと枝分かれが無駄に増えるため、Tree‑of‑Thoughtsの考え方で「ステップ単位（連続トークン列）」を木のノードにする。

- 環境とデータ  
  タスクはCountdown（4つの整数から与えられた目標を+,-,*,/で作る）を20,000問で学習、評価は820問。基礎モデルは Qwen‑2.5‑1.5B‑Instruct。

- MCTS実装上の工夫  
  - ノード＝1つの推論ステップ（<step>…</step>）、終端が<answer>。  
  - 各葉からK個のシーケンスを生成して「シーケンス単位」の行動空間を構築。シーケンスの合計対数確率をsoftmaxしてpUCTの事前確率に使用（生確率の積は数値不安定）。  
  - 並列MCTS（Nエージェントが同一木を共有）＋仮想損失（virtual loss）で分岐の多様性確保。  
  - 価値ヘッドはトランスフォーマーの最終隠れ状態→MLP→tanhで実装し、探索のガイダンスに利用。

- 軌跡選択と蒸留（オンラインPPO/CISPO）  
  - MCTSをM反復行い、最終的にルートの訪問回数最大で軌跡を選択して共有バッファへ。  
  - トレーナーがバッファを引き、AdamWで1ステップのPPO（CISPO）更新を行う。損失は以下の合成：
$$
L_{total} = c_{ppo} L_{ppo} + c_{value} L_{value} + c_{KL}\, \mathbb{D}_{KL}(\pi_\theta \mid\mid \pi_{ref})
$$
$$
L_{value} = \mathbb{E}\left[(V(s_t)-r)^2\right]
$$
CISPOの形は著者式でトークンごとの advantage を用いる（端末報酬を各トークンに割当て）。KLは DeepSeek‑R1 の近似式を採用：
$$
\mathbb{D}_{KL}(\pi_\theta \mid\mid \pi_{ref}) = \frac{\pi_\theta}{\pi_{ref}} - \log\frac{\pi_\theta}{\pi_{ref}} - 1
$$

- インフラとハイパーパラメータ（要点）  
  8×H100、ジェネレータ6GPU／トレーナ2GPUの分担。MCTSではN=16ワーカー、K=4完了、M=100反復。比較対象はCISPO（GRPO系）と Best‑of‑N（N=64）。

- 結果（要旨）  
  評価は mean@16（各プロンプト16回生成して0/1評価を平均）。MCTS蒸留は11.3%、CISPOは8.4%、Best‑of‑Nは7.7%。小モデル実験である点に注意。

## 実践ポイント
- Tree‑of‑Thoughts的に「ステップ＝行動」に切り替えると探索の効率が上がる。  
- 訓練時は密報酬（例：$$r=1.0-2\cdot\min\!\left(\frac{|t-p|}{t},1.0\right)$$）で安定化、評価は0/1の疎報酬で直感的に見る。  
- 並列MCTS＋仮想損失で探索多様性を稼ぐ。ノード事前確率はシーケンスの合算対数確率をsoftmaxにかけるのが実装上安定。  
- 探索で得た軌跡をオンラインPPO（CISPO）で蒸留することで、「探索なしでも」性能向上が得られる。  
- 小型モデルや限られたGPU予算で試す価値あり。MCTSの反復数や並列ワーカー数は重要な「つまみ」なのでまずこれを増減して効果を確認する。

興味があれば、まずは小問目のデータ（Countdown類似）でK=4, N=8程度の並列MCTS＋オンラインPPOをプロトタイプで回すことを推奨します。
