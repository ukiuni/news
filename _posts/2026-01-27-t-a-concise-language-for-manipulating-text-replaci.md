---
layout: post
title: "t: a concise language for manipulating text, replacing common usage patterns of Unix utilities like grep, sed, cut, awk, sort, and uniq - t：grep/sed/cut/awk/sort/uniq の使用パターンを置き換える簡潔なテキスト操作言語"
date: 2026-01-27T18:38:34.698Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/alecthomas/t"
source_title: "GitHub - alecthomas/t: `t` is a concise language for manipulating text, replacing common usage patterns of Unix utilities like grep, sed, cut, awk, sort, and uniq."
source_id: 929748980
excerpt: "tでgrep/sedを置換、ログやCSV集計が短く高速化し可読性も向上"
image: "https://opengraph.githubassets.com/760aa8b3ec4e5c1a0e29df5ee0235b028b35b04ea9f6bbb4bb88fcc4d3bcbef2/alecthomas/t"
---

# t: a concise language for manipulating text, replacing common usage patterns of Unix utilities like grep, sed, cut, awk, sort, and uniq - t：grep/sed/cut/awk/sort/uniq の使用パターンを置き換える簡潔なテキスト操作言語
シェル芸をもっと短く──新しいテキスト処理言語 t でワンライナーが読みやすく、速くなる理由

## 要約
t は行・配列・ネストを意識した小さな言語で、grep/sed/awk 等の典型的なテキスト処理パイプラインを短く読みやすく置き換えるツールです。

## この記事を読むべき理由
日常的にログ解析やCSV加工、ワンライナー処理を行う日本の開発者や運用エンジニアにとって、コマンドが短く明快になることで作業効率と可読性が大幅に上がります。CI や VS Code の統合ターミナルからも即利用可能です。

## 詳細解説
- データモデル：入力は行の配列。s（split）でネストが生まれ、j（join/flatten）で平坦化。@ でネストに降り、^ で戻る。選択（selection）は配列のサブセットを返すため、スライスや複合選択が容易。
- 演算子群（抜粋）：
  - 変換：l（小文字化）、u（大文字化）、r（正規表現置換）、n（数値化）、t（trim）
  - フィルタ：/regex/（保持）、!/regex/（除外）、x（空削除）
  - 集約・整列：o（降順ソート）、O（昇順）、d（重複集計してカウント）、#（要素数）
  - 構造：s / S<delim>（分割）、j / J<delim>（結合・平坦化）、g（グルーピング）、p（分割）
- 典型例（単語頻度トップ20）
  - 従来（tr|sort|uniq）に相当する処理が、t ではほぼ1要素で表現可能：
  
```bash
bash
t ' sjld:20 ' file
```

  - 内訳：s（行→単語）、j（平坦化）、l（小文字化）、d（重複カウント）、:20（上位20件取得）
- ネスト操作：@ を使えば各行のフィールド操作やカラム操作が直感的。CSVやログ解析でのグルーピング（g）やカラム整形（c）も得意。

## 実践ポイント
- インストール（シンプル）：
  
```bash
bash
curl -fsSL https://raw.githubusercontent.com/alecthomas/t/master/install.sh | sh
```

- まずは手元のログで試す：IPごとのリクエスト集計は t ' sg0 d ' access.log のように短く書ける。
- VS Code での活用：統合ターミナルやタスクでワンライナーを保存しておくと、繰り返し解析が楽。
- 日本語注意点：デフォルトの分割は空白ベース。日本語トークン化が必要なら外部ツールで前処理するか、カスタム区切り（S<delim>）を活用する。
- 学習コツ：まずは s, j, @, d, g, r, l の組合せでよく使うワンライナーを置き換えてみると効果が実感しやすい。

以上を参考に、まずは身近なログやCSVで t を試してみると、短く読みやすいワンライナーの恩恵をすぐに感じられます。
