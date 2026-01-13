---
layout: post
title: "hgit: git in 200~ lines of code - Gitを約200行で実装した小さなリポジトリ"
date: 2026-01-13T11:00:46.576Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/onajourney/hgit"
source_title: "GitHub - onajourney/hgit: Git in 220 lines. Built on hako."
source_id: 427982891
excerpt: "約220行のRust実装でMerkleツリー式Gitの核を学べる入門デモ"
image: "https://opengraph.githubassets.com/355dae1efb2f2f316f41bbaa3e39951c8fea30c3c98a456d5426b40cb1b633bd/onajourney/hgit"
---

# hgit: git in 200~ lines of code - Gitを約200行で実装した小さなリポジトリ
超シンプルな「Git」を触って学べる —— たった数百行で動くMerkleツリー式バージョン管理の本質を理解できるデモ

## 要約
hgitはRustで書かれた、hakoという極小ライブラリ上に構築された「Gitに似た」実装。実装は約220行で、内容アドレス（ハッシュ）によるツリー構造だけでコミット、ログ、チェックアウトを実現している。

## この記事を読むべき理由
Gitの内部がブラックボックスに感じる日本の初学者／若手エンジニアにとって、余計な機能を削ぎ落した実装は理解の近道になる。教育やプロトタイピング、組み込み向けの軽量VCS設計の参考にもなる。

## 詳細解説
- コアアイデア：すべてはツリー（Merkle tree）
  - ファイル（blob）→ Leaf（content）
  - ディレクトリ／構成→ Branch（entries）
  - コミット→ Branch([tree, parent, message])
  - 同じ内容は同じハッシュになるため自動的に重複排除される。

- hakoのプリミティブ（非常に少ない）
  - I：32バイトのBLAKE3ハッシュ（Identity）
  - combine：複数ノードからツリーを作る関数
  - Store：内容アドレス化された保存層
  これら3つだけで「Git的な動作」が生まれる、というのが著者の主張。

- 実装の構成（リポジトリ内）
  - hako（lib.rs） ≈ 58行：基盤のツリー操作
  - git（main.rs） ≈ 173行：init / commit / log / checkout を提供
  - ビルドはCargoで実行（Rust製）

- 使い方（例）
```bash
# bash
git clone https://github.com/onajourney/hgit
cd hgit
cargo build --release

# リポジトリ作成と簡単な操作
./target/release/hgit init
echo "hello" > file.txt
./target/release/hgit commit "first"
echo "world" > file.txt
./target/release/hgit commit "second"
./target/release/hgit log
./target/release/hgit checkout <commit-hash>
```

## 日本市場との関連性
- 教育リソースとして最適：大学や社内トレーニングで「なぜGitはこう動くのか」を見せる教材になる。
- 組み込み・制約環境での応用可能性：フル機能のGitが重い場面で、概念を流用した軽量VCSを設計するヒントに。
- Rust人気の高まり：日本でもRustを学ぶ開発者が増えており、実例コードとして読みやすく追跡しやすい。

## 実践ポイント
- まずはローカルでビルドして動かす：コード量が少ないので、main.rs/lib.rsを開いて一行ずつ追うと理解が早い。
- .hakoストレージを直接覗いてみる：内容アドレス化されたファイル配置を観察するとMerkleツリー概念が実感できる。
- 教材化する：新人研修で「Gitの核」を短時間で伝える演習に使える（変更差分ではなく、ハッシュとツリーの関係にフォーカス）。
- 拡張の練習：例えば差分圧縮やリモート同期を一機能ずつ付け足して、フルGitとの違いを体験する。

興味が湧ったらリポジトリを読んでみてください。行数が少ないぶん、実装から得られる学びは大きいです。
