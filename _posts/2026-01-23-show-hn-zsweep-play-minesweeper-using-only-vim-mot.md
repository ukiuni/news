---
layout: post
title: "Show HN: Zsweep – Play Minesweeper using only Vim motions - Zsweep：Vim操作だけでマインスイーパを遊ぶ"
date: 2026-01-23T17:05:51.389Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://zsweep.com"
source_title: "Zsweep"
source_id: 46667849
excerpt: "hjklだけで遊べるブラウザ版マインスイーパ、鍵盤操作だけで高速攻略とVim練習が同時にできる"
---

# Show HN: Zsweep – Play Minesweeper using only Vim motions - Zsweep：Vim操作だけでマインスイーパを遊ぶ
魅せるVimゲーミング—キーボードだけで火花を散らすマインスイーパ

## 要約
Zsweepはブラウザで動くマインスイーパで、カーソル移動や操作をすべてVimライクなモーション（hjklなど）で行えるキーボード専用インターフェイスを提供します。

## この記事を読むべき理由
Vimを使う開発者やキーボード中心のワークフローを好む人にとって、日常のタイピング感覚のまま手を休めずに遊べるユニークなゲーム体験。Vim操作の練習にもなり、日本のエンジニアコミュニティに刺さる遊び方です。

## 詳細解説
- ゲーム概要：ブラウザ上で動くマインスイーパ。標準的なボードサイズ（9x9、16x16、30x16）やタイマー、残り地雷数が表示されます。  
- キー操作（画面に表示される例）：tab = restart、esc = settings、enter = reveal（開く）、spc = flag / chord（旗立て／チャード操作）、/ や Vimモーションでの移動を想定。  
- Vimモーション採用：hjklでのセル移動や、w/b/gg/Gのようなジャンプ系操作を使える設計が特徴（サイトは「Vim motions」を前面に出しています）。  
- チャード（chord）操作：従来のマインスイーパで隣接フラグと一致して一括開放する動作に対応しているようで、スペース等で実行します。  
- UIとUX：マウスを使わないため集中が途切れず、タイピング習熟者は高速でプレイ可能。ブラウザベースなので即プレイできます（zsweep.com）。

## 実践ポイント
- 初級者はまず9x9モードでhjklに慣れる。  
- フラグ立て（spc）とチャード操作のタイミングを練習するとミスを減らせる。  
- Vimコマンド（gg/Gや数字＋移動）での高速移動を試して、操作効率を上げる。  
- 会議の合間やペアプログラミングの気分転換に最適。まずは zsweep.com を開いてキーボードだけで遊んでみてください。
