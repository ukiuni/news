---
layout: post
title: Salesforce Executives Say Trust in Large Language Models Has Declined - Salesforce幹部、大規模言語モデルへの信頼が低下したと語る
date: 2025-12-28T04:15:07.144Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.theinformation.com/articles/salesforce-executives-say-trust-generative-ai-declined"
source_title: "Salesforce Executives Say Trust in Large Language Models Has Declined"
source_id: 436502215
excerpt: "SalesforceがLLMへの信頼低下を公言、企業導入の安全対策見直しが急務"
---

# Salesforce Executives Say Trust in Large Language Models Has Declined - Salesforce幹部、大規模言語モデルへの信頼が低下したと語る

## 要約
Salesforce幹部が「大規模言語モデル（LLM）への信頼が低下した」と明言。精度・安定性・ガバナンスの課題が企業導入の足かせになっている。  

## この記事を読むべき理由
Salesforceは主要CRMベンダーであり、その慎重姿勢は日本企業のAI導入戦略にも直結する。CRM／カスタマーサポート、営業支援、社内自動化を検討するエンジニアやプロダクト責任者は今すぐ評価基準とガードレールを見直す必要がある。

## 詳細解説
- 背景：ここ数年でLLMは生成品質と生産性向上の期待から急速に導入が進んだが、実運用で「誤情報（hallucination）」「不安定な振る舞い」「データ漏洩リスク」「アップデートによる挙動変化」などが問題化している。Salesforce幹部の発言は、こうした現場での反省とリスク認識の表明と読める。  
- 技術的ポイント：
  - Hallucination：モデルが確証なしに虚偽の事実や不正確な数値を生成する。これが顧客向け回答や営業提案で致命的になる。
  - 再現性とバージョン管理：モデル更新で応答傾向が変わり、SLAや検証済みワークフローが崩れる。
  - データガバナンス：顧客データを学習やプロンプトに使う際のプライバシーとコンプライアンス（日本ではAPPI対応、データローカリティの検討が必要）。
  - 成果測定の難しさ：単純なメトリクス（回答スコアや節約時間）だけではビジネス価値を正確に測れない。
  - 技術的緩和策：RAG（Retrieval-Augmented Generation）で外部確定情報に基づかせる、ファインチューニング／微調整でドメイン適合、プロンプトの設計（system/assistant指示）、返答検証用のルールベースフィルタリング、Explainability／モデルカードで可視化、継続的なモニタリングと赤チームテスト。
- ビジネスインパクト：Salesforceクラスの企業が慎重だと、顧客企業もベンダー選定基準を厳格化する。結果として「安全性・説明可能性・SLA」を備えたソリューションが選ばれやすくなる。

## 実践ポイント
- 評価を厳格化する：社内ユースケースごとに受け入れ基準（正答率、誤情報率、応答安定性）を定義し、自動テストを組む。  
- RAGを初期構成に組み込む：外部ナレッジベースを参照させ、生成前後で出典照合を行う。  
- 人間の監督（Human-in-the-loop）：重要な意思決定や顧客向け回答は必ず有人承認フローを設ける。  
- データガバナンス強化：学習やログ保存に関する同意・マスキング・保存ポリシーを整備し、APPI・契約要件を満たす。  
- モデル運用のSLAと監視：レスポンス変化や品質低下を検知するモニタリング（アンサンブル比較、フィードバックループ）を実装。  
- 小さく安全にローンチ：限定部門からの段階的展開とA/Bで効果検証。  
- ベンダー評価基準を更新：説明責任、更新ポリシー、セキュリティ保証、誤答時の対応窓口を契約条件に入れる。

