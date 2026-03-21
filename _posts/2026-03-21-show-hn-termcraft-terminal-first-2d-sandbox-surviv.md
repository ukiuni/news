---
layout: post
title: "Show HN: Termcraft – terminal-first 2D sandbox survival in Rust - Show HN: Termcraft — ターミナル中心の2Dサンドボックスサバイバル（Rust製）"
date: 2026-03-21T20:28:20.522Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/pagel-s/termcraft"
source_title: "GitHub - pagel-s/termcraft: Terminal-first 2D sandbox survival in Rust. · GitHub"
source_id: 47469949
excerpt: "ターミナルだけで遊べるRust製2Dサバイバル、低リソースでクラフトと探索を再現"
image: "https://opengraph.githubassets.com/d7ef6ac6fc25344a70db4a079d626513d585c199f2acca08d953ac57467ebfce/pagel-s/termcraft"
---

# Show HN: Termcraft – terminal-first 2D sandbox survival in Rust - Show HN: Termcraft — ターミナル中心の2Dサンドボックスサバイバル（Rust製）
ターミナルだけで遊べる“クラシック感”満載の2Dサバイバル。低リソースで懐かしいゲーム体験を開発者向けに再現したTermcraftの魅力。

## 要約
TermcraftはRustで書かれた「ターミナル優先」の2Dサンドボックスサバイバルで、オーバーワールド／ネザー／エンド生成、クラフト、モブ、チェストなど初期のブロック系サバイバルをサイドビューで再構築している。

## この記事を読むべき理由
- ローカル開発環境（VS CodeやSSHターミナル）だけで遊べるため、低スペックPCやリモート作業環境でも楽しめる。  
- Rust製プロジェクトの構成やターミナル入出力を活かしたゲーム設計は、ゲーム開発やツール作りの学習材料としても有益。

## 詳細解説
- コア機能: 手続き生成のオーバーワールド／ネザー／エンド、採掘・設置・インベントリ・クラフト・かまど・醸造、体力・空腹・戦闘、流体や重力、作物・村・ダンジョン・ネザー要塞など。  
- 入出力設計: 「ターミナル第一」を掲げ、raw inputやマウス（対応ターミナルで）を利用。右クリックが不安定な端末向けにキー操作のフォールバックが用意されている。  
- 開発面: 単一プレイヤーが主要モード。クライアント/サーバーコードは存在するが実験段階。保存はリポジトリ内の saves/ にローカル保存。  
- 技術スタック: Rust（ほぼ100%）で実装。テスト・静的解析・リリース用スクリプトもリポジトリ内にある（cargo test / cargo clippy 等）。

インストール例（Rustツールチェーン必須）:

```bash
# Rust を導入（未導入の場合）
# https://rustup.rs を参照
git clone https://github.com/pagel-s/termcraft.git
cd termcraft
cargo run --release
# または最適化済バイナリをビルド
cargo build --release
./target/release/termcraft
# ローカルにインストールする場合
cargo install --path .
```

主な操作（抜粋）: A/D または ←→ 移動、W/↑/Space ジャンプ、E インベントリ、左クリック 採掘、右クリック 設置/操作、F で明示的相互作用。開発用ショートカット：F5〜F9で次元移動や装備切替。

## 実践ポイント
- まずはローカルで cargo run --release して挙動を確認。ターミナルによってマウス右クリックが不安定なので、Fキー操作を試す。  
- saves/ 以下にセーブされるため、バックアップやバージョン管理がしやすい（リポジトリで遊ぶ設計）。  
- Rust学習用途として、cargo test や cargo clippy を動かし、コード構成やゲームロジックの実装手法を読むと得るものが大きい。  
- 日本のコミュニティに翻訳やローカライズ、ターミナル互換性改善の貢献余地あり。興味があればIssueやPRで参加を検討。
