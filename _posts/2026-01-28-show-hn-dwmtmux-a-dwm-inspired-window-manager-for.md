---
layout: post
title: "Show HN: Dwm.tmux – a dwm-inspired window manager for tmux - dwm風のタイル型ペイン管理をtmuxで実現する「dwm.tmux」"
date: 2026-01-28T14:50:03.356Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/saysjonathan/dwm.tmux"
source_title: "GitHub - saysjonathan/dwm.tmux: dwm-inpsired tiling pane management for tmux"
source_id: 46739704
excerpt: "tmuxでdwm風の大きなメイン＋スタック配置を即導入、ターミナル作業が劇的に速くなる。"
image: "https://opengraph.githubassets.com/28c23ed0e9db4f6deff6543a00b3f4a3b6ebaa029b161959d80ecd7a227c94fd/saysjonathan/dwm.tmux"
---

# Show HN: Dwm.tmux – a dwm-inspired window manager for tmux - dwm風のタイル型ペイン管理をtmuxで実現する「dwm.tmux」
クリックせずにはいられないタイトル：tmuxをdwmの感覚で使い倒す――ターミナル操作が格段に速くなる軽量レイアウト

## 要約
dwm.tmuxは、dwmの「大きなメイン＋右側にスタック」レイアウトをtmux上で再現するシェルスクリプト群。tmuxの操作をタイル型ウィンドウマネージャ風に直感的に扱えます。

## この記事を読むべき理由
リモートサーバ作業やターミナル中心の開発が多い日本のエンジニアにとって、画面管理を効率化することは生産性直結。軽量で設定もシンプルなため、すぐ導入して効果を実感できます。

## 詳細解説
- 必要条件：tmux > 3.2
- インストール（デフォルトは /usr/local プレフィックス）:
```bash
git clone https://github.com/saysjonathan/dwm.tmux.git
cd dwm.tmux
make
# カスタムプレフィックス例
make PREFIX=$HOME
```
- 設定読み込み（~/.tmux.conf に追記）:
```bash
echo 'source-file /usr/local/lib/dwm.tmux' >> $HOME/.tmux.conf
```
- レイアウト概念：左に大きなMainペイン（pane 0）、右に小さなStack（S1,S2,...）。Mainは常に0番。
- 主要コマンド（デフォルトでMeta=Alt/Option想定。環境によってはMetaキー設定が必要）:
  - newpane (Meta-n) : 新しいペインを作りMainに配置
  - newpanecurdir (Meta-w) : 現在のディレクトリで新規ペイン
  - killpane (Meta-c) : ペインを閉じる（Mainならスタック先頭を昇格）
  - movepane[0-9] (Meta-Shift-[0-9]) : ペインを指定ウィンドウへ移動
  - nextpane / prevpane (Meta-j / Meta-k) : ペイン選択（時計回り/反時計回り）
  - rotateccw / rotatecw (Meta-< / Meta->) : ペイン回転
  - layouttile (Meta-t) : レイアウトをリフレッシュ（Main+Stackに戻す）
  - zoom (Meta-Enter) : 選択ペインをMain化
  - float (Meta-Space) : 浮動（フローティング）切替
  - decmfact / incmfact (Meta-h / Meta-l) : Mainサイズ調整
  - window[0-9] (Meta-[0-9]) : ウィンドウ切り替え、他に新規/削除/ポップアップ用コマンドあり
- 調整用環境変数：
  - mfact：Mainペイン比率（%ではなくtmux内部比率）
  - killlast：0以外でウィンドウ内最後のペインもkill可能
- カスタマイズ例（dwm.tmux読み込みの後に追加）:
```bash
# kill last pane even if it's the last
setenv -g killlast 1
# キーバインド変更例
bind -n M-q killpane
bind -n M-t newpanecurdir
```
- ライセンス：MIT。軽量で依存少なめ、既存tmux設定との共存も容易。

## 実践ポイント
- まずはローカルでclone→make→sourceして、tmuxセッションでMetaキー（Alt/Option）を意識して操作してみる。
- 日本語キーボードや端末でMetaが効かない場合は、tmux側で別キーにリマップして試す。
- mfactやkilllastを調整して、自分の作業スタイル（ログ確認重視／編集中中心など）に合わせる。
- リモートサーバやターミナル多用ワークフロー（CIログ監視・デバッグ・ペアプロ）で即効性あり。導入コストが低いので週次のワークフロー改善につなげやすい。
