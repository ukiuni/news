---
layout: post
title: "Sharpie, the fantasy console disguised as an emulator - Sharpie：エミュレータに見せかけたファンタジーコンソール"
date: 2026-01-31T03:51:19.400Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ChristosMaragkos/Sharpie"
source_title: "GitHub - ChristosMaragkos/Sharpie: A fantasy console written in C# with a simple but powerful assembly language"
source_id: 413167832
excerpt: "Sharpie v0.2はVS Code統合と高速アセンブラで短時間に16ビット風ゲーム制作が可能"
image: "https://repository-images.githubusercontent.com/1114626690/418f3617-4f89-44c9-9c0d-1905d67f0e6e"
---

# Sharpie, the fantasy console disguised as an emulator - Sharpie：エミュレータに見せかけたファンタジーコンソール
魅惑の16ビットレトロ開発環境──手早くレトロゲームと低レイヤー学習を両立するSharpie v0.2

## 要約
SharpieはC#で実装された16ビットの「ファンタジーコンソール」で、独自アセンブリ言語・高速アセンブラ・SDK・エディタ統合を備え、レトロ風ゲーム制作と低レイヤー学習を手軽に始められます（v0.2公開）。

## この記事を読むべき理由
日本のインディー開発者や教育現場では、レトロ風表現・小さな制約での設計演習が人気です。SharpieはVS Code/Neovim統合や軽量な開発フローを提供するため、短時間でプロトタイプを作りたい人に最適です。

## 詳細解説
- ハードウェアスペック（ポイント）
  - CPU: カスタム16ビットアーキテクチャ
  - レジスタ: 32個（16×2ページ）
  - メモリ: 64KBアドレス空間
  - カラー: 32色パレット、パレットスワップ対応
  - グラフィック: スプライトレンダリング、カメラ、65536×65536の内部座標空間、テキストオーバーレイ
  - オーディオ: 8モノフォニックチャンネル、Square/Triangle/Sawtooth/Noise、最大128楽器
  - 入力: 2プレイヤー対応

- SDKとツール
  - 高速CLIアセンブラ（GUI版あり）で .asm を .shr カートリッジに変換
  - VS Code / Neovim 用のシンタックスハイライトとエディタサポート（tools/editor-support）
  - PNG→ASM 変換などのユーティリティ（ImageSharp利用）

- ワークフロー
  - コード編集（エディタ統合）→ アセンブル（Sharpie.Sdk）→ Runnerへドラッグして実行
  - リポジトリ構成: /src（C#本体）、/tools（SDK/アセンブラ）、/assets（素材）

- ライセンスと配布方針
  - 本体はLGPL‑2.1。ランナー単体の商用化は推奨しない方針で、商用価値はゲーム側に集中させたい意図あり。

## 実践ポイント
- まず試す: Releasesからv0.2ビルドを入手してRunnerで動かす
- エディタ統合: tools/editor-support を設定してVS Codeで快適に開発
- 最小サンプル
```asm
; asm
.INCLUDE "my_sprites.asm"
LDI r1, $01
OUT_R r1
```
```bash
# bash
Sharpie.Sdk -i mygame.asm
# 生成した mygame.shr を Runner にドラッグ
```
- 用途案: ゲームジャムのプロトタイプ、大学/ワークショップでの低レイヤー学習、チップチューン風サウンド制作
- 貢献・情報収集: Issue/DiscussionやWikiでアーキテクチャ情報や将来的なROMパッケージ化の計画をチェック

興味が湧ったら公式リポジトリ（ChristosMaragkos/Sharpie）を見て、v0.2をダウンロードして触ってみてください。
