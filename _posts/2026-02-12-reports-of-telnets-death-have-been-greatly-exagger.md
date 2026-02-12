---
layout: post
title: "Reports of Telnet’s Death Have Been Greatly Exaggerated - Telnetの“死”に関する報告は大きく誇張されていた"
date: 2026-02-12T00:37:06.114Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.terracenetworks.com/blog/2026-02-11-telnet-routing"
source_title: "Reports of Telnet’s Death Have Been Greatly Exaggerated &mdash; Terrace Networks"
source_id: 822819845
excerpt: "CVE対策前に要検証：Telnet消失はISP遮断でなく観測バイアスやスキャナ回避の可能性が高い"
image: "http://static1.squarespace.com/static/68753b4b6af18340a5cecce3/t/698cdbae9e200c2530587627/1770838963696/telnet_heatmap.png?format=1500w"
---

# Reports of Telnet’s Death Have Been Greatly Exaggerated - Telnetの“死”に関する報告は大きく誇張されていた
「本当にTelnetが消えたのか？」測定のワナを暴く最新検証

## 要約
GreyNoiseが報告した大規模なTelnet流量の「突然消失」は、Terrace Networksらの検証でコアISPによる一斉遮断では説明できない可能性が高いと示されました。測定アーティファクトやスキャナの回避が原因と考えられます。

## この記事を読むべき理由
日本でも組み込み機器や古い運用機器にTelnetが残る現場は多く、CVE-2026-24061のような脆弱性対策に関する議論が活発です。ネットワーク遮断を前提に運用変更する前に、データの見方・検証手法を知っておくことは重要です。

## 詳細解説
- 背景：GreyNoiseはCVE公表後にTelnetセッション数が急減したと報告。見た目は「一晩で数万→数百」に落ちるステップ関数的変化。これがコアISPによるフィルタリングの証拠だと受け取られ議論に発展。
- Terraceの検証：
  - 自社センサーでTCP三者ハンドシェイクが成立したポート23接続（IPスプーフィングを排除）を調べた結果、問題とされたAS群からの端末IPは引き続き観測され、1月14日付近での大規模な消失は確認できなかった。
  - RIPE Atlas を使ったTelnetトレース（報告で「遮断」とされた56 ASのうち55で接続確立）や、Dataplane.orgなど他観測データとも整合。
- なぜ差が出たか：
  - セッション数（total sessions）をそのまま可視化すると、単一の大規模スキャナやパスワード当てツールが大量の短時間セッションを作り、統計を歪める。
  - スキャナ側が特定の観測点（例：GreyNoise）を指紋化して避けることで、その観測点からは「消えた」ように見える可能性がある（測定バイアス）。
  - 結論：コアISPによる一斉遮断の直接証拠は無く、観測点バイアスやスキャナ挙動の影響が尤もらしい説明。

## 実践ポイント
- まずエッジ（端末／サービス）のパッチ：CVE-2026-24061をはじめ脆弱性は放置しない。
- ログ／指標は「ユニークな送信元IP」やフィンガープリントで見る：セッション数のみで判断しない。
- 複数の観測箇所でクロスチェックする：自前センサー、公開データ（GreyNoise、Dataplane、RIPE Atlas等）を組み合わせる。
- ネットワークが遮断している前提での運用変更は慎重に：まず到達性テスト（traceroute/TCP handshake）で確認する。
- 日本の現場向け：IoTや産業機器にTelnetが残存しているケースがあるため、資産棚卸し→パッチ／ファイアウォールでの制限を優先する。
