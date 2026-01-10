---
layout: post
title: "flow - a keyboard-first Kanban board in the terminal - ターミナルで動くキーボードファーストなカンバン「flow」"
date: 2026-01-10T22:15:32.619Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jsubroto/flow"
source_title: "GitHub - jsubroto/flow: A keyboard-first Kanban board in your terminal"
source_id: 466099998
excerpt: "ターミナルでvim風キーだけでカード操作、Git管理もできる軽量Kanbanを試したくなる"
image: "https://opengraph.githubassets.com/6d0fd3c51d8db67caafaa10b564c06c7f5012348da6e17ef014afcc789c70709/jsubroto/flow"
---

# flow - a keyboard-first Kanban board in the terminal - ターミナルで動くキーボードファーストなカンバン「flow」
「ブラウザを開かず、キーひとつでカードを動かす」──集中したままタスクをさくっと整理したくなる人向けのミニマルなターミナルKanban。

## 要約
flowはRust製の軽量なターミナル向けカンバン。キーボード中心の操作でカード移動・表示ができ、ボードは平文ファイルで保存されるため手元で簡単に編集・バージョン管理できる。

## この記事を読むべき理由
- ブラウザ頼みのタスク管理に疲れている開発者／エンジニアにとって、集中を切らさずに操作できる代替手段になる。  
- VS Codeの統合ターミナルやWSL環境で気軽に使え、ファイルベースなのでGitでチーム共有や差分管理がしやすい。

## 詳細解説
flowの設計は「キーボード操作」と「ファイルベースの永続化」に重点を置いています。主なポイントは以下。

- 操作体系：hjklまたは矢印で移動、Enterでカードの説明表示、H/Lでカードを左右（列間）に移動。ほぼvimライクな操作でターミナル慣れした人には直感的です。  
- ボード保存形式：boardsディレクトリ配下のテキスト/Markdownファイルで管理。例：
  - board.txt — カラムの定義と順序
  - cols/<column>/order.txt — そのカラム内のカードID順
  - cols/<column>/<ID>.md — カード本文（Markdown）  
  この構成は人間が編集可能で、差分（git）に強く、部分的な修正に耐えます。
- モードと永続化：デフォルトはdemoモード（boards/demo）。ローカル永続化を有効にするには環境変数でプロバイダを指定します。
  - FLOW_PROVIDER=local でローカルモード
  - デフォルトのローカル保存先: ~/.config/flow/boards/default
  - カスタムパスは FLOW_BOARD_PATH=/path/to/board
- 実行：ソースはRust/Cargoプロジェクト。開発環境で試すには `cargo run` を使用。移動操作はローカルで即時永続化されます。
- 技術スタック：Rustで実装（ターミナルUIはratatui等を利用）。軽量かつネイティブな見た目・操作感を重視。

注意点：まだ初期段階のプロジェクトで機能追加や破壊的変更の可能性あり。拡張性より操作体験とファイル永続性に重きを置く設計です。

## 実践ポイント
- まず触る：リポジトリをクローンしてdemoで起動。
```bash
# リポジトリをクローンしてデモ実行
git clone https://github.com/jsubroto/flow.git
cd flow
cargo run
```
- ローカルで使う：自分のボードを使うなら環境変数をセット。
```bash
FLOW_PROVIDER=local cargo run
# カスタムボードを指定する場合
FLOW_BOARD_PATH=~/myboards/project1 cargo run
```
- ファイル編集でカスタマイズ：VS Codeなどで cols/<column>/<ID>.md を直接編集すれば即反映（reload可能）。Gitで管理すると履歴や差分が追いやすい。  
- チーム運用のヒント：共有リポジトリにboardsディレクトリを置き、pull/pushで軽いタスク共有。CLI好きなメンバーにとっては導入障壁が低い。  
- 統合案：VS Codeのターミナルで常時起動させるか、tmux/paneで運用するとIDEワークフローを崩さずに使える。

短く言えば、flowは「最小限の操作でタスクを動かしたい」エンジニア向けのツール。ターミナル中心のワークフローを好む日本の個人開発者や小規模チームには試す価値が高いです。
