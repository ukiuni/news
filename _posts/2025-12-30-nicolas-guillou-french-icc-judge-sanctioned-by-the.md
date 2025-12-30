---
layout: post
title: "Nicolas Guillou, French ICC judge sanctioned by the US: 'You are effectively blacklisted by much of the world's banking system' - フランス人ICC判事ニコラ・ギユー、米国制裁で「事実上世界の銀行システムから排除された」"
date: 2025-12-30T12:17:50.737Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.lemonde.fr/en/international/article/2025/11/19/nicolas-guillou-french-icc-judge-sanctioned-by-the-us-you-are-effectively-blacklisted-by-much-of-the-world-s-banking-system_6747628_4.html"
source_title: "Nicolas Guillou, French ICC judge sanctioned by the US and \"debanked\""
source_id: 46432057
excerpt: "米国制裁で国際刑事裁判所判事が事実上デバンキングされ、決済インフラに波紋広がる"
---

# Nicolas Guillou, French ICC judge sanctioned by the US: 'You are effectively blacklisted by much of the world's banking system' - フランス人ICC判事ニコラ・ギユー、米国制裁で「事実上世界の銀行システムから排除された」
破滅的な「デバンキング」がもたらす国際司法と決済インフラへの波紋 — テック視点で読み解く

## 要約
米国が国際刑事裁判所（ICC）の判事・検察官複数人を制裁し、対象者が銀行サービスから実質的に締め出される「デバンキング」問題が浮上。これは国際決済・コンプライアンス技術と金融インフラに直接影響する。

## この記事を読むべき理由
制裁は単なる外交の道具ではなく、決済ネットワーク、KYC/AMLシステム、クラウドや決済APIを使うサービスに実務的な負荷を与える。日本の金融機関や決済系スタートアップ、インフラを設計するエンジニアは、どのようにシステムを守り、誤判定や業務停止を防ぐかを知る必要がある。

## 詳細解説
- 背景：トランプ政権下の米財務省（OFAC）は、ICCが出した逮捕状に関与したとして複数のICC関係者を制裁対象に指定。制裁は資産凍結や米国人／米ドル決済へのアクセス制限を伴う。
- 「デバンキング」とは：銀行や決済業者が制裁リスク・コンプライアンス負担を避けるために関係者の口座・サービス提供を停止する現象。コレスポンデントバンキングと決済チェーン上の排除が波及する。
- テクニカルインパクト：
  - 決済プロバイダや銀行はOFACや他国の制裁リスト（SDN等）を自動照合する。これらは商用データベンダ（Refinitiv、World-Check 等）や自社マッチングエンジンで管理される。
  - 自動照合はファジーマッチや名前変種、役職ベースのヒットが多く、誤検出（false positives）を大量発生させると業務停止や顧客離れを招く。
  - USD決済が絡むと米国の影響力が強まり、日本の銀行や決済サービスも二次制裁リスクを回避するため米基準を事実上採用する傾向がある。
  - 代替技術（暗号資産、非米系決済ネットワーク）は一時的な回避手段に見えても、取引追跡やオンチェーン分析による監視の対象になり得る。
- 国際法・ガバナンスの問題：欧州側は制裁の越境適用に対抗する仕組み（ブロッキング規定、補償メカニズム）を検討しているが、実効性と技術的実装は未成熟。

## 実践ポイント
- サンクション対応エンジニア向けチェックリスト：
  - 制裁リストの自動更新を実装し、ベンダーAPI（OFAC、EU、UK等）を定期取得する。
  - 名前照合の閾値とホワイトリスト運用を明確化し、誤検知時の手動レビューワークフローとSLAを設定する。
  - 重要な顧客に対する事前モニタリングと異常検知（地理的な資金移動、決済パターンの急変）を導入する。
  - 決済経路（コレスポンデントバンク、決済プロバイダ）での依存関係を可視化し、代替ルートの評価を行う。
  - 暗号資産の利用は法務・コンプライアンスと密に連携し、オンチェーン解析ツールでトレース可能性を確保する。
- ビジネス側への提言：
  - 日本企業はUSDクリアリング経由での二次影響を想定し、制裁シナリオのBCP（事業継続計画）に組み込む。
  - 法的リスクが高い案件は早期に法務と外部専門家に相談。欧州の「ブロッキング規定」等の動向を注視する。
  - 開発チームはコンプライアンス要件を仕様段階で組み込み、監査ログや決定根拠を保存できる設計にする。

## 引用元
- タイトル: Nicolas Guillou, French ICC judge sanctioned by the US: 'You are effectively blacklisted by much of the world's banking system'
- URL: https://www.lemonde.fr/en/international/article/2025/11/19/nicolas-guillou-french-icc-judge-sanctioned-by-the-us-you-are-effectively-blacklisted-by-much-of-the-world-s-banking-system_6747628_4.html
