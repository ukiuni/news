---
  layout: post
  title: "Show HN: Open-Source 8-Ch BCI Board (ESP32 and ADS1299 and OpenBCI GUI) - オープンソース8ch BCIボード（ESP32＋ADS1299＋OpenBCI GUI）"
  date: 2026-01-05T18:12:42.721Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/Cerelog-ESP-EEG/ESP-EEG"
  source_title: "GitHub - Cerelog-ESP-EEG/ESP-EEG: Cerelog ESP-EEG High-precision 8-channel biosensing board designed for EEG, EMG, ECG, and Brain Computer Interface (BCI) research applications."
  source_id: 46502051
  excerpt: "ESP32＋ADS1299搭載の低ノイズ8chオープンBCI基板、OpenBCI GUI/LSL対応"
  image: "https://opengraph.githubassets.com/65fb82fa1ea3d0c92a23971e48491bffee1b3d31b9a69db34f3631196eef44fa/Cerelog-ESP-EEG/ESP-EEG"
---

# Show HN: Open-Source 8-Ch BCI Board (ESP32 and ADS1299 and OpenBCI GUI) - オープンソース8ch BCIボード（ESP32＋ADS1299＋OpenBCI GUI）
研究クラスのノイズ低減を備えた「ESP-EEG」で、手元で始めるBCI/EEGプロトタイピング

## 要約
CerelogのESP-EEGは、ESP32 + TI ADS1299を採用したオープンソースの高精度8チャネル生体センサ基板で、OpenBCI GUIフォークやLab Streaming Layer（LSL）経由で既存の解析ツールと連携できます。研究用途向けのノイズ対策（アクティブ・クローズドループ・バイアス）やWi‑Fi対応（β）も特徴です。

## この記事を読むべき理由
大学やスタートアップ、ホビイスト問わず、日本でもBCI・EEG・EMG・ECGの実験を手軽に始めたい人にとって、安価に入手できる“研究寄り”ハードとソフトの組み合わせは貴重です。国産外の研究成果やツールとの接続性（LSL、BrainFlow）を確保している点も実運用で役立ちます。

## 詳細解説
- ハードウェア核
  - ADC: Texas Instruments ADS1299（24-bit、研究グレード）
  - チャネル: 8差動チャネル + 1アクティブバイアス（Drive Right Leg）
  - マイコン: ESP32-WROOM-DA（デュアルコア、Wi‑Fi/BT対応）
  - サンプリング: デフォルト250 SPS
  - 電源/コネクタ: USB-C（データ/電源）＋JST-PH 3.7V LiPo対応バッテリー
- ソフトウェアと互換性
  - OpenBCI GUIのカスタムフォークを用意。GUIでの可視化とLSLストリーミングが可能。
  - Pythonクライアント経由でLab Streaming Layerへ直接ストリームでき、Matlabや他の解析ソフトと統合可能。
  - BrainFlow対応手順・テストスクリプト（filtered_plot.py）あり。リポジトリ内にサンプルやファームウェア、回路図、3Dプリント用データも同梱。
  - Wi‑Fiによるストリームはベータ段階で、OpenBCI GUIフォーク／LSLとの組み合わせで運用。
- ノイズ対策（差別化ポイント）
  - 多くの廉価版デバイスが採る「オープンループ」ではなく、ADS1299の機能を使い共通モードを測定→反転→体内へ能動駆動するTrue Closed‑Loop Active Bias（Drive Right Leg）を実装。
  - 結果として50/60Hz雑音や運動アーチファクトに強く、非シールド環境でも研究に耐えるノイズフロア削減を狙う設計。
- 重要な安全注意
  - 本機は絶縁（galvanic isolation）を備えないため、必ずバッテリー駆動のノートPCやモバイル機器で使用すること。家庭用コンセントに接続されたデスクトップや充電中のラップトップへの接続は感電やノイズ増大のリスクがあります。
  - 製品は医療機器ではなく、研究・教育目的向け。UL/FCC認証は取得していません。

## 実践ポイント
1. リポジトリをクローンして、README→firmware→hardwareの順で目を通す。回路図と3Dモデルで組立イメージを把握する。
2. OpenBCI GUI（Cerelogのフォーク）とLSL Pythonクライアントを使えば、すぐに可視化と外部ソフトへのストリームが可能。まずは用意されたfiltered_plot.pyで動作確認を。
3. 絶対にバッテリー駆動で運用する。日本の100V系コンセント環境では特に注意（ラップトップのAC接続はNG）。
4. BrainFlow経由で既存の解析パイプラインに接続：リアルタイム解析や機械学習モデルの入力に使える。
5. ノイズ評価を行う：Drive Right Legの効果を確かめるために、同一条件で「バイアス有り/無し」を比較すると効果が確認しやすい。
6. 法規・倫理面の確認を忘れずに：研究や人体計測を行う場合は所属機関の倫理審査や安全基準に従うこと。

興味があるなら、GitHubのリポジトリとCerelogのドキュメント、Discordコミュニティ（リポ内リンク）を参照してプロジェクトに参加してみてください。
