---
layout: post
title: "Show HN: FluidCAD – Parametric CAD with JavaScript - Show HN: FluidCAD – JavaScriptで操るパラメトリックCAD"
date: 2026-04-10T20:14:57.691Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://fluidcad.io/"
source_title: "Parametric CAD for everyone | FluidCAD"
source_id: 47721997
excerpt: "JavaScriptで直感的に設計できる、リアルタイム反映のパラメトリックCAD"
---

# Show HN: FluidCAD – Parametric CAD with JavaScript - Show HN: FluidCAD – JavaScriptで操るパラメトリックCAD
驚くほどシンプルに3D設計ができる「コードと直感」を両立した新世代CADツール

## 要約
FluidCADはJavaScriptで記述するパラメトリックCAD。リアルタイムビューと操作履歴（非破壊のフィーチャーツリー）で、試行錯誤を高速化します。

## この記事を読むべき理由
コードベースのCADは自動化・再現性で強みを発揮します。日本のものづくり、教育、スタートアップや個人のプロトタイピングに直結する実用性が高く、既存CADとのSTEP互換もあるため導入障壁が低いです。

## 詳細解説
- コードで定義: JavaScriptでスケッチ、押し出し（extrude）、フィレット、シェル、ブーリアンなどの標準操作を記述。最小限の数学で形状参照（面・辺・頂点）できるため読みやすい。
- リアルタイム表示: エディタと連携して編集すると即座に3Dビューポートに反映。マウスで押し出し量を直接操作するハイブリッドなプロトタイピングも可能。
- ヒストリーと非破壊編集: フィーチャーツリーをステップ再生・ロールバックでき、どの操作で形状がどう変わったか追跡できる。
- トランスフォーム／パターン: フィーチャーシーケンスごとに線形・円形パターンやミラー、回転を適用して複雑な繰り返し形状を簡潔に作成。
- 互換性: STEPのインポート／エクスポート（色付き対応）で既存CADワークフローやCAM、CNC、3Dプリントに接続可能。
- スマートデフォルト: 多くの操作は直近のスケッチや選択を自動で利用。冗長なコードが減り可読性が上がる。

## 実践ポイント
- まずはインストール:
```javascript
npm i fluidcad
npx fluidcad init
```
- VS Code拡張を入れて「Show FluidCAD Scene」を実行するとエディタとビューポートを連携可能。
- 最初のサンプル（円を押し出す）:
```javascript
sketch("xy", () => {
  circle(50)
})
const e = extrude(50)
fillet(5, e.startEdges())
shell(-2, e.endFaces())
```
- すぐ試す用途例: 3Dプリント用ケース、機構部品のパラメトリック設計、教育用のモジュール化教材。
- ワークフロー提案: 1) スケッチ→2) 押し出し→3) フィレット/シェルで仕上げ→4) パターンで複製→5) STEP出力して加工へ。

日本のものづくり現場や学習環境でも「コードで再現できる設計」は価値が高く、FluidCADはその第一歩を低コストで始められるツールです。
