---
layout: post
title: "Xfwl4 – The Roadmap for a Xfce Wayland Compositor - Xfwl4：Xfce向けWaylandコンポジタのロードマップ"
date: 2026-01-27T14:18:49.606Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://alexxcons.github.io/blogpost_15.html"
source_title: "Alexxcon's Software Development Blog"
source_id: 46779645
excerpt: "XfceがRustでxfwm4互換Waylandコンポジタ「xfwl4」を開発、移行影響と対応が注目されています"
---

# Xfwl4 – The Roadmap for a Xfce Wayland Compositor - Xfwl4：Xfce向けWaylandコンポジタのロードマップ
Xfceの“見た目はそのまま、中身は最新”を目指す新・Waylandコンポジタ誕生へ — xfwm4の操作感を維持しつつRustで一から再実装

## 要約
Xfceは寄付金を投じて、長年のコア開発者Brian Tarricone氏を資金提供し、既存のxfwm4と同等の挙動を目指す新しいWaylandコンポジタ「xfwl4」をRust＋smithayで一から開発します。並行開発によりX11側の安定性を損なわず、Wayland特有の設計で柔軟に拡張します。

## この記事を読むべき理由
日本でもデスクトップLinuxや組み込みLinuxでWayland移行は現実的な課題です。Xfceは軽量デスクトップの重要な選択肢であり、xfwl4の動向は日本のデスクトップユーザー、ディストリビュータ、パッケージメンテナ、組み込みベンダーに直接影響します。

## 詳細解説
- 背景と方針  
  既存のアプローチ（xfwm4にWayland対応を付与する）は、X11依存設計が深く残るため不向きと判断。リスクを抑えるため、X11実装（xfwm4）を壊さず並行して新実装を進める方針になりました。

- 言語とライブラリの選択  
  xfwl4はCではなくRustで実装。理由はメモリ安全性によるクラッシュ低減と、開発者の好み。Wayland基盤はsmithayを採用します。smithayは公式Wayland拡張やwlrootsプロトコルを幅広くサポートし、高レベルの抽象化を避け深いカスタマイズが可能で、ドキュメントも充実しています。wlrootsはC主体でRustバインディングが作りにくい点が考慮されました。

- 目標機能と互換性  
  目標は「xfwm4と同じ操作感」――可能な限り既存の挙動を再現し、xfwm4の設定ダイアログやxfconf設定の再利用を計画。とはいえWaylandとX11ではプロトコルや概念が異なるため、差分を吸収する設計が必要です。

- 関連作業とインフラ変更  
  - セッション起動の大幅変更（Waylandではコンポジタがセッションのルートになる）  
  - xdg-session-managementのサポート検討  
  - XWaylandサポートの実装予定  
  - Xfce CIコンテナやビルド環境の更新（mesonでRustビルドを扱えるように）

- 開発状況と参加方法  
  Brian氏は既に作業を開始しており、最初の開発リリースは年央を目標。詳細はissueやWIPソース、Matrixの#xfce-devチャネルで追えます。資金はOpen Collective経由の寄付で賄われています。

## 実践ポイント
- デスクトップユーザー／管理者向け  
  現行のxfwm4からの移行で設定がなるべく維持される予定だが、セッション構成やXWayland周りの挙動差に備えてテスト環境で検証を行うこと。  
- ディストリビュータ／メンテナ向け  
  ビルド環境にmeson＋Rustの対応が必要になるため、CIやパッケージングの準備を早めに始めるとスムーズ。  
- 開発者／貢献者向け  
  smithayとRustの知識が歓迎される。Issueやソースをチェックし、Matrixで議論に参加すると影響力を持てます。  

興味があれば、#xfce-devで議論に参加し、リリースを追ってテストしてみてください。
