---
layout: post
title: "Show HN: TinyCity – A tiny city SIM for MicroPython (Thumby micro console) - TinyCity：MicroPython向けの小さな都市シム"
date: 2026-01-15T15:41:07.687Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/chrisdiana/TinyCity"
source_title: "GitHub - chrisdiana/TinyCity: TinyCity is a city simulation game inspired by SimCity for MicroPython"
source_id: 46632768
excerpt: "限られたPicoで動くMicroPython製の都市シムTinyCityを遊んでみよう"
image: "https://opengraph.githubassets.com/0d8b0fbd82a7620791f7ff62d802884216a4430c949a9a9cf2f212f7c8895663/chrisdiana/TinyCity"
---

# Show HN: TinyCity – A tiny city SIM for MicroPython (Thumby micro console) - TinyCity：MicroPython向けの小さな都市シム
小さなマイコンで作る「シムシティ」風ゲーム — Pico/Thumbyで遊べるミニ都市経営シミュ

## 要約
Raspberry Pi RP2040上で動くMicroPython製の都市シミュレーションゲーム「TinyCity」。限られた画面・CPU・メモリで、ゾーニング、電力、犯罪・汚染、災害などを簡潔にシミュレートする作品です。

## この記事を読むべき理由
マイコンやMicroPythonで「ちゃんと動く」本格的なシミュレーションを見たい人、教育用プロジェクトや趣味のハードウェアゲーム制作の参考にしたい日本のメイカー／学生にとって、実装の工夫や学びが多いからです。Raspberry Pi PicoやThumbyのような小型デバイスが国内でも手に入りやすい点も追い風です。

## 詳細解説
- 何が動くか  
  TinyCityはSimCity風のゲーム要素を削ぎ落とし、RP2040上のMicroPythonで動作するように最適化した都市シムです。地形（複数の地形 or ランダムマップ）、住宅・商業・工業のゾーン、予算管理、人口増減、電力網、犯罪・汚染、ランダムに発生する災害、マイルストーンによるボーナス、セーブ/ロード機能などを備えます。警察署・消防署・発電所・スタジアム等の施設を配置して成長を図ります。

- 技術的ポイント（初心者向けに平易に）  
  1) ハード制約への対応：小型デバイスは画面解像度・メモリが限られるため、タイルベースの描画やステップごとの簡易計算（完全な物理や複雑なAIを回さない）で高速化しています。  
  2) シンプルなシミュレーションルール：人口・需要・電力供給・犯罪率などは複雑な方程式ではなく、閾値＋確率イベントで表現され、MicroPythonでも十分に動きます。  
  3) イベント駆動と保存：災害はランダムイベントとして扱い、進行状態はファイル（MicroPythonの小さなファイルシステム）に書き出してセーブ/ロードします。  
  4) 開発の足がかり：コードはPythonなので読みやすく、ゲームロジックやUIを学ぶ教材として最適です。GPL-3.0で公開されており、ソースを参考に改造・学習できます。

- 背景・由来  
  本作はArduboy向けのMicroCityに触発されており、小型ゲーム機コミュニティでの「レトロ風ミニゲーム」をMicroPython上で実現した例です。

## 実践ポイント
- すぐ試す手順（基本）  
  1) 必要なもの：RP2040搭載ボード（Raspberry Pi PicoやThumbyなど）、MicroPythonファームウェア、PC（Thonny推奨）。  
  2) リポジトリをクローン：`git clone https://github.com/chrisdiana/TinyCity`（PC上で実行）。  
  3) ThonnyでMicroPythonボードに接続し、リポジトリ内のソースをボードへコピー（READMEやsrcフォルダを確認）。  
  4) main/shellから起動して遊ぶ。操作や税率変更などはメニューから行えます（READMEのTips参照）。

- 日本の現場での活用アイデア  
  - プログラミング授業やワークショップの題材：ゲーム性があるので学生の関心を引きやすい。  
  - ハードウェア改造の足がかり：表示を別ディスプレイに切り替えたり、入力を独自ボタンに接続して実験できる。  
  - ローカル化／機能拡張：日本向けのイベントや課題（災害対応シナリオなど）を組み込むと教育用途で面白くなる。

- 見ておくべきポイント（学習のコツ）  
  - 描画ルーチン、ゲームループの更新頻度、保存処理の実装を確認して、リソース制約での設計手法を学ぶ。  
  - ランダムイベントやマイルストーンのトリガー条件を読み、シンプルなルール設計の考え方を掴む。

ライセンスはGPL-3.0。ソースはGitHubで公開されており、改造・教育利用の土台として最適です。興味があればリポジトリを覗いて、Thonny＋Picoで一度動かしてみることをおすすめします。
