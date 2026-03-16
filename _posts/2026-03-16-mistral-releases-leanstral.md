---
layout: post
title: "Mistral Releases Leanstral - MistralがLeanstralを公開"
date: 2026-03-16T22:02:42.733Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mistral.ai/news/leanstral"
source_title: "Leanstral: Open-Source foundation for trustworthy vibe-coding | Mistral AI"
source_id: 47404796
excerpt: "Lean 4対応の低コスト定理証明エージェントLeanstralが実運用を可能に。"
image: "https://mistral.ai/img/mistral-cover.png"
---

# Mistral Releases Leanstral - MistralがLeanstralを公開
魅力的タイトル：定理証明を“実用レベル”へ——MistralのLeanstralが示す「証明するコード生成」の未来

## 要約
MistralがLean 4向けに設計したオープンソースのコードエージェント「Leanstral」を公開。少ない計算資源で実務的な定理証明・仕様検証を行えるよう最適化され、モデル再現性と低コスト運用を両立している。

## この記事を読むべき理由
定理証明や形式検証は研究だけでなく、自動運転・医療機器・金融システムなど日本の高信頼領域で重要性が増しています。Leanstralは「実運用で使える」証明支援を目指しており、現場エンジニアや研究者が実際に使える道を開きます。

## 詳細解説
- 対象と設計思想：LeanstralはLean 4（数論やソフトウェア仕様を表現できる定理証明系）専用に訓練されたコードエージェント。単発の数学問題ではなく、リアルなリポジトリやPR単位での証明完遂を評価対象にしている点が特徴。
- アーキテクチャと効率性：6Bのアクティブパラメータを持つスパース（疎）アーキテクチャを採用し、並列推論とLean自身の厳密な検証機能を組み合わせることで、性能とコスト効率を両立している（モデル表記例：Leanstral-120B-A6B）。
- 評価（FLTEval）：従来の競技数学中心の評価ではなく、PRごとの定理完成や概念定義を成功させるかを測る独自スイートFLTEvalで検証。大規模OSSモデルやClaude系と比較して少ないコストで高い実用性を示した。
- 実例：StackExchangeの実際の移行問題で、コンパイルが止まる原因（defとabbrevの違いによる定義的等値性）を再現コードで突き止め、適切な修正案を提示。プログラム言語の定義からLeanへ翻訳・補題証明まで行ったケースもある。
- 拡張性：MCP（modular code providers）経由で既存開発フローに組み込みやすく、特にlean-lsp-mcpとの組み合わせで最適化されている。

## 実践ポイント
- 今すぐ試す：Mistral Vibeに統合済みでゼロセットアップ。/leanstall コマンドで開始可能。APIは labs-leanstral-2603（期間限定で低コスト／無料枠あり）。
- 自ホスト運用：Apache 2.0の重み（weights）をダウンロードして社内環境で動かせるため、機密性が要求される日本企業にも適応可能。
- ワークフロー提案：まずは小さなLeanリポジトリでPRごとにFLTEval相当の通過基準を設け、Leanstralを使った自動修正提案→人の最終レビューのループを構築するのが効果的。
- 注目点：Leanstralは「証明を自動化する」だけでなく「証明可能性を早期に判定」することでレビュー負荷を下げるため、日本の安全クリティカル開発現場でのベンチマーク導入を推奨。
