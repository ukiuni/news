---
layout: post
title: "Did you notice the command error exit in the shell? - シェルでコマンドのエラー終了に気づいていますか？"
date: 2026-04-13T13:32:56.197Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://monzool.net/blog/2026/04/10/error-banner-in-shell/"
source_title: "Error banner in shell - Monzool&#039;s Personal Publishing"
source_id: 1296057494
excerpt: "zshでgitコマンドが非0終了したら赤い枠のエラーバナーで即通知する小技"
image: "https://monzool.net/blog/wp-content/uploads/2026/04/guru-1.png"
---

# Did you notice the command error exit in the shell? - シェルでコマンドのエラー終了に気づいていますか？
git失敗を見逃さない。目に留まる「赤いエラーバナー」をシェルに仕込む小技

## 要約
コマンドが非0で終了したときだけ、シェル上に目立つ赤いボックスでエラーを表示するzsh用の小さな仕組み。特にgitコマンドの失敗を見落とさないための工夫。

## この記事を読むべき理由
慌てて作業していると、gitのブランチ作成ミスや他コマンドの失敗を見落としがち。日本の開発現場でも手元のミスがCIや共有ブランチに影響するため、即検知できるUIは有用です。

## 詳細解説
- アイディアはシンプル：直前に実行されたコマンドをフックで捕まえ、次のプロンプト表示時にその終了コードを確認して、失敗（exit != 0）かつ対象コマンド（例：git）なら目立つバナーを表示する。
- zshでは preexec() で直前コマンドを保存し、precmd() で直前コマンドの終了コード（$?）を見て判定するのが一般的。
- 表示はUnicode枠線とzshの色指定（print -P と %F/%K）で作るため、ノイズ少なく確実に目を引く実装になる。
- 元記事は「feature/🔥」のような絵文字付きブランチ名で fatal が出たケースを例に、失敗を見逃した経験からこの仕組みを作っています。

コード（.zshrc に追加）:
```zsh
print_error_box() {
  local msg=" $1 "
  local width=${#msg}
  local border=$(printf '%*s' "$width" '' | tr ' ' '─')
  print -P "%F{red}┌${border}┐%f"
  print -P "%F{red}│%f%K{red}%F{white}${msg}%f%k%F{red}│%f"
  print -P "%F{red}└${border}┘%f"
}

typeset -g LAST_CMD=""
preexec() { LAST_CMD="$1" }

precmd() {
  local exit_code=$?
  if (( exit_code != 0 )) && [[ "$LAST_CMD" == git* ]]; then
    print_error_box "GURU MEDITATION ERROR"
  fi
}
```

## 実践ポイント
- .zshrc に上記を追加して zsh を再読み込みするだけで動作（oh-my-zsh 等のフックと干渉しないか確認）。
- 対象コマンドは git* 以外にも変更可能（例：docker*, make*）。心当たりのエラーを拾うよう調整する。
- チーム運用では「絵文字入りブランチ禁止」や「git switch -c」をルール化すると根本対策に。
- bash では DEBUGトラップと PROMPT_COMMAND を使って同様の仕組みが作れる（実装は少し異なる）。
