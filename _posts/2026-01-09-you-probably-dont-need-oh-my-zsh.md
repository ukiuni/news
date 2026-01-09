---
layout: post
title: "You probably don't need Oh My Zsh - おそらくあなたは Oh My Zsh を必要としていない"
date: 2026-01-09T14:28:44.144Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rushter.com/blog/zsh-shell/"
source_title: "You probably don&#39;t need Oh My Zsh | Artem Golubin"
source_id: 468382426
excerpt: "Oh My Zshをやめ、starship＋fzfで起動を高速化しターミナルの1秒を取り戻す"
image: "https://rushter.com/static/uploads/img/2026/zsh.png"
---

# You probably don't need Oh My Zsh - おそらくあなたは Oh My Zsh を必要としていない
Oh My Zshを捨ててターミナルの「1秒」を取り戻すミニマルZsh入門

## 要約
Oh My Zsh（OMZ）は便利だが起動時に余計なスクリプトを読み込むためシェルの起動が遅くなる。最小限の設定＋starship＋fzfで軽く速く、必要な機能は自前で追加するのが賢い。

## この記事を読むべき理由
VSCodeの統合ターミナルやMac/Linuxの普段使いで、毎回の「新しいタブ」が体感で遅いと感じているなら必見。日本の開発現場（クラウドやコンテナ、多言語プロジェクト）でも反応速度は生産性に直結します。

## 詳細解説
- 問題点：OMZは大量のシェルスクリプトで構成されており、ターミナルを開くたびにそれらを解釈するため起動時間が伸びる。更新チェックや多くのプラグインも起動コストを増やす。
- 最小構成の考え方：まずは必要最小限を使い、足りない機能だけを手動で追加する。Zsh自体の補完や履歴機能は標準で強力。
- スタートアップ測定：起動時間は次のコマンドで測れる（Linux/macOS）。
```bash
/usr/bin/time -f "%e seconds" zsh -i -c exit 0
```
- 代替プロンプト：starshipは単一バイナリで高速。多言語、仮想環境、git状況などを軽く表示でき、OMZの多くのプラグインを代替する。
- 履歴検索：zsh-autosuggestionsが好みでない人は、fzfでCtrl+Rに割り当てると対話的で取り回しが良い。
- 追加の便利設定：viモードや拡張履歴（タイムスタンプ）など、小さな設定で効率が上がる。

技術的ポイント（抜粋実装例）：
- 最小の.zshrc例
```zsh
export HISTSIZE=1000000
export SAVEHIST=$HISTSIZE
setopt EXTENDED_HISTORY
setopt autocd
autoload -U compinit; compinit
```
- starship の有効化（.zshrcに追加）
```bash
eval "$(starship init zsh)"
```
- starship の一例設定（~/.config/starship.toml）
```toml
# toml
[aws]
disabled = true

[nodejs]
disabled = true

[character]
success_symbol = '[➜](bold green)'

[cmd_duration]
min_time = 500
format = 'underwent [$duration](bold yellow)'
```
- fzf を使った履歴検索（.zshrcに追加）
```zsh
source <(fzf --completion)  # fzf の zsh サポートが入っている場合
# または Ctrl+R にバインドする簡易例（fzf がインストール済みであること）
bindkey '^R' fzf-history-widget
```
- vi モード（好みで）
```zsh
set -o vi
bindkey -v '^?' backward-delete-char   # バックスペースの調整
```

効果の目安：OMZデフォルトで ~0.3–1.0秒かかっていた起動が、ミニマル構成＋starship＋fzfで 0.07秒 程度まで短縮できる例がある（環境依存）。

## 実践ポイント
- 1) まず計測：/usr/bin/time コマンドで現在の起動時間を計る。
- 2) 最小構成に置き換える：まずは上の最小 .zshrc を試す。補完は compinit で十分。
- 3) プロンプトは starship に一本化：設定は細かく無効化して表示ノイズを減らす（クラウド系は不要なら無効化）。
- 4) 履歴検索は fzf と Ctrl+R：視認性が高く誤入力も減る。
- 5) 必要なプラグインだけ手動追加：頻繁に更新されるサードパーティコードを自動で毎回読み込まない。
- 6) VSCode統合ターミナルやリモート環境でも同様に効果あり。特にWSLやsshでの短いセッションで効果を実感しやすい。

まとめ：まずはシンプルに戻して、体感で遅い部分だけを段階的に足していく。OMZは便利だが「全部入り」を使う前に、本当に必要かを問い直す価値は十分にあります。
