---
layout: post
title: Show HN: AutoLISP interpreter in Rust/WASM – a CAD workflow invented 33 yrs - Show HN: Rust/WASMによるAutoLISPインタープリタ – 33年前に発明されたCADワークフロー
  ago'
date: 2025-12-26 17:29:30.727000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://acadlisp.de/noscript.html
source_title: AutoLISP Interpreter in Rust/WASM - acadlisp.de
source_id: 46393271
excerpt: ブラウザでAutoLISP実行、AutoCAD不要でCSV→DXF図面を即生成
---
# Show HN: AutoLISP interpreter in Rust/WASM – a CAD workflow invented 33 yrs - Show HN: Rust/WASMによるAutoLISPインタープリタ – 33年前に発明されたCADワークフロー

## 要約
AutoLISPインタプリタをRustで実装しWASMにコンパイルした「acadlisp」により、AutoCAD不要でブラウザ上でAutoLISPを実行、SVG/DXFを出力できる。1991年に生まれたCSV＋テンプレート＋LISPによる設計自動化ワークフローを現代的に保存・再現したプロジェクトだ。

## この記事を読むべき理由
古いCADスクリプトや手作業の設計テンプレートを抱える日本の製造・設備系エンジニアにとって、AutoCADライセンスなしでレガシー自動化を検証・再利用できる手段は実務的価値が高い。さらにRust/WASMでブラウザ化されているため、社内ツールやWebサービスへの組み込みが容易だ。

## 詳細解説
- 背景：1991年、ドイツの小規模電気工事会社で「CSVで部品を定義→テンプレートとLISPで図面自動生成」というワークフローが生まれた。手作業を減らすための実戦的な工夫で、テンプレートがテンプレートを生成するなどLISPの自己生成性を活かしている。
- 技術構成：言語実装はRust。ターゲットをWebAssemblyにしてブラウザ上で動作させることで、AutoCADのインストールやライセンスを不要にしている。
- 入出力と互換性：SVGとDXF（AutoCAD R12 / AC1009）を出力可能。古いDXF互換性は既存のCAD資産と連携しやすい点で日本の現場に有利。
- サポートするAutoLISP機能：基本的な関数群（defun, setq, if, while, cond, リスト処理、三角関数）に加え、CADコマンドを呼ぶための command が実装されている。これにより既存のAutoLISPスクリプトの多くがそのまま試せる可能性が高い。
- LISPの特徴的利点：ホモアイコニシティ（コード＝データ）、自己修正、記号処理に強いことから、テンプレート生成やルールベースの配置・配線自動化に向く。

## 実践ポイント
- まずはブラウザでインタラクティブデモを試す：AutoCADが不要なので既存スクリプトの動作確認が素早くできる。
- レガシーAutoLISPを移行・検証：社内に残るAutoLISPスニペットをまずWASM実行で動かし、問題箇所を特定する（DXF出力で既存CADに取り込み確認）。
- Excel/CSV→図面の自動化：部品表をCSV化し、テンプレート＋AutoLISPで図面生成する流れを再構築すると手入力工数が劇的に減る。
- Web連携：WASMで動くため、社内の軽量Webツール（部品DBと連携して図面を即座に生成・プレビュー）に組み込むのが現実的。
- 小さく試す：まずは短いdefunで矩形や配線を描画してSVG/DXFの出力を確認し、徐々にテンプレートやBOM連携を拡張する。

Example（簡単なAutoLISP例）:
```lisp
(defun draw-box (x y w h)
  (command "LINE" (list x y) (list (+ x w) y) "")
  (command "LINE" (list (+ x w) y) (list (+ x w) (+ y h)) "")
  (command "LINE" (list (+ x w) (+ y h)) (list x (+ y h)) "")
  (command "LINE" (list x (+ y h)) (list x y) ""))
(draw-box 10 10 100 50)
```

