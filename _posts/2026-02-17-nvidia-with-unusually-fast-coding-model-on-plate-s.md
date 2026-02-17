---
layout: post
title: "Nvidia with unusually fast coding model on plate-sized chips - 皿サイズのチップで異例に高速なコーディングモデル、Nvidiaを迂回"
date: 2026-02-17T00:49:37.293Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/ai/2026/02/openai-sidesteps-nvidia-with-unusually-fast-coding-model-on-plate-sized-chips/"
source_title: "OpenAI sidesteps Nvidia with unusually fast coding model on plate-sized chips - Ars Technica"
source_id: 46996852
excerpt: "WSE搭載のCodex‑Sparkが秒速1,000トークン超でIDE補完を圧倒的高速化"
image: "https://cdn.arstechnica.net/wp-content/uploads/2026/02/GettyImages-2225076517_resize-1152x648.jpg"
---

# Nvidia with unusually fast coding model on plate-sized chips - 皿サイズのチップで異例に高速なコーディングモデル、Nvidiaを迂回
コード補完が“秒速”で返ってくる未来？OpenAI×Cerebrasの高速Codexが開幕

## 要約
OpenAIがGPT-5.3‑Codex‑SparkをCerebrasの皿サイズWafer Scale Engineで稼働させ、コーディング向けに1,000トークン/秒超の高速推論を実現。ChatGPT Pro経由やVS Code拡張で提供され、速度重視の設計でプロトタイピングを加速する。

## この記事を読むべき理由
日本の開発者やプロダクト担当が、IDE内での待ち時間短縮や迅速な試作サイクルをどう活かせるかを見極めるため。クラウド/ハードウェア多様化が国内ベンダー・オンプレ選定にも影響します。

## 詳細解説
- モデルと用途：GPT‑5.3‑Codex‑Sparkはテキスト（コード）専用にチューニングされた軽量高速モデル。深い知識より「速さ」を優先し、重めのGPT‑5.3本体とは役割を分けている。コンテキスト窓は128,000トークン。
- 性能：OpenAI公表で1,000+ トークン/秒を達成。従来の同社Nvidia基盤モデルは数十〜百数十トークン/秒が中心で、今回の跳躍はインフラとチューニングの組合せによる。Cerebras側では別モデルで2,100〜3,000トークン/秒の実測もあり、Sparkはモデル複雑さによるオーバーヘッドを含む数値と見られる。
- ハードウェア面：動作基盤はCerebrasのWafer Scale Engine（WSE）3――基板一枚分に相当する大型チップ。OpenAIはNvidia依存の低減を進め、AMDやAWSとの契約、自社チップ設計など複数路線を並行している。
- 提供形態と制約：現時点でCodex‑SparkはChatGPT Pro（月額プラン）やCodexアプリ、CLI、VS Code拡張で利用可能。APIは限定パートナーに順次開放中。OpenAI側の独立検証データは限定的で、精度と速度のトレードオフに注意。

## 実践ポイント
- VS Codeワークフロー：Codex拡張を試し、補完やスニペット生成の応答時間を測定して通常ワークフローでの効用を確認する。
- プロトタイプ向け運用：高速モードは素早い反復に最適。最終コードは必ず静的解析・テストで検証する（速度はバグを覆い隠すことがある）。
- コスト・調達観点：クラウドやHWの多様化（Nvidia以外）を検討すると、レイテンシ/コストの最適化余地が生まれる。オンプレや国内クラウド事業者との交渉材料にも。
- セキュリティとコンプライアンス：APIや生成コードのデータ取り扱いを確認し、企業ポリシーに合わせた利用ルールを整備する。

短期的には「早い」ことで開発生産性が向上する場面が増えますが、精度・安全性の確認を怠らないことが鍵です。
