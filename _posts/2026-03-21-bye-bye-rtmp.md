---
layout: post
title: "bye bye RTMP - RTMPにさよなら"
date: 2026-03-21T22:54:52.193Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://daniel.haxx.se/blog/2026/03/21/bye-bye-rtmp/"
source_title: "bye bye RTMP | daniel.haxx.se"
source_id: 1036171148
excerpt: "curlが16年支えたRTMPを公式に削除、早急な移行対策を要確認"
image: "https://daniel.haxx.se/blog/wp-content/uploads/2021/06/trimming-hedge.jpg"
---

# bye bye RTMP - RTMPにさよなら
驚きの決断：curlが16年支えたRTMPを公式に切り捨てる理由とこれから取るべき対策

## 要約
curl/libcurlがRTMPサポートを削除。古いライブラリ依存・テスト未整備・利用者少数が理由で、初回非対応リリースは8.20.0（2026-04-29）。

## この記事を読むべき理由
多くの日本企業や開発現場で残る古いストリーミング環境や、ディストリビューションのパッケージ管理、CI/運用に直接影響するため。移行や保守方針を早めに検討する価値がある。

## 詳細解説
- 背景：RTMPはAdobe/Flash由来のプロプライエタリなストリーミングプロトコルで、かつてライブ配信に使われたがHTTP(S)系の普及で存在感は低下。curlは2010年にRTMP対応を統合して以降約16年サポートしてきた。  
- 依存関係：curlは実装をオープンソースの `librtmp`（rtmpdumpプロジェクト由来）に依存。だが `librtmp` 自体にテストがなく、長期間リリースも行われていなかった。  
- テストと利用状況：curl側にもRTMP関連のテストが皆無で、2025年の利用者調査では直近1年でRTMP利用者は2.2%に留まった。少数ユーザー + 未テストのコードは保守リスクと判断された。  
- 廃止のプロセス：警告と猶予（6か月）を挟んだ上で削除が実行。互換性（API/ABI）についてはSONAMEは据え置きで、実運用で影響が出ない限り問題視しない方針。  
- 影響範囲：curlから削除されたURLスキームは `rtmp`, `rtmpe`, `rtmps`, `rtmpt`, `rtmpte`, `rtmpts` の6種類。curl公式のサポートスキーム数は27に減少。初回非対応リリースは curl 8.20.0（2026-04-29）。

## 実践ポイント
- 自分のコードベース/CIを確認：`rtmp` スキームや `librtmp` への依存を grep で検出。  
- 代替技術へ移行：ライブ配信には WebRTC、HLS、DASH、RTSP over HTTP などHTTP系や標準化されたプロトコルを検討。  
- パッケージ管理者向け：ディストリの curl パッケージや `librtmp` レシピを見直し。不要であれば依存削除、必要なら独自ビルドで保守。  
- 維持したいなら貢献を：RTMPを残したければ `librtmp` と curl にテストを追加し、メンテナンスを申し出る必要あり。  
- ログ・監査：運用中の配信ログでRTMP使用を検出して関係者に周知し、移行計画を立てる。

この記事をきっかけに、自社サービスやOSS依存の棚卸しとストリーミング戦略の見直しを。
