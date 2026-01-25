---
layout: post
title: "Doom has been ported to an earbud - DOOMをイヤホンに移植"
date: 2026-01-25T14:40:40.005Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://doombuds.com"
source_title: "DOOMBUDS"
source_id: 46753484
excerpt: "イヤホンでDOOMが動く！UARTとMJPEGで帯域を克服した移植プロジェクト"
---

# Doom has been ported to an earbud - DOOMをイヤホンに移植
イヤホンの中で悪魔が走る。耳の中で遊ぶクラシックFPSという狂気のハードウェアハック

## 要約
DOOMをPinebuds Pro（オープンファームウェア対応イヤホン）に移植し、インターネット越しに順番待ちで遊べるようにしたプロジェクト。UART帯域・JPEG圧縮・ファームウェア改造で限られた資源を引き出している。

## この記事を読むべき理由
日本でも組み込み・IoTやレトロゲーム文化は盛ん。限られたリソースで動かす技術的工夫や、オープンハードを活用したプロダクト作りの具体例として学びが多い。

## 詳細解説
- 全体構成：  
  1) イヤホン上で動くDOOMポート  
  2) イヤホンとサーバーをつなぐシリアルブリッジ（MJPEGをTwitchへ）  
  3) キュー管理やキー入力転送を行うウェブサーバー  
  4) ブラウザ側の静的フロントエンド（画面表示・通信）

- 通信の制約：  
  Bluetoothは実効1Mbps程度で遅く、UARTの方が有利。UARTで使える帯域は約2.4Mbps。DOOMのフレームバッファは320×200＝96kB（8bit）なので生の転送はフレームレートが激減するため圧縮が必須。

- MJPEGを選択した理由：  
  H.264等はCPU/RAM負荷が高すぎるため、フレームを連続JPEGにして送るMJPEGを採用。典型的な高品質JPEGフレームは約11–13.5KB。理論上のFPSは次のように見積もられる：  
  $ \displaystyle \frac{2{,}400{,}000}{11{,}000\times 8}\approx 27.3\ \text{FPS} $（楽観）  
  $ \displaystyle \frac{2{,}400{,}000}{13{,}500\times 8}\approx 22.2\ \text{FPS} $（保守的）

- CPU・RAMの工夫：  
  既定の100MHzから300MHzにクロックアップ、低消費モードを無効化。Cortex‑M4F@300MHzでDOOM本体は動くがJPEGエンコードで限界（実測約18FPS）。RAMはデフォルト768KB→コプロセッサ無効で約992KBに。DOOMは通常4MBだが、定数化・ルックアップテーブル事前生成・キャッシュ無効化などで削減。

- ストレージ（WAD）問題：  
  元のshareware WADは4.2MBでイヤホンのフラッシュに収まらないため、コミュニティ作成の縮小WAD（Squashware, 約1.7MB）を利用して解決。

- 運用上の小技：  
  長時間のキュー待ちでの帯域節約として、途中から低遅延MJPEGをTwitchの配信に流すなどの工夫あり。

## 実践ポイント
- 試すならPinebuds Proが前提。レポジトリDOOMBudsとDOOMBUDS-JSを参照してビルド／接続手順を確認。  
- UART帯域を想定して動画圧縮はMJPEGが現実的。帯域計算は上の式を使って概算する。  
- メモリ削減テク：定数化、フラッシュから読み出す、不要機能の削除、コプロセッサの無効化。  
- 法的注意：WADなどゲーム資産のライセンスに注意（shareware以外は権利関係を確認）。  
- 日本のイベントやハッカースペースでのデモに向く題材。IoT/組み込みの学習用途や製品デモのアイデアソースになる。

興味があれば、まずはリポジトリを見てビルド手順とライセンスを確認することをおすすめする。
