---
layout: post
title: "Show HN: Whosthere: A LAN discovery tool with a modern TUI, written in Go - Whosthere：モダンTUIでLANを可視化するGo製ツール"
date: 2026-01-23T14:51:30.503Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ramonvermeulen/whosthere"
source_title: "GitHub - ramonvermeulen/whosthere: Local Area Network discovery tool with a modern Terminal User Interface (TUI) written in Go.  Discover, explore, and understand your LAN in an intuitive way. Knock Knock.. who&#39;s there? 🚪"
source_id: 46731432
excerpt: "Go製モダンTUIでLAN内の機器を高速発見＆詳細確認できるWhosthere"
image: "https://opengraph.githubassets.com/fbbf00aff79a295efcca9eb54dda4119f2b4042754da79ceee2dd88b6db296f1/ramonvermeulen/whosthere"
---

# Show HN: Whosthere: A LAN discovery tool with a modern TUI, written in Go - Whosthere：モダンTUIでLANを可視化するGo製ツール
誰があなたのネットワークにいるか、一目で分かる。端末で使える直感的なLAN探索ツール「Whosthere」を試してみよう

## 要約
WhosthereはGoで書かれたローカルネットワーク探索ツールで、mDNS／SSDP／ARPスイープを並列に実行し、TUIで発見した機器を直感的に表示します。ルート権限不要でOUIによるメーカー表示や簡易ポートスキャン、デーモン＋HTTP APIも備えています。

## この記事を読むべき理由
- 自宅や小規模オフィスのLANにある機器（IoTや共有プリンタなど）を手早く把握できる。  
- 端末好き／CLI慣れした人に好適なモダンなTUIを持ち、設定やテーマ化で使いやすくカスタマイズ可能。  
- ルート権限不要なので初心者でも安全に試せる（ただしスキャン権限は要確認）。

## 詳細解説
- 発見手法：mDNS（サービス広告）、SSDP（UPnP）、ARPキャッシュを埋めるためのTCP/UDPスイープを同時に実行。スイープでARPを誘発し、OSのARPテーブルを参照してデバイスを認識するため、特権を必要としないのが特徴。  
- 並列性：複数スキャナを同時に動かす設計で高速に探索。発見後はOUIデータでMACからメーカー名を付与して分かりやすく表示。  
- TUI：矢印キーや検索、デバイス詳細表示、テーマ切替（CTRL+t）など操作性が高い。主要キー操作やポートスキャン起動が用意されている。  
- ポートスキャナ：候補ポートの一覧でスキャン可能（デフォルトで一般的なポートを列挙）。利用は対象ネットワークの許可がある場合に限定すべき。  
- デーモン & HTTP API：バックグラウンドで常駐し、/devices や /device/{ip} 等の簡易APIで他ツールと連携可能。  
- 設定：YAMLでスキャン間隔やタイムアウト、テーマ、スキャナ有効/無効などを細かく調整できる。ログはXDG準拠のパスに出力。  
- プラットフォーム：Linux、macOSを公式サポート。Wayland下でのクリップボード制約やX11依存の注意点あり。  
- セキュリティ/倫理：READMEでも明示されている通り、権限のないネットワークでのスキャンは違法・不適切な場合があるため、自分のネットワークや許可のある環境でのみ使用すること。

## 実践ポイント
- インストール（例）
```bash
# Homebrew (macOS / Linuxbrew)
brew tap ramonvermeulen/whosthere
brew install whosthere

# go install
go install github.com/ramonvermeulen/whosthere@latest

# またはソースから
git clone https://github.com/ramonvermeulen/whosthere.git
cd whosthere
make build
```
- 使い方（基本）
```bash
# インタラクティブTUI
whosthere

# デーモン起動（HTTP API）
whosthere daemon --port 8080
```
- すぐ試せる設定：~/.config/whosthere/config.yaml を作り、scan_interval や port_scanner.tcp のリストを調整すると自分のネットワークに合わせた結果が得られる。  
- 注意点：ポートスキャンやネットワークスイープは必ず対象ネットワークの許可を得てから実行する。Wayland環境ではクリップボード関連の制約があるため注意。  
- 日本の現場での活用例：家庭のスマート家電一覧確認、小規模オフィスの機器把握、ラボ環境での迅速なデバイス検出やCIの前段階チェックなど。

興味があればリポジトリ（https://github.com/ramonvermeulen/whosthere）でソースを見て、テーマ追加やプラットフォーム対応のPRを検討してみてください。
