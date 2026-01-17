---
layout: post
title: "I hotreload Rust and so can you - Rustをホットリロードする方法"
date: 2026-01-17T17:43:25.094Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kampffrosch94.github.io/posts/hotreloading_rust/"
source_title: "I hotreload Rust and so can you | Kampffrosch&#39;s blog"
source_id: 1657225339
excerpt: "実行中にRustコードを差し替え、再起動不要で瞬時に動作確認できるホットリロード手法を実装解説"
---

# I hotreload Rust and so can you - Rustをホットリロードする方法
Rustを実行中に差し替えて開発スピードを爆速にする「ホットリロード」入門

## 要約
Rustコードを再起動せずに差し替える開発向けテクニックを、ホスト（永続状態）とワーカー（差し替え可能）に分けるアーキテクチャで具体的に解説します。OSは主に Linux（x86_64-unknown-linux-gnu）を想定します。

## この記事を読むべき理由
- コンパイルの遅さで試行錯誤が止まることが多いRust開発者（特にゲーム開発者）にとって、実行中にコードを差し替えられると開発体験が劇的に改善します。  
- 日本でもゲーム・ツール開発や高速なフィードバックループが求められる分野で即戦力になるノウハウです。Windows中心の環境でもWSLやCIで再現できますが、Linuxが最も扱いやすいです。

## 詳細解説
1) 基本アイデア  
- プロジェクトを「host（永続状態を持つ）」「worker（差し替え可能）」そして共通APIを置く「base」の3クレートに分割。  
- workerはビルド時に動的ライブラリ（cdylib → .so）と静的ライブラリ（rlib）を生成。開発時は.dylibを読み込み、配布時は静的リンクで運用する。

2) 共有API（base）  
- hostとworkerは共通のTraitでやり取り。例：描画や入力を抽象化する `Context`。
- これによりシンプルな型共有が可能で、スクリプト言語を別に用意する必要がなくなる。

3) workerのビルド設定（抜粋）
```rust
# Cargo.toml (worker)
[lib]
crate-type = ["cdylib", "lib"]
```

4) ランタイムでの読み込み（libloading）  
- hostは libloading クレートで .so を dlopen し、未修飾の extern "C" 関数シンボルを取得して呼び出す。  
- シンボルを得た `Library` オブジェクトを保持しておくこと（drop すると dlclose されるため関数ポインタが無効化される）。

5) C++/glibc 周りの小ネタ  
- スレッドローカルの扱いで dlclose を阻む glibc のチェックを回避するため、開発専用で `__cxa_thread_atexit_impl` をダミーで定義する（リークのリスクがあることを理解して使う）。

6) stateless なリロードの流れ  
- cargo-watch 等で worker を自動ビルド、ファイル作成時間の変化を検出して古い .so を drop → 新しい .so を load する。  
- 変更検知はファイルメタデータ（作成時間）で十分高速（著者の環境で ~20μs）。

7) stateful なリロード（状態保持）  
- 永続化したい状態は host が保持し、worker側へはサイズ・アライメント情報と生ポインタだけ渡す。C風の型消去ラッパーを使う（例：PersistWrapper）。これで reload 時も state が保持される。  
- worker 側で state を作るファクトリ関数（hot_create）を用意し、初回生成は worker に任せる構成も可能。

8) 注意点（重要）  
- Rustは安定ABIを提供していないので、同じコンパイラ・同じフラグでホストとワーカーをビルドすることを前提にしている。つまりこれは「開発用のホットリロード」であり、一般的なプラグインAPIとしての公開には向かない。  
- trait object（動的ディスパッチ）や vtable はライブラリ内に置かれるため、vtable を跨いで state を持ち続けると再ロード後にセグフォ（無効な vtable）を起こす恐れがある。trait object を状態として保存する場合は vtable を再解決する戦略が必要（最悪は避ける）。

## 実践ポイント
- リポジトリ構成: base / host / worker のワークスペースを作る。  
- worker は cdylib と lib を同時に出す（開発は .so、配布は静的）。  
- host 側で libloading を使い、Library を保持しておく（drop 回避）。  
- 自動ビルドは cargo-watch 等で。デフォルトのデバウンスを短くすると反映が速くなる。  
- 永続状態はポインタ＋サイズ＋align のラッパーで持つ（PersistWrapper）。ただしメモリ管理や安全性は設計次第。  
- trait object を long-lived state にするのは避けるか、リロード毎に再初期化する仕組みを作る。  
- 開発環境は可能なら Linux を推奨（ビルド・リンクが速く、ホットリロードのサポートが安定）。

短時間での試作に非常に有効な手法ですが、ライブラリ依存や複雑な状態を増やすと再現性の低い不具合に繋がる点は常に念頭に置いてください。
