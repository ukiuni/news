---
layout: post
title: "Lent and Lisp - レントとリスプ"
date: 2026-03-21T01:39:12.730Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://leancrew.com/all-this/2026/02/lent-and-lisp/"
source_title: "Lent and Lisp - All this"
source_id: 47425257
excerpt: "Lispで500年分の暦を解析し、ラマダン・四旬節・旧正月が重なる稀な日を発見する方法を公開"
image: "https://leancrew.com/all-this/resources/snowman-background.jpg"
---

# Lent and Lisp - レントとリスプ
歴史的祝祭と暦計算をLispで追う──ラマダン、四旬節、旧正月が重なる「奇跡の日」をコードで発見する

## 要約
著者はReingold & DershowitzのCalendrical CalculationsライブラリをCommon Lisp（CLISP）で使い、ラマダン初日、四旬節（Ash Wednesday）、旧正月が一致する日を500年分調べた。元コードの小さな修正と簡潔なスクリプトで、稀な一致日が算出できることを示す。

## この記事を読むべき理由
暦・天文計算はグローバルなサービスや地域対応（国際カレンダー表示、祝日判定、イベント通知）で重要。日本でも旧正月やイスラム暦に関心があるプロダクト開発者やデータ解析者に直接役立つ手法が学べる。

## 詳細解説
- 元ライブラリ: Calendrical Calculations（Reingold & Dershowitz）のLisp実装（calendar.l）。豊富な暦変換と天文関数を含む。
- 問題点: Cambridge版のcalendar.lはパッケージ宣言やexport一覧が先頭にあり、そのままだとCLISPやSBCLで読み込みエラーになるケースがある。簡単な対処でCLISPでは動作させられる（先頭の (in-package "CC4") と (export '(...)) を削除し、calendar.lisp として保存）。
- 実装の要点:
  - 実行環境はCLISPを想定（シバンに -q を使いウェルカムを抑制）。
  - ラマダン初日をイスラム暦の fixed 日付に変換し、gregorian に戻す（fixed/from/absolute の概念に注意）。
  - Ash Wednesday は Easter から46日戻した日（aw = (easter g-year) - 46）。
  - chinese-new-year-on-or-before 関数で旧正月がラマダン前日に来るかを判定。
  - get-decoded-time の複数戻り値、setq/multiple-value-setq の使い方に留意。
- 実行例（出力の一部）: 1799-02-06、1830-02-24、1928-02-22、2026-02-18 が該当。三者一致は稀で、最短の間隔は31年、一般的には98年周期が多い。
- 実行制約: SBCLでは定義順の厳密さにより動かないことがある。CLISPは定義順に寛容で、手早く試せる。

主要な処理の抜粋例（動かす場合は先に編集した calendar.lisp を同じディレクトリへ）:

```lisp
#! /usr/bin/env clisp -q
;; 編集済み Calendrical Calculations を読み込む
(load "calendar.lisp")

;; ラマダン1日 → 固定日 → グレゴリオ年 → Ash Wednesday 判定
(setq f (fixed-from-gregorian (list t-year t-month t-day))
      ti-year (first (islamic-from-fixed f)))
(dotimes (i 500)
  (setq iy (+ (- ti-year 250) i)
        r  (fixed-from-islamic (list iy 9 1))    ; Ramadan 1 の fixed
        g-year (gregorian-year-from-fixed r)
        aw (- (easter g-year) 46))               ; Ash Wednesday
  (when (equal aw r)
    (format t "~a~%" (gregorian-date-string r))))
```

## 実践ポイント
- Calendrical Calculations のLisp版を試すなら、まず元ファイルの先頭(in-package/export)をコメントアウトして calendar.lisp として保存し、CLISPで読み込む。  
- Ash Wednesday 判定は (easter year) から46日引く。ラマダンは fixed ←→ islamic 関数で扱う。  
- get-decoded-time の複数戻り値は multiple-value-setq で受け取る。  
- 日本向け応用例：旧正月を含む国際カレンダー表示、宗教イベントに合わせた通知スケジューリング、祝日データの検証などに即活用できる。  

参考：Reingold & Dershowitz「Calendrical Calculations」を参照すると、さらに高度な天文・暦関数が使える（最新版を入手して関数仕様を確認することを推奨）。
