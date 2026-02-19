---
layout: post
title: "A terminal weather app with ASCII animations driven by real-time weather data - ターミナルで動くASCIIアニメ天気アプリ（リアルタイム気象データ連動）"
date: 2026-02-19T19:17:36.885Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Veirt/weathr"
source_title: "GitHub - Veirt/weathr: a terminal weather app with ascii animation"
source_id: 47076659
excerpt: "ターミナルで動くASCII天気アプリが実データで雨雪雷を軽快アニメ表示"
image: "https://opengraph.githubassets.com/77092bdeef5d04b49c8416f86e13cd663b68334a08ab72556821594f94510e91/Veirt/weathr"
---

# A terminal weather app with ASCII animations driven by real-time weather data - ターミナルで動くASCIIアニメ天気アプリ（リアルタイム気象データ連動）

魅せるターミナル天気表示。ASCIIアートとリアルタイム気象でデスクトップもサーバーも楽しくするツール

## 要約
Rust製のCLIツール「weathr」は、Open-Meteoの実データを使い、雨・雪・雷・昼夜・飛行機などのASCIIアニメで天気を可視化する軽量ターミナルアプリです。自動位置検出やシミュレーション機能も備えます。

## この記事を読むべき理由
日本の開発者やサーバ運用者にとって、軽量で依存が少ない天気表示ツールはローカル開発環境やSSH接続先で手軽に状況確認できる実用ツールです。可視化が会話やデモで使いやすく、dotfilesやtmuxに組み込めます。

## 詳細解説
- コア技術：Rustで実装されたTUIアプリ。ASCIIアートをターミナルに描画し、アニメーションを組み合わせて天候を表現します。ソースはGitHubで公開、ライセンスはGPL-3.0。
- 気象データ：Open-MeteoのAPIを利用（CC BY 4.0）。緯度経度で天候を取得し、降水・雪・雷などの状態を描画に反映します。
- 位置検出：設定で自前座標を指定可能。auto=true時はipinfo.ioでIPベースの位置推定を行います（プライバシー配慮が必要）。
- インストール方法：Cargo経由やAUR、Nixフレークなどをサポート。ソースビルドにはRust toolchainが必要。
  ```bash
  # Rustがある場合
  cargo install weathr
  # Archユーザー（AUR）
  yay -S weathr
  ```
- 設定：プラットフォーム毎のconfigパス（Linux: ~/.config/weathr/config.toml、macOS: ~/Library/Application Support/weathr/config.toml）。温度単位や風速単位、HUD表示のオン/オフを設定可能。
- 実行オプション：--simulate で天候を擬似再現（rain, snow, thunderstormなど）。--imperial/--metric、--auto-location、--hide-hud 等のフラグあり。
- アクセシビリティ／環境：NO_COLORで色無効、COLORTERM/TERMで端末機能を検出。サーバーや低帯域環境で動作しやすい設計。
- 著作と素材：ASCIIアートは複数作者クレジットあり。将来は複数の気象API（OpenWeatherMap等）対応予定。

## 実践ポイント
- まずはローカルで試す：cargo install weathr で導入後、`weathr --simulate rain` や `weathr --simulate snow --night` で動作確認。
- dotfiles連携：起動コマンドを .bashrc や tmux 起動スクリプトに組み込み、作業環境のちょっとした"気分演出"に。
- サーバー監視用途：軽量なのでヘッドレスサーバに入れてバナー代わりに表示（自動位置検出はOFF推奨）。
- プライバシー配慮：IPベースの自動位置検出を使いたくない場合はconfigで緯度経度を明示。
- カスタマイズ：HUD表示や単位設定で自分の用途に合わせる。アクセシビリティが必要ならNO_COLOR=1を利用。

元リポジトリ（デモや詳細設定、クレジット、Issue/Roadmap）は GitHub: https://github.com/Veirt/weathr を参照してください。
