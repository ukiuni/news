---
layout: post
title: "kip: A programming language based on grammatical cases of Turkish - トルコ語の格を型にしたプログラミング言語「Kip」"
date: 2026-01-17T09:45:22.238Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/joom/kip"
source_title: "GitHub - joom/kip: A programming language based on grammatical cases of Turkish."
source_id: 951988538
excerpt: "母音調和と格接尾辞で引数役割を型化し、順序自由な文法的関数呼び出しを実現するKip"
image: "https://opengraph.githubassets.com/e547f81cc9cd9f1ee45477e6775b774015239c1d30c6f654a5b95624c6ddc4bb/joom/kip"
---

# kip: A programming language based on grammatical cases of Turkish - トルコ語の格を型にしたプログラミング言語「Kip」
トルコ語の「格（case）」で関係を型付けする実験言語――自然言語の形態論を型システムに取り込んだ面白い試みを日本語でわかりやすく紹介します。

## 要約
Kipはトルコ語の名詞格（格接尾辞）と母音調和を型システムに使う研究/教育用プログラミング言語です。形態素解析器（TRmorph／Foma）を使い、語尾で引数の役割を決められるため、柔軟な引数順や自然言語に近い表記が可能になります。

## この記事を読むべき理由
- 日本語話者に馴染みのある「助詞で関係を示す」感覚と親和性が高く、言語設計の直感的な例になっているから。  
- 自然言語処理（形態論）と型理論を結ぶインパクトある実験例として、コンパイラやDSL設計、ローカライゼーション／言語資源活用のヒントが得られます。  

## 詳細解説
- 基本アイデア  
  Kipはトルコ語の名詞格（例：主格＝無接辞、対格 -i、与格 -e、場所 -de、起点 -den、属格 -in、具格 -le など）を「引数の役割を示す型」として扱います。語形変化（母音調和）や接尾辞の形を解析して、どの引数がどのパラメータに対応するかを決めます。

- 代表的な言語機能
  - 格を使った関数呼び出し：接尾辞で役割が分かるため、引数順を柔軟にできる（例: (5'le 3'ün farkını) yaz. と (3'ün 5'le farkını) yaz. は同等）。  
  - 代数的データ型、多相型、パターンマッチ（条件接尾辞 -sa/-se で分岐）。  
  - 効果と入出力は接尾辞 -ip/-ıp/-up/-üp と binding のための olarak で表現。  
  - 組み込みで整数、文字列、リストなど。例としてフィボナッチや自然数の加算がREADMEにある簡潔なサンプルで示されています。  

- 実装の技術スタック
  - 実装は主に Haskell（Stack）で、形態素解析は TRmorph（Foma）を利用。Foma は有限状態形態素解析器で、trmorph.fst が付属しています。  
  - 解析で曖昧さがある語（複数解析候補）はパーサが候補を保持し、型検査フェーズで解決します。意図的な曖昧さはアポストロフィで強制的に指定可能（taka'sı 等）。  
  - コンパイル結果は .iz というキャッシュ（型チェック済みバイトコード）として保存され、コンパイラのハッシュが変わると自動無効化されます。

- なぜ面白いか（理論的・実務的な観点）
  - 自然言語の形態論（接尾辞や母音調和）を型システムに組み込む設計は、言語学とプログラミング言語理論の交差点にあり、型の表現力を拡張するヒントになります。  
  - 日本語は助詞で文法的役割を示す点で類似性があり、日本語話者にとって概念の応用やローカライズの示唆が得られます（ただし日本語の解析手法は異なります）。

## 実践ポイント
- 試してみる（ローカルで動かす手順）
  ```bash
  # 依存: foma, Stack が必要
  chmod +x install.sh
  ./install.sh
  # REPL を起動
  stack exec kip
  # ファイル実行
  stack exec kip -- --exec path/to/file.kip
  ```
- 注目すべきソース（学習に便利）
  - src/Kip/TypeCheck.hs — 格の使用を検証する型検査器  
  - src/Kip/Render.hs — 形態素変化を反映する整形処理  
  - src/Language/Foma.hs — Haskell ⇄ Foma（TRmorph）連携コード  
  - vendor/trmorph.fst — 形態素トランスデューサ本体  
- アイデア応用のヒント
  - 自然言語の格や助詞を利用したDSL設計（日本語助詞を入力シンタックスに使う小さなDSLなど）を試してみる。  
  - 形態素解析器（Foma/TRmorph）とコンパイラの組み合わせは、形態論的に豊かな言語を扱う際の実践的アプローチになる。  
  - .iz のキャッシュ設計は、開発中の反復を速くする仕組みとして参考になる。  
- さらに読み進めるべき箇所
  - README の example プログラムや tests フォルダで実際のコード／入出力を確認すること。学習コストは低めで、言語設計の直感を掴みやすいです。

興味が湧いたらまずREPLを立ち上げて例を動かし、src 以下の TypeCheck/Render の仕組みを覗いてみてください。トルコ語の格という「自然言語的な型」が、言語設計にどんな新しい視点を与えるかが手に取るように分かります。
