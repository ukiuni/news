---
layout: post
title: "Why NUKEMAP isn't on Google Maps anymore - なぜNUKEMAPはGoogle Maps上にないのか"
date: 2026-01-14T14:13:22.755Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.nuclearsecrecy.com/2019/12/13/why-nukemap-isnt-on-google-maps-anymore/"
source_title: "Why NUKEMAP isn&#039;t on Google Maps anymore | Restricted Data"
source_id: 46615374
excerpt: "NUKEMAPがGoogleの高額APIと不安定さでMapbox＋Leafletに移行した実録"
image: "https://i0.wp.com/blog.nuclearsecrecy.com/wp-content/uploads/2019/12/Old-NUKEMAP.jpg?fit=1854%2C744&ssl=1"
---

# Why NUKEMAP isn't on Google Maps anymore - なぜNUKEMAPはGoogle Maps上にないのか
魅力的タイトル: 「人気サイトがGoogle地図を捨てた理由 — 無料時代の終焉と代替地図で生き残る方法」

## 要約
Google Maps APIの仕様変更と料金改定で、教育系で人気のインタラクティブ地図「NUKEMAP」はGoogle依存をやめ、Mapbox＋Leafletへ移行した。これは小規模開発者や教育現場にとって重要な先行事例だ。

## この記事を読むべき理由
Googleの地図APIはかつて無料で手軽に使え、実験的サービスや教育プロジェクトを大量に生んだ。だが近年の価格・サポート方針の変化は、日本のスタートアップ、大学、自治体の実装コストや長期運用リスクにも直結するため、選択肢と移行戦略を知っておく価値がある。

## 詳細解説
- 背景：NUKEMAPは2012年にGoogle Maps APIで実装され、多くのアクセスを得る「教育的デモ」だった。Googleは機能やプラグインを度々廃止・非推奨にし、API側にはスタンドアロン版にある多くの機能が回されないままになった（例：Google Earth Pluginの廃止で3D機能が失われた）。
- 料金問題：GoogleはAPIの課金体系を変更し、「動的マップロード」などで急速にコストが膨らむモデルに移行。NUKEMAP作者は利用規模で数千〜数万ドル規模の請求増を経験し、小規模な教育・非営利プロジェクトにとっては継続が困難になった。
- サポートと運用の不確実性：学術個人や小規模開発者は“教育機関としての割引”が受けにくく、サポート窓口に辿り着くのも困難。結果として運用の不確実性（将来急に料金が跳ね上がる／機能が切られる）を嫌って代替へ移行する判断が合理的になった。
- 移行先と技術的対応：NUKEMAPはMapbox（タイル・スタイル提供）＋Leaflet（軽量なオープンソースJS地図ライブラリ）へ移行。Leafletは標準で大円（great circle）描画を持たないため、作者はプラグインを自作して対応した。Mapboxは個別の支援やクレジットを提供し、実務上の連絡とサポートが得やすい点が評価された。
- 物理・モデル面の注記：フォールアウト等の物理モデルは計算上の簡便化を使う。NUKEMAPでは崩壊率を表す経験式としてWignerのフタルク則のように減衰を近似する式を参照している（単純化された時間依存は $t^{-1.2}$ のような形で表現されることがある）。

## 実践ポイント
- 小〜中規模の地図アプリ開発は、まずLeaflet＋タイルサービス（MapboxやOSSタイル）で設計する。可搬性とコスト予測がしやすい。  
- 料金試算は必須：GoogleでもMapboxでも「動的リクエスト」「タイルロード」単位で課金が変わる。必ず公式の料金計算ツールで想定PVを入れて試算する。  
- 3D表現が必須なら要検討：グローバルな3D建造物データやGoogle Earthクラスの機能は限られるため、CesiumJSなどの組合せや静的エクスポート（KMZ）で代替案を検討する。  
- 教育現場の授業設計：学生には「将来のランニングコストとベンダーロックイン」を教えるべき。短期プロジェクトなら使いやすさで選ぶが、公開サービスや流行を期待するアプリはオープンソース基盤が安全。  
- マイグレーションの実務：Leaflet移行時はプラグイン実装（大円、描画最適化、投影差対応）とタイルキャッシュ戦略を用意する。Mapbox等と交渉してクレジット／サポートを得ると運用が楽になる。

短く言うと：無料時代が終わり、サービスの「持続性」と「コスト透明性」が最重要になった。NUKEMAPの移行は、日本の開発者・教育者が同じ判断を迫られたときの良い参考例になる。
