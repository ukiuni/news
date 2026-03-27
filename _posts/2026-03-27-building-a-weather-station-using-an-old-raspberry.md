---
layout: post
title: "Building a Weather Station Using an Old Raspberry Pi - 古いRaspberry Piで作る気象観測ステーション"
date: 2026-03-27T15:48:29.689Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/nandofm/building-a-weather-station-using-an-old-raspberry-pi-5333"
source_title: "Building a Weather Station Using an Old Raspberry Pi - DEV Community"
source_id: 3385945
excerpt: "古いラズパイで簡単始動、近隣データで線形回帰補正するベランダ気象観測"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fv9qyjrue94xqyq3ytp8n.jpg"
---

# Building a Weather Station Using an Old Raspberry Pi - 古いRaspberry Piで作る気象観測ステーション
古いRaspberry Piをベランダに置いて、自分だけの小さな気象観測ステーションを作る方法

## 要約
PimoroniのWeather HATを古いRaspberry Pi（例：Pi 2）に接続し、センサーデータを取得して、温度補正は近隣の気象局データを使った線形回帰で行うというハンズオン事例。

## この記事を読むべき理由
狭い日本の住宅事情でも実現しやすい手順と、「CPU熱で歪む温度」の実務的な補正方法（固定オフセットでは不十分）を学べるため、DIYからデータ品質まで一気に理解できます。

## 詳細解説
- ハードウェア
  - 本文ではRaspberry Pi 2 model B+とPimoroni Weather HATを採用。Weather HATはGPIOに差すだけで温度・湿度・気圧などが取得でき、風速・降雨センサーも接続可能（スペースがあれば拡張可）。
- ソフトウェア
  - Pimoroniが提供するPythonライブラリをインストールしてサンプルを動かすだけでデータ取得は容易。GitHubに例が揃っている。
- 実際の課題
  - 問題点は「温度センサがPiのCPUに近いため熱影響を受ける」こと。公式チュートリアルの固定オフセットは状況によって誤差が変わるため不十分。
- 補正手法
  - 近隣の気象観測所の温度と自ステーションの同時時系列データを収集し、差分に対して線形回帰モデルを作ることで、温度補正を動的に算出。特に高温領域で差が大きくなる傾向があり、固定値より改善されるが完全ではない点に注意。
- 物理的保護
  - ランチボックス＋底上げ＋通気孔で簡易シェルターを作成。通気はCPU冷却に必要だが、風の影響で低めに出る場合もあるため、塞ぎ方と穴の配置はトレードオフ。

## 実践ポイント
- 必要なもの：Raspberry Pi（中古可）、Pimoroni Weather HAT、簡易ケース（透明ランチボックス等）、小物（接着、ゴム足）、インターネット接続。
- セットアップ手順（簡潔）
  1. HATをGPIOに差す、PimoroniのPythonライブラリをpipで導入。
  2. サンプルを動かしてデータ取得確認。
  3. ケースに入れて通気孔を開け、Piを底上げしてセンサを壁面から離す。
  4. 近隣の公開気象データと自ステーションの同期データを取得し、線形回帰で補正係数を計算。
  5. 補正を適用してログを取り、可視化／外部送信（次のフェーズ）。
- キャリブレーションのヒント：データは時間帯・風速・直射日光で差が変わるため、数日〜数週間のデータでモデルを作る。単純な線形回帰でまずは効果を確認。
- 発展案：風速・降雨センサ追加、Pi 5でのオンデバイス解析（軽量モデル）やNextcloudでデータ保管・公開。

短時間で始められ、データ品質改善の学びが得られる良い入門プロジェクトです。
