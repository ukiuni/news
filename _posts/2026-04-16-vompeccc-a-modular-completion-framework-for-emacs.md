---
layout: post
title: "VOMPECCC: A Modular Completion Framework for Emacs - VOMPECCC：Emacs向けモジュール式補完フレームワーク"
date: 2026-04-16T18:18:23.884Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.chiply.dev/post-vompeccc"
source_title: "VOMPECCC: A Modular Completion Framework for Emacs | Charlie Holland's Blog"
source_id: 361372192
excerpt: "VOMPECCCでEmacs補完を分解して必要機能だけ組合せる最適解"
image: "http://sveltekit-prerender/images/vompeccc-banner.jpeg"
---

# VOMPECCC: A Modular Completion Framework for Emacs - VOMPECCC：Emacs向けモジュール式補完フレームワーク
Emacs補完を「分解して組み替える」——VOMPECCCで作る柔軟かつ軽量な補完環境

## 要約
VOMPECCCはVertico/Orderless/Marginalia/Prescient/Embark/Consult/Corfu/Capeの8つの小さなパッケージ群で、Emacsの標準APIを使って補完の表示・マッチング・ソート・注釈・アクション・インバッファ補完を分離・再構成する設計思想を実現するものです。

## この記事を読むべき理由
Emacsをカスタマイズして生産性を上げたい日本の開発者にとって、従来の「全部入り」HelmやIvyよりもメンテ性・軽量性・互換性に優れ、必要な機能だけを組み合わせられるVOMPECCCは実用的な選択肢です。LSPや大規模プロジェクトでもパフォーマンス面で恩恵があります。

## 詳細解説
- 補完は単一機能ではなく、少なくとも「表示(Display)」「絞り込み(Matching)」「並び替え(Sorting)」「注釈(Annotation)」「アクション(Actions)」「インバッファ補完(Backends/Popup)」の独立した関心事に分かれる。  
- かつてのHelm/Ivyは多機能だが多くを一つのAPIに詰め込み、拡張性や再利用性で制約があった（プロプライエタリAPIに依存しがち）。  
- VOMPECCCのアプローチはUnix哲学に近く、各パッケージが1つの責務に集中し、Emacs標準の完成API（completing-read, completion-styles, completion-at-point-functions等）を介して疎結合に動く。主要コンポーネントの役割は次の通り：
  - Vertico：ミニバッファの縦リスト表示（表示層）
  - Orderless：柔軟なマッチング（フィルタ層）
  - Marginalia：候補の注釈表示（注釈層）
  - Prescient：使用頻度／履歴に基づく並び替え（ソート層）
  - Embark：候補に対する文脈アクション（アクション層）
  - Consult：強化されたコマンド群・検索（コマンド層）
  - Corfu：インバッファのポップアップ表示（in-buffer display）
  - Cape：インバッファ用のバックエンド集合（backends）
- メリット：小さなパッケージで軽量、任意の組み合わせで利用可、既存コマンドに自然に馴染む、個別アップデートや置換が容易。  
- デメリット：最初は自分で組み合わせる手間がある（設定を収束させる必要）、極稀に拡張間で微調整が必要になる場合がある。

## 実践ポイント
すぐ試せる最小セットの導入例（use-package前提）。必要なものだけ選んで有効化するのがVOMPECCC流。

```emacs-lisp
;; emacs-lisp
;; 例：vertico + orderless + marginalia + consult の最小構成
(use-package vertico
  :ensure t
  :init (vertico-mode 1))

(use-package orderless
  :ensure t
  :init (setq completion-styles '(orderless basic)))

(use-package marginalia
  :ensure t
  :init (marginalia-mode 1))

(use-package consult
  :ensure t)
```

導入の順序は自由。Corfu/Capeはインバッファ補完を強化するので、コード補完が目的なら追加する。まずはVertico + Orderlessで挙動を確かめ、必要に応じてPrescientやEmbarkを追加すると良い。
