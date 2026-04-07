---
layout: post
title: "BrewOps: I built a production-grade HTCPCP server because nobody else would - BrewOps：誰も作らなかったから本番品質のHTCPCPサーバを作った"
date: 2026-04-07T00:02:28.481Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/axrisi/brewops-i-built-a-production-grade-htcpcp-server-because-nobody-else-would-3clh"
source_title: "BrewOps: I built a production-grade HTCPCP server because nobody else would - DEV Community"
source_id: 3442098
excerpt: "冗談RFC「HTCPCP」を本気で本番運用まで作り上げたGo製サーバの技術と運用ノウハウを公開"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Ftvm28zcajlobfp3i4i4n.png"
---

# BrewOps: I built a production-grade HTCPCP server because nobody else would - BrewOps：誰も作らなかったから本番品質のHTCPCPサーバを作った

実在する「418 I'm a Teapot」サーバで遊べる！RFCジョークを本気でプロダクション級に仕上げたエンジニアの挑戦

## 要約
RFC 2324（HTCPCP、1998年の“コーヒーポット”プロトコル）を完全準拠で実装したGo製サーバ「BrewOps」。本番監視、SLA、攻撃検知（DoCS）やライブダッシュボードまで備えたジョークプロジェクトだが、技術的完成度は本物。

## この記事を読むべき理由
珍しいプロトコル実装というだけでなく、「プロトコル準拠」「可観測性」「レート制御」「運用監視」を冗談プロジェクトに真面目に適用した例は、実務での設計・SRE教材として学びが多いからです。日本のクラウド／SRE実務にも応用できる視点があります。

## 詳細解説
- 背景: RFC 2324（HTCPCP）は1998年のエイプリルフールRFCで、BREW/WHENなど独自HTTPメソッドと418 I'm a Teapotを定義。作者はこの「誰も実装してない部分」を本気で実装。
- 機能概要: BREW/GET/WHEN/PROPFINDをサポート。RFC7168（TEA拡張）も対応。Accept-Additions ヘッダ（クリームやウイスキー等）や Safe: if-user-awake ヘッダなど仕様に準拠。
- 実装技術: Go（標準ライブラリのみ）、単一バイナリ（brewopsd）、ゼロ外部依存。net/http はカスタムHTTPメソッドをそのまま通すため実装がシンプル。
- 運用周り: Docker（Brewfile）、Compose（サービス名 barista）、nginx経由で動作。SLA（99.97% は固定値）、リアルタイムダッシュボード（SSE）、インシデントタイムライン、メトリクス（Total brews、418s、Caffeine dispensed 等）。
- 面白機構: 新しいポットはリクエストで自動生成。5つに1つがランダムで「ティーポット」に（BREWすると418を返す）。ポットの状態遷移（idle→grinding→brewing→pouring→ready→cooling→idle）をgoroutineで管理。ジャニターが定期クリーン。
- セキュリティ／運用観点: RFCに従い「Denial of Coffee Service（DoCS）」検出を実装。30秒で10回超のBREWはDoCSと判定して警告を出すがサービスは継続。Cloudflare等のプロキシは非標準メソッドを破棄するため注意が必要。
- UI/UX: フロントはシンプルなHTML/CSS/JSのみ。端末向けはASCIIアート、ブラウザ向けはJSONを返す二重対応（Acceptで切替）。

## 実践ポイント
- まず動かして遊ぶ（ダッシュボードを開いてからcurlで試すとインシデントに反映されます）:
```bash
# 新しいポットでブリュー（自動作成）
curl -X BREW https://brewops.10mins.email/pot -d 'start'

# ティーポットを突く（418が返る）
curl -X BREW https://brewops.10mins.email/pot-2 -d 'start'

# milk用のWHENメソッド（RFC準拠の遊び）
curl -X WHEN https://brewops.10mins.email/pot-0
```
- 学びどころ:
  - Goのnet/httpは非標準メソッドを扱える。新しいプロトコル実験に向く。
  - 非標準メソッドはCDN/プロキシ（例: Cloudflare）で遮断される可能性があるためデプロイ設計に注意。
  - 小ネタでも「可観測性（メトリクス・SSE・インシデント）」を入れると運用練習になる。
  - ハッカソンや社内イベントで「冗談プロトコル」を真面目に作ると学習効果が高い。

日本の読者への一言：冗談のプロトコルでも「運用設計」「監視」「脆弱性対策」の良い教材になります。軽いネタ実装から実践的な運用ノウハウを学んでみてください。
