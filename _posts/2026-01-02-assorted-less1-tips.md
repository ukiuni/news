---
  layout: post
  title: "Assorted less(1) tips - less(1) の雑多な小技集"
  date: 2026-01-02T13:06:20.803Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://blog.thechases.com/posts/assorted-less-tips/"
  source_title: "Assorted less(1) tips | Tim's blog"
  source_id: 1094105101
  excerpt: "lessの小技でログ検索・絞り込みやブックマークが劇的に捗る"
  ---

# Assorted less(1) tips - less(1) の雑多な小技集
lessが手放せなくなる、実践に効く小技だけを厳選したガイド

## 要約
lessは単なるページャー以上の道具で、複数ファイル操作、柔軟な検索・フィルタ、ブックマーク、画面内オプション切替などでログ確認や長時間実行の出力確認が劇的に楽になる。

## この記事を読むべき理由
大きなログやソースを素早く読み回す作業は日本のエンジニアでも日常的。再実行に時間がかかるコマンド出力やリモート環境での調査で、lessの小技を知っているか否かで生産性が大きく変わります。

## 詳細解説
- 起動方法
  - パイプの末尾: command | less
  - 直接ファイル指定: less README.md src.c *.log
- 起動後にファイル追加
  - :e file.h で引数リストに追加
  - :n / :p で次・前へ、:x で先頭へ戻る、:d で現在ファイルを引数リストから削除
- ジャンプ
  - 行番号へ: 3141G で 3141 行目へ
  - 位置へ: 75% でファイルの 75% へ
- 高度な検索
  - /pattern, ?pattern（後方検索）、n / N で次/前
  - 修飾子: ! 次に合致しない行、* 複数ファイル検索、@ 先頭ファイルから、@* 先頭から複数ファイル
    - 例: /@*pattern は最初のファイルから全体を検索
- 行の絞り込み（内部grep）
  - &pattern で表示行を絞る（patternにマッチする行のみ）
  - &!pattern でマッチしない行のみ表示（ログ調査に便利）
- ブックマーク
  - m<letter> でマーク、'<letter> でジャンプ（ファイル跨ぎで有効）
- 括弧対応ジャンプ
  - 画面先頭に開き括弧ならそれを押すと対応閉じ括弧にジャンプ（逆も可）
  - カスタムペアは Alt+Ctrl+f / Alt+Ctrl+b で定義
- オプションの切替
  - lessを終了せずに -S（行折り返しOFF）や -R（ANSI色表示）などをその場で切替可能（入力例: -S）
  - よく使うオプションは環境変数 $LESS に入れる（例: LESS="-RNe"）
- 外部コマンド実行
  - !date や !bc のように外部コマンドを実行可能
- その他
  - v で $VISUAL エディタを起動（現在のファイルを開く）
  - o / O で stdin からの収集内容をファイルに追記/上書き出力

## 実践ポイント
まずはすぐ使えるコマンドを数個覚えるだけで差が出ます。
```bash
# 色付きログを行番号付きで読む
LESS="-RNe" less server.log

# ログ内でerrorだけを表示
&error

# 全ファイルの先頭から"timeout"を検索
/@*timeout

# ヘッダファイルを作業中の less に追加
:e include/foo.h

# 重要箇所にブックマーク（例: o, e）
mo   # mark 'o'
me   # mark 'e'
'o   # jump to 'o'

# その場で長行折り返しを切り替え
-S
```
短時間で効率化したければ、「&（フィルタ）」「/@*（全ファイル検索）」「-S（その場で行折り返し切替）」の3つをまず試してみてください。

## 引用元
- タイトル: Assorted less(1) tips
- URL: https://blog.thechases.com/posts/assorted-less-tips/
