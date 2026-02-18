---
layout: post
title: "Google Public CA is down - Google Public CAがダウン"
date: 2026-02-18T01:34:00.014Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://status.pki.goog/incidents/5oJEbcU3ZfMfySTSXXd3"
source_title: "Google Trust Services Status Dashboard"
source_id: 47055696
excerpt: "Google Public CAの発行停止で証明書自動更新が一時失敗、即時確認と代替手順が必要"
---

# Google Public CA is down - Google Public CAがダウン
証明書発行が止まると何が起きる？今すぐ確認すべき5つの対策

## 要約
GoogleのPublic CA（ACME API：SXG/TLS）で発行停止のインシデントが発生し、新規発行や自動更新が一時的に止まっています。影響が続くとCI/CDや公開サイトの証明書自動更新に影響が出る可能性があります。

## この記事を読むべき理由
日本の開発チームやパブリッシャー（特にSXG/Signed Exchangeを利用する媒体）、Googleの証明書やACMEを使った自動化を組み込んでいるサービス運用者は、短時間の障害でもデプロイや証明書更新に直撃するため、即時の確認と対策が必要です。

## 詳細解説
- 発生状況：Google Trust Servicesのステータスでインシデントが報告され、ACME API（SXG, TLS）に影響。発生は2026-02-17 11:18 US/Pacific（日本時間：約2026-02-18 04:18 JST）。12:14 PST（約05:14 JST）時点で「発行が停止し始めている」との更新があり、修正は約8時間で展開予定と発表されました（おおよそ日本時間2026-02-18 13:00頃の見込み）。  
- 技術的影響：ACMEはCertbotなどクライアントでTLS証明書を自動取得/更新する仕組み。発行停止が続くと、
  - 新しいドメインでの証明書取得が失敗する
  - 自動更新が切れる直前の証明書が更新できない可能性がある
  - SXG（Signed Exchange）署名用証明書の発行も停止し、検索表示や配信に影響する可能性がある  
 ただし、既存の有効な証明書自体は直ちに失効するわけではありません（期限までは有効）。
- 範囲と注意点：公式ステータスページでACME系のみが明示されているため、Google Cloudその他サービス全体の停止を意味するものではありません。影響有無は使用しているCAや設定に依存します。

## 実践ポイント
- すぐ確認すること：
  1. 直近で期限切れを迎える証明書がないか（まず72時間〜1週間以内の有効期限を優先確認）。
  2. CI/CDや自動更新ジョブのログ（ACMEチャレンジ失敗を確認）。
  3. 使用中のCAがGoogle Public CAかどうか（ACMEエンドポイントを確認）。  
- 対策案：
  - 期限が近い証明書がある場合は手動で他CAからの取得を検討する（短期的な代替）。
  - 自動化スクリプトに「フェイルオーバー先のCA」や失敗時のリトライ・アラートを組み込む。
  - SXGを利用するメディアは署名プロセスの失敗ログを監視し、影響範囲を把握する。  
- 監視と連絡：
  - 公式ステータスページを逐次確認：https://status.pki.goog/incidents/5oJEbcU3ZfMfySTSXXd3
  - 影響が大きい場合はサポート窓口へ連絡し、ログや環境情報を準備しておく。

短期的には落ち着く可能性が高いですが、自動化に依存している環境ほど事前のフェイルオーバー設計が有効です。
