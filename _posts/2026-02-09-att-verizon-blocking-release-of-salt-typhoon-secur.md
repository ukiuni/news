---
layout: post
title: "AT&T, Verizon blocking release of Salt Typhoon security assessment reports - AT&T、VerizonがSalt Typhoonのセキュリティ評価報告書の公開を阻止"
date: 2026-02-09T15:40:51.291Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.reuters.com/business/media-telecom/senator-says-att-verizon-blocking-release-salt-typhoon-security-assessment-2026-02-03/"
source_title: "AT&T, Verizon blocking release of Salt Typhoon security assessment reports"
source_id: 46945497
excerpt: "AT&TとVerizonがSalt Typhoon報告書公開を阻止、通信の脆弱性と透明性が危機"
image: "https://www.reuters.com/resizer/v2/CJEZ677WKZLOPAVE2OC7FD6SMU.jpg?auth=8e965e0ab9715ec2c4510ee2916f27b2d5c03371a44738e07d4b9085ed198f6b&amp;height=1005&amp;width=1920&amp;quality=80&amp;smart=true"
---

# AT&T, Verizon blocking release of Salt Typhoon security assessment reports - AT&T、VerizonがSalt Typhoonのセキュリティ評価報告書の公開を阻止
なぜ大手キャリアが「報告書の公開を止めた」のか？Salt Typhoon問題が示す通信インフラの透明性と危険

## 要約
米メディア報道によれば、AT&TとVerizonが「Salt Typhoon」と名付けられたセキュリティ評価報告書の公開を阻止しているとされ、脆弱性情報の隠匿と透明性の欠如が議論を呼んでいる。

## この記事を読むべき理由
ネットワーク事業者の扱う情報は社会インフラや企業サービスの安全性に直結します。公開可否の判断はセキュリティ習熟度だけでなく、規制・サプライチェーン管理の成熟度を示します。日本のエンジニアや事業者にも直接影響するテーマです。

## 詳細解説
- 「報告書」に通常含まれるもの：脆弱性一覧、攻撃シナリオ（レッドチーム演習）、ログ／トラフィック解析、推奨対応（設定変更・パッチ・アーキテクチャ改善）および機器ベンダーの評価。  
- 評価手法：ペネトレーションテスト、設定監査、ファームウェア／ソフトウェア解析、侵害検知の検証などが一般的。  
- なぜ公開が止められるのか（可能性）：国家安全保障や法令、機器ベンダーとのNDA、顧客・事業リスク、攻撃者への“青写真”提供を懸念したため、という説明が考えられる。  
- 問題点：過度な非公開は利用者・規制当局の監視や対策を妨げる。逆に無加工の公開は攻撃手法を安易に提供するリスクがあるため、適切な「秘匿と公開のバランス」が重要。  
- 技術的焦点（想定される項目）：RAN/コア（SS7・Diameter・SCTP）、BGP経路・ルーティング、IMS/VoLTE、管理インタフェースの認証、ファームウェアの署名・更新プロセス、サプライチェーンの改ざんリスク。

## 日本市場との関連
- 日本の主要キャリア（NTTドコモ、KDDI、ソフトバンク）やローカルISP、MVNOも同様の評価・報告を行う可能性が高く、報告の扱いが今後の規制や顧客信頼に影響します。  
- 緊急時の情報共有や電気通信事業法・総務省の枠組みでの対応が鍵。日本企業は「公開のための標準的なレッドチーム報告フォーマット」や「編集済み（要約・機密削除）公開」の取り組みを検討すべきです。

## 実践ポイント
- 事業者向け：外部監査・第三者評価を受け、公開できる形でのサマリ（技術的要約＋対策）を用意する。  
- エンジニア向け：ネットワーク分離、最小権限、ログ/検知体制の強化、ベンダーのパッチ・署名ポリシーを確認する。  
- コミュニティ／規制対応：報告の赤線（絶対に非公開にすべき情報）と白書化できる領域を定義し、総務省や業界団体と協調して公開基準を整備する。

（注）本記事は元記事タイトル等の公表情報に基づく要約・解説であり、個別の事実関係や法的帰結については報道元・公式資料を参照してください。
