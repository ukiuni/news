---
layout: post
title: "Majutsu, Magit for jujutsu - Majutsu：jujutsu向けMagit風インターフェース"
date: 2026-02-11T19:43:15.238Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/0WD0/majutsu"
source_title: "GitHub - 0WD0/majutsu: Majutsu! Magit for jujutsu"
source_id: 1157991527
excerpt: "Magit風操作でEmacsからjjを直感的に扱えるMajutsu紹介"
image: "https://opengraph.githubassets.com/7dc3b40f17a938e6c00ed03d3a65a3c9da5a8ad7f45f24f285db40c335bc2518/0WD0/majutsu"
---

# Majutsu, Magit for jujutsu - Majutsu：jujutsu向けMagit風インターフェース
Emacsユーザー必見：Magit感覚で新しいVCS「jj（jujutsu）」をガシガシ操作する方法

## 要約
MajutsuはEmacs向けプラグインで、Magitの操作性をjj（jujutsu）リポジトリに持ち込み、履歴閲覧・編集・rebase・squashなどを快適に行えます。

## この記事を読むべき理由
Emacsでの作業効率を高めたい日本の開発者／趣味プログラマへ。もしチームで新しい分散VCS（jj）を試すなら、Magit慣れした操作感で移行コストを下げられます。

## 詳細解説
- 何ができるか：MajutsuはMagitのUI思想をjj向けに実装。ログビュー、差分編集（jj diffedit相当）、注釈（annotate）、rebase/restore/squash/splitなどの操作をEmacs内で完結できます。Magitと連携してblobをMagitで開くことも可能です。
- 操作感：M-x majutsu や majutsu-log で起動。n/pでリビジョン移動、RETで該当項目へ移動、?でヘルプ。blobバッファでe（またはEvilならi）で編集モードに入り、保存でjj diffeditが適用されます。
- 主要コマンド（抜粋）：
  - n / p：次／前のリビジョン
  - RET：選択項目を開く
  - g：リフレッシュ
  - a：absorb（取り込み）
  - b：bookmark
  - c：describe
  - C：commit、d：diff、r：rebase、s：squash、S：split、Z：workspaces
  - C-/（Undo） / C-?（Redo）
- 依存・要件：Emacs 29.1以上、jj（jujutsu） v0.37.0以上、magit/transient/with-editorなど。
- ライセンス：現在はGPL-3.0（過去のコードにMIT表記あり）。

## 日本市場との関連
- Emacsをコアツールにしている日本の開発コミュニティや教育現場では、Magitが根強い。MajutsuはMagit慣れしたユーザーがjjを評価・導入する際の橋渡しになるため、採用検討のハードルを下げます。
- 新しいワークフローやVCSを試験導入するスタートアップやOSSプロジェクトにも有用です。

## 実践ポイント
- インストール例（Doom / use-package等）：
```emacs-lisp
;; Doom Emacs (packages.el)
(package! majutsu :recipe (:host github :repo "0WD0/majutsu"))

;; use-package + straight.el
(use-package majutsu
  :straight (:host github :repo "0WD0/majutsu"))
```
- まずはローカルjjリポジトリで M-x majutsu を実行し、n/pやRETで履歴を触ってみる。blobでeを押して保存→jj diffeditが動く一連の流れを確認するのが習得の近道。
- Magitを使い慣れているなら、主要操作（rebase, squash, diffedit, annotate）を優先的に試すと効果が早く実感できます。
- 要件を満たしていない場合（Emacs / jjのバージョン不足）は、該当バージョンにアップデートしてから試してください。

以上。MajutsuはMagitの快適さをjjに持ち込み、Emacs中心の開発者にとって移行と試用の敷居を下げるツールです。興味があれば公式リポジトリでREADMEとマニュアルを確認してみてください。
