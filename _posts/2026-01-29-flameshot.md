---
layout: post
title: "Flameshot - 強力でシンプルなスクリーンショットソフト"
date: 2026-01-29T22:41:46.815Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/flameshot-org/flameshot"
source_title: "GitHub - flameshot-org/flameshot: Powerful yet simple to use screenshot software :camera_flash:"
source_id: 46815297
excerpt: "注釈付きスクショを高速作成、GUI/CLI対応で業務効率が格段に上がるFlameshot導入法"
image: "https://opengraph.githubassets.com/a9ec7bd6a33bcbd4f62aaecf4673e6bb5de1818c46af3cbd283b4be0a900ccba/flameshot-org/flameshot"
---

# Flameshot - 強力でシンプルなスクリーンショットソフト

Flameshotでスクショ作業が劇的に速くなる — 初心者でも使える高機能ツール

## 要約
FlameshotはLinux／Windows／macOS対応のオープンソースなスクリーンショットツールで、キャプチャ→注釈→保存／クリップボード共有をGUIとCLI両方で高速に行えます。

## この記事を読むべき理由
ドキュメント作成やバグ報告、技術サポートでスクショを多用する日本のエンジニアやビジネスユーザーにとって、手早く注釈付き画像を作れることは生産性向上に直結します。Flameshotは設定自由度が高く、職場のワークフローに組み込みやすい点が魅力です。

## 詳細解説
- 主な特徴  
  - GUI上で矩形選択、矢印・線・ペン・モザイク・テキスト追加などの編集が可能。  
  - Imgurアップロード対応、クリップボードコピー、一括保存など実用的な出力オプション。  
  - D-Bus経由のトレイアイコン、キーボードショートカット対応。  

- コマンド／ワークフロー例  
  - GUI起動: `flameshot gui`（指定パス保存: `-p`、遅延: `-d`）  
  - 全画面保存: `flameshot full -p ~/captures -d 5000`  
  - 画面番号指定・クリップボードコピー: `flameshot screen -n 1 -c`  
  - Windowsでコンソール出力が必要なら `flameshot-cli.exe` を使う。  

- キーボードと環境設定  
  - GUIモードのローカルショートカット（例: Ctrl+Cでコピー、Ctrl+Sで保存、Gでカラーピッカー）。  
  - デスクトップ毎のグローバルホットキー設定方法（KDE/GNOME/XFCE/Fluxbox の手順）。  
  - 設定ファイル: Linux `~/.config/flameshot/flameshot.ini`、Windowsは `%APPDATA%\flameshot\flameshot.ini`。保存パスなどを直接編集可能。  

- インストールと注意点  
  - 各ディストリでパッケージあり（apt/pacman/dnf 等）、HomebrewやMacPorts、Snap/Flatpak、Windows用配布も。  
  - macOSはGatekeeper対応（初回は右クリック→Open等が必要）。Flatpak版はコマンドのシンボリックリンクが要る場合あり。  
  - Wayland環境は実験的サポート。トレイ表示には拡張（Gnome AppIndicator）やシナリオ依存の対応が必要。  

## 実践ポイント
- まずはショートカットに `flameshot gui` を割り当てる（PrtSc など）。  
- よく使う保存先を `flameshot.ini` の savePath に設定して自動保存を有効化。  
- マウスホバーやツールチップを撮るなら `-d 2000` の遅延オプションを使う。  
- 自動起動でD-Bus初期化の遅延を避ける：起動時に Flameshot を常駐させる。  
- Windowsでスクリプトから使う場合は `flameshot-cli.exe` を使って標準出力を取得する。  

短時間で注釈付きスクショを量産したい人はまずインストールしてキーバインドを設定し、いつものスクショフローを置き換えてみてください。
