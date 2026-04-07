---
layout: post
title: "Apollo Guidance Computer restoration videos - Apollo Guidance Computer 復元ビデオ"
date: 2026-04-07T06:41:55.341Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.curiousmarc.com/space/apollo-guidance-computer"
source_title: "curiousmarc.com - Apollo Guidance Computer"
source_id: 47641528
excerpt: "実機復元でAGCの失われたコードと回路を完全再現する作業を詳細に追う動画シリーズ"
image: "https://lh3.googleusercontent.com/sitesv/APaQ0ST0VEfnTjE3OI7X3JRMnG-QdqRQCj6bSPrKTOMhd_CQEEtM7FO36nhqsdgKvGhzmGKEW4eStPpCIy5oJ8QyG16ylXiHYppv3juiz3v6XyX67MfH8LlEWY3xlDrxJPhDOixR-_Lfe7HgS9fkvnKPNBIcgdDot-4j=w16383"
---

# Apollo Guidance Computer restoration videos - Apollo Guidance Computer 復元ビデオ
月面着陸の“脳”を復活させる――レトロコンピュータ復元の最前線

## 要約
CuriousMarc が公開する一連の動画は、アポロ計画で月着陸機を制御した「Apollo Guidance Computer（AGC）」の実機復元過程を詳細に記録し、回路図・コアメモリ修復・FPGAによる完全再現や失われたプログラム復元までを追うドキュメントです。

## この記事を読むべき理由
日本のエンジニアや学生にとって、AGC復元は「組込み系の原点」「ハードウェアとソフトの境界を理解する教材」「FPGAや低レイヤ技術を学ぶ実践的教材」として極めて価値があります。保存・再現の手法は産業技術保存や教育にも応用可能です。

## 詳細解説
- AGC の意義: アポロ着陸の誘導・制御を担った専用コンピュータで、当時の最先端アーキテクチャ（ワード幅、リアルタイム割り込み、コアロープ読み出しによる不揮発記憶など）を備えます。
- 復元プロジェクトの軸:
  - 実機診断と修理: 回路図（agc_schmeatics.zip）やオリジナル・ハンドブックを参照しつつ、実装部品やコネクタ（Malco）の再製作、基板や配線問題の特定・修復を行っています。
  - コアメモリ（消去可能メモリ）問題: 磁性コアを織り込んだプレーンの配線切断やドライバ故障の解析、X線やワイヤ修繕による復旧作業が動画で詳報されています。
  - コアロープ（不揮発プログラム）からのコード復元: 実機を使い歴史的なプログラム（Sundial-E、Sundance、Retread 等）をダンプ、逆アセンブルして失われたソフトを再現。
  - FPGA エミュレーション: Mike Stewart らがゲート精度のAGC FPGA実装（rotinom 等）を作成し、実機と同等の信号レベルでミッションを再現可能にしています。
- 参考資源と報道: Virtual AGC（ibiblio）が公式的リファレンスで、CuriousMarc の動画プレイリスト、WSJ や各種ポッドキャストでの報道も多数あります。

## 実践ポイント
- まず見る: CuriousMarc の AGC 復元プレイリストと Virtual AGC（ibiblio.org/apollo）で資料と動画を確認する。
- 学ぶ順序: 回路図 → AGC ハンドブック → コアメモリ説明動画 → FPGA 実装リポジトリ（rotinom, agc_monitor）。
- 手を動かす: Virtual AGC のエミュレータでまず動作を追い、次に小型FPGAプロジェクトで命令セットやI/Oを再現してみる。
- 保存と発信: 日本でも同様の機材保存・復元に関心があるコミュニティ（大学の計算機史研究会、レトロコンピューティングクラブ）と協業して資料のアーカイブ化・翻訳を検討する。
- 注意点: 実機修復は高電圧・特殊部品が絡むため、作業は専門家と連携して安全・信用できる資料に基づいて行うこと。
