---
layout: post
title: "Trusted access for the next era of cyber defense - 次のサイバー防御時代のための信頼されたアクセス"
date: 2026-04-14T21:05:00.911Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://openai.com/index/scaling-trusted-access-for-cyber-defense/"
source_title: "Trusted access for the next era of cyber defense | OpenAI"
source_id: 47770770
excerpt: "検証済み守備側へ限定提供、GPT‑5.4‑Cyberで脆弱性解析と自動防御を革新"
---

# Trusted access for the next era of cyber defense - 次のサイバー防御時代のための信頼されたアクセス
GPT‑5.4‑Cyberで“守る側”のAIを拡張する——OpenAIが提示する信頼ベースのアクセス戦略

## 要約
OpenAIは「Trusted Access for Cyber（TAC）」を拡大し、サイバー防御向けに微調整したGPT‑5.4‑Cyberを限定提供。本人確認と段階的なアクセス管理で、守る側に強力なAIツールを安全に配布しようとしている。

## この記事を読むべき理由
日本の企業・OSSやインフラ事業者にとって、AIが攻守両面で進化する今、適切な検証と運用ルールのもとで防御力をAIで強化する手法を理解することは急務だから。

## 詳細解説
- プログラム拡大: TACを数千人の個人検証者・数百のチームへ拡張。アクセスは本人確認（KYC）や信頼シグナルに基づく段階的な方式。  
- モデル: GPT‑5.4‑Cyberは「サイバー許容（cyber‑permissive）」に微調整されており、通常の拒否境界を下げて防御ワークフロー（例：バイナリ逆解析、マルウェア分析、脆弱性発見）を支援する。  
- 安全設計の原則: 民主化されたアクセス（正当な守備側へ広く提供）、反復的デプロイ（小規模かつ段階的に学習して改善）、エコシステム強化（助成やオープンソース連携、Codex Security等）を掲げる。  
- 既存施策: $10Mの助成、Codexによるオープンソース向け自動スキャンで既に多数の重大脆弱性修正に寄与。  
- 制約と注意点: より許容的なモデルは限定的提供・厳格な検証を前提。Zero‑Data‑Retention等の無可視利用やサードパーティ経由では制御が難しいため制限が付く可能性が高い。OpenAIは「能力に応じて防御も拡張」が必要と明言。

## 実践ポイント
- 責任ある利用申請: 個人は chatgpt.com/cyber で本人確認、企業は営業窓口経由でTAC申請を検討。  
- 開発パイプライン統合: Codex Securityや自動SASTをCIに組み込み、コード作成時点で継続的に脆弱性を検出・修正する。  
- バイナリ解析導入の準備: GPT‑5.4‑Cyberはソース無しでの解析支援が可能になるため、SBOMやビルド再現性・署名ポリシーを整備して証跡を残す。  
- 運用ルール整備: アクセス権限、ログ保管、監査フロー、第三者プラットフォームの利用制約（ZDRなど）を明確化。  
- エコシステム連携: OSSプロジェクトへの貢献や助成プログラム活用、国内ベンダーとの協業で「守る側」の基盤を強化する。

短く言えば、OpenAIの方針は「検証された守備側に強力なAIを安全に配布し、防御をAIと共に前倒しで強化する」こと。日本の現場でも本人確認・CI統合・監査を先行させ、次世代ツールを安全に取り込む準備を。
