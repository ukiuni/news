---
layout: post
title: "My Login Shell in Assembly - アセンブリで作った僕のログインシェル"
date: 2026-04-09T23:46:03.494Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://isene.org/2026/04/Bare.html"
source_title: "My Login Shell in Assembly &#8211; Geir's Everything"
source_id: 783262325
excerpt: "起動8μs・依存ゼロのx86_64アセンブリ製対話シェルbareでsyscallを学べ"
---

# My Login Shell in Assembly - アセンブリで作った僕のログインシェル
起動8μs、依存ゼロ。カーネル直結の“裸”シェル bare に触れてみませんか？

## 要約
作者は Ruby → Rust を経て、最終的に x86_64 アセンブリで動く対話型シェル「bare」を作り、126KB・起動8マイクロ秒という極小・極速のシェルを公開しました。

## この記事を読むべき理由
シェルの内部動作や Linux の syscall を学びたい人、ツールの起動速度や依存削減に興味がある人、日本の開発現場での高速化／軽量化のアイデア源として有益です。

## 詳細解説
- アプローチ：作者はまず Ruby（rsh, 4,048 行, 起動 ~300ms）、次に Rust（rush, 4,280 行, 起動 ~26ms）を作り、最終的に x86_64 アセンブリ一ファイル（bare.asm）で実装。結果はバイナリ126KB、起動8µs。
- 依存の排除：libc もランタイムも使わず、すべての操作を生の syscall（read, write, fork, execve, pipe, dup2, wait4, ioctl, getdents64 など）で行う設計。
- 実装の肝：
  - NASM 構文の単一ソースファイルで構築。
  - 端末制御は ioctl(TCSETS) と 60 バイトの termios 構造体を直接扱う。
  - タブ補完は opendir + getdents64 でディレクトリを走査。
  - Git 情報は .git/HEAD を直接読み、.git/index と ref の mtime を比較して「dirty」を判定。
  - 履歴・設定・ジョブ管理は open/read/write/fork/wait4（WUNTRACED）等の syscall ベースで自前実装。
  - ヒープを使わず BSS に静的バッファを確保（カーネルがゼロ初期化する）。
- 機能面：動的プロンプト（git 状態表示）、パイプ/リダイレクト、コマンド置換、ブレース展開、グロブ、エイリアス、タブ補完、Ctrl‑R 履歴検索、シンタックスハイライト、ジョブ制御、テーマ、プラグイン（~/.bare/plugins）、AI プラグイン対応など、一般的なシェルと遜色ない機能を持つ。
- 教訓：生アセンブリで作ることで「シェルが何をしているか」を非常に明確に学べる。SIGTTOU やプロセスグループ、端末所有権、リンク/書き込み先の問題など、実運用で出る罠を直接経験できる。

## 実践ポイント
- リポジトリを試す（ビルドとインストールは自己責任で、仮想環境推奨）：
```bash
git clone https://github.com/isene/bare.git
cd bare
make
sudo make install
```
- 学習用途として：ソース（bare.asm）を追いながら syscall 単位で挙動を確認すると、端末制御・ジョブ制御の理解が深まる。
- 日本の現場での応用例：コンテナや組込みツールの起動コスト削減、開発ツールの最小化、教育用サンプルとして有用。
- 注意点：移植性や保守性は低め。普段使いにするならバックアップのシェルを用意し、まずは非本番環境で試すこと。

元記事に興味がある人はリポジトリを覗いて、実装から Linux の低レイヤを学んでみてください。
