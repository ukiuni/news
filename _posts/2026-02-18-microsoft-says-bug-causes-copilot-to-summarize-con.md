---
layout: post
title: "Microsoft says bug causes Copilot to summarize confidential emails - Microsoft、バグによりCopilotが機密メールを要約してしまう問題"
date: 2026-02-18T20:21:13.817Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.bleepingcomputer.com/news/microsoft/microsoft-says-bug-causes-copilot-to-summarize-confidential-emails/"
source_title: "Microsoft says bug causes Copilot to summarize confidential emails"
source_id: 438487860
excerpt: "Copilotのバグで機密ラベル付き送信済み/下書きメールが要約され漏洩リスク"
image: "https://www.bleepstatic.com/content/hl-images/2025/09/16/Copilot_headpic.jpg"
---

# Microsoft says bug causes Copilot to summarize confidential emails - Microsoft、バグによりCopilotが機密メールを要約してしまう問題
Copilotが「送信済み／下書き」の機密メールを勝手に要約してしまう――あなたの組織のDLPは本当に守れているか？

## 要約
Microsoft 365のCopilot（WorkタブのChat）が、Sent Items／Draftsにある「機密」ラベル付きメールを読み取り要約してしまうバグが確認され、Microsoftは修正を展開中と発表しました。

## この記事を読むべき理由
日本企業でもOutlook＋Microsoft 365は標準的な業務基盤。機密ラベルやDLPに依存している組織は、社外漏洩・コンプライアンス違反のリスクを再評価する必要があります。

## 詳細解説
- 問題の範囲：Copilotの「work tab」Chat機能がSent ItemsとDraftsフォルダ内のメールを誤って処理し、内容を要約してしまう。機密（sensitivity）ラベルやDLPポリシーが設定されていても回避されるケースが発生。  
- 発生日・追跡：同事象は1月下旬に検出（トラッキングID CW1226324）。Microsoftは2月初旬から修正の展開を開始し、現在も展開状況を監視・影響ユーザーへ連絡中。  
- 原因：Microsoftは「不特定のコードエラー」が原因と説明。具体的な修正内容や影響ユーザー数は未公表。事象はアドバイザリ（限定的影響を想定）として扱われている。  
- 関連サービス：Copilot ChatはWord/Excel/PPT/Outlook/OneNoteへ展開済み（企業向けMicrosoft 365）。Chatが「コンテンツを参照して要約」を行う特性が、機密ラベルの期待動作と衝突。

## 実践ポイント
1. まず管理者としてMicrosoft 365管理センターのCopilot/AI設定を確認し、影響が収まるまでWorkタブChatの機能制限や無効化を検討。  
2. DLP・感度ラベル運用を再点検：Sent Items／Draftsを含めたルール適用範囲と例外を確認。  
3. 監査ログを確認し、Copilotによるアクセスや要約の痕跡（該当期間のOutlookアクセス・API呼び出し）を調査。  
4. 重要データ保持ポリシーとユーザー向け注意喚起を発出。機密メールの取り扱いルールを改めて周知。  
5. Microsoftの公式アラート（サービスヘルス）とサポート連絡を継続監視し、必要ならインシデント報告と補償対応を準備。

（補足）日本の個人情報保護法や企業内の機密管理要件に照らして影響を評価し、監督部署／法務と連携してください。
