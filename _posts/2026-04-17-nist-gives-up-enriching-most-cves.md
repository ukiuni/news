---
layout: post
title: "NIST gives up enriching most CVEs - NISTがほとんどのCVEの「追記」を断念"
date: 2026-04-17T16:15:01.727Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://risky.biz/risky-bulletin-nist-gives-up-enriching-most-cves/"
source_title: "Risky Bulletin: NIST gives up enriching most CVEs - Risky Business Media"
source_id: 47806777
excerpt: "NISTがほぼ全CVEの詳細追記を停止、NVD依存企業は即対策必須"
image: "/static/img/RB-OG-Social.jpg"
---

# NIST gives up enriching most CVEs - NISTがほとんどのCVEの「追記」を断念
魅力的タイトル: NVDが「重要な脆弱性だけ」に絞る――日本の現場が今すぐ取るべき対策

## 要約
NISTがNVD（National Vulnerability Database）で全CVEへの詳細追記（enrichment）をやめ、重要と判断した脆弱性のみを対象にする方針に変更した（2026年4月15日施行）。さらにNIST自身のCVSSスコア付与も停止し、CVE発行元のスコアをそのまま表示するようになります。

## この記事を読むべき理由
多くの日本企業やセキュリティ製品はNVDをデータソースにしており、今回の方針転換は脆弱性検出・優先度付け・パッチ運用の精度に直接影響します。特にサプライチェーンや国際クラウド/OSSに依存する企業は即対応が必要です。

## 詳細解説
- 変更内容
  - NISTは「enrichment（脆弱性詳細の付与）」を、CISA KEV対象、米連邦機関で使われるソフト、NISTが定義する“critical software”の3カテゴリに限定。
  - “critical software”はOS、ブラウザ、セキュリティ製品、ファイアウォール、バックアップ、VPNなど広範。
  - NIST自身のCVSSスコア付与を停止し、発行元が付けたスコアを表示する方針に。
- 背景
  - 脆弱性件数の急増（例：2024年に未追記CVEが数千→数万に膨張）と予算削減で追いつけなくなったための現実的決断。
  - AIベースの検出が普及すると、さらに「雑多な」CVEの増加が予想されるため、優先度集中へシフト。
- 影響
  - NVD依存の脆弱性管理ツールやスキャナーはデータ欠落やカバレッジ低下に直面。自前でenrichmentするか複数ソースを統合する必要。
  - 発行元が自社製品のCVEに低いCVSSを付けるケースが増えるリスク（利害の衝突）。「一つの真実」は事実上消滅。
  - インシデント対応やパッチ優先度付けの判断基準が分散し、運用負荷が上がる。

## 実践ポイント
- インベントリの整備：重要資産（critical software含む）を明確化し、優先度リスト化する。
- 複数フィードの導入：NVDに加えてJPCERT/CCやJVN、CISA KEV、MITRE、商用脆弱性フィードを組み合わせる。
- KEV監視：CISA KEVの更新を自動化し、即応ルールを作る。
- 自前のenrichment：脆弱性の影響範囲、利用可能なエクスプロイト、攻撃の実証情報を自社で付与するワークフローを構築する。
- CVSSの信頼検証：発行元スコアを鵜呑みにせず、実環境での影響を評価して再スコアリングする運用を作る。
- SBOMとサプライチェーン把握：依存ライブラリやファームウェアの追跡で“雑多な”CVEを有用にフィルタリング。
- ツール/ベンダー調整：脆弱性管理ツールのルールやしきい値を見直し、誤検知ノイズを抑える。

出典: Risky Business（「NIST gives up enriching most CVEs」, 2026-04-17）
