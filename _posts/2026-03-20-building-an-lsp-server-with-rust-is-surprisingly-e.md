---
layout: post
title: "Building an LSP Server with Rust is surprisingly easy and fun - RustでLSPサーバを作るのは意外と簡単で楽しい"
date: 2026-03-20T04:21:24.662Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://codeinput.com/blog/lsp-server"
source_title: "Building an LSP Server with Rust is surprisingly easy and fun | Blog | Code Input"
source_id: 950632344
excerpt: "Rustとtower-lspで短時間にエディタ横断LSPを作れる方法"
image: "https://codeinput.com/img/blog/lsp-server/post_thumb.webp"
---

# Building an LSP Server with Rust is surprisingly easy and fun - RustでLSPサーバを作るのは意外と簡単で楽しい
エディタ拡張を“言語サーバ”として共通化する──Rustで試すと驚くほど手早く楽しく作れます

## 要約
Rustとコミュニティ版のtower-lsp-serverを使えば、初歩的なLSPサーバは短時間で構築でき、エディタ横断で同じロジックを共有できます。テストも簡単で、Neovim等への接続も手軽です。

## この記事を読むべき理由
エディタごとに別実装を作ると保守が大変な日本の開発現場（VS Code / Neovim / Helixなど混在）で、LSPは「一度実装すればどのエディタでも使える」現実的な選択肢になります。特に高速性や型安全性を重視するならRustは有力です。

## 詳細解説
- LSPの本質: JSON-RPCベースのプロトコル。エディタはメソッド名（textDocument/completion 等）付きJSONを送り、サーバは応答する。
- Rust側の選択肢: 最も使われてきたtower-lspのフォークである「tower-lsp-server」が活発。最小限はLanguageServerトレイトのinitializeとshutdownを実装するだけで動作する。
- テストのしやすさ: 実際のエディタを起動せず、initializeリクエストを直接投げて応答を検査できる。serde_jsonやtower-serviceで手元検証が可能。
- エディタ接続: TCPやスタンダードIO経由で接続可能。非同期ランタイム（Tokio）を入れればTCPサーバとして動かしてNeovim等に接続できる。
- 実装例（機能例）:
  - カスタム補完: initializeでcapabilitiesを宣言し、Completionを実装すれば特定トリガーで候補表示。
  - ドキュメント書換: apply_editを使って入力ワードを自動置換。
  - エディタ内AI: 特定行をトリガーにLLMへリクエストして返答を挿入（費用とプライバシーに注意）。
- 注意点: LSPは定められたメソッド群で設計されているため、用途によっては制約がある。ただしエディタ統合や即時フィードバック系の用途には強い。

## 実践ポイント
- 依存追加（Cargo.toml）例:
```rust
tower-lsp-server = "0.23.0"
```
- エディタ不要で試す: serde_json / tower-service を入れてinitializeリクエストを投げ、返るcapabilitiesを確認する。
- NeovimへTCP接続（例）:
```lua
:lua vim.lsp.start({ name = 'custom_tcp', cmd = vim.lsp.rpc.connect('127.0.0.1', 9292), root_dir = vim.fn.getcwd() })
```
- まずは「補完」と「簡単なapply_edit」から実装して挙動を把握する。LLM連携はコストやセキュリティを必ず考慮する。
- 日本の現場では、CODEOWNERSやファイル走査のような共通ロジックをLSP化するとメンテ性が劇的に向上する可能性が高い。

以上を踏まえ、短時間でプロトタイプを立てて「エディタ横断の共通ロジック」を試してみることをおすすめします。
