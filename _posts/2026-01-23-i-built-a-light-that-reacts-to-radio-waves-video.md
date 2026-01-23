---
layout: post
title: "I built a light that reacts to radio waves [video] - 無線波に反応するライトを作った"
date: 2026-01-23T06:25:57.127Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=moBCOEiqiPs"
source_title: "I built a light that can see radio waves - YouTube"
source_id: 46728808
excerpt: "無線（Wi‑Fi/Bluetooth）の見えない電波をLEDで可視化する自作ライト"
image: "https://i.ytimg.com/vi/moBCOEiqiPs/maxresdefault.jpg"
---

# I built a light that reacts to radio waves [video] - 無線波に反応するライトを作った
見えない「電波」を光で見せる──自宅やオフィスの電波環境が一目でわかるDIYアイデア

## 要約
作り手は、周囲の無線信号（Wi‑FiやBluetoothなど）を検知してLEDの明るさや色を変える「ライト」を自作し、見えない電波の存在と強さを視覚化している。

## この記事を読むべき理由
都市部でのWi‑Fi/IoT増加や5G展開が進む日本では、電波干渉や信号環境の理解が実用的価値を持つ。初心者でも取り組める工作として、遊びながら無線の基礎を学べるため紹介する。

## 詳細解説
- 仕組みの概略  
  - アンテナで空間の電波を受信 → RF検出器（ダイオード型のエンベロープ検出器、または対数利得のRF検出IC）で信号強度を直流に変換 → マイコン（例：ESP32やRaspberry Pi）でADC読み取り → LED（NeoPixel等）を制御して明るさ・色に変換。  
- 検出対象と帯域選択  
  - 家庭環境なら2.4GHz（Wi‑Fi/Bluetooth）、5GHz（Wi‑Fi）、FM/AMなど幅広い。用途に応じてバンドパスフィルタや指向性アンテナで目的帯域を絞る。  
- 実装上の注意点  
  - 検出は「電力検出（パワー）」であり、復調して中身を読むわけではない（プライバシー侵害にならない）。ノイズや隣接チャネルの影響を受けるためキャリブレーションが必要。SDR（RTL‑SDR等）を使えば周波数スペクトラムを細かく可視化できるが、回路は複雑になる。  
- 応用例  
  - アート作品として空間の“にぎわい”を可視化、Wi‑Fiデッドスポットの発見、電子工作ワークショップでの教育素材。

## 実践ポイント
- 手軽に始める材料例：RF検出モジュール（例：簡易ダイオード検出回路やAD8313等）＋ESP32＋NeoPixel。  
- もう一歩踏み込む：RTL‑SDR＋Raspberry Piでスペクトラムを取得し、より細かい周波数可視化を実装。  
- 設計ヒント：指向性アンテナで発信源の方向を推定、ソフトで移動平均を取るとちらつきが減る。  
- 日本での実用性：集合住宅やオフィスで電波混雑の「見える化」に有効。地域の電波利用ルールやプライバシーに注意して制作すること。  
- 学びの進め方：まずは既製モジュールでプロトタイプを作り、回路やフィルタの理解を深める。

興味があれば、使用部品リストや回路図、ESP32用の簡単な制御フロー（ADC→色マッピング）を別途まとめますか？
