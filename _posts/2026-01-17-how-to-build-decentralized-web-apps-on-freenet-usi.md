---
layout: post
title: "How to Build Decentralized Web Apps on Freenet Using Rust and WebAssembly - Freenet上でRustとWebAssemblyを使って分散型Webアプリを作る方法"
date: 2026-01-17T19:55:08.250Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://freenet.org/resources/manual/tutorial/"
source_title: "Building Decentralized Apps on Freenet | Freenet"
source_id: 424346500
excerpt: "RustとWASMでFreenet上に検閲耐性の分散Webアプリを実装・公開する実践ガイド"
---

# How to Build Decentralized Web Apps on Freenet Using Rust and WebAssembly - Freenet上でRustとWebAssemblyを使って分散型Webアプリを作る方法
中央サーバー不要で動く検閲耐性アプリを、Rust＋WASMでFreenet上にデプロイする実践ガイド

## 要約
Freenetは中央サーバーなしで検閲耐性のあるサービスを動かせるP2P基盤で、アプリはRustで書いてWASMにコンパイルし「Contract（共有状態）」「Delegate（端末内秘密領域）」「UI（ブラウザ）」の三層で動きます。本稿はアーキテクチャと開発フローのポイントを初心者向けに整理します。

## この記事を読むべき理由
日本でもプライバシー重視や検閲回避、災害時のローカル通信など分散型・ローカルファーストなアプリへの関心が高まっています。Freenetはそうした用途に向く実装パターンを提示しており、Rust＋WASMの実務的な組合せを学べば安全で効率的な分散アプリ開発に直結します。

## 詳細解説
- アーキテクチャ概観  
  - Contract（ネットワーク層）: アプリの共有バックエンド。WASMとしてネットワーク上のピアで動くが、ブロックチェーンとは違い「複製された汎用データ構造」を扱う点が特徴。コードハッシュが契約キーになり、任意のピアで検証されるため秘密情報は保管できない。  
  - Delegate（ローカル信頼領域）: ユーザー端末内で動き、秘密鍵や暗号処理などを担う。ネットワークに晒されないため秘密情報はここに置く。  
  - UI（フロント）: 標準的なWebアプリ。ローカルのFreenetカーネルとWebSocketで通信し、場合によってはUI自体をWebコンテナ契約として配布可能。

- 一貫性モデル（重要）  
  Freenetはピア間で更新の順序が異なることがあるため、契約の状態は「交換や合成が順序に依存しない」設計が必要です。具体的には状態を可換モノイド風に扱い、ピア間は「Summary（要約）」と「Delta（差分）」をやり取りして効率的に同期します。

- 開発の流れ（要点）  
  1. 環境: Rust（rustup）とWASMターゲット、Freenetコアのビルド。  
  2. プロジェクト構成: Cargoワークスペースで common / contracts / delegates / ui を分けるのが標準的。  
  3. Contract実装: freenet-scaffold の #[composable] マクロで summary/delta/merge/verify を自動生成。Contractは validate/update/summarize/get_delta のインタフェースを実装する。  
  4. Delegate実装: 秘密管理や署名、暗号処理をここに置く。UIからの要求へ非公開処理で応答する。  
  5. UI: 任意のWebフレームワーク（RiverはDioxus）で作成し、WebSocket経由でカーネルとやり取りする。UIをWASMで共通コードと共有できる点が強み。  
  6. ビルド/テスト/公開: WASMにビルドして freenet publish で配布。公開時はWASMのハッシュ（契約キー）でアクセスする。

- ミニコード例（状態定義のイメージ）
```rust
// Rust
use freenet_scaffold_macro::composable;
use serde::{Deserialize, Serialize};

#[composable]
#[derive(Serialize, Deserialize, Clone, Default, Debug)]
pub struct AppState {
  pub members: Members,
  pub messages: Messages,
}
```

- 制約と現状  
  - 現状はRust/WASM主体。  
  - ネットワークやツール群は発展途上で、公式ビルドが必要なケースあり。  
  - 実運用でのスケールや公開ネットワークの成熟度は今後改善予定。

## 実践ポイント
- 最短で触る手順（概略）  
  1. Rustをrustupで導入、WASMターゲットを追加: `rustup target add wasm32-unknown-unknown`  
  2. freenet-core をクローンしてローカルビルド（開発環境として）  
  3. Riverリポジトリを参照して実例を動かす: `git clone https://github.com/freenet/river.git` → `cargo make dev-example`（ローカルでUIを試せる）  
  4. 自分のワークスペースを作り、common/contracts/delegates/ui を分離して開発開始。  
  5. ビルドしてWASMを生成、ローカルで `freenet local` を動かしてテスト。公開は `freenet publish --code target/.../my_contract.wasm --state initial_state.cbor` を使う。  

- 日本での応用アイデア  
  - 災害時のローカルメッセージング、自治体と市民のローカル情報共有、検閲回避が必要なコンテンツ配布、プライバシー重視のチャットやドキュメント共同編集など。

- 学習リソース  
  - River リポジトリを参照して実装パターンを読むことを強く推奨。freenet-scaffold のドキュメントで composable 状態の考え方を理解する。

まずはRiverのサンプルを動かして、Contract/Delegate/UIの役割を体感することが一番の近道です。
