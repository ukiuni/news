---
layout: post
title: "Lindenmayer.jl: Defining recursive patterns in Julia - Lindenmayer.jl：Juliaで再帰パターンを定義する"
date: 2026-02-20T04:53:01.682Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cormullion.github.io/Lindenmayer.jl/stable/"
source_title: "Lindenmayer.jl · Lindenmayer"
source_id: 47035698
excerpt: "JuliaでL-Systemを使いタートル描画で植物的フラクタルを即座に生成、独自描画も挿入可能"
---

# Lindenmayer.jl: Defining recursive patterns in Julia - Lindenmayer.jl：Juliaで再帰パターンを定義する
魅せるコードで育てる「植物的」フラクタル — Juliaで遊ぶ生成アート入門

## 要約
Lindenmayer.jlはL-System（Lindenmayer system）を扱うJuliaパッケージで、再帰的な文字列置換ルールからタートル描画（Luxor.jl）を生成し、フラクタルや植物的な成長パターンを簡単に描けます。

## この記事を読むべき理由
- 生成アートやプロシージャルコンテンツが注目される今、L-Systemはゲーム・可視化・教育用途で即戦力になる技術です。  
- Juliaで手軽に試せる実装があるため、数式よりも「ルールを書く」ことで視覚結果を得たい日本のエンジニア／デザイナーに最適です。

## 詳細解説
- 基本概念：L-Systemは「文字列の検索と置換ルール」と「初期状態（Axiom）」を繰り返すことで自己相似な指示列を生成します。生成された文字列は「タートル命令」として解釈され、線分や回転、色・太さの変更などの描画操作になります。  
- Lindenmayer.jlの構成：LSystem構造体はルール（DictやVector）、初期状態、評価後のstate（内部命令列）を持ちます。描画は主に drawLSystem() を使いますが、evaluate()→render() の分離でカスタムワークフローにも対応します。  
- 主要命令例：F/G = 前進、+ / - = 回転（角度は評価時に指定）、数字 = 線幅、t/T = 色相操作、[ / ] = 状態のプッシュ/ポップ、* = 外部関数呼び出し（asteriskfunction）。命令一覧は豊富で、独自のプレースホルダ文字も使えます。  
- asteriskfunction：ルール内の * により外部関数（Turtleを受け取る）を呼べます。ここで任意の図形や色付け、状態変化を行い、描画表現を大幅に拡張できます。  
- パフォーマンス注意：反復ごとに文字列（指示列）が指数的に増大するため、iterationsの増やし過ぎに注意。evaluate()で一度評価してからrender()する流れはメモリ／描画制御に有利です。

## 実践ポイント
- インストール（初めてのとき）:
```julia
julia> using Pkg; Pkg.add("Lindenmayer")
```
- Sierpinski風の例（SVG出力）:
```julia
using Lindenmayer
sierp = LSystem(Dict("F"=>"G+F+Gt","G"=>"F-G-F"), "G")
drawLSystem(sierp, forward=10, turn=60, iterations=6, startingx=-300, startingy=-300, filename=:svg)
```
- asteriskfunctionで独自描画を差し込む（例：位置に円を描く）:
```julia
f(t::Turtle) = circle(Point(t.xpos,t.ypos), 5, :fill)
drawLSystem(myls, forward=50, turn=137.5, iterations=50, asteriskfunction=f)
```
- evaluate()/render()分離：大きなシステムはまず Lindenmayer.evaluate(ls, n) で評価し、Lindenmayer.render(ls, turtle, forward, turn) で描くとメモリ管理しやすい。  
- 日本での活用案：自治体デザイン、ゲームのプロシージャル地形・植生生成、講義／ワークショップでのアルゴリズム視覚化、SVG出力を使ったWeb表現など。  
- デバッグ：環境変数でデバッグ出力を切り替え可能（例：ENV["JULIA_DEBUG"]=Lindenmayer）。

短時間で目に見える成果が出るので、まずは iterations と forward/turn を触りながら遊んでみてください。
