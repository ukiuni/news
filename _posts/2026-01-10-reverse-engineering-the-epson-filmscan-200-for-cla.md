---
layout: post
title: "Reverse Engineering the Epson FilmScan 200 for Classic Mac - クラシックMacのためのEpson FilmScan 200リバースエンジニアリング"
date: 2026-01-10T14:18:38.938Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ronangaillard.github.io/posts/reverse-engineering-epson-filmscan-200/"
source_title: "Reverse Engineering the Epson FilmScan 200 for Classic Mac | Ronan Gaillard"
source_id: 46474065
excerpt: "Mac SE/30でEpson FilmScan 200をSCSI逆解析で復活"
---

# Reverse Engineering the Epson FilmScan 200 for Classic Mac - クラシックMacのためのEpson FilmScan 200リバースエンジニアリング
捨てられた35mm機材を蘇らせる——Mac SE/30でSCSIスキャナを動かしたレトロハック

## 要約
1997年製のSCSI専用フィルムスキャナ「Epson FilmScan 200」を、Mac SE/30（System 7）上で動く独自ドライバとして復活させた取り組みを紹介。サービスマニュアルと古いSANEパッチを手掛かりに、コマンド解釈、フレーム選択の謎、カラー対応までを解決した事例。

## この記事を読むべき理由
- 日本でもフィルム現像やレトロコンピュータ愛好者が増えており、古いハードを使ってデジタル化するニーズが高い。  
- SCSI機器や往年のプロトコルに挑む際の実践的な手法（ドキュメント探索、逆アセンブル、既存オープンソースの活用）が学べる。

## 詳細解説
- ハードウェアの特徴  
  - FilmScan 200はSCSIの「Processor」（0x03）デバイスタイプを使い、ESC/I（Epsonのスキャナ言語）コマンドをSCSIのSEND/RECEIVEでやり取りする設計。通常のスキャナ向けコマンド群とは異なる。
  - 最大1200 DPI、フレームサイズは24×36mm（1120×1680px）。

- 情報源と方針  
  - サービスマニュアルがプロトコルやタイミング情報の基礎を提供。  
  - メーカーのTWAINプラグインから68kドライバを抽出して逆アセンブルし、コマンドの流れを把握。だが、全ての答えがそこにあるわけではない。

- 開発環境とAPIの扱い方  
  - 開発はTHINK C 5.0（68k）で、SCSI Manager APIを直接使用。主要操作は SCSIGet → SCSISelect → SCSICmd / SCSIRead / SCSIWrite（TIB使用）→ SCSIComplete。各ステップでエラーハンドリングとリソース解放が必要。
  - カラースキャン用に約5.6MBのバッファ（パーティション8MB推奨）が必要。

- 基本的なスキャン手順（単一モノクロフレームの成功パターン）  
  1. ESC @（Init） → ACK  
  2. ESC C 0x00（モノクロ） → ACK  
  3. ESC R（解像度1200） → ACK  
  4. ESC A（スキャン領域） → ACK  
  5. ESC G（スキャン開始）  
  6. ループでRECEIVE（ヘッダ＋データ）→ ACK、終了ビットまで読み続ける  
  - 出力はPGM（モノクロ）で保存すると現代macOSでも開ける。

- フレーム選択でのハマりどころと解決策  
  - サービスマニュアルにあるESC P（SetBay）はパラメータの形式が不明確で、0-index/1-indexの混乱で失敗。  
  - 発見した解：SANEの非公式パッチ（古いウェブサイトで公開）にある実装は、パラメータを[frame, frame]の両バイト同値・1始まり（1〜6）で送る方式。これで期待通りにフレーム移動する。  
  - さらに、毎フレームごとにESC @を送り直すとキャリブレーションで約30秒無駄になるため、起動時に1回だけ初期化するのが高速化の鍵。

- カラー対応の実装ポイント  
  - カラー時はESC C 0x02で動作するが、スキャナは各ラインごとに3ブロック（G, R, B の順）を返す。つまり1ラインにつきGデータ→Rデータ→Bデータを受け取ってバッファし、後でインタリーブしてRGB出力にする必要がある。  
  - 出力組立例（擬似コード）: output[i*3] = rBuf[i]; output[i*3+1] = gBuf[i]; output[i*3+2] = bBuf[i];  
  - 色順の取り違え（GとRの混同）で初回は緑被りになるため順序確認は必須。

- 結果と運用ワークフロー  
  - 最終的なドライバは約450行のCコードで、6コマ一括スキャンを行いPPM/PGMで保存。SE/30上で6コマのカラー1200 DPIスキャンは約10分。  
  - ファイル転送は現代機側でPythonの簡易FTPサーバを立て、SE/30のFTPクライアント（例：Fetch）でアップロードする運用が手軽。

## 実践ポイント
- 必須資料をまず探す：サービスマニュアルと古いSANEパッチやコミュニティ配布コードは宝。Googleキャッシュや古い個人サイトも当たり。  
- コマンド検証手順：一連のSEND/RECEIVEログを取る（ヘッダとステータスビットの理解が鍵）。  
- フレーム指定は「[n, n]（1始まり）」を試すこと。0始まりを安易に信じない。  
- カラーはラインごとにG→R→Bの順に来る点を実装で考慮する。バッファは各チャンネル分確保。  
- パフォーマンス：初期化は一度だけ。RESETを多用すると時間を浪費する。  
- 現代との橋渡し：PGM/PPMなどシンプルなフォーマットで保存し、FTPやUSB経由で取り出すと互換性が高い。  
- ハードの代替案：USB-SCSIアダプタは動作が不安定なので、可能なら当時のSCSIを持つ実機（例：SE/30）を使う方が現実的。

この記事は、レトロ機材を有効活用してフィルムをデジタル化したいエンジニア／趣味者にとって、実践的なヒントと探索の道筋を示すケーススタディです。
