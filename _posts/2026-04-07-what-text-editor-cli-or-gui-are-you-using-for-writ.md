---
layout: post
title: "What text editor (cli or gui) are you using for writing non-code? - コード以外の執筆にどのテキストエディタを使っていますか？"
date: 2026-04-07T16:33:02.279Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lobste.rs/s/vq6o44"
source_title: "What text editor (cli or gui) are you using for writing non-code? | Lobsters"
source_id: 810652556
excerpt: "Vim・Emacs・GUI・組版を比較し日本語執筆向け最適解を提示"
image: "https://lobste.rs/story_image/vq6o44.png"
---

# What text editor (cli or gui) are you using for writing non-code? - コード以外の執筆にどのテキストエディタを使っていますか？
思わず書きたくなるエディタはどれ？──現場の「使える」選択肢ガイド

## 要約
開発者コミュニティでは用途や文字種（英語 vs 日本語/CJK）、集中モードの有無で選択が分かれる。軽量CLI、モダンなモーダル、GUIでの長文対応、組版ツールまで使い分けが鍵。

## この記事を読むべき理由
エディタ選びは生産性に直結します。日本語入力や履歴書・技術記事作成など、日本の現場で直面する課題を踏まえた「実際使える」選択肢と運用ヒントが得られます。

## 詳細解説
- モーダル系（Vim/Neovim, kakoune, Helix）  
  高速なキーバインドとカスタマイズ性が魅力。プラグインでMarkdownや見出し移動（jump list/gO）を強化できるが、CJK入力と組み合わせると操作感が難しくなることがある。
- Emacs + Org mode / Doom Emacs + Evil  
  ノート管理やアウトライン作成、長文編集に強い。EvilでVim慣れとの折り合いをつける人が多い。拡張でPDF注釈やLaTeX連携も可能だが、カスタマイズの工数は大きい。
- 軽量CLI（nano, micro）  
  すぐ開いて書く・修正する用途に最適。学習コストが低く普段使いに向く。
- GUI長文エディタ（Sublime Text, BBEdit）  
  Markdownや長文の執筆、サイト記事作成に便利。視覚的に編集しやすく、外部プレビューツールやエクスポートが使いやすい。
- 専門組版ツール（Typst, Pandoc, groff, LaTeX）  
  高品質な出力（履歴書・論文・印刷物）にはTypstやPandoc→PDFの組合せが実用的。LaTeXは強力だが学習コストが高い。
- ノートアプリ／個人Wiki（Obsidian, Trilium, Logseq）  
  日次ノート、リンク型の知識管理に有効。ObsidianはCLIやプラグインが充実し、スクリプト連携でワークフロー自動化が可能。
- 専用ハード／集中ツール（Freewrite, goyo/pencilプラグイン）  
  気を散らさず書きたいときに効果的。vim-pencilやgoyoはVim上で「執筆モード」を作るプラグイン。

CJK（日本語・韓国語）の注意点：モーダルエディタはIMEとの相性で入力が煩雑になるため、日本語主体の執筆ではGUIのMarkdownエディタ（Apostrophe等）や設定を工夫したIME運用が現実的。

参考になる小ネタ（Obsidian CLIを使ったワンライナー追記例）:
```bash
#!/usr/bin/env bash
obs () {
  local text="$*"
  if [[ -z "$text" ]]; then
    echo "Usage: obs <text to append>"
    return 1
  fi
  if [[ "-" == "$text" ]]; then
    text=$(cat)
  fi
  local timestamp
  timestamp=$(date +"%m/%d %H:%M")
  local entry="- ${timestamp} -- ${text}"
  obsidian daily:append content="$entry"
}
```

## 実践ポイント
- 目的で選ぶ：短いメモ→nano/micro、長文→Sublime/Emacs、学術/履歴書→Typst or Pandoc。  
- 日本語を書くならまずGUIアプリを試す。モーダル操作はIMEの挙動を確認してから導入。  
- ノートは1フォルダ（例: ~/Notes）で管理し、Markdown＋Pandocで変換ルートを持つと汎用性が高い。  
- 集中したいときは「執筆モード（goyo/pencil, darkroom-mode）」や専用ハードを検討。  
- 小さな自動化（Obsidian CLIやシェル関数）で日常のメモ取りが楽になる。

短時間でいろいろ試して、自分の書く内容（技術メモ・長文・日本語）に最適な組合せを見つけてください。
