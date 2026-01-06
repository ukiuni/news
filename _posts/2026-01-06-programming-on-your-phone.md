---
  layout: post
  title: "Programming on your phone - スマホでプログラミングする方法"
  date: 2026-01-06T00:06:48.502Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://youtu.be/ncLD_SdmkIk?si=GjlPOAVuYf6G7wyp"
  source_title: "Informal introduction to numbers and strings in python - YouTube"
  source_id: 471403858
  excerpt: "スマホだけでPython入門と実用ワークフローを学び、通勤時間にプロトタイプを作る方法を具体解説。"
  image: "https://i.ytimg.com/vi/ncLD_SdmkIk/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AHeA4ACygaKAgwIABABGEggZShhMA8=&amp;rs=AOn4CLDRK_p1Gn4y3T_2usFj_QeLSsrYOA"
---

# Programming on your phone - スマホでプログラミングする方法
スマホ一台で「ちょっと試す」から「実用スクリプト」まで—移動時間が学習と生産性の時間に変わる。

## 要約
スマホ上でのPython入門として、数値（整数・小数）と文字列の基礎、スマホ特有の制約と実用的ワークフローを解説する短いガイド。

## この記事を読むべき理由
通勤・出張・待ち時間が学習の機会に変わる日本では、ノートPCを開けられない場面での実用的な技術が価値を持ちます。スマホでのプログラミングは学習効率を上げ、プロトタイピングや簡単な自動化の導入ハードルを低くします。

## 詳細解説
- 基本概念（数値）
  - Pythonの整数は int、浮動小数点は float。四則演算や剰余、べき乗は通常通り扱える。
  - 例: 10 // 3 は切り捨て除算、10 % 3 は剰余、2 ** 8 はべき乗。
- 基本概念（文字列）
  - 文字列はシングル／ダブルクォートで定義。結合は +、繰り返しは *、長さは len()。
  - f文字列（f"…{var}…") で可読性の高い埋め込みが可能。
  - 文字列はイミュータブルなのでスライスやメソッドで新しい文字列を返す。
- 日本語（UTF-8）とエンコーディング
  - スマホ環境ではUTF-8が標準。日本語処理での問題は少ないが、外部ファイルやAPIとのやり取りでエンコーディング指定を確認すること。
- スマホ特有のポイント
  - エディタ：Pydroid、Termux、QPython、Replitのモバイル等が代表的。簡単なスクリプト実行やREPLで即試せる。
  - 入力性：ソフトウェアキーボードは慣れや外付けキーボードで補う。ショートカットやスニペット機能を活用する。
  - バッテリ・CPU：長時間の重い計算は避け、外部サーバ（SSH）へオフロードするワークフローが現実的。
- ワークフロー例
  - ローカルで小さな実験 → Gitでリポジトリにプッシュ → PCで本格開発。またはSSHでリモートに接続して実行。

## 実践ポイント
- すぐ試せるコード（スマホでも短く試せる）
```python
# python
# 数値
a = 10
b = 3
print(a // b, a % b, a / b, 2 ** 8)

# 文字列（日本語対応）
name = "太郎"
msg = f"こんにちは、{name}さん！"
print(msg.upper(), len(msg))
```
- 推奨アプリ：Pydroid（学習向けGUI）、Termux（端末＋パッケージ管理）、Replit（クラウドREPL）。
- 日本向けの注意：ファイル入出力でShift_JISに出力するサービスがあるなら明示的にエンコーディングを指定する（例: open("file.csv","w",encoding="shift_jis")）。
- 生産性向上のコツ：スニペットを作る、外付けキーボードやトラックパッドを検討、Git連携やSSHでリソースを使い分ける。

短時間で学べてすぐ使えるのがスマホ開発の強み。まずは移動時間の5分で上のコードをREPLで動かしてみてください。
