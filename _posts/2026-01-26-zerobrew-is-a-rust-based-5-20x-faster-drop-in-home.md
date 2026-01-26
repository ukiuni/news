---
layout: post
title: "zerobrew is a Rust-based, 5-20x faster drop-in Homebrew alternative - zerobrew：Rust製のHomebrew互換で5〜20倍高速化"
date: 2026-01-26T03:41:58.458Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/lucasgelfond/zerobrew"
source_title: "GitHub - lucasgelfond/zerobrew: A drop-in, 5-20x faster, Rust-based experimental Homebrew alternative"
source_id: 850553738
excerpt: "zerobrewでHomebrewを置き換え、再インストール最大20倍高速化"
image: "https://opengraph.githubassets.com/ecf3c91680430687b619c27dee3b648dbc87cc08d63c388d4568d08d56daca83/lucasgelfond/zerobrew"
---

# zerobrew is a Rust-based, 5-20x faster drop-in Homebrew alternative - zerobrew：Rust製のHomebrew互換で5〜20倍高速化

Homebrew互換をそのまま置き換えられる実験的なパッケージマネージャ。Rustで書かれ、キャッシュと並列処理でインストール速度を大幅に改善します。

## 要約
zerobrew（zb）はHomebrewのCDNを使い、パッケージをコンテンツアドレッサブルに格納して再インストールを即時化。Coldで約2×、Warmでは最大20×の高速化を目指す実験的プロジェクトです。

## この記事を読むべき理由
Mac（特に開発環境）で頻繁にパッケージを入れ替える日本の開発者やCI運用者にとって、インストール時間短縮は生産性とコスト（時間）の削減に直結します。既存のHomebrewワークフローを大きく変えずに高速化できる点が魅力です。

## 詳細解説
- 主要アイデア
  - コンテンツアドレッサブルストア：パッケージをSHA256でキー管理（例: /opt/zerobrew/store/{sha256}/）。既に存在すれば再インストールは瞬時。
  - APFS clonefile：APFSのコピーオンライト機能を使い、ディスク上のオーバーヘッドをほぼゼロにします。
  - 並列ダウンロードと重複排除：同一ファイルの並列取得やCDN接続の競争でダウンロード性能を引き上げます。
  - ストリーミング実行：ダウンロード、展開、リンク処理を同時実行して待ち時間を削減。
  - HomebrewのCDNを利用：既存のボトルをそのまま使えるため、brewコマンドを置き換えやすい。
- ベンチマーク（リポジトリの結果より）
  - トップ100パッケージ全体: Homebrew 452s → ZB cold 226s（約2.0×）、ZB warm 59s（約7.6×）
  - 例：libsodium は cold 6.0×、warm 18.1×、tesseract は warm 最大で29.5× 等
  - ただし ffmpeg のようにColdで遅くなるケースもあるため一律の保証はなし。
- 実装／開発
  - Rust主体（zb_cli, zb_core, zb_io 等）、シェルスクリプトでインストールラッパー提供。
  - 現状は実験段階で、多くのコアformulaは動作するが一部は調整が必要。

## 実践ポイント
- 試す（ユーザ向け）
  - インストール（公式スクリプトを実行し、表示される export を反映するかターミナル再起動）
```bash
curl -sSL https://raw.githubusercontent.com/lucasgelfond/zerobrew/main/install.sh | bash
# インストール後、表示される export を実行
```
  - 主要コマンド例
```bash
zb install jq
zb install wget git
zb uninstall jq
zb reset     # 全削除
zb gc        # ストアのガベージコレクション
```
- 開発者向け
```bash
cargo build --release
cargo install --path zb_cli
./benchmark.sh           # 100パッケージベンチ
./benchmark.sh --format html -o results.html
```
- 注意点
  - 現在は「実験的」：重要な開発マシンでの全面置換は慎重に。まずは検証用マシンやCIで試すこと。
  - APFS依存の挙動や一部formulaの互換性問題があり得るため、問題があればIssue/PRで貢献可能。

日本の開発現場では、ローカル開発やCIのビルド時間短縮に直接効くため、まずは試験導入して効果を見極める価値があります。
