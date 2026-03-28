---
layout: post
title: "BubbleWrap your dev env and agents - 開発環境とエージェントをBubbleWrapで隔離"
date: 2026-03-28T20:28:02.824Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dpc.pw/posts/bubblewrap-your-dev-env-and-agents/"
source_title: "BubbleWrap your dev env and agents"
source_id: 894296038
excerpt: "bwrapで開発環境をほぼ透過的に隔離し、LLM暴走の被害を最小化"
---

# BubbleWrap your dev env and agents - 開発環境とエージェントをBubbleWrapで隔離
代理が暴走しても被害最小。BubbleWrapで「ほぼ透過」な軽量サンドボックス運用術

## 要約
BubbleWrap（bwrap）でホームやシステムの大部分を読み取り専用で再マウントし、LLMエージェントや外部ツールを「ほぼ同じUX」のまま限定実行する手法を紹介します。

## この記事を読むべき理由
LLMエージェントやサードパーティ依存が増える中、仮想マシンやコンテナを使わずに軽量かつ実用的な隔離を導入できる手法は、開発効率を落とさずセキュリティを向上させたい日本のエンジニアに有益です。

## 詳細解説
- 考え方
  - 目標は「システム保護」「悪意のある依存からの防御」「普段の開発体験を変えないこと」。
  - 完全分離（VMや別アカウント）ではなく、bwrapで必要最小限だけ書き込み可能にして残りをread-onlyにする。
- 実装の肝
  - bwrapを使い、/bin /usr/bin /etc 等を--ro-bindで読み取り専用マウント、作業ディレクトリのみ書き込み可にする。
  - /tmp /run は --tmpfs にして一時領域をクリーンに保つ。
  - 必要なソケット（SSH, GPG, YubiKey など）は明示的に bind して渡す。ハードウェア認証が必要な場合は例外的に許可する。
  - プロジェクト単位で追加バインドを与えるために ISOLATE_EXTRA_CONFIG（.isolate）を使う仕組み。
- 運用例（Nixとの組み合わせ）
  - エージェント（例: Claude/Slopus）をラッパーで常に isolate 経由で起動するよう flake に登録。
  - tmux の default-command を auto-isolate に差し替え、作業ディレクトリに .isolate があれば自動で隔離環境に入る運用。
- GUI対応
  - Wayland/X11、GPUデバイス、/dev/dri 等をプロジェクト側で追加バインドすれば、UIアプリも表示可能。
- 注意点
  - どのパスをread-only/bindするかは慎重に検討すること。過剰に許可すると意味が薄れる。
  - TIOCSTI 等カーネル設定や治安設定の有無をチェックする（記事でも警告あり）。

## 実践ポイント
- 必要ツール: bubblewrap をインストール（ディストリで bwrap パッケージ）。
- 簡易 auto-isolate 起動ラッパー（例）:
```bash
#!/usr/bin/env bash
# bash
if [[ -f "$(pwd)/.isolate" ]]; then
  ISOLATE_EXTRA_CONFIG="$(pwd)/.isolate" exec ~/bin/isolate "$@"
else
  exec "$@"
fi
```
- tmux に組み込む（~/.config/tmux/tmux.conf）:
```bash
# bash
set-option -g default-command "$HOME/bin/auto-isolate ${SHELL}"
```
- プロジェクトごとの .isolate で追加バインド（例: Wayland / GPU）を定義する。
- まずは非破壊で試す：読み取り専用バインド中心で動作確認し、必要に応じて個別にbindを追加する。

以上を取り入れれば、LLMエージェントや怪しい依存が暴走しても被害を限定しつつ、普段通りの開発体験をほぼ維持できます。
