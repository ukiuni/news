---
layout: post
title: "Common Lisp Development Tooling - Common Lisp 開発ツール群"
date: 2026-03-21T21:41:25.654Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.creativetension.co/posts/common-lisp-development-tooling"
source_title: "Common Lisp Development Tooling — creative:tension"
source_id: 47470734
excerpt: "REPL中心の六層構成でSBCL＋Quicklispを使い短時間で環境構築する手順"
---

# Common Lisp Development Tooling - Common Lisp 開発ツール群
今日から始めるCommon Lisp──「生きてる」開発環境を6層で一気に理解する

## 要約
Common Lispの開発環境は「対話的で生きている」プロセスを前提に設計されており、ツールは機能ごとに6つの層に分かれる。各層の役割と代表的ツールを理解すれば、導入とトラブルシュートが格段に楽になる。

## この記事を読むべき理由
Lispは他の言語と似て非なる開発モデル（REPL主導、コンパイル時のコード実行、条件/リスタート）を採るため、初心者が環境構築で挫折しやすい。日本のエンジニアが短時間で「動く」環境を作り、原因追跡できるようになるための最短マップを示す。

## 詳細解説
開発環境は下記の6層に分けられる（下が低レイヤ）：

- レイヤー0：マシン（macOS / Linux / Windows）  
  CPUやパス配置（Homebrewの場所、MSYS2経由など）が以降のツールに影響する。

- レイヤー1：コンパイラ／ランタイム（例：SBCL, CCL, ECL, LispWorks）  
  SBCLが事実上の標準。REPLが「生きた」開発の中心で、マクロや条件/リスタートによりコンパイル時と実行時の境界が曖昧になる。

- レイヤー2：ビルドシステム（ASDF）  
  .asdでソース順や依存を定義。ASDFはほとんどの実装に同梱されるが、ソース検索パス（~/.local/share/common-lisp/source/等）を理解しておかないと「system not found」になる。

- レイヤー3：パッケージリポジトリ（Quicklisp, Ultralisp, ocicl）  
  Quicklispが定番で月次ディストで安定性を提供。ociclはOCIベースで隔離機能と組み合わせやすい。QuicklispはREPL内で動く点が他言語のパッケージマネージャと異なる。

- レイヤー4：プロジェクト単位の隔離（Qlot, ociclなど） — オプションだが複数プロジェクトでバージョン衝突を避けたい場合は必須に近い。

- レイヤー5：Swank/SLYNK（サーバ）＋クライアント（SLIME, SLY, Alive, SLIMV, Vim/Neovimプラグインなど）  
  エディタとREPLをつなぐプロトコル。ここがLispの「ライブ」体験をエディタへ橋渡しする。

- レイヤー6：エディタ（Emacsが最も成熟、ほかVSCode Alive, Vim/Neovim, Pulsar, Lem）  
  エディタ選びは生産性に直結。Emacs+SLIME/SLYは最も機能豊富だが、VSCodeやNeovimのプラグインでも十分始められる。

重要な特徴：Lispはプロセス内でライブラリを取得・読み込みするスタイル（QuicklispがREPL内で機能）で、マクロがコンパイル時にコードを生成するなど「ランタイムとコンパイルの境界が動的」である点が他言語と決定的に異なる。

## 実践ポイント
- 始めはSBCL + Quicklispで環境構築。Roswellを使うと初期設定が楽。  
- エディタはまずEmacs+SLIMEまたはVSCode+AliveでREPL統合を体験する。  
- ASDFのソース検索パスとQuicklispの設置場所を確認して「system not found」を切り分ける。  
- 複数プロジェクトでバージョン衝突が起きるならQlotかociclで隔離を導入する。  
- チーム開発ならSBCLのバージョン固定やCIでのビルド確認をルール化する。

短時間で動かしたければ、「SBCL起動 → Quicklisp導入 → (ql:quickload ...) → エディタでREPL接続」の順に試すと挫折しにくい。
