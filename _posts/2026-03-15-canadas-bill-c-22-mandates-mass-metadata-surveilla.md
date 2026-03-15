---
layout: post
title: "Canada's bill C-22 mandates mass metadata surveillance of Canadians - カナダのC-22法案が国民の大量メタデータ監視を義務化"
date: 2026-03-15T23:18:40.972Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.michaelgeist.ca/2026/03/a-tale-of-two-bills-lawful-access-returns-with-changes-to-warrantless-access-but-dangerous-backdoor-surveillance-risks-remains/"
source_title: "A Tale of Two Bills: Lawful Access Returns With Changes to Warrantless Access But Dangerous Backdoor Surveillance Risks Remain - Michael Geist"
source_id: 47392084
excerpt: "法案C-22がメタデータ大量監視を合法化、企業と技術者は緊急対応を"
image: "https://www.michaelgeist.ca/wp-content/uploads/2026/03/screenshot_4102.png"
---

# Canada's bill C-22 mandates mass metadata surveillance of Canadians - カナダのC-22法案が国民の大量メタデータ監視を義務化
クリックせずにいられない！「見えない監視」が合法化へ――エンジニアも知っておくべきC-22の核心

## 要約
カナダの新法案C-22は「通信事業者への迅速な情報確認」と、通信ネットワークに対する事実上の協力・検査義務（SAAIA）を二本柱に導入。個人の中身（コンテンツ）は一定程度保護されるが、メタデータの大量保持・監査体制と秘密指定が拡大し、セキュリティや国際データ共有のリスクが残る。

## この記事を読むべき理由
技術者・プロダクト担当は、通信事業者やプラットフォームに求められる技術的対応、データ保持方針、法的リスク（海外との情報共有やセキュリティ影響）を即座に把握する必要があるため。

## 詳細解説
- 法案の構成：①「データ・情報への迅速なアクセス」部分は、前回（Bill C-2）の過度な捜査権を縮小。通信事業者（ISPや携帯事業者）に対し「その人にサービス提供しているか」を確認させる無令状の確認要求を認める一方、他の加入者情報は裁判官の審査を受ける開示命令が必要になる。  
- SAAIA（Supporting Authorized Access to Information Act）：旧案と比べてほぼ踏襲。重要点は「電子サービス提供者（ESP）」概念を導入し、単なる通信事業者を超えプラットフォームも対象になり得ること。ESPには「評価・試験のための合理的な支援」「秘密保持（非公開）」が義務付けられる。  
- メタデータ保持：コア提供者には最大1年のメタデータ（送受信の伝送データ等）保持が規定される（※コンテンツ、ブラウジング履歴、SNS活動は保持の対象外と明記）。ただし「体系的な脆弱性を導入することを要求しない」例外があるが、具体運用でセキュリティ低下や秘密扱いによる透明性欠如の懸念が強い。  
- 国際連携・法的枠組み：法案は2AP（ブダペスト条約の追加議定書）や米国のCLOUD Actとの整合を見据えており、越境データ共有の増加・他国法執行機関との協力が想定される。  
- 監視リスク：無令状の範囲は限定されたが、ネットワーク上の「直接アクセス」や機器設置・検査に関する要件は残り、セキュリティ、プライバシー、コスト、秘密指定による監督不足が問題になる。

## 実践ポイント
- システム設計：メタデータ収集・保持を最小化し、保存期間を短くする方針を明確化する。保持が必要なら暗号化と厳格なアクセスログを実装する。  
- セキュリティ監査：外部からのテストや「検査要求」に備え、改変・介入がシステムの脆弱性を生まない設計とインシデント対応計画を整備する。  
- 法務・プライバシー：法務と連携して保全命令や秘密指定に関する対応プロセスを作成。国際的なデータ要求（CLOUD Act等）への影響を評価する。  
- ビジネス判断：日本の事業者・クラウド利用者は、カナダでのサービス提供やカナダ拠点とのデータ連携が法的・運用リスクを招かないか再評価する。  
- 公開・透明性：可能な範囲で透明性レポートやPRA（Privacy Impact Assessment）を公表し、利用者信頼の維持に努める。

短く言えば、C-22は「加入者の即時確認」を抑えつつも、「メタデータとネットワーク協力」を通じた大規模な監視基盤を合法化する構図。技術者は設計と法務の両面で早めの対策が必要。
