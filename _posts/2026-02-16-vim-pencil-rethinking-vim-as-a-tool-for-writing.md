---
layout: post
title: "Vim-pencil: Rethinking Vim as a tool for writing - Vim-pencil：Vimを文章執筆ツールとして再考する"
date: 2026-02-16T11:55:31.888Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/preservim/vim-pencil"
source_title: "GitHub - preservim/vim-pencil: Rethinking Vim as a tool for writing"
source_id: 46997356
excerpt: "最小限設定でVimを執筆特化エディタに変えるvim-pencilの実践ガイド"
image: "https://opengraph.githubassets.com/c4d9bea5c595cf576a6ae40289fc7f12a5216d993fae84604c04c1ef002ca831/preservim/vim-pencil"
---

# Vim-pencil: Rethinking Vim as a tool for writing - Vim-pencil：Vimを文章執筆ツールとして再考する
Vimでコードだけでなく「書く」ための快適さを手に入れる—vim-pencilが提案する、モーダル編集と文章ワークフローの融合。

## 要約
vim-pencilはMarkdownやテキストなどのプローズ編集に特化したVimプラグインで、行折返し（soft/hard）自動判別、挿入時の自動整形、Conceal対応、バッファ単位設定などで執筆作業を滑らかにします。

## この記事を読むべき理由
日本でもVim／Neovim愛用者は多く、技術ブログやドキュメント、論文執筆をVimで完結させたいニーズが増えています。vim-pencilは「書く操作」を意識した最小限の改良で生産性を上げるため、IDEやワープロからの移行ハードルを下げます。

## 詳細解説
- 対応ファイル種別：text, markdown, mail, rst, tex, textile, asciidoc 等のプローズ向け。
- 折返しモード：soft（表示折返し）とhard（実際に改行を挿入）をバッファ単位で扱い、modeline等で自動検出します。
- 自動整形（autoformat）：hardモード時に挿入中の自動整形を有効にでき、表やコードブロックでは自動整形を一時停止（ブラックリスト）します。
- 挿入モード改善：句読点などでundoポイントを作るなど、執筆向けの細かな操作性向上。
- Conceal対応：Markdownの*_装飾_*等を隠して見た目を整える（対応シンタックスや端末の太字/斜体対応が必要）。
- ステータス表示：バッファごとのモード（hard/auto/soft）をステータスラインに表示可能。
- 設定はバッファスコープが基本で、グローバル設定を侵さずに既存ワークフローを壊しません。
- 実装は純粋なVimscriptで依存なし。インストールはPlug/Pathogen/Vundleやネイティブパッケージで簡単。

## 実践ポイント
- インストール例（vim-plug）：
```vim
" vim
call plug#begin('~/.vim/plugged')
Plug 'preservim/vim-pencil'
Plug 'tpope/vim-markdown' " Conceal対応用
call plug#end()
```
- ファイルタイプ自動初期化（例）：
```vim
" vim
augroup pencil
  autocmd!
  autocmd FileType markdown,text call pencil#init()
augroup END
```
- 好みの折返し／自動整形設定例：
```vim
" vim
let g:pencil#wrapModeDefault = 'soft'  " デフォルトをsoftに
let g:pencil#autoformat = 1            " hard時にautoformat有効
let g:pencil#textwidth = 74            " hard時の幅
```
- 一時的に自動整形を止めたい場合は、キーを割り当ててInsertでサスペンド可能（例：let g:pencil#map#suspend_af = 'K'）。
- Concealで装飾を綺麗に見せるには対応フォント（等幅で太字/斜体を持つもの）と、対応シンタックス／カラースキームを合わせる。VSCodeでNeovim拡張を使う場合は端末設定とフォントに注意。

vim-pencilは「最小限の調整で執筆体験を向上」させる設計です。まずはMarkdownで試し、テキスト幅やautoformatの挙動を自分の書き癖に合わせてチューニングしてみてください。
