---
layout: post
title: "Time Station Emulator - タイムステーションエミュレータ"
date: 2026-01-27T22:52:07.135Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/kangtastic/timestation"
source_title: "GitHub - kangtastic/timestation: Synchronize most radio-controlled (&quot;atomic&quot;) clocks and watches using almost any phone or tablet"
source_id: 46786183
excerpt: "スマホスピーカーでJJY等の時刻電波を再現し、電波時計を瞬時に同期するブラウザツール"
image: "https://opengraph.githubassets.com/9bfea646166935ccca2286261b25263348088eb3b7bc55613fe1434e32e51135/kangtastic/timestation"
---

# Time Station Emulator - タイムステーションエミュレータ
魅力的なタイトル: スマホで「原子時計」を再現？ポケットのスピーカーが電波時計を目覚めさせる仕組み

## 要約
ブラウザだけで動くTime Station Emulatorは、スマホやタブレットのスピーカーを使って短距離の「時刻電波」を再現し、多くの電波時計・電波腕時計を同期させられるツールです。

## この記事を読むべき理由
日本ではJJY対応の電波時計が普及しており、市街地の電波干渉や受信不良で自動同期が失敗することが多い。修理や検証、ホビー用途で手元の端末だけで時計を確実に合わせられる実用的な手段だからです。

## 詳細解説
- 何をするか：ブラウザ（WebAssembly）上で時刻信号を生成し、音声出力経路の「高調波漏れ」を利用して実際の低周波時報局（BPC/DCF77/JJY/MSF/WWVB）と同等の電波成分を短距離で発生させ、時計を同期させる。
- 対応局：中国 BPC、ドイツ DCF77、日本 JJY、英国 MSF、米国 WWVB をエミュレート。
- 技術面の肝：
  - ネットワーク時刻を NTP 風のアルゴリズムで取得。
  - 音声DACで再生可能なサンプルレートの下で、元の搬送波の「奇数高次分周（サブハーモニクス）」を作り出す設計。再生時に発生する高調波が環境に漏れて元の周波数成分を復元する仕組み。
  - DST/BST、うるう秒（DUT1 相当）、±24時間のオフセット指定など、時刻情報は比較的忠実にエミュレート。
- 実行環境：
  - ブラウザで完結（インストール不要）。ただし WebAssembly と ≥44.1kHz PCM を出力できるDACが必要。
  - 推奨：2019年以降のスマホ/タブレットの内蔵スピーカー。Bluetooth や高級オーディオ機器、音声圧縮の影響で失敗しやすい。
  - 既知の非対応: 2024年時点で iOS Safari と Android Firefox に互換性問題あり。
- 配布とライセンス：https://timestation.pages.dev/ でホスト。主要コードは MIT ライセンス（一部データはUnicodeやアイコン由来のライセンスあり）。

## 実践ポイント
- 使い方（手短に）：
  1. サイトを開く（可能ならChromeなど対応ブラウザ）。
  2. エミュレートする局を選択（日本ならJJY）。時計側も同じ局/タイムゾーン設定に。
  3. 時計を強制同期モードにする（機種ごとに操作が異なる）。
  4. スピーカーを時計のアンテナ近くに置き、音量を上げる（視覚的な音量インジケータで確認）。耳を近づけないでください。
  5. 最大数分で同期が完了することが多い。
- 注意点：
  - 範囲は非常に短い（数cm〜数十cmが目安）。スピーカーの位置調整が成功の鍵。
  - Bluetooth やハイエンド再生機器は効果が薄い傾向。
  - 法規的な問題や他無線機器への影響に注意して、自己の所有する時計や実験環境で使うこと。
- 活用例（日本向けアイデア）：
  - JJY受信が弱いビル内や地下での同期作業。
  - 電波時計の修理・動作確認。
  - エンジニアの検証ツール（IoT機器の時刻同期挙動確認）。

以上。興味があれば実際のページ（timestation.pages.dev）で手早く試してみてください。
