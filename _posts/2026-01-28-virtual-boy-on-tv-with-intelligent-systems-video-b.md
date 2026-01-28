---
layout: post
title: "Virtual Boy on TV with Intelligent Systems Video Boy - インテリジェントシステムズのビデオボーイでVirtual Boyをテレビ出力"
date: 2026-01-28T14:49:21.215Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hcs64.com/video-boy-vue/"
source_title: "Intelligent Systems Video Boy VUE"
source_id: 46792572
excerpt: "インテリジェントシステムズのビデオボーイでバーチャルボーイ映像をテレビ出力、PALで高画質保存可能"
---

# Virtual Boy on TV with Intelligent Systems Video Boy - インテリジェントシステムズのビデオボーイでVirtual Boyをテレビ出力
魅惑の“開発機”が残した、Virtual Boy映像をそのままテレビで見るための魔法装置

## 要約
Intelligent Systems製「Video Boy (VUE)」は、Virtual Boy用カートリッジを差してテレビやモニタにステレオ（左右を赤/緑で表示）出力する開発向けユニット。内部はVirtual Boy基板＋映像変換ボードで構成され、PAL 50fps出力をネイティブに作るのがポイント。

## この記事を読むべき理由
レトロゲーム保存や配信をする日本の愛好家・開発者にとって、オリジナルの映像信号を正しく取り扱う知見（PAL出力の扱い、RGB/S-Video優先など）は品質向上と保存性確保に直結します。さらに内部設計は開発ツールの技術的興味をそそります。

## 詳細解説
- 用途と成り立ち：Intelligent Systemsが開発・提供したデバッグ／デモ用途の機器で、任天堂の取材や開発現場でも使われた記録あり。カートリッジを差すと実機の左右表示をそれぞれ赤・緑でテレビ表示する仕組み。
- 出力仕様：AVマルチアウトはPAL（50FPS）に対応。Virtual Boy本来のタイミングを保つためNTSC（約60FPS）への変換を避けている点が重要。
- ハード構成：ケース内は（左）モニタ変換基板、（中央上）Virtual Boyメイン基板（MAI-VUE-X8, Ver. C相当）、（右）電源。映像は横方向に走査する「列」を生成するため、行・フレームに回転・バッファする変換回路が必要で、基板上にSRAM（複数の32KB×8）やXilinx XC3064 FPGA×2、1Mbit EPROM（NEC D27C1024）といった構成が見られる。
- 映像処理：FPGA＋PROMで入力を保持しスキャン出力へ変換。MB40778 DAC×2とNintendo製S-RGBエンコーダでRGB/S-Video/コンポジット出力を生成。384×256相当のフレームバッファ設計が推測され、2ビット/ピクセル表現を拡張して8bit相当で取り回している可能性が高い。
- 操作系：フロントにカートリッジ／リンク／コントローラ端子、底面にDIPスイッチ（SW1）。特にスイッチ7/8が左右表示の選択（8=左/赤、7=右/緑、両方=アナグリフ合成）。スイッチ5はオンにすると動作停止になる旨が報告されている。
- 実際の画質：S-VideoやRGBが最も鮮明。コンポジットはややぼやける。配信用にElgatoで取り込み→ffmpegのyadifでフィールド deinterlace がよく使われる実例あり。
- 開発向け拡張：SCANERポートやデバッガ用コネクタ（CN1/CN2）の未実装箇所があり、VUE-DEBUGGERとの連携を見越した設計痕がある。

## 実践ポイント
- 高画質取得：可能ならRGB出力を使う（DB9→3×RCAケーブル等）。S-Videoが次点。コンポジットは画質低下に注意。
- キャプチャ環境（日本向け注意）：Video BoyはPAL 50Hz出力のため、日本のNTSC機材やテレビではスペック差で問題が出る。PAL対応キャプチャカード／モニタか、変換品質に注意したラインコンバータを用意する。
- スイッチ確認：底面DIPの7/8で左右表示切替、両方でアナグリフ表示。5は無効化されるので触らないこと。
- 配信・保存：取り込みはフィールド解除（例：ffmpeg + yadif）で安定。色分離（赤/緑）を意識してカラー補正を行うと見栄えが良くなる。
- 技術資料参照：Intelligent SystemsのVUE関連資料やレトロ保存コミュニティ（Planet Virtual Boy、個人ブログ等）を参照するとデバッグ仕様や実例が見つかる。

興味があるなら、入手時はラベル表記（MAI-VUE-X8、Ver. C等）や付属ケーブルの有無、PAL出力である点を確認すると失敗が少ない。
