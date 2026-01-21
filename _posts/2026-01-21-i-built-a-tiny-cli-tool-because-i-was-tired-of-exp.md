---
layout: post
title: "I built a tiny CLI tool because I was tired of explaining my repo structure - リポ構成を説明するのに疲れたので作った小さなCLIツール"
date: 2026-01-21T13:27:35.386Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/zero-badger/repoviz"
source_title: "GitHub - zero-badger/repoviz: A simple CLI tool to visualize repository structure"
source_id: 421262989
excerpt: "Repovizでリポジトリ構成を一瞬で可視化し、PRやREADME作成の説明工数を激減"
image: "https://opengraph.githubassets.com/33745ca5ff9407db57223ffbcb65b8af967fd0107746d29d4c57ecdfc7cd55b5/zero-badger/repoviz"
---

# I built a tiny CLI tool because I was tired of explaining my repo structure - リポ構成を説明するのに疲れたので作った小さなCLIツール
説明ゼロで伝わる！リポジトリ構成を一瞬で可視化する「Repoviz」

## 要約
Repovizはローカルのディレクトリ構造をツリー表示し、ターミナル出力や.md/.txtへのエクスポート、対話モードでの探索を可能にする小さく速いRust製CLIツールです。面倒なスクリーンショットや手書きのツリーを不要にします。

## この記事を読むべき理由
チーム内のコードレビュー、オンボーディング、PR説明、ドキュメント作成で「フォルダ構成を説明する手間」を削減できます。日本のスタートアップや大規模モノレポ運用の現場でも、構成共有の負担を減らす実用ツールとして即導入可能です。

## 詳細解説
- 何をするか  
  Repovizは指定ディレクトリを走査して、見やすい木構造で出力します。端末でそのまま表示するか、Markdown／プレーンテキストとして保存可能です。対話モードを使えばシェル風に再起動不要で探索できます。

- 主な機能
  - ターミナルにツリーを出力
  - `.md` / `.txt` へエクスポート
  - 対話モード（help、exit、パス指定での表示など）
  - デフォルトで `.git`, `node_modules`, `target`, `.idea`, `.vscode` 等の雑多なフォルダを無視
  - Rustで書かれており依存が少なく高速

- インストール（ソースから）
  ```bash
  cargo build --release
  # バイナリは target/release/repoviz に生成される
  sudo mv target/release/repoviz /usr/local/bin/
  ```

- 使い方の例
  ```bash
  repoviz .                # カレントディレクトリのツリーを表示
  repoviz . -c structure.md  # structure.md に保存
  repoviz                  # 対話モードで起動
  ```

- 現状と今後  
  現状は初期バージョンで、無視リストの設定や追加フォーマットなどが今後の改善予定。OSSとしてPRやIssueを受け付けています。

## 実践ポイント
- 少人数チームのPRテンプレートに「構成図（repoviz出力）」を追加すると、レビュアーの理解コストが下がる。  
- READMEの「プロジェクト構成」セクションを自動更新するスクリプトに組み込めば、ドキュメントの鮮度を保てる。  
- VS Codeの統合ターミナルで repoviz を実行し、出力をそのままREADMEに貼るだけで視覚的な説明が完成する。  
- Rust環境がない場合は事前にRustをインストールするか、リポジトリで配布されるバイナリ（将来公開される可能性あり）を利用するとよい。

Repovizは「説明する時間」をコード制作に回せるシンプルな効率化ツールです。まずはローカルリポジトリで試して、PRやオンボーディングでの活用を検討してみてください。
