---
layout: post
title: "I made a terminal pager - ターミナル用ページャーを作った"
date: 2026-04-15T22:59:18.823Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://theleo.zone/posts/pager/"
source_title: "I Made a Terminal Pager | Leo Robinovitch @ The Leo Zone"
source_id: 47786164
excerpt: "Go製の軽量ターミナルページャーloreでUnicodeや検索・選択が快適に"
---

# I made a terminal pager - ターミナル用ページャーを作った
lessだけじゃ満足できない人へ：Goで作った新しい端末ページャー「lore」と、その核となる再利用可能なViewportコンポーネントを読み解く

## 要約
Goで書かれた再利用可能な「viewport」コンポーネントを核に、ターミナルで大容量テキストを快適に閲覧・検索・選択できる軽量ページャー「lore」を作った話。Unicode幅やANSIスタイル、検索／フィルタリング、選択機能など設計上の工夫を詳述する。

## この記事を読むべき理由
ターミナルでログや長文を読む機会が多い日本の開発者にとって、表示の正確さ（幅、折り返し、絵文字など）と操作性は生産性に直結する。本家lessの知識がある人も、TUI設計やGoでの実装パターン、実運用で便利なショートカット設計を学べる。

## 詳細解説
- ターミナルの性質: 端末はモノスペースのグリッド（行×列）で文字が描画される。ANSIエスケープで色付けでき、出力が画面高さを超えるとページャーに渡すのが一般的（PAGER環境変数）。
- PAGERの使われ方: gitやmanはstdoutがTTYかどうかを確認し、TTYならPAGERに出力をパイプする。PAGERをcatにすれば出力を直に流す運用も可能。
- TUIとViewport: TUIでは画面を複数のコンポーネントに分けることが多く、その中で「テキスト表示領域（viewport）」は再利用性の高い基本要素。ビューはリサイズ、スクロール、折り返し（または横パン）、ANSI処理、検索、選択などを担う。
- コンポーネント構成: 実装は大きく item（文字列を端末セル幅で扱う単位）、viewport（表示・操作の本体）、filterableviewport（検索フィルタ追加）の3つで構成され、Bubble Teaフレームワークに容易に組み込める設計。
- Unicode幅の扱い: 絵文字や結合文字が端末上で占めるセル幅は1〜2だったり0だったりする。実装はバイト列→コードポイント→グラフェム→ターミナルセル幅のマッピングを内部に保持し、Take/Width APIで幅指定の切り出しを効率的に行う。
- 検索・フィルタリング: 正確一致（/）、正規表現（r）、大文字小文字無視（i）など単一キー割当で操作感を速くし、マッチの前後コンテキスト表示やマッチ間移動（n/N）をサポート。
- アイテム選択: 表示アイテムをオブジェクトジェネリックで扱い、選択有効化／無効化が可能。選択されたオブジェクトはGetSelectedItemで取り出せ、Enter押下で詳細表示へ遷移するような連携が容易。
- loreの位置付け: lessの全機能を目指すのではなく、日常的に欲しい操作性に絞った軽量ページャー。PAGERに設定して通常のCLI出力を置き換えられる。実装ノウハウは他のTUI（例: kl）にも還元可能。

## 実践ポイント
- loreを試す（Go環境またはDockerで可）:
```bash
# Goがあれば
go run github.com/robinovitch61/viewport/examples/filterableviewport@latest

# Dockerなら
docker run -ti golang:1.26-alpine \
  go run github.com/robinovitch61/viewport/examples/filterableviewport@latest
```
- 日常運用: ~/.zshrcなどで export PAGER=lore を設定すると git 等で自動的に使える。
- 実装で注意する点:
  - Unicodeセル幅の処理（wcwidth相当）を必ず入れること。
  - 大量テキストではアイテムの遅延/事前構築（SingleItem / MultiItem）でパフォーマンスを確保する。
  - 検索は操作性優先で単一キー割当を検討する（/, r, i, n/N）。
- 日本語市場での応用例: 日本語ログやutf-8混在メッセージの閲覧、k8sログ監視ツールとの統合、社内CI出力の見やすさ向上など。特にマルチバイト／結合文字の扱いが重要な場面で有用。

参考として、より低レイヤ寄りの端末処理を扱う libghostty 等のプロジェクトにも注目すると実装の幅が広がる。
