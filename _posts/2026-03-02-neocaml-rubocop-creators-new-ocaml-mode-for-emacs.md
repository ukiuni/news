---
layout: post
title: "Neocaml – Rubocop Creator's New OCaml Mode for Emacs - Neocaml — Rubocop作成者によるEmacs向け新OCamlモード"
date: 2026-03-02T10:06:10.775Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/bbatsov/neocaml"
source_title: "GitHub - bbatsov/neocaml: A modern, TreeSitter-powered, Emacs major mode for OCaml"
source_id: 47185911
excerpt: "Tree‑sitterで高速化、REPLとocamllspに対応するEmacs用neocaml。"
image: "https://opengraph.githubassets.com/5a924577c79699e3a39bd175be54f534d04d00285c97cce5e334817ae7883e84/bbatsov/neocaml"
---

# Neocaml – Rubocop Creator's New OCaml Mode for Emacs - Neocaml — Rubocop作成者によるEmacs向け新OCamlモード
EmacsでOCaml開発がぐっと快適に。Tree‑sitter採用で軽く速い「neocaml」を今すぐ試すべき理由

## 要約
Tree‑sitterを核にしたEmacs向けOCamlメジャーモード「neocaml」は、軽量かつモダンな構成でフォントロック、インデント、REPL連携、Eglot/ocamllsp統合を提供します。MELPAから導入可能で、既存のtuareg/caml-modeよりシンプルに使えます。

## この記事を読むべき理由
- EmacsでOCamlを書いている／これから書く日本のエンジニアにとって、より安定で高速なシンタックス解析とREPL体験は生産性直結です。  
- ocamllsp/Eglotやutopと自然に連携するため、最近のLSP中心ワークフローに馴染みます。日本のOSS/研究・金融分野でOCamlを使う現場でも導入コストが低い点が魅力です。

## 詳細解説
- 基本設計  
  - Tree‑sitterベースのフォントロック（4レベル）とインデントを採用。正規表現やSMIEに比べて構文認識が堅牢で高速。  
  - .ml/.mli 用の2つのメジャーモードを提供し、ff-find-other-file（C-c C-a）で実装／インターフェースを行き来可能。  
- REPL連携（neocaml-repl）  
  - バッファから定義や領域をREPLへ送れるコマンド群を用意。utopも容易に設定可能。主なキーバインド例:
```emacs-lisp
;; REPL 操作用例
C-c C-z ; neocaml-repl-switch-to-repl
C-c C-c ; neocaml-repl-send-definition
C-c C-r ; neocaml-repl-send-region
C-c C-b ; neocaml-repl-send-buffer
C-c C-l ; neocaml-repl-load-file
```
- LSP/Eglotとの統合  
  - neocamlは eglot 用に言語IDを設定し、ocamllspとの組合せで補完・ジャンプ・型情報がシームレスに動作。ocaml‑eglot を入れると独自拡張（case析出、hole移動等）も使えます。  
- インストールと設定（簡易）  
  - MELPAから M-x package-install neocaml。Tree‑sitter文法が無ければ M-x neocaml-install-grammars を実行。  
```emacs-lisp
;; Eglot に登録（use-package例）
(use-package neocaml :ensure t :config
  (with-eval-after-load 'eglot
    (add-to-list 'eglot-server-programs
                 '((neocaml-mode neocaml-interface-mode) . ("ocamllsp")))))
;; utop を使う場合
(setq neocaml-repl-program-name "utop"
      neocaml-repl-program-args '("-emacs"))
```
- その他機能  
  - Imenu（言語別カテゴリ）、コメント操作（M-; / M-j / M-q）、_build配慮（build成果物からソースへ誘導）、outline/tree‑sitter folding対応など。

## 日本市場との関連性
- 日本の研究機関や金融系でのOCaml採用例がある中、Emacsは根強いエディタです。neocamlは標準化されたLSP環境とTree‑sitterの恩恵で、チーム導入時の「個人設定地獄」を軽減します。  
- GUI版Emacs起動時のPATH問題（utopやocamlが見つからない）には exec-path-from-shell で対応する旨も覚えておくと良いです。

## 実践ポイント
- まずはMELPAでインストールし、M-x neocaml-install-grammars を実行。  
- Eglot + ocamllsp を登録してLSPを有効化する。  
- REPLは utop 推奨。neocaml-repl-minor-mode を有効にしてキーバインドを使い倒す。  
- 既存の tuareg/caml-mode があれば競合を避けるためにアンインストールまたはファイル関連付けを整理する。  
- インデントは treesit、ocp-indent、または indent-relative を用途に応じて選択。treesit-font-lock-level を 4 にすると最大限の強調が得られます。

neocamlは「軽くて今どき」のEmacs用OCamlモードです。EmacsでOCamlを書くなら、まず試してみる価値があります。
