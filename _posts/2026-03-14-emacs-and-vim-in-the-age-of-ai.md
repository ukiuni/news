---
layout: post
title: "Emacs and Vim in the Age of AI - AI時代のEmacsとVim"
date: 2026-03-14T05:39:29.114Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://batsov.com/articles/2026/03/09/emacs-and-vim-in-the-age-of-ai/"
source_title: "Emacs and Vim in the Age of AI | (think)"
source_id: 47319071
excerpt: "AI時代、EmacsとVimは拡張性と端末連携で編集の役割を再定義し生き残る戦略がある"
image: "https://batsov.com/assets/img/og-image.png"
---

# Emacs and Vim in the Age of AI - AI時代のEmacsとVim
AIで「職人ツール」はどう変わる？EmacsとVimが生き残るための現実的シナリオ

## 要約
AIツールの台頭はEmacs/Vimにリスクと機会を同時にもたらす。編集の役割が「書く」から「指示・評価」に移るなか、拡張性と端末志向は両エコシステムの強みになり得る。

## この記事を読むべき理由
日本でも企業でのAI導入や若手の開発環境選択が進む今、普段使っているエディタがどのように変わるか、具体的な影響と現場で取れるアクションがわかるから。

## 詳細解説
- リスク
  - VS CodeやAIネイティブ編集器（Cursor等）は大手リソースでAI統合を先行し、キーバインドや拡張文化そのものを置き換える可能性がある。
  - 「タイプ速度」が価値だった時代から、AI出力をどう仕様化・検証するかが重要になり、従来の習熟優位が薄れる。
  - コア開発の人手・資金差が拡大。高速でAPIやモデルに追随できる組織が有利。
  - 極端な自動化シナリオではエディタ需要そのものが減る可能性も想定されるが、短中期では限定的。

- 機会
  - Elisp/VimScript/Luaといった拡張言語の障壁がAIで低減。自然言語で「こうしたい」と書けばAIが適切な設定や関数を生成できる。
  - プラグインや保守作業の敷居が下がり、コントリビュータの裾野が広がる。テストコード・ドキュメント生成で既存メンテナの効率も向上。
  - ターミナルネイティブなAIツール（Claude Code、Aider等）はEmacs/Neovimと自然に連携でき、GUI一体型よりも柔軟なワークフローを提供。
  - Emacsはエディタを超えた「OS的」存在として、メール・ノート・タスク管理など多領域でAIを横断統合できる強みがある。

- エコシステムの現状（短い例）
  - Emacs側：gptel、aider.el、copilot.el、agent-shell 等のAI統合が増加。
  - Neovim側：avante.nvim、copilot.lua、gp.nvim 等、AI志向のプラグインが活発。

- 倫理・運用上の懸念
  - モデルの学習データ・著作権、運用コスト（電力・計算資源）は無視できない課題。
  - セキュリティ・ライセンス面のチェックやオンプレ/ローカルモデルの採用検討が必要。

## 実践ポイント
- まず試す：端末内で動くAI CLI（例：Claude CodeやCopilot CLI）をvterm/terminal splitで動かし、手元のEmacs/Neovimと組み合わせてみる。
- 小さく導入：設定ファイルの自動生成やエラーメッセージ説明など「学習コスト削減」用途から活用開始する。
- プラグイン投資：興味があるならgptelやcopilot.el、avante.nvimなどの既存プラグインを試し、運用上の期待値・懸念をチェックする。
- コントリビュートの勧め：AIを使ってドキュメント整備やテスト生成を行い、コミュニティ参画のハードルを下げる。
- 企業・チームでは：AI利用ポリシー（データ漏洩・ライセンス）とコスト評価を先に決め、オンプレモデルや閉域運用を検討する。

（短期的には「編集者としての役割の再定義」が鍵。Emacs/Vimの哲学はまだ価値があり、AIを取り込める柔軟さが生存のカギになる。）
