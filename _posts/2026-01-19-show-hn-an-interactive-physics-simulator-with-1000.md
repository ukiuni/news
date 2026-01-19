---
layout: post
title: "Show HN: An interactive physics simulator with 1000's of balls, in your terminal - ターミナルで千個単位のボールが弾けるインタラクティブ物理シミュレーター"
date: 2026-01-19T23:10:39.157Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/minimaxir/ballin"
source_title: "GitHub - minimaxir/ballin: A colorful interactive physics simulator with thousands of balls, but in your terminal!"
source_id: 46682115
excerpt: "ターミナルで何千個ものカラフルなボールが高速物理で弾ける様子を即体験できるRust製シミュレータ"
image: "https://opengraph.githubassets.com/0a8fad0803964302774c51eaadb61dd0de8045f688f02354f6a7e595598e9d86/minimaxir/ballin"
---

# Show HN: An interactive physics simulator with 1000's of balls, in your terminal - ターミナルで千個単位のボールが弾けるインタラクティブ物理シミュレーター

ターミナルだけで色と動きが楽しめる、Rust製の超高速物理シミュレーター「ballin」。文字だけの画面で何千個ものボールがリアルに弾む様子は一見の価値あり。

## 要約
ターミナル表示（Braille Unicodeを活用）で何千個ものボールを物理エンジン（rapier 2D）で高速にシミュレートするTUIアプリ。クリックやキー操作でインタラクティブに遊べ、シーンをJSONで保存・共有できる。

## この記事を読むべき理由
- Rustや物理エンジンでのパフォーマンス最適化に興味がある人に最適。  
- 端末ベースで視覚的に楽しめるデモは勉強会やデモンストレーション、授業教材として使いやすい。  
- 日本の開発環境（ターミナル文化、軽量ツールを好む層）と相性が良く、低リソースで派手な表現が可能。

## 詳細解説
- 技術基盤: Rustで書かれたTUIアプリ。物理計算はrapier 2Dを利用（リポジトリでは安定性のため0.31.0を使用）。  
- 表示トリック: Braille Unicodeを使うことでターミナルの文字格子を細かいピクセル代わりにして、小さな丸（ボール）を見やすく表現。  
- パフォーマンス: 作者は「10,000個で実効120+ FPS」を報告。ただし環境依存（端末の描画制限やCPU/GPU）で、上限は安全のため15,000個にハードコードされている。  
- インタラクション: マウスクリックで押し出し（repulse）や噴水（geyser）、上部クリックでボール生成、キー操作で重力・摩擦・効果強度の調整、図形挿入や色変更、シーンの保存/読み込みが可能。  
- 制限と注意点: 高速で移動するボールが形状をすり抜ける「トンネリング」が起きる可能性がある（CDDを有効化すると解消できるが大幅な性能低下）。rapierのバージョン差異で安定性の問題があり、最新版で動作不安定なため旧バージョン採用とのこと。  
- 開発メモ: 初期実験にはClaude Opus 4.5が活用されたと明記されている。

## 実践ポイント
- すぐ試す（macOS / Linux 想定）:
```bash
# macOS Apple Silicon
curl -sL https://github.com/minimaxir/ballin/releases/latest/download/ballin-macos-arm.tar.gz | tar xz
# macOS Intel
curl -sL https://github.com/minimaxir/ballin/releases/latest/download/ballin-macos-intel.tar.gz | tar xz
# Linux x64
curl -sL https://github.com/minimaxir/ballin/releases/latest/download/ballin-linux.tar.gz | tar xz
# Rustがあれば
cargo install ballin
```
- 使い方のコツ: 推奨端末（例: Ghostty）を使うとFPS制限の影響を避けられる。実行後は ? でヘルプ、c でカラーモード切替、スペースやShift+1..6でボール投入。--color や --balls フラグで起動時設定が可能。  
- 活用アイデア: 社内ハッカソンのデモ、物理概念の授業用ビジュアル、端末愛好家向けのライブコーディングネタに最適。日本のイベントでのデモやスクリーンキャストも映える。  
- 注意: 低スペック環境ではボール数を減らす、または端末サイズを広げて視認性とFPSを確保すること。

興味が湧ったらGitHubリポジトリ（minimaxir/ballin）をチェックして、端末でカラフルに遊んでみてください。
