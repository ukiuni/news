---
layout: post
title: "console: a debugger for async rust - 非同期Rust向けデバッガ「console」"
date: 2026-03-21T23:55:26.882Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/tokio-rs/console"
source_title: "GitHub - tokio-rs/console: a debugger for async rust! · GitHub"
source_id: 1638951780
excerpt: "tokio-consoleで非同期Rustのタスクやボトルネックをリアルタイム可視化"
image: "https://opengraph.githubassets.com/f1c08e37b0ef78b8f9e443e0ed643881bbedce746c42103f91db72dfb6a32024/tokio-rs/console"
---

# console: a debugger for async rust - 非同期Rust向けデバッガ「console」
非同期タスクの内部が見える化される！tokio-consoleでRustのasync実行をデバッグして可視化する方法

## 要約
tokio-consoleは、Tokio/tracingで動く非同期Rustアプリの診断・デバッグツール群（console-subscriberで計測、gRPC/protobufでストリーム、tokio-consoleで表示）です。タスクの状態、ウェイク数、リソースのドロップなどをリアルタイムに観察できます。

## この記事を読むべき理由
日本でもバックエンドやマイクロサービスでRust＋Tokio採用が増えています。非同期のパフォーマンス問題は見つけにくく、tokio-consoleは「どのタスクがボトルネックか」を即座に教えてくれるため、開発効率と運用信頼性が大きく向上します。

## 詳細解説
- 構成要素
  - console-subscriber: tracing-subscriberのLayerとしてアプリ内で計測データを収集。
  - Wire protocol: gRPC + protobufでデータをストリーミング。console-apiはtonic用の生成コードを含む。
  - tokio-console: CLIクライアント（他にGUI等の実装も可能）。
- 計測の仕組み
  - アプリはconsole-subscriberを組み込み、タスク生成/終了やウェイクイベントをEmitterとして外部に送信。
  - tokio-consoleは既定でlocalhost:6669へ接続し、タスク一覧、スタック、ウェイク統計、警告（self-wakes, lost-waker 等）を表示。
- 有効化の注意点
  - Tokioのタスク情報を得るにはコンパイル時に tokio_unstable cfg を有効化する必要あり（RUSTFLAGS または .cargo/config.toml で設定）。
  - tracingのターゲット（tokio, runtime）をTRACEレベルにする必要がある。console_subscriber::init() を使えば自動で設定される。
- 運用面
  - 接続はURL/IP:PORT、Unixドメインソケット（file://...）、vsock（VM向け）に対応。
  - CLIは各種オプション（--warn, --retain-for, --log-dir, --lang など）で表示やログを調整可能。
  - 開発用の例（app.rs, dump.rs）がリポジトリに含まれる。

## 実践ポイント
- Cargo.tomlに依存追加（例）
```rust
# Cargo.toml
console-subscriber = "0.5"
```
- mainで初期化（ワンライナー）
```rust
# src/main.rs (Rust)
fn main() {
    console_subscriber::init();
    // tokio::main 内であれば非同期処理を開始
}
```
- tokio_unstable を有効化（ビルド時）
```bash
# 一時的に
RUSTFLAGS="--cfg tokio_unstable" cargo build

# 恒久的に .cargo/config.toml に追加
[build]
rustflags = ["--cfg", "tokio_unstable"]
```
- tokio-console をインストールして接続
```bash
cargo install --locked tokio-console
tokio-console http://127.0.0.1:6669
```
- まずはローカル/ステージングで動作確認：ポートマッピングやUnixソケットで接続し、本番はログ保持やサンプリングで負荷を抑える。
- 試すべきオプション
  - --warn 自己ウェイクやlost-waker検出
  - --retain-for タスク完了後の表示保持時間
  - --lang en_US.UTF-8（WindowsでUTF-8表示を保証する場合）

リポジトリ／ドキュメントを参照して、まずは手元の小さなサービスで動かしてみることを推奨。
