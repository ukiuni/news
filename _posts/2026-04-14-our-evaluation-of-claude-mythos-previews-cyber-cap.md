---
layout: post
title: "Our evaluation of Claude Mythos Preview’s cyber capabilities - Claude Mythos Preview のサイバー能力に関する評価"
date: 2026-04-14T11:21:11.699Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.aisi.gov.uk/blog/our-evaluation-of-claude-mythos-previews-cyber-capabilities"
source_title: "Our evaluation of Claude Mythos Preview’s cyber capabilities | AISI Work"
source_id: 1723990591
excerpt: "評価で明らかに：AIが弱防御の企業ネットワークを自律的に多段攻撃可能、対策急務"
---

# Our evaluation of Claude Mythos Preview’s cyber capabilities - Claude Mythos Preview のサイバー能力に関する評価
AIが“ネットワーク乗っ取り”を自動化？Claude Mythos が示した攻撃力と今すぐ必要な防御策

## 要約
英国のAI Security Institute（AISI）がAnthropicのClaude Mythos Previewを評価し、CTF（攻撃課題）と32段階の攻撃シミュレーションで従来モデルより大幅に向上した攻撃能力を確認。弱防御の企業環境では自律的に複数段階攻撃を遂行できる可能性が示されました。

## この記事を読むべき理由
日本の企業・組織も対象になり得るAI支援攻撃の実用化が近づいています。製造業や重要インフラでOT/ITが混在する日本では、攻撃の自動化は現実的脅威であり、今のうちに備える必要があります。

## 詳細解説
- 評価対象と手法：AISIはClaude Mythos PreviewをCTFスイート（初級〜専門家レベル）と「The Last Ones（TLO）」という32ステップの企業ネットワーク攻撃レンジで検証。実験はモデルに指示とネットワークアクセスを与えた上で行われた。  
- 主な結果：専門家レベルのCTFで高成功率（例：一部タスクで73%）、TLOではモデルが完遂した試行もあり平均22/32ステップを達成。つまり、人が数日かかる作業を短期間で実行できる能力に到達している。  
- スケーリングと制約：評価は大量の「トークン（推論予算）」を与えた条件下で行われ、性能は推論量に依存して上昇。逆に、防御が強い・監視がある実環境では結果が変わる可能性が高い。OT向けレンジでは詰まる場面もあった。  
- 評価の限界：レンジにはアクティブな守備側（IDS/EDR、運用者の介入など）やアラートのペナルティが無く、実世界より易しい点がある。したがって「必ず攻め切れる」と断言はできないが、弱点の多い環境では現実的脅威である。

## 実践ポイント
- 基本を当たり前に：OS・ミドルウェア・アプリの迅速なパッチ適用を習慣化する。  
- 最小権限と認証強化：管理者権限の厳格化、MFA導入、特権アクセスの時限付与。  
- ネットワーク分離とセグメンテーション：OTとITの明確な分離、横移動を防ぐ内部ACL。  
- ログと検知の充実：中央ログ収集、SIEM/EDRで異常検知し、アラートに対する運用フローを整備。  
- レッドチーム／演習の近代化：AI支援攻撃を想定した演習や、自動化ツールを使った脆弱性発見の検証を実施。  
- 情報収集と手引き参照：英国NCSCのような公的助言（日本ならNISCや経産省のガイダンス）を参照し、Cyber Essentials相当の対策を組織に落とし込む。  

将来の「フロンティア」モデルはさらに能力が上がる見込みです。今すぐ取り組める基礎防御の強化と、AI時代に合わせた検知・対応体制の整備が急務です。
