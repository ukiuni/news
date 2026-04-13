---
layout: post
title: "Little LaTeX Pearls - 小さな LaTeX の珠玉"
date: 2026-04-13T19:48:18.992Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ionathan.ch/2026/04/08/LaTeX.html"
source_title: "Little LaTeX Pearls &middot; Jonathan Chan"
source_id: 764442295
excerpt: "卒論や学会・arXiv対応で差がつく、実務向けLaTeX小技集（パッケージ順序・間隔・定理・数式タグ）"
image: "https://ionathan.ch/assets/images/banner.avif"
---

# Little LaTeX Pearls - 小さな LaTeX の珠玉
LaTeXで論文を書く人なら知っておきたい、実務で効く「小技」集 — 卒論・学会投稿で差がつく設定とマクロ。

## 要約
著者が大学院で使い続けてきた、パッケージ読み込み順・スペーシング・定理・数式タグなどの小さなTweakを短くまとめた実用メモです。

## この記事を読むべき理由
LaTeXでの細かい崩れ（間隔、参照名、PDFメタデータ、arXiv提出問題）は地味に時間を食います。日本の学生や研究者が学会テンプレやarXiv対応をする際、すぐ使える実践的ノウハウが得られます。

## 詳細解説
- パッケージの読み込み順
  - 一部パッケージは順序依存。例: mathtools は unicode-math より先、thmtools は cleveref より先、hyperref は cleveref より先など。競合でundefinedや見た目崩れを起こすので注意。

- 略語の後の空白
  - \eg のような略語マクロは \@ と xspace を組み合わせると良い:
```tex
% tex
\usepackage{xspace}
\newcommand{\eg}{e.g.\@\xspace}
```

- イタリック→直立の衝突（italic correction）
  - イタリック体の直後に直立文字や数式が詰まる場合は italic correction の \/ を挿入:
```tex
% tex
If \/ $ \vdash \Gamma $ and $x:A\in\Gamma$ then $\Gamma\vdash x:A$.
```

- 句読点の上に脚注を重ねる
  - 脚注を句点の直上に表示したいときのマクロ例:
```tex
% tex
\newlength{\punctwidth}
\newcommand{\punctstack}[1]{#1\settowidth{\punctwidth}{#1}\kern-\punctwidth}
Here's a sentence\punctstack{.}\footnote{footnote above punctuation.}
```

- 表示数式の前後間隔
  - \abovedisplayskip / \belowdisplayskip を調整する場合は \begin{document} の後で設定すること:
```tex
% tex
\begin{document}
\setlength{\abovedisplayskip}{0.25\baselineskip}
\setlength{\belowdisplayskip}{0.25\baselineskip}
\end{document}
```

- よく変える長さパラメータ（例）
  - \jot, \fboxsep, \abovecaptionskip, \belowcaptionskip, \floatsep, \textfloatsep, \intextsep など。enumitem の topsep/parsep/itemsep もよく調整する。

- 定理の見出し直後で改行したい場合
  - \leavevmode を使って改行を安定させる:
```tex
% tex
\begin{theorem}[長い定理名]
\leavevmode\\
$$0+1=1$$
\end{theorem}
```

- カスタム QED（LuaLaTeX + fontspec）
```tex
% tex
\usepackage{fontspec}
\newfontfamily{\qedfont}{DejaVu Sans}
\renewcommand{\qedsymbol}{\qedfont\char"220E}
```

- タイトル中の数式や改行（hyperref と PDF メタデータ）
  - \textorpdfstring を使い、PDFメタ情報に入れる代替テキストを指定する。

- 数式タグを手動で付ける（mathtools）
```tex
% tex
\usepackage{mathtools}
\mathtoolsset{showmanualtags}
\newtagform{brack}{[}{]}
\usetagform{brack}
\begin{gather}
0+1=1\nonumber\\
1+1=2\tag{fib3}
\end{gather}
\usetagform{default}
```

- LLNCS 固有の定理環境問題や nameref の不具合
  - makeatletter を使った小さなフックで回避できるケースがある（テンプレ依存）。

- arXiv 対策
  - 最近は \pdfoutput=1 を設定するだけで通ることが多い。

## 実践ポイント
- まず mathtools, hyperref, cleveref の読み込み順を確認する。
- 略語用マクロは xspace と \@ を組み合わせて定義。
- 論文テンプレで表示数式の余白が気になるなら \abovedisplayskip 等を \begin{document} 後に調整。
- LuaLaTeX を使えるならフォントで QED 記号をUnicodeにすると見栄えが良い。
- arXiv提出前に \pdfoutput=1 を追加しておく。
- Overleaf/共同執筆ではこれらのマクロを自分のプリセット（styファイル）にまとめておくと再利用が楽。

以上の小技は「大きなレイアウト調整」の前に試すと時間短縮になります。必要なら具体的なテンプレ（acmart, llncs, arXiv）向けに最小再現例を作成します。
