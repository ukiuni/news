---
layout: post
title: "What's wrong with Electron IPC and how it could be improved - ElectronのIPCは何がまずいのか、どう改善できるか"
date: 2026-04-13T13:38:30.426Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://teamdev.com/mobrowser/blog/what-is-wrong-with-electron-ipc-and-how-to-fix-it/"
source_title: "What's wrong with Electron IPC and how it can be fixed | MōBrowser Blog"
source_id: 363973685
excerpt: "ElectronのIPCを型付き契約＋コード生成で安全かつ可視化し、リファクタ地獄を解消する方法"
image: "https://teamdev.com/mobrowser/blog/what-is-wrong-with-electron-ipc-and-how-to-fix-it/hero_og.jpg"
---

# What's wrong with Electron IPC and how it could be improved - ElectronのIPCは何がまずいのか、どう改善できるか
クリックせずにはいられない！Electronアプリ開発で遭遇する“IPC地獄”をスッキリ解決する考え方

## 要約
Electronのプロセス間通信（IPC）は、文字列チャネルと手作業のラッパーに頼るため規模が大きくなると保守性・型安全性・可視性が急速に低下する。記事は「契約（contract）を明示し、コード生成で型付きRPC風インタフェースにする」ことでこれを改善できると提案する。

## この記事を読むべき理由
日本でもElectronは業務アプリや社内ツール、デスクトップ製品で広く使われており、チーム開発や長期保守でIPCの破綻に直面しやすい。今のままではバグが実行時まで潜み、リファクタが怖くなるため、具体的な改善案を知る価値が高い。

## 詳細解説
- 背景：ElectronはChromiumのマルチプロセスモデルを採用し、UIを描くrenderer（サンドボックス）と権限操作を行うmainに分かれる。これらを連携させるのがIPC。
- 現行モデルの流れ（簡略）
  - mainでipcMain.handle('channel', handler)を登録
  - preloadでcontextBridge.exposeInMainWorldで限定APIを公開
  - rendererはwindow.xxxを呼ぶことでipcRenderer.invoke('channel')を実行
- 問題点（要点）
  - チャネル名が文字列：タイプミスや存在確認は実行時まで発覚しない。
  - 契約が分散：handler、preload、rendererに同じ仕様を手作業で維持する必要がある。
  - リファクタのコストが高い：名前変更やペイロード変更で漏れが起きやすい。
  - 可視性が低い：どのAPIが利用可能か一目で分からない。
- 提案された改善案
  - IDL（例：Protocol Buffers）でサービス/メッセージを定義し、main/renderer双方の型付きスタブを生成する。
  - 生成コードを使えば「単一の契約」ができ、TypeScriptでコンパイル時チェック、発見性、生成されたドキュメントが得られる。
- 期待効果
  - 型安全性の向上、早期エラー検出、リファクタ容易化、ボイラープレート削減。

小さなイメージ（proto定義の例）:

```proto
syntax = "proto3";

service DialogService {
  rpc OpenFile(google.protobuf.Empty) returns (google.protobuf.StringValue);
}
```

生成された呼び出しは型付きのAPIになる（概念例）。

## 実践ポイント
- まず現行IPCを棚卸し：使っているチャネル一覧とpayloadの形をドキュメント化する。
- 小さなAPIから契約化を試す：1〜2個の重要なIPCを.protoやZodスキーマで定義してコード生成してみる。
- 自動テストを追加：生成APIに対する単体テストで互換性を確保する。
- preloadは最小公開に留める：contextBridgeで露出する関数は契約準拠にする。
- 代替検討：既存のツール（tRPC風アプローチ、zod + codegen、protobuf）を比較して自分のスタックに合うものを採用する。

短期的には「誤字や形のミスマッチを減らす」、中長期的には「大規模化しても安全に進化できる」ことが得られます。
