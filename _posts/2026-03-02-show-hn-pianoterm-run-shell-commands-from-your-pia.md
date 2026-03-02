---
layout: post
title: "Show HN: Pianoterm – Run shell commands from your Piano. A Linux CLI tool - Pianoterm：ピアノ鍵盤でシェルコマンドを実行するLinux CLIツール"
date: 2026-03-02T22:13:57.845Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/vustagc/pianoterm"
source_title: "GitHub - vustagc/pianoterm: Linux CLI tool to assign shell commands to keys on a USB MIDI Keyboard"
source_id: 47223863
excerpt: "USB MIDI鍵盤でワンキー操作で任意のシェルコマンドを実行、配信やライブで即戦力に"
image: "https://opengraph.githubassets.com/3260878d234eb4d7031f3719eedc8942ac316738bc16b806a7700ab3475c27e5/vustagc/pianoterm"
---

# Show HN: Pianoterm – Run shell commands from your Piano. A Linux CLI tool - Pianoterm：ピアノ鍵盤でシェルコマンドを実行するLinux CLIツール
ピアノがショートカットに早変わり！USB MIDI鍵盤でキーを押すだけで任意のシェルコマンドを走らせる「Pianoterm」の遊び方と実用例

## 要約
USB接続のMIDI鍵盤のキーに任意のシェルコマンドを割り当てて実行する、軽量なLinux用CLIツール。ALSAを前提にシンプルな設定ファイルでキー→コマンドをマッピングします。

## この記事を読むべき理由
- ライブ配信／パフォーマンスや作業効率化で、手元の鍵盤からワンボタン操作を実現できるため、日本の音楽系エンジニアやストリーマー、Raspberry Piなどでの自動化に役立ちます。

## 詳細解説
- 仕組み：PianotermはCで書かれたCLIで、ALSA経由のMIDI入力を監視し、設定ファイルで定義したキーコードに対応するシェルコマンドを実行します。トリガーはキーが押されたとき(on_press)か離したとき(on_release)を選べます。
- 設定：設定は$HOME/.config/pianoterm/configにプレーンテキストで記述。ポート指定とMIDIノート番号（例：88鍵なら最初が21、最後が108）をコマンドに紐付けます。
- ポートとキー検出：MIDIデバイスのポートは aconnect -i で確認し、特定のキーコードは aseqdump -p <port> で確認します。
- ビルド：リポジトリをクローンして make でビルド。依存はCコンパイラとalsactlなど。MITライセンス。

例（設定ファイルの一部）:
```ini
# ini
# trigger can be on_release or on_press
on_press

# syntax: port = command
21 = playerctl previous
22 = playerctl play-pause
23 = playerctl next
108 = /home/me/my_script.sh
```

ビルド・起動例:
```bash
# bash
git clone https://github.com/vustagc/pianoterm.git
cd pianoterm && make
pianoterm <port>
```

## 実践ポイント
- まず aconnect -i と aseqdump -p <port> でポートとノート番号を確認する。
- よく使う操作（再生/停止、次トラック、スライド切替など）を低いノート番号に割り当てると扱いやすい。
- スクリプトを割り当てる場合は実行権限を付与して絶対パスを指定する（例：/home/user/script.sh）。
- 配信やライブ用途では on_press/on_release を使い分けて誤操作を防ぐ。
- 日本の現場では、Linuxベースの配信環境やRaspberry Piでのリモート操作、MIDI対応機器と連携したインスタレーションに向く。

元リポジトリ: https://github.com/vustagc/pianoterm
