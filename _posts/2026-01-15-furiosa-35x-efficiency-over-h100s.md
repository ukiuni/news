---
layout: post
title: "Furiosa: 3.5x efficiency over H100s - Furiosa：H100比で3.5倍の効率？"
date: 2026-01-15T01:50:45.400Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://furiosa.ai/blog/introducing-rngd-server-efficient-ai-inference-at-data-center-scale"
source_title: "Introducing Furiosa NXT RNGD Server: Efficient AI inference at data…"
source_id: 46626410
excerpt: "空冷ラック対応でH100比3.5倍、低電力で大規模推論可能なNXT RNGD Server"
---

# Furiosa: 3.5x efficiency over H100s - Furiosa：H100比で3.5倍の効率？
驚くほど省電力で導入しやすい「NXT RNGD Server」が示す、データセンター向けAI推論の新常識

## 要約
FuriosaAIが発表した「NXT RNGD Server」は、RNGDアクセラレータ搭載のターンキー推論サーバーで、従来のGPUベース構成に比べて電力効率を大幅に改善し、既存の空冷データセンターでも導入可能な点が最大の特徴です。

## この記事を読むべき理由
日本の多くのデータセンターは空冷・ラックあたり電力制限が厳しく、オンプレや機密性の高いワークロードを抱える企業が多い点で、低消費電力かつ導入が容易な推論プラットフォームは現実的な選択肢になります。導入コストや運用電力を抑えて大規模推論を回したい企業／エンジニアは必読です。

## 詳細解説
- ハードウェアの肝：
  - RNGDアクセラレータを最大8枚搭載可能（サーバー当たり最大4 PFLOPS FP8が同社公表値）。
  - メモリは384 GB HBM3（帯域12 TB/s）＋1 TB DDR5。
  - 電力消費はシステム全体で約3 kW、一般的な空冷ラック環境に適合。
  - FP8、BF16、INT8、INT4をサポートし、推論精度と効率のトレードオフに柔軟に対応。
- ソフトウェアと運用：
  - Furiosa SDK と Furiosa LLMランタイムをプリインストール、Kubernetes/Helmとのネイティブ連携でデプロイが簡易。
  - vLLM互換やOpenAI APIサポートをうたっており、既存の推論フローに統合しやすい。
- 実測例と効果：
  - LG AI Researchの例では、4枚構成でEXAONE 3.5 32Bをバッチ1で運用し、4Kコンテキストで60 tokens/s、32Kで50 tokens/sを達成（単一サーバーの報告）。
  - 同社は「H100比で3.5x効率」と銘打っており、主張は主に消費電力当たりの推論スループット改善に基づくものと読み取れます。
- セキュリティ／運用面：
  - Secure Boot、TPM、BMCのアテステーション、冗長電源などエンタープライズ要件に配慮した設計。

## 実践ポイント
- 導入検討：
  - まずは4カード構成でパイロットを組み、代表的なモデル（自社で使うLLM）をバッチ1・低遅延条件で測定してみる。LGの事例が指標になります。
- コスト／運用面のチェックリスト：
  - ラックの電力制限（kW／ラック）と空冷対応を確認。3 kW/システムは多くの既存ラックで許容されやすい。
  - 電力×性能でのTCO試算を行い、クラウドGPU（例：H100系）との比較を数値で出す。
- ソフトウェア互換性：
  - Furiosa SDKとvLLM互換性を検証し、既存のKubernetes環境へ統合できるか確認する。OpenAI API互換の有無は移行コストを下げる要素。
- ガバナンス／データ主権：
  - 機密データや法規制の関係でオンプレ必須のワークロードは、オンサイト推論への移行候補に最適。
- スケジュール：
  - Furiosaは2026年1月出荷見込みで受注中とのこと。POや検証スケジュールを逆算して発注計画を立てる。

短くまとめると、NXT RNGD Serverは「既存の空冷データセンターで、電力とコストを抑えて大規模推論を動かしたい」日本企業にとって現実的な選択肢です。まずは小規模評価で性能と互換性を確かめることをおすすめします。
