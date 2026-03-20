---
layout: post
title: "Just Put It on a Map - 地図に示せば説得力は倍増"
date: 2026-03-20T12:49:47.473Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://progressandpoverty.substack.com/p/just-put-it-on-a-map"
source_title: "Just Put It On a Map - by Lars Doucet"
source_id: 47397372
excerpt: "ブラウザだけで地価を3D可視化、駐車場の埋蔵資産を炙り出すツール群"
image: "https://substackcdn.com/image/fetch/$s_!t9fz!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85a016fb-964a-41f9-86ad-3ee56f5e53ac_1375x705.png"
---

# Just Put It on a Map - 地図に示せば説得力は倍増
魅せるデータで都市政策を動かす──「地価を3Dで見せる」新しい説得の技術

## 要約
米国の非営利が公開したオープンツール群（CivicMapper, PutItOnAmap）が、土地評価や遊休地・駐車場の可視化をブラウザで完結させ、都市計画やアドボカシーで効果的に説得力を高める手法を示している。

## この記事を読むべき理由
地価や未利用地の分布は都市政策の意思決定に直結します。日本でも再開発・駐車場転用・中心市街地活性化などで「どこに資源が埋もれているか」を分かりやすく示せれば、行政や住民の合意形成が格段に進みます。

## 詳細解説
- 中心部ほど地価が指数的に高くなる傾向：著者はNYCや地方都市の地価マップを3D化して、中心と周辺で10倍〜100倍の差が普通に現れることを示す。視覚化は直感と現実のギャップを埋める。
- ツール群の構成：
  - CivicMapper：都市単位の3D可視化と分析用公開サイト。ベクトルタイルを用いた大規模都市対応パイプラインを構築中。
  - PutItOnAmap (PIOAM)：ローカル実行を重視した“GISのスイスアーミーナイフ”。MITライセンスで公開。
    - 3D Parcel Explorer：parquet等のデータを読み込んで3D表示・統計・異常検出が可能。
    - Data Fetcher：自治体公開データを取得。
    - GIS Format Converter：フォーマット変換。
    - GIS File Constructor：ファイル結合（SQL不要）。
- 駐車場検出と遊休地分析：公開衛星画像（NAIP 等）とオープンなセグメンテーションモデル（HuggingFaceで公開された研究モデル）を使い、表面駐車場ポリゴンを抽出→評価額と結合して「どれだけ土地価値が駐車場に埋もれているか」を算出。
- ローカル処理の利点：データを外部サーバに送らずブラウザで処理する設計は、プライバシー／法務リスクを下げ、自治体内での導入ハードルを低くする。
- 実務上の注意点：データ品質問題（単位ミスやフィールド誤指定）で「異常に高い柱」が出るケースが多く、3Dで可視化すると異常検出とクレンジングが効率化する。大規模データはメモリ負荷に注意。

## 実践ポイント
- まず入手：自治体のオープンデータポータルからParcel（地番／評価額／面積）や建物データを取得する。
- ローカルで試す：PIOAMのData Fetcher→Format Converterで必要フォーマットにし、3D Parcel Explorerに読み込む。
- 可視化のコツ：評価額を「面積当たり」に正規化してから色付け・3D化すると中心傾斜が見えやすい。異常な尖塔はデータミスのサイン。
- 駐車場分析：衛星画像ベースの駐車場セグメンテーション結果を Parcel と結合すれば、再開発候補地や政策ターゲットが定まる。
- 提案資料化：スクリーンショットや統計（上位駐車場ランキング、空地の土地価合計）を作り、行政や住民向けに数値とビジュアルをセットで提示する。

（補足）日本で試す場合、国土数値や各自治体のオープンデータ、商用衛星／航空写真のライセンスを確認してください。
