---
layout: post
title: "96% Engineers Don’t Fully Trust AI Output, Yet Only 48% Verify It - エンジニアの96%がAI出力を完全には信頼していないが、検証するのはわずか48%"
date: 2026-02-09T04:31:24.667Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://newsletter.eng-leadership.com/p/96-engineers-dont-fully-trust-ai"
source_title: "96% Engineers Don’t Fully Trust AI Output, Yet Only 48% Verify It"
source_id: 405651169
excerpt: "96%がAI出力を完全に信頼せず、検証は48%しか行わない現場の危機と即効対策"
image: "https://substackcdn.com/image/fetch/$s_!JxAs!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49e78d49-c5ea-4ffd-b0e7-f38bd9d691aa_1600x787.jpeg"
---

# 96% Engineers Don’t Fully Trust AI Output, Yet Only 48% Verify It - エンジニアの96%がAI出力を完全には信頼していないが、検証するのはわずか48%
AI生成コードを「速さ」で使っていませんか？——信頼していないのに確認していないエンジニア多数の実態

## 要約
Sonarの調査（1149名、2025年10月実施）で、96%がAI出力を完全には信頼しておらず、しかし「常に検証する」エンジニアは48%に留まる。AI活用は進むが検証・ガバナンスが追いついていない。

## この記事を読むべき理由
日本の開発現場でもAIツールは普及中。だが検証不足は品質低下や機密漏洩リスクにつながり得る。実務で即効性のある対策が必要な読者向け。

## 詳細解説
- 調査のサマリ：1149名対象。72%が毎日AIを使用、現状でコードの42%がAI生成/支援、2027年に65%予測。  
- 信頼と検証のギャップ：96%が「完全には信頼しない」と回答する一方、常にチェックするのは48%。これは「信頼できない→でも手を抜く」悪循環を示す。  
- 品質の問題点：61%が「見た目は正しいが信頼できないコードが出る」と回答。AIは文脈依存で、曖昧なプロンプトや複雑なコードベースでは誤出力が増える。  
- セキュリティとアカウント運用：57%が機密情報流出を懸念、35%が個人アカウントで利用。企業側のツール支給やポリシー不足が要因。  
- ツール事情：GitHub CopilotとChatGPTが上位。チーム平均で4ツールを併用。企業規模で好みが分かれる（大手はChatGPT利用が相対的に少ない）。  
- 必要なスキル：コードレビュー／検証が最重要。効率的なプロンプト設計も上位の必須スキル。

## 実践ポイント
- コードをAIに頼る前提で「必須の検証ルール」を設ける（自動テスト、静的解析、必須レビューチェック等）。  
- 機密データはプロンプトに含めない。企業アカウント・SAML連携など公式ツール配布を推進する。  
- PR前にAI生成部分だけのユニットテストと簡易ベンチを導入。CIでガードする。  
- プロンプト設計をチームでテンプレ化（コンテキスト、期待出力、制約を明示）。  
- ツールは「複数併用」前提で評価基準を決め、必須ツールを揃えて学習コストを下げる。

以上を踏まえ、AIは速度を与えるが「責任」は人間に残る。日本のチームではガバナンスと検証文化の整備が急務です。
