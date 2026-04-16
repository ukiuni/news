---
layout: post
title: "Six Characters - 6文字の正体"
date: 2026-04-16T19:18:35.275Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ajitem.com/blog/iron-core-part-2-six-characters/"
source_title: "Six Characters // a.s"
source_id: 47749659
excerpt: "PNRの6文字と発券番号の違い、NUC/ROEで運賃が変わる仕組みを図解で解説"
image: "https://ajitem.com/optimized/images/blog/iron-core-part-2-six-characters-hero.webp"
---

# Six Characters - 6文字の正体
あなたの搭乗券に書かれた「DDTCIV」は何を指すのか？航空業界の60年モノの仕組みをやさしく読み解く

## 要約
PNRの6文字（例：DDTCIV）はGDS内でのみ一意な「セッション識別子」であり、真の不変キーは発券番号（E‑ticket）である。さらに、運賃計算行は存在しない通貨（NUC）と為替（ROE）を使う、70年代から続く複雑なルールで構築されている。

## この記事を読むべき理由
国内外の出張・旅行管理、旅行系サービス開発、決済や会計に関わるエンジニア／担当者は、PNR・発券番号・運賃構成の違いを理解することでトラブル対応やシステム設計が格段に楽になります。

## 詳細解説
- PNR（Passenger Name Record）
  - 6文字のロケーター（例：DDTCIV）はGDS（例：Amadeus）内で一意。別のGDSで同じ6文字が別人に割り当てられる可能性があるため、航空会社側は自社の「レコードロケーター」を別途管理する。
- IATAが定めるPNRの必須要素（RP1830）
  1. NM（名前） 2. IT（旅程） 3. AP（連絡先） 4. TK（発券情報） 5. RF（予約作成者）
  - パスポートや支払情報は任意。最小構成はこの5つ。
- 発券番号（E‑ticket）
  - 3桁のIATA数値コード＋10桁シリアル（例：098‑5801178331）が航空会社内で不変の主キー。PNRは変わっても発券番号は保持されるので実務上の「真の識別子」。
- 運賃計算行（Fare Construction）
  - 例: NAG AI X/DEL AI LON Q DELLON14.00 Q DELLON21.00 228.08 NUC263.08 END ROE88.687919
  - トークン意味：
    - NAG／DEL／LON：都市コード（LONはロンドン全体）  
    - AI：運賃キャリア  
    - X/：通過（fare not broken）  
    - Q：構成サーチャージ（燃料YQとは別）  
    - NUC：Neutral Unit of Construction（存在しない中立通貨）  
    - ROE：NUC→現地通貨の換算率（IATAが週次公開）
  - 例の換算：
    $$
    263.08\ \text{NUC}\times 88.687919 \approx 23330\ \text{INR}
    $$
  - 発券時点でROEを適用し、最終通貨額が決まる（異なる発券地では別のROE・通貨で計算される）。
- ツアーコード／BSP決済
  - PNRに埋め込まれるツアーコードは法人料金の識別や請求先処理に使われ、複数組織の会計処理を跨ぐトレーサビリティを与える。

## 実践ポイント
- 発券番号をシステムの第一キーとして扱う（PNRは参照ハンドルと認識する）。  
- 運賃行を見るときは：都市コード／Xの有無／キャリア／NUC合計／ROEを順に確認する。  
- 海外発券・再予約で金額が変わる場合、まずROEとNUC表記をチェックする。  
- 法人管理者はPNR内のツアーコードやBSP情報を利用して経費照合フローを整備する。  

次回（原著Part 3）は、旅行代理店端末のコマンドライン文化とその実務優位について解説されます。
