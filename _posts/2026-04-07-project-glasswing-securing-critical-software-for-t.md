---
layout: post
title: "Project Glasswing: Securing critical software for the AI era - Project Glasswing：AI時代の重要ソフトウェアを守る"
date: 2026-04-07T18:29:02.598Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.anthropic.com/glasswing"
source_title: "Project Glasswing: Securing critical software for the AI era \ Anthropic"
source_id: 47679121
excerpt: "Project Glasswingが古い脆弱性をAIで大量発見、重要ソフトを先手で修復へ"
image: "https://cdn.sanity.io/images/4zrzovbb/website/65641e7846f10255c4a3415a10bbf5793ae87b13-1200x630.jpg"
---

# Project Glasswing: Securing critical software for the AI era - Project Glasswing：AI時代の重要ソフトウェアを守る
AIが“自動で脆弱性を発見する”時代に、守る側が先手を取るための超産業横断プロジェクト

## 要約
Anthropicが開発した高性能モデル「Claude Mythos Preview」を使い、AWSやGoogle、Microsoftなど主要企業と連携して重要ソフトウェアの脆弱性を大規模に発見・修正する取り組みが「Project Glasswing」。AIは既に人間レベルで脆弱性発見・悪用が可能になっており、防御側の対応を急ぐ必要がある。

## この記事を読むべき理由
AIが自動でゼロデイを見つけ・悪用する能力を持つ今、ソフトウェア供給網（OSS含む）や金融／インフラ系のシステムを守るための実務が変わります。日本の企業やOSSメンテナ、セキュリティ担当者にとって「AIを防御に使う」具体的な実例と協力の枠組みは必読です。

## 詳細解説
- 背景：従来は高度な専門家に限られていた脆弱性探索・エクスプロイト作成のノウハウが、最新のフロンティアAIで大幅に自動化され、コストと時間が急低下。悪用されれば被害拡大が速くなるため、防御側もAIを使って先手を打つ必要がある。
- Mythos Previewの能力：コード解析・推論・エージェント的探索（自律的に探索→検証→チェーン化）が非常に高く、既存の自動テストや数百万回のテストをすり抜けた古い脆弱性も発見。評価ベンチマーク（例：CyberGym）で従来モデルを大きく上回る結果を出している。
- 実例（要点）：
  - OpenBSD：27年前の脆弱性をリモート接続でクラッシュさせうる問題を発見。
  - FFmpeg：16年前のバグを自動検出ツールが見逃していた箇所で発見。
  - Linuxカーネル：複数脆弱性を自律的に連鎖させ権限昇格を達成。
- ガバナンスと配慮：Anthropicはパートナーにモデルを提供し、業界で共有しつつパッチ前に詳細を公開しない責任ある開示を行う。$100M分の利用クレジット、$4MのOSS支援を表明。
- 参加企業：AWS、Apple、Google、Microsoft、Cisco、CrowdStrike、Linux Foundation、NVIDIA、Palo Altoなど大手が防御目的で参画。

## 実践ポイント
- OSSメンテナー向け：重要依存ライブラリはAI支援の静的解析／自動スキャンを導入し、外部からのスキャン権限を検討する（優先度の高い脆弱性から対応）。
- 開発チーム向け：CI/CDにAIベースの脆弱性スキャンを組み込み、パッチ投入のワークフローと責任ある公開ルールを整備する。
- セキュリティ管理者向け：サプライチェーン（OSS含む）リスク評価を見直し、脆弱性発見から修正までの時間短縮を最優先にする。インシデント対応演習にAIシナリオを加える。
- 経営層向け：AIで攻撃も防御も劇的に変わる点を認識し、人材育成と外部連携（ベンダー／コミュニティ）に投資する。

この動きは日本のインフラ・金融・製造のセキュリティ戦略にも直結します。まずは自社の重要ソフトウェア資産に対してAI支援スキャンの導入検討と、OSSメンテナへの支援体制づくりを始めましょう。
