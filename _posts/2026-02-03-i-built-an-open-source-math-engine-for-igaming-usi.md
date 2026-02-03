---
layout: post
title: "I built an Open-Source Math Engine for iGaming using Python and PID Control - iGaming向けオープンソース数学エンジン（Python + PID制御）"
date: 2026-02-03T13:06:50.015Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Katunyu-Boonchumjai/The-Chamelot-Engine"
source_title: "GitHub - Katunyu-Boonchumjai/The-Chamelot-Engine: Advanced Slot Machine Math Engine with PID Controller for RTP Stability"
source_id: 410391077
excerpt: "PIDでRTPを安定化するPython製スロットMath Engineの実践解説"
image: "https://opengraph.githubassets.com/c9a8615b646ed906f8c962f029988a6495a23a9087328a30fda4bc127631609f/Katunyu-Boonchumjai/The-Chamelot-Engine"
---

# I built an Open-Source Math Engine for iGaming using Python and PID Control - iGaming向けオープンソース数学エンジン（Python + PID制御）

魅力的なタイトル: RTPをPIDで“制御”する！オープンソースのスロット用Math Engine「The Chamelot」で学ぶ実践制御テクニック

## 要約
Pythonで実装されたオープンソースのスロット向けRTP（Return to Player）安定化エンジン「The Chamelot」は、PID制御を用いて実稼働に近い乱高下（Black Swan）下でも目標RTPに収束させることを目指しています。

## この記事を読むべき理由
ゲーム開発やギャンブル系アルゴリズムに関心がある日本のエンジニアが、RTPの安定化という実務的課題に対する制御理論（PID）適用例を、実コード（Python）で学べるからです。カジノ系だけでなく、確率・報酬設計やバランス調整の考え方として国内ゲーム開発にも応用できます。

## 詳細解説
The Chamelotは次の流れでRTPを監視・調整します。

- 基本指標
  - 目標RTP: $$\text{RTP\_target} = \sum_i P_i \cdot V_i$$
  - ハウスエッジ: $$H = 1 - \text{RTP\_target}$$
  - 回転ごとのターンオーバー: $$T_n = \sum \text{Bet}_i$$
  - 目標利益: $$\text{Target}(n) = H \cdot T_n$$
  - 実際の利益: $$P_n = \sum (\text{Bet}_i - \text{Payout}_i)$$
  - 誤差（%）: $$e(n)=\frac{P_n - \text{Target}(n)}{T_n}\times 100$$

- PID制御
  - 誤差に対してPIDが制御信号 $u$ を計算し、非対称の範囲でクランプします：
    $$u_{\text{clamped}} = \max(-0.9,\ \min(2.0,\ u))$$
  - ウェイト（シンボル頻度など）を次のように更新：
    $$\text{weight}_{\text{new}} = \text{weight}_{\text{old}} \times (1 + u_{\text{clamped}})$$

- 実装と検証
  - 言語: Python 3.8+
  - 主要ファイル: core/rtp_engine.py（PIDロジック）、demo.py（Black Swan / Chaos / Soak シミュ）
  - Chaos Stress Test: 10,000スピンで90.0%目標RTPに高精度で収束するデモが含まれます。
  - 可視化: Matplotlibによるダッシュボード出力（output/recovery_dashboard.png等）

- ライセンスと用途
  - CC-BY-NC 4.0（商用利用不可・教育/研究向け）。商用利用は作者へ要連絡。

## 実践ポイント
- まずリポジトリをクローンして動かす:
```bash
pip install -r requirements.txt
python3 demo.py
```
- core/rtp_engine.pyでPIDゲインやクランプ範囲（現在は -0.9〜+2.0）を確認し、シミュで感触を掴む。
- 小規模な「Chaos」テスト（例: 1,000スピン）で挙動を観察してからパラメータ調整する。
- 国内向けにはギャンブル規制や倫理面を確認すること。実務で使う場合はライセンスと著者への商用許諾を必ず確認する。

元リポジトリ: Katunyu-Boonchumjai / The-Chamelot-Engine (教育・研究目的で読むことを推奨)
