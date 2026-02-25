---
layout: post
title: "About memory pressure, lock contention, and Data-oriented Design - メモリ圧力・ロック競合とデータ指向設計について"
date: 2026-02-25T15:19:35.303Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mnt.io/articles/about-memory-pressure-lock-contention-and-data-oriented-design/"
source_title: "About memory pressure, lock contention, and Data-oriented Design"
source_id: 396868764
excerpt: "Matrix Rust SDKのRoom Listがソートとメモリ配置見直しで99%近く高速化"
image: "https://mnt.io/image/site-poster.jpg"
---

# About memory pressure, lock contention, and Data-oriented Design - メモリ圧力・ロック競合とデータ指向設計について
Room Listが“固まる”原因は意外なところに——クイックソートの乱数とデータ配置で得た劇的な改善

## 要約
Matrix Rust SDKのRoom Listが断続的に「空白」になり長時間応答しない現象は、内部のソート処理が大量の一時割当とロック競合を生み、メモリ圧力で遅延を招いていた。Data-oriented Design（データ指向設計）でメモリ配置とアロケーションを変え、実行時間を98.7%削減・スループットを7718.5%改善した。

## この記事を読むべき理由
モバイルやクロスプラットフォームUIで「リスト表示が遅い」「突発的にフリーズする」問題は日本のアプリ開発でも頻出。Rustやリアクティブストリームを使う現場、Android/iOSのパフォーマンス改善に直結する実践的な気づきが得られる。

## 詳細解説
- 背景：Matrix Rust SDKのRoom Listは、変更差分（VectorDiff）を流す高階ストリームでリアクティブにUIを更新する設計。差分だけを扱うため本来は効率的。
- 問題の観測：ある状況でRoom Listが「空白」に見える。解析で眼に入ったのは eyeball_im_util::vector::sort::SortBy による膨大な割当（約322k回、743MiB）。端末で最悪数分待たされるケースがあった。
- 根本原因：
  - SortByの初期ソートは内部でVector::sort_by（クイックソート）を使い、実装が擬似乱数（PRNG）をピボットに使っていたため、実行ごとに比較回数が大きく変動。確率的に「病的」な比較回数が発生し得る。
  - ソート中に大量の一時オブジェクト（Roomを囲むArcや中間Vector等）が生成され、頻繁なアロケーション/解放がGC的に負荷を生む（Android上で顕著）。
  - 高負荷下でロック（Mutex等）が競合し、スレッド待ちが発生、結果“フリーズ”に似た遅延を招く。
- 対策の要点（記事のアプローチ）：
  - データ指向設計でメモリレイアウトを連続化（SoAや連続配列に近い構造へ）し、要素あたりのアロケーションを削減。
  - 一時バッファやソート用メモリを再利用し、新しい割当を抑制。
  - ホットパスからArc/重い参照カウントや細粒度ロックを排し、読み取り側を軽くする。
  - ソートアルゴリズムやピボット選定を見直し、最悪ケースを避ける（例：イントロソートや安定した手法、事前に予約したバッファ）。
- 成果：上記の再設計で実行時間がほぼ100%短縮、スループットは数十倍に改善した（元記事の計測結果）。

## 実践ポイント
- まずプロファイルを取る：Android Studioのメモリアロケーション/コールツリーでホットスポットを特定する。
- ホットパスの割当を減らす：UI更新の差分処理で要素ごとのArcやBoxを作り続けない。可能なら参照を軽くする・連続配列に変更する。
- バッファ再利用：ソートやマージで使う一時Vectorを都度確保しない（reserveやpoolを活用）。
- ロックと共有状態を最小化：読み取り多めならロックフリーやコピーオンライトの戦略を検討。
- ソート戦略を見直す：ランダム化に頼るクイックソートの最悪ケースを回避するか、安定で予測可能な手法へ切替える。
- テストと検証：初期化時（初回の全体ソート）が遅くなっていないかを評価し、実機で再現テストを行う。
- UI向け差分は軽量に：VectorDiffのような差分ストリーム設計は強力だが、差分単位の重量化（重い値を流す）は避ける。

以上はRustやモバイルUIでの実務に直結する示唆です。ソートやメモリ配置は「アルゴリズム」だけでなく「データの置き方」で大きく変わる、という点が肝です。
