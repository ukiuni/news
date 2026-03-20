---
layout: post
title: "We rewrote our Rust WASM Parser in TypeScript – and it got 3x Faster - Rust製WASMパーサをTypeScriptへ書き直したら3倍速くなった"
date: 2026-03-20T22:26:18.075Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.openui.com/blog/rust-wasm-parser"
source_title: "Rewriting our Rust WASM Parser in TypeScript | OpenUI"
source_id: 47461094
excerpt: "境界コスト削減とインクリメンタル化でWASM→TSパーサが3倍高速化"
image: "https://www.openui.com/meta-image.png"
---

# We rewrote our Rust WASM Parser in TypeScript – and it got 3x Faster - Rust製WASMパーサをTypeScriptへ書き直したら3倍速くなった
WASMの“速さ”は本当に正解？境界コストとアルゴリズム最適化が効いた驚きの実践レポート

## 要約
Rust→WASMで動かしていたストリーミングDSLパーサをTypeScriptへ移植したら、1回あたりで最大4.6x、ストリーミング全体では最大3.3xの高速化を達成した。原因は「WASM/JSの境界コスト」と「ストリーミング時のアルゴリズム的非効率」。

## この記事を読むべき理由
LLM出力をリアルタイムにレンダリングするWebアプリ（チャットUIやコンポーネント生成など）は日本でも急増中。短いチャンクを何度も処理するケースでは、言語選択よりも「境界の扱い」と「インクリメンタル処理設計」がUXに直結します。本記事はその実例と対処法を初心者向けに整理します。

## 詳細解説
- パーサの構成（6段階）
  - autocloser → lexer → splitter → parser → resolver → mapper → ParseResult  
    （部分テキストを文法的に補正→字句解析→文ごとに切る→AST生成→参照解決→公開フォーマットへ）

- WASM境界でのコスト（WASM Boundary Tax）
  - 従来フロー：JS文字列をWASMにコピー（malloc + memcpy）→Rustで解析→結果をserde_jsonで文字列化→文字列をJSへコピー→V8がJSON.parseで復元  
  - つまり「コピー + シリアライズ／デシリアライズ」が毎呼び出しで発生。Rustの解析自体は速くても境界で時間を食う。

- serde-wasm-bindgenで直接JsValueを返す試み
  - 一見有効に見えるが、実行は遅く（約+9〜29%）、理由は「Rustのデータ構造をフィールド単位でJSオブジェクトに逐一変換」する細かい境界クロスが多発するため。対してJSON方式はRust内で完全に文字列化→1回のコピー→V8のC++最適化で高速。

- 本当の解決策：TypeScriptへ全面移植
  - 同一の6段構成をV8ヒープ上で動作させ、境界を除去。結果（one-shot parse, 中央値, µs, 1000回）
    - simple-table: TS 9.3 vs WASM 20.5 → 2.2x  
    - contact-form: TS 13.4 vs WASM 61.4 → 4.6x  
    - dashboard: TS 19.4 vs WASM 57.9 → 3.0x

- さらに出てきたアルゴリズムの落とし穴：O(N²)なストリーミング
  - 問題：LLMの各チャンク到着ごとに累積テキスト全体を再パースすると、チャンク数に対して二乗的にコストが増える（例：1000文字を20文字ずつで送ると総処理量が大きく膨らむ）。
  - 改善：ステートメント単位で確定した文をキャッシュする「ステートメントレベルのインクリメンタルキャッシュ」を導入。確定文は再パース不要、未確定末尾だけ毎回処理する設計にしてO(N)へ。
  - 実測（全ストリーム合計時間、中央値）
    - contact-form: Naïve TS 316µs → Incremental TS 122µs（2.6x）  
    - dashboard: Naïve TS 840µs → Incremental TS 255µs（3.3x）

- 要点まとめ
  - 境界の「少ない大きな操作」は「多数の小さな操作」より勝つ（JSONの一括コピー vs 細かなJsValue構築）。
  - 言語選択前にプロファイリング：計算が重いか、境界越えが多いかで選ぶべき技術が変わる。
  - アルゴリズム的改善（O(N²)→O(N)）が言語最適化より効果的なケースが多い。

## 実践ポイント
- まず計測：どこで時間が消費されているか（計算、メモリコピー、シリアライズ等）をプロファイルする。  
- 頻繁に短い呼び出しを行う処理は、同一ヒープ（V8）で動かす方が有利なことが多い。WASMは「大きな入力→小さな出力／インプレース変換」に向く。  
- ストリーミング処理では「確定部分のキャッシュ」と「未確定部分だけ再処理」するインクリメンタル設計を採ると劇的に総コスト削減できる。  
- serde-wasm-bindgenの「直接返却」は万能ではない：内部で細かな境界変換が発生している点に注意する。  
- 日本のWebアプリ／チャットUI開発では、リアルタイム性とJIT最適化が効くV8の恩恵を活かす設計を検討すると良い（ユーザー体感の改善に直結します）。

元記事の要点を把握し、まずは自分のケースで「どのコストがボトルネックか」を確かめてください。
