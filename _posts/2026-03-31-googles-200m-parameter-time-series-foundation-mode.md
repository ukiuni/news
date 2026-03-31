---
layout: post
title: "Google's 200M-parameter time-series foundation model with 16k context - Googleの16kコンテキスト対応・200Mパラメータ時系列基盤モデル"
date: 2026-03-31T05:57:22.558Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/google-research/timesfm"
source_title: "GitHub - google-research/timesfm: TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting. · GitHub"
source_id: 47583045
excerpt: "TimesFM 2.5は200Mで16k履歴を扱い現場向け高精度予測を実現"
image: "https://opengraph.githubassets.com/8f9e578462693f3d1aa9cd119b618d5d924eb7d966f5f238cc6c3fe0e9d0c1b3/google-research/timesfm"
---

# Google's 200M-parameter time-series foundation model with 16k context - Googleの16kコンテキスト対応・200Mパラメータ時系列基盤モデル
16kの長期コンテキストで“先読み”する実用派AI — TimesFM 2.5が時系列予測の常識を揺るがす

## 要約
Google ResearchのTimesFM 2.5は、パラメータを500Mから200Mに削減しつつ、コンテキスト長を2048から最大16,000に拡張。長期依存を扱う高精度な時系列予測を、より軽量かつ現場向けに提供します。

## この記事を読むべき理由
日本の企業・開発者にとって、金融市場、需要予測、エネルギー、製造の異常検知や予防保守など「長期の時系列」を精度高く扱うことは競争力直結。TimesFMは実運用で使える性能とAPI/BigQuery連携を備え、実装コストを下げる可能性があります。

## 詳細解説
- アーキテクチャ: デコーダーのみの「foundation model」を時系列向けに事前学習。自己回帰的に未来を生成する設計で、系列の長期依存を効率的に学習する。
- 主要アップデート（2.5）:
  - パラメータ: 500M → 200M（軽量化）
  - コンテキスト長: 2048 → 最大16k（長期履歴を活用可能）
  - 連続的な分位予測（continuous quantile）を最大1kステップ先まで対応可能にするオプションの30M分位ヘッド
  - 周波数インジケータを廃止し、前処理/正規化で柔軟に対応
  - 推論APIとドキュメントの改善、Flax（JAX）版で高速化予定
  - XReg経由で外部共変量（カレンダーやメタデータ）サポートを復活
- 運用面:
  - Hugging FaceコレクションとBigQuery統合があり、クラウド環境や大規模データパイプラインとの親和性が高い
  - PyTorch／Flax両方のバックエンド例が用意され、CPU/GPU/TPUやApple Silicon上での実行が想定されている

## 実践ポイント
- まず試す: リポジトリをクローンして公式チェックポイントを読み込み、手持ちの時系列データで短期→長期の性能を比較。
```python
# Python
pip install -e .[torch]
from timesfm import TimesFM_2p5_200M_torch
model = TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
```
- 長コンテキスト活用: 履歴が数千〜万のケース（センサログ、需要履歴、マーケットデータ）で16kを試し、性能向上を評価する。
- 確率予測: 不確実性が重要な業務（在庫／容量計画など）はcontinuous quantileヘッドを有効化して分位点での予測を取得する。
- 外部変数（祝日やプロモーション）: XRegを使って共変量を入れ、実務精度を引き上げる。
- スケールと運用: BigQuery連携やFlax版を検討し、バッチ推論・オンライン推論のコストとレイテンシを設計する。

短時間で試せて、現場で価値が出やすいアップデートです。まずは手元データで16kコンテキストの恩恵を確認してみてください。
