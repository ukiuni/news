---
layout: post
title: "UDP vs. TCP in Multiplayer Gaming: State Synchronization and Lag Compensation - マルチプレイヤーゲームにおけるUDP vs TCP：状態同期とラグ補償"
date: 2026-02-05T10:39:23.114Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://systemdr.substack.com/p/udp-vs-tcp-in-multiplayer-gaming"
source_title: "UDP vs. TCP in Multiplayer Gaming: State Synchronization and Lag Compensation"
source_id: 408772178
excerpt: "リアルタイム対戦でTCPが生む致命的ラグと、UDP＋予測・補償で快適化する実践設計を具体解説"
image: "https://substackcdn.com/image/fetch/$s_!H71c!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1beba6a-9af3-45e2-8b0f-d56ccff40fb3_4500x3250.png"
---

# UDP vs. TCP in Multiplayer Gaming: State Synchronization and Lag Compensation - マルチプレイヤーゲームにおけるUDP vs TCP：状態同期とラグ補償
驚くほど快適にする「ネットワークの選び方」—TCPが対戦ゲームを殺す理由と、UDPで勝つための実践設計

## 要約
TCPの順序保証がリアルタイム対戦では致命的な遅延（Head‑of‑Line Blocking）を生み、UDPを基盤にした独自の“信頼性と補正”のレイヤーが快適なゲーム体験を作る、という話です。

## この記事を読むべき理由
日本のゲーム開発者やプレイヤーは「遅延＝回線速度」と誤解しがちですが、実際はプロトコル設計が体感ラグを決めます。対戦性の高いタイトルやネットワーク調整で差を出したいなら必読です。

## 詳細解説
- TCPの問題点：TCPは順序と再送を保証するため、途中のパケット欠損で後続パケットを止めてしまいます（Head‑of‑Line Blocking）。例えば60FPSだと１フレームは $16.6\ \mathrm{ms}$、RTTが100msだと数フレーム分の処理がまとめて来て“テレポート”や“フリーズ”が発生します。  
- UDPの利点：UDPは順序保証や再送をしないため、古い状態に縛られず最新の情報を即時処理できます。リアルタイムでは“新鮮さが完全性より重要”です。  
- 必要な補完手法（Netcodeの三本柱）  
  1. クライアントサイド予測：プレイヤー操作を即座に反映し、応答性を改善。  
  2. サーバー整合（Server Authoritative）：サーバーが真の状態を計算し、差分があればクライアントは補正（リコンシリエーション）する。  
  3. エンティティ補間：他プレイヤーは少し過去のスナップショットを補間して滑らかに表示（例：約 $50\ \mathrm{ms}$ のバッファ）。  
- 最適化技術：  
  - デルタ圧縮：前回受けたスナップショットとの差分だけ送る。  
  - 選択的信頼性（RUDP）：移動は不確実でOK、チャットや勝敗イベントは信頼性を担保するハイブリッド設計。  
  - ラグ補償（Rewind）：射撃判定時にサーバーが過去時点に戻して判定。  
- 実運用上の設計配慮：ジッタ、ロス、遅延の可観測化を初期設計から組み込み、プレイヤー向けに指標を出す。UDPは万能でなく、ターン制やロビー等はTCP/WebSocketが適切。  
- 事例：ValveのSource（CS系）が予測と補償を確立、Riotは厳格なサーバ検証＋大胆な補償、Rocket Leagueは物理の再現性のため120Hz同期＋物理リワインドを採用。

## 実践ポイント
- ゲームループの同期はUDPを採用：移動・物理は不確実チャネルで20–30Hz程度送る。  
- 重要イベントはRUDPで信頼性を付与（シーケンス番号＋ACK）。  
- クライアント側で必ず予測を行い、サーバー到着時に差分をリコンシリエートする。  
- デルタ圧縮と送信頻度の設計で帯域を節約（静止時はほぼ差分ゼロ）。  
- 開発初期からパケットロス率・RTTヒストグラム・ジッタを収集し、インゲームで可視化する。  
- Unity/Unreal等の高レイヤーを使う場合でも、これらの基本原理を理解してパラメータをチューニングする。

元記事のデモや実装例は参考リンク（GitHub等）を確認して、まずは小さなプロトタイプで遅延／パケットロス下の挙動を可視化してみてください。
