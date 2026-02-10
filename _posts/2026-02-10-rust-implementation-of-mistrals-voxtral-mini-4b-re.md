---
layout: post
title: "Rust implementation of Mistral's Voxtral Mini 4B Realtime runs in your browser - MistralのVoxtral Mini 4B Realtimeをブラウザで動かすRust実装"
date: 2026-02-10T03:28:35.462Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/TrevorS/voxtral-mini-realtime-rs"
source_title: "GitHub - TrevorS/voxtral-mini-realtime-rs"
source_id: 46954136
excerpt: "ブラウザだけで動くQ4量子化4B音声モデルをRustで低遅延実現"
image: "https://opengraph.githubassets.com/1861f86c9957d9905c209f2e0b4916c5f5204a662f6e104f27388a7ee7b96e57/TrevorS/voxtral-mini-realtime-rs"
---

# Rust implementation of Mistral's Voxtral Mini 4B Realtime runs in your browser - MistralのVoxtral Mini 4B Realtimeをブラウザで動かすRust実装

魅力的タイトル: ブラウザだけで動く4B音声認識モデル──Rustで実現した「Voxtral Mini 4B Realtime」体験ガイド

## 要約
Rust + Burnフレームワークで実装されたVoxtral Mini 4B（Realtime）が、量子化（Q4 GGUF）経路を使えば約2.5GBでWASM＋WebGPUにより完全クライアント側で動作する。ネイティブ（f32）とブラウザ両方の実行パスを提供するプロジェクト。

## この記事を読むべき理由
ブラウザ上で大容量モデルをプライバシーを保ったまま動かせる点は、日本の企業や音声アプリ開発者にとって通信コスト低減・ユーザーデータ保護の両面で大きな魅力。導入ハードルや実装の工夫も分かる。

## 詳細解説
- コア技術
  - 実装言語：Rust、MLフレームワーク：Burn
  - 実行パス：f32（ネイティブ、約9GB）とQ4 GGUF（量子化、約2.5GB・ブラウザ対応）
  - ブラウザ動作：WASM + WebGPU（カスタムWGSLシェーダで量子化解除＋行列積を実行）
- アーキテクチャ（簡略）
  - 音声16kHz → メルスペクトログラム → 因果エンコーダ（32層、次元1280、スライディングウィンドウ）→ 4xダウンサンプル → Adapter → 自己回帰デコーダ（26層、次元3072、GQA）→ トークン → テキスト
- ブラウザ化の技術的課題と対策
  - 2GBアロケーション上限：データを分割して扱うShardedCursor
  - 4GBアドレス空間制約：2段階ロード（パースしてからリーダを破棄）
  - 埋め込み表の巨大化（1.5GiB）：Q4埋め込みをGPUへ、CPU側で行のルックアップ
  - 同期GPU読み出し不可：非同期into_data_async()を使用
  - WebGPUワークグループ制限：cubecl-wgpuのパッチ適用
- 実務上の注意点
  - GGUFファイルはブラウザArrayBuffer制限回避のため512MB以下でシャーディング
  - upstreamの左パディング仕様はQ4で認識問題を起こすため、パディングを32→76に調整（詳細はsrc/audio/pad.rs）
- ビルド/実行の概略
  - ネイティブ：モデル重みをダウンロードし cargo run --release（wgpu等のfeature）
  - ブラウザ：wasm-packでビルド、自己署名証明書でHTTPS（WebGPUはセキュアコンテキスト必須）、devサーバでロードしてモデルシャードを取得
- テストとライセンス
  - GPU依存テストはローカルで実行推奨。ライセンスはApache-2.0。

## 実践ポイント
- まず手軽に試す：HuggingFace Spaces上のホストデモで動作を確認。
- ローカルで試す場合：Q4 GGUF（約2.5GB）をシャードしてブラウザ実行を検証。WebGPU対応ブラウザとHTTPSが必要。
- 精度とコストのバランス：ブラウザ向けはQ4でメモリ節約だが精度やprefix問題（パディング）を確認すること。
- 日本向け活用案：会議録音のクライアント側文字起こし、社内データの社外送信を避ける音声UI、オフライン対応のモバイル/社内ブラウザアプリ。
- 開発ヒント：パフォーマンス検証はローカルGPUで行い、WebGPUのワークグループ制約や非同期読み出しの実装を重点的に確認する。
