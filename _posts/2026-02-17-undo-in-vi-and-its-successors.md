---
layout: post
title: "Undo in Vi and Its Successors - ViのUndoとその系譜"
date: 2026-02-17T14:39:48.480Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://utcc.utoronto.ca/~cks/space/blog/unix/ViUndoMyViews"
source_title: "Chris&#39;s Wiki :: blog/unix/ViUndoMyViews"
source_id: 47047443
excerpt: "Vimやnvi、BusyBoxなどで異なるUndo挙動と確認・対処法が短時間で分かる"
---

# Undo in Vi and Its Successors - ViのUndoとその系譜
「u」で戻れると思ったら違った？Vi系エディタのUndoルールを短時間で把握する

## 要約
古典的なviは単一レベルのUndo（`u`がトグル）を採用し、POSIXはこれを規定した。一方でVim系は多段Undo/Redo（`u` / Ctrl‑r）を標準にしており、実用性は大きく異なる。

## この記事を読むべき理由
サーバや組み込み機器、遠隔編集で「vi」を開いたとき挙動が違うと作業効率を大幅に損ないます。日本の現場でもBusyBoxやnvi、Vimなど混在するため、Undo挙動を理解しておくとトラブル回避に直結します。

## 詳細解説
- 歴史とPOSIX: Bill Joyの古典viは単一Undoで、`u`を押すと直前の変更を取り消すか、すでにUndoしていれば「Undoの取り消し（Redo）」になる。POSIXのvi仕様はこの挙動を踏襲している。
- Vim系: `u`は多段Undoのみ、RedoはCtrl‑r。どちらも回数指定が可能（例: `10u` や `10<C‑r>`）で、カーソル移動や検索を挟んでもUndo/Redoの連続性が保たれる点が使い勝手で優れる。
- nvi: POSIX互換を保ちながら多段Undoをサポートするが方式が特殊。`u..` のように `u` を `.` で延長して複数回取り消す設計で、`.` にカウントはないため一括Undo不可。途中でカーソル移動などを挟むとシーケンスが壊れる可能性がある。
- BusyBoxや軽量実装: 最小実装では`u`を繰り返して多段Undoに見せるがRedoがない場合が多い（組み込み/IoTで妥当）。
- Emacsのevilやその他派生: 実装や設定に依存し挙動が曖昧なことがあるため注意が必要。
- 結論（原著者の見解）: VimのUndo/Redoモデルが最も直感的で「人に優しい」。

## 実践ポイント
- 使っているviが何か確認する:
```bash
# 例
which vi
vi --version  # 出ないこともある
vim --version
busybox | grep vi
```
- 日常はVim推奨。Vimで永続Undoを有効にする設定例:
```bash
# vimrc
set undofile
set undodir=~/.vim/undo
set undolevels=1000
```
- サーバ等で`vi`を開いたら、まず簡単な編集で`u`/`Ctrl-r`を試して挙動を確認する（BusyBoxやnviだと違う）。
- nviやBusyBox環境ではUndoの途中でカーソル移動や別操作を挟まないよう注意する。

元記事: "Undo in Vi and Its Successors"（Chris Siebenmann, 2026）
