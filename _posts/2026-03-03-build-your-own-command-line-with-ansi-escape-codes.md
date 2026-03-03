---
layout: post
title: "Build your own Command Line with ANSI escape codes - ANSIエスケープコードで自作コマンドラインを作る"
date: 2026-03-03T12:00:37.298Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html"
source_title: "Build your own Command Line with ANSI escape codes"
source_id: 392020300
excerpt: "ANSIエスケープで端末を動的なCLIとリッチ表示に変える方法をPython例で実践解説"
---

# Build your own Command Line with ANSI escape codes - ANSIエスケープコードで自作コマンドラインを作る
端末が一瞬でリッチUIに変わる！ANSIエスケープで作る動くプログレス＆自作コマンドライン入門

## 要約
端末はただのテキスト出力場所ではなく、ANSIエスケープコードを使えば色付け・カーソル移動・画面消去などで動的なUIを作れます。この記事はその基本と、Pythonでの実装例をやさしく説明します。

## この記事を読むべき理由
Gitのプログレスやターミナル型ツールのUIは、ANSI制御で実現されています。日本でもCLIツールやバッチ処理を作る場面は多く、ちょっとした演出でユーザビリティやデバッグ効率がぐっと上がります。

## 詳細解説
- エスケープ開始文字は ESC（\u001b）。これに続くコードで端末に命令を送る。
- テキスト装飾
  - 色（8色）: 例）赤 = \u001b[31m、リセット = \u001b[0m。色を出したら必ずリセットする。
  - 明るい色（16色）: コードに ;1 を追加（例：\u001b[31;1m）。
  - 256色: \u001b[38;5;{ID}m（前景）、背景は48;5;{ID}m。
  - 装飾: 太字 \u001b[1m、下線 \u001b[4m、反転 \u001b[7m。
- カーソル制御（動的表示の肝）
  - 上: \u001b[{n}A、下: \u001b[{n}B、右: \u001b[{n}C、左: \u001b[{n}D
  - 行先頭に戻す方法（多く使う）: 大きめの左移動例 \u001b[1000D を出して上書きする。
  - これでプログレス表示や複数行の更新が可能。最初に空行を確保しておくのが実装上のコツ。
- 応用例
  - 進捗％やASCIIバーを同一行で更新（上書き）、複数バーは「下に空行を確保 → 毎回上に移動して再描画」。
  - 自作REPLは、カーソル移動と削除を組み合わせれば簡単な編集機能を実装できる（ただし既存の Readline / Prompt Toolkit の利用も検討）。

動作環境の注意: 多くのUnix系（Linux, macOS）端末で動作。Windowsはバージョンや端末によって挙動が異なるため要確認。

簡単なPython例:
```python
# python
print("\u001b[31mHello World\u001b[0m")  # 赤で表示してリセット

import sys, time
for i in range(1, 101):
    sys.stdout.write("\u001b[1000D" + str(i) + "%")  # 行頭へ寄せて上書き
    sys.stdout.flush()
    time.sleep(0.02)
print()
```

## 実践ポイント
- 色を使うときは必ず \u001b[0m でリセットする。
- 可搬性を考え、まずは macOS / Ubuntu で動作確認する（Windowsは別途検証）。
- 「上書き表示」は大きめの左移動→新描画、または行単位でカーソル移動して再描画する。
- 本番用途は Readline/JLine/Prompt Toolkit 等の成熟ライブラリを検討。学びや小ツール作成には生のANSIを試すと理解が深まる。
- ターミナル幅・エンコーディングに注意して表示崩れを防ぐ。

（元記事：Haoyi — "Build your own Command Line with ANSI escape codes"）
