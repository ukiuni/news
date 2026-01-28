---
layout: post
title: "Mousefood – Build embedded terminal UIs for microcontrollers - Mousefood — マイコン向け組み込みターミナルUIを作る"
date: 2026-01-28T19:03:55.208Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ratatui/mousefood"
source_title: "GitHub - ratatui/mousefood: embedded-graphics backend for Ratatui"
source_id: 46798402
excerpt: "MousefoodでESP32などの小型ディスプレイに高速でターミナル風UIを簡単実装"
image: "https://opengraph.githubassets.com/d9360b58d365fad63b6af04f6439ab48ee2fce2bdf1814c48b198a4b65702d46/ratatui/mousefood"
---

# Mousefood – Build embedded terminal UIs for microcontrollers - Mousefood — マイコン向け組み込みターミナルUIを作る
小型ディスプレイで「ターミナル風UI」を動かす――Ratatu i 用 no-std バックエンド「Mousefood」が組み込み開発を楽にする

## 要約
Mousefood は Rust の Ratatui（ターミナルUIライブラリ）を組み込み機器向けに動かすための no-std embedded-graphics バックエンドで、低フットプリントなディスプレイ上にリッチな TUI を描画できます。

## この記事を読むべき理由
ESP32／RP2040 などマイコンを使う国内のメーカー／ホビイストが、小型液晶や電子ペーパーでターミナル風UIを手早く作れるようになるため。プロトタイプや携帯デバイス、IoT の操作画面を短期間で整えたい人に特に有益です。

## 詳細解説
- アーキテクチャ: no-std 環境で Ratatui を動かすため、embedded-graphics を使ってピクセル単位で描画する EmbeddedBackend を提供。任意のディスプレイドライバ（ILI9341, SSD1306 等）やエミュレータに接続可能。
- フォントと特殊文字: 組み込み用の bitmap フォントは文字セットが小さいため、ボックス描画やブロック文字が足りない。Mousefood はデフォルトで embedded-graphics-unicodefonts を使い、ボックス描画・ブレイルなど多めのグリフを提供。代替に軽量な ibm437 機能もあり、用途で切替可能。太字/斜体は EmbeddedBackendConfig にフォントを渡すことで対応（すべて同サイズである必要あり）。
- 色とテーマ: ANSI パレットがデフォルト。ColorTheme でカスタムカラーや組み込みテーマ（例: tokyo_night）が使えるため、見た目を簡単に調整可能。
- EPD（電子ペーパー）対応: WeAct／Waveshare 用のドライバ機能があり、flush_callback を通してフレームを渡す設計。低消費電力表示のプロダクトにも適合。
- シミュレータ: embedded-graphics-simulator 経由でデスクトップ上で動かせるサンプルあり（開発・デバッグが容易）。
- 性能と制約: フラッシュ容量が限られるためバイナリ肥大に注意。フォント機能や高描画率を狙う場合は opt-level = 3 を推奨。ただしサイズ増加のトレードオフあり。
- 動作確認済みボード: ESP32 (Xtensa), ESP32-C6 (RISC-V), STM32, RP2040, RP2350 等。ライセンスは Apache-2.0 / MIT のデュアルライセンス。

## 実践ポイント
- まず導入: 
```rust
// rust
// Cargo.toml に追加
cargo add mousefood
```
- 最小サンプル（README 抜粋）:
```rust
// rust
use mousefood::embedded_graphics::{mock_display::MockDisplay, pixelcolor::Rgb888};
use mousefood::prelude::*;
use ratatui::{Frame, Terminal};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut display = MockDisplay::<Rgb888>::new();
    let backend = EmbeddedBackend::new(&mut display, EmbeddedBackendConfig::default());
    let mut terminal = Terminal::new(backend)?;
    terminal.draw(draw)?;
    Ok(())
}
```
- 開発フロー: まず simulator で UI を作り込み → 実機（例: ESP32 + ILI9341 / e-paper）へ移植。フォント・テーマは EmbeddedBackendConfig で調整。EPD は flush_callback の使い方を README の Waveshare/WeAct 例に従う。
- 日本語（漢字）対応注意: embedded-graphics-unicodefonts はボックス描画や多くの記号を提供するが、フルの日本語（大量の漢字）フォントはサイズ面で現実的でない場合あり。日本語が必須ならビットマップの部分表示、ラスタ化フォントの外部提供、または必要箇所を画像で用意する戦略を検討。
- 最適化: 実機に載せる前にバイナリサイズとフレーム更新速度を測定。opt-level や不要機能の feature 切り分けで調整。

元リポジトリ（examples と docs.rs）を参照して、まず simulator を試すのが最短の近道です。
