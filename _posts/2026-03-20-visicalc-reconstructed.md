---
layout: post
title: "VisiCalc Reconstructed - VisiCalc 再構築"
date: 2026-03-20T16:08:35.129Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://zserge.com/posts/visicalc/"
source_title: "VisiCalc reconstructed"
source_id: 47410871
excerpt: "数千行の最小C実装でVisiCalcを再構築、式解析・再計算・TUIを解説"
image: "https://zserge.com/logo.png"
---

# VisiCalc Reconstructed - VisiCalc 再構築
たった数千行で蘇る伝説のスプレッドシート —— VisiCalc を再構築して学ぶミニマル実装

## 要約
元記事は、1979年の名作 VisiCalc を最小限の C コードで再構築する手順を示す。データモデル、再帰下降パーサ、単純な再計算ロジック、ncurses ベースの TUI を組み合わせ、実用的かつ学習しやすいスプレッドシート実装を紹介する。

## この記事を読むべき理由
VisiCalc は「パーソナルコンピュータを仕事道具に変えた」歴史的アプリで、その設計は今なお学ぶ価値がある。日本のエンジニアや学習者にとって、極小実装を追うことは UX 設計、言語処理（パーサ）、リアクティブ計算の基礎を理解する最短ルートになる。

## 詳細解説
- 基本コンポーネント
  - セルは「EMPTY / NUM / LABEL / FORMULA」といった型、数値 val、入力テキスト text を持つ。グリッドは固定列×行の配列。
  - 例（簡略化）:
    ```c
    // C
    #define MAXIN 128
    enum { EMPTY, NUM, LABEL, FORMULA };
    struct cell { int type; float val; char text[MAXIN]; };
    #define NCOL 26
    #define NROW 50
    struct grid { struct cell cells[NCOL][NROW]; int cc, cr, vc, vr; };
    ```

- 式パーサ（再帰下降）
  - 文法は典型的な優先順位付き（expr -> term ('+'|'-' term)*, term -> primary ('*'|'/' primary)*）。
  - primary は数値・セル参照・関数呼び出し・括弧を扱う。VisiCalc では式の先頭に '+' を使うことがある点に注意。
  - セル参照は "A1"/"AB12" のように列文字列→数値、行番号→0ベースで解析する。

- 関数と範囲
  - @SUM(A1...C3) のような範囲集計や、@ABS/@INT/@SQRT 等の単一引数関数を実装。
  - 範囲走査でセル値を取得し集計するロジックを用意する。

- 再計算（リアクティブではなく反復）
  - 完全な依存グラフを構築する代わりに、セル更新時にグリッド全体を何度か反復して再評価する方法（最大パス数を上限にループし、変化がなくなるまで続ける）。
  - シンプルでメモリ効率が良く、古いマシン向け設計の思想を現代でも活かせる。

- 入力判定と setcell
  - 入力先頭文字で LABEL/NUM/FORMULA を判定し、セルに書き込み後に recalc() を呼ぶ。
  - 例: 先頭が '+', '-', '(', '@' → FORMULA、数値にパースできれば NUM、それ以外は LABEL。

- TUI（ncurses）
  - 画面はステータスバー、編集行、列ヘッダ、セルグリッドの 4 領域で構成。ビューポートを使って画面サイズに合わせスクロールする。
  - モードは READY / ENTRY / GOTO。コマンド（/B: blank, /Q: quit, /F: format）や Enter/Tab による編集確定と移動をサポート。
  - 現セルを反転表示し、数値は右寄せ、ラベルは左寄せ、エラーは "ERROR" 表示。

- エラーハンドリング
  - 計算エラーは NaN を使って伝播させる。これにより数式評価中の不正が後続計算へ自然に届く。

## 実践ポイント
- 小さく始める：まずは NCOL=4,NROW=8 などでセル構造と parser を実装して動作確認する。
- パーサは再帰下降で書くと理解しやすい。primary/term/expr の順で実装し、セル参照と関数呼び出しを追加する。
- 再計算は最初は全体反復で十分。後で実測プロファイルを取り、必要なら依存グラフに切替える。
- UI はまずコンソール（ncurses）で十分。慣れたら Web（React）や GUI に移植して学びを活かす。
- 単体テストを用意する：セル参照・範囲・関数・再計算の変化を自動テストでカバーすると安心。

この再構築は「少ないコードで動く仕組み」を学ぶ良い教材になる。歴史的名作の設計から、現代の小規模プロジェクトで使える実践知が得られる。
