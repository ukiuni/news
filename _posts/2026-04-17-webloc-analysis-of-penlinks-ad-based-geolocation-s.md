---
layout: post
title: "Webloc: Analysis of Penlink's Ad-Based Geolocation Surveillance Tech - Webloc：Penlinkの広告ベース地理位置監視技術の解析"
date: 2026-04-17T20:28:32.894Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://citizenlab.ca/research/analysis-of-penlinks-ad-based-geolocation-surveillance-tech/"
source_title: "Uncovering Webloc: An Analysis of Penlink’s Ad-based Geolocation Surveillance Tech - The Citizen Lab"
source_id: 47758309
excerpt: "広告データで何億端末の移動履歴が追跡される実態と日本への示唆"
image: "https://citizenlab.ca/wp-content/uploads/2026/04/COBWEBS_illustration-02.png"
---

# Webloc: Analysis of Penlink's Ad-Based Geolocation Surveillance Tech - Webloc：Penlinkの広告ベース地理位置監視技術の解析
広告データであなたの“移動履歴”が丸見えに？Weblocの正体と日本への示唆

## 要約
Weblocはアプリやデジタル広告から取得した位置情報を大量に集め、数億の端末の移動や属性を過去数年分さかのぼって追跡できる商用監視システムで、Cobwebs→Penlink経由で法執行・治安機関に販売されている。

## この記事を読むべき理由
広告データがどのように「監視ツール」になるかを知ることは、個人のプライバシー対策と企業・行政の透明性要求の基礎になります。日本でもサーバーや販売網の痕跡が確認されており、今後の議論に直接関わる話題です。

## 詳細解説
- 何をしているか：Weblocはモバイルアプリや広告配信のデータ（広告ID、位置座標、プロファイル情報など）を取り込み、最大で5億台規模の端末から連続的にデータを参照・検索できる。顧客は個人や集団の移動、滞在履歴、属性推定を数年分さかのぼって分析できる。
- 仕組み（初心者向け）：スマホ内の広告SDKや広告入札（RTB）の仕組みから位置データが流出し、それを業者が買い集めて結合する。Weblocはそのデータを検索・可視化するプラットフォームとして機能する。
- 誰が使っているか：報告では米国のICEや軍、州・地方警察、ハンガリーの国内情報機関、エルサルバドル警察などが挙がる。欧州では情報公開請求の多くが拒否・保留され、透明性が低い。
- 企業・政治的つながり：Cobwebs（創業者ら）とスパイウェア業者Quadreamとの関係が指摘され、同社製品群（Tangles、Lynx、Trapdoorなど）は位置情報以外のソーシャルエンジンにも関与する可能性がある。Trapdoorはフィッシングやマルウェア配布を助ける可能性があると技術解析は示唆する。
- インフラ分布：調査で関連サーバーは多国に分散（日本含む）しており、データ保管・処理の国際的な越境が懸念材料になる。

## 実践ポイント
- 個人：アプリの位置情報権限を「常に許可」から「アプリ使用時のみ」に変更。広告IDリセットや広告トラッキング無効化、不要なアプリの削除を行う。Exodus Privacyなどでアプリのトラッカーを確認する。
- 開発者/企業：不用意に位置情報を外部に送らない。SDK導入時のデータフローを精査し、利用目的と保存期間を明確に。
- 市民/政策面：地方自治体・警察のツール導入について情報公開を求め、監視技術の導入には明確な法的ガイドラインと監査を要求する。日本では個人情報保護法（APPI）や行政の情報公開制度を活用して透明性を促す。
