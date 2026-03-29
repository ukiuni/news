---
layout: post
title: "Show HN: Create a full language server in Go with 3.17 spec support - GoでLSPサーバをゼロから作る（仕様3.17対応）"
date: 2026-03-29T13:21:30.242Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/owenrumney/go-lsp"
source_title: "GitHub - owenrumney/go-lsp: Go LSP helper library support 3.17 of the LSP specification (mostly) · GitHub"
source_id: 47510005
excerpt: "Go製ライブラリでLSP仕様3.17を簡単実装、最短で高機能言語サーバを構築"
image: "https://opengraph.githubassets.com/600cef9c0074f6f63afdce4bc6a626ce3780220f3fc57acd6f4f68eca0411f9e/owenrumney/go-lsp"
---

# Show HN: Create a full language server in Go with 3.17 spec support - GoでLSPサーバをゼロから作る（仕様3.17対応）
魅せるGo製LSPライブラリで「自分の言語ツール」を最速で作る方法

## 要約
go-lspはLSP仕様3.17にほぼ対応したGo製ライブラリで、JSON-RPCの処理・メッセージ配送・型定義を肩代わりしてくれるため、言語固有のロジックに集中してLSPサーバを構築できます。

## この記事を読むべき理由
日本でも独自言語や静的解析ツール、エディタ拡張（VS CodeやVim/Neovim経由）を作るニーズが増えています。go-lspを使えば、LSPの煩雑な実装を省いて短期間で高品質な開発体験を提供できます。

## 詳細解説
- 目的と強み  
  - LSP（Language Server Protocol）実装の共通部分（JSON-RPCフレーミング、メソッド登録、型定義）を提供。開発者はInitialize/Shutdownやホバー・補完など言語固有のハンドラだけを書けば良い。  
  - 仕様ターゲットはLSP 3.17。typeHierarchy、inlayHint、inlineValue、pull diagnosticsなど最近の機能をサポートしている。

- サポート範囲（概要）  
  - ライフサイクル、テキスト同期、補完、ホバー、定義/参照/シンボル、リネーム、フォーマット、セマンティックトークン、ワークスペース操作、サーバ→クライアント通知（diagnostics、showMessageなど）ほとんどをカバー。

- 使い方の流れ（ポイント）
  - ハンドラ構造体を作り、LifecycleHandler（Initialize/Shutdown）を実装。必要な機能は該当ハンドラインターフェースを満たすだけで自動的に能力をadvertiseする。
  - トランスポートはio.ReadWriteCloserに依存し、stdio（エディタ連携）、TCP、WebSocketなど用途に応じて選択可能。
  - サーバ側からエディタへは srv.Client を通じて diagnostics や showMessage、progress などを送れる。
  - カスタムJSON-RPCメソッド／通知を登録でき、拡張機能やエディタ専用APIを追加可能。

- 開発支援機能
  - servertest パッケージ：メモリ内パイプでクライアントを模擬し、LSPシナリオの単体テストが簡単に書ける。diagnosticsの待ち合わせやHoverの取得などが可能。
  - ロギング：標準の slog をサポート。JSONハンドラで本番ログ、テキストハンドラで開発用デバッグ出力を選べる。
  - Debug UI：オプションでWeb UIを立ち上げ、全LSPトラフィックを可視化（リクエスト/レスポンス、タイムライン、検索等）。

- クイックスタート（概念例）
```go
package main

import (
  "context"
  "os"
  "github.com/owenrumney/go-lsp/lsp"
  "github.com/owenrumney/go-lsp/server"
)

type Handler struct{}

func (h *Handler) Initialize(ctx context.Context, params *lsp.InitializeParams) (*lsp.InitializeResult, error) {
  return &lsp.InitializeResult{Capabilities: lsp.ServerCapabilities{
    HoverProvider: &lsp.HoverOptions{},
  }}, nil
}
func (h *Handler) Shutdown(ctx context.Context) error { return nil }
func (h *Handler) Hover(ctx context.Context, params *lsp.HoverParams) (*lsp.Hover, error) {
  return &lsp.Hover{Contents: lsp.MarkupContent{Kind: lsp.MarkupKindMarkdown, Value: "Hello from server"}}, nil
}

func main() {
  srv := server.NewServer(&Handler{})
  if err := srv.Run(context.Background(), server.RunStdio()); err != nil {
    os.Exit(1)
  }
}
```

## 日本市場との関連
- 日本語向けlint／補完／型解析（Go/TypeScript/Python/独自DSL）での採用メリットが大きい。特にリポジトリ内の日本語ドキュメントやコメント解析、社内DSLのエディタ統合に有効。  
- クラウドIDEやCodespaces、社内ツールのためにTCP/WebSocketでの接続も可能なので、SaaS型の開発支援ツールにも組み込みやすい。  
- 社内での品質ゲート（diagnostics自動投稿）やCI連携をservertestと組み合わせてテスト自動化できる点も実用的。

## 実践ポイント
- まずは go get github.com/owenrumney/go-lsp で導入し、最小のLifecycleHandlerを実装してRunStdioでVS Codeと接続してみる。  
- 機能追加は「対応するハンドラインターフェースを実装するだけ」で済むため、段階的に補完→ホバー→診断→セマンティックトークンの順で拡張すると開発コストが下がる。  
- servertestでユニットテストを書き、Debug UIでLSPメッセージを観察するとデバッグが劇的に楽になる。  
- 本番では slog を JSON 出力にしてログ集約（例：Cloud Logging）へ送り、パフォーマンス監視はDebug UIのタイムラインや独自メトリクスで補う。

短時間で編集体験を向上させたいエンジニア／チームにとって、go-lspは「LSPの重労働部分」を引き受けてくれる強力な選択肢です。興味があればリポジトリのREADMEとexamplesから手を動かして試してみてください。
