---
layout: post
title: "Show HN: I ported Manim to TypeScript (run 3b1B math animations in the browser) - ManimをTypeScriptへ移植（3Blue1Brownの数式アニメをブラウザで実行）"
date: 2026-02-28T05:29:12.494Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/maloyan/manim-web"
source_title: "GitHub - maloyan/manim-web: Mathematical animations for the web — Manim in TypeScript"
source_id: 47155375
excerpt: "ブラウザで3B1B風数式アニメをTSで即実行、React/Vue統合とPython変換対応"
image: "https://opengraph.githubassets.com/b0c6ca4948bd9947f1ddc93a7522b1499be0b4f82c660d18165423a881647ac0/maloyan/manim-web"
---

# Show HN: I ported Manim to TypeScript (run 3b1B math animations in the browser) - ManimをTypeScriptへ移植（3Blue1Brownの数式アニメをブラウザで実行）

ブラウザだけで3Blue1Brown風の数式アニメを作る──Python不要でTypeScript/フロント側に直結する「manim-web」

## 要約
manim-webはManimをTypeScriptで再実装し、ブラウザ上で数学アニメーション（LaTeX、グラフ、3D、トランスフォームなど）を直接動かせるライブラリ。React/Vue統合や既存のPythonスクリプトをTypeScriptへ変換するツールも提供する。

## この記事を読むべき理由
日本の教育コンテンツ、技術ドキュメント、プロダクトデモ制作において、動画制作や演示をフロントエンドだけで完結させられる点が即戦力になるため。オンライン授業や技術ブログ、プロトタイプ作成で工数を大幅に削減できる。

## 詳細解説
- コア機能：円・四角・多角形・矢印などの幾何オブジェクト、Text/MathTex（KaTeX）、Axes/FunctionGraph、VectorField、BarChart、3Dオブジェクト（Sphere, Cube, Cylinder, ThreeDAxes）やオービット操作までサポート。アニメーションはCreate/Transform/FadeIn/Writeなど豊富。
- 実行環境：ブラウザで完結。npmパッケージとして配布され、既存のフロントエンドツールチェーン（Vite等）で組み込み可能。
- フレームワーク統合：React用のManimSceneコンポーネントやVue対応が用意され、JSX/テンプレート内で直接アニメーションを組み込める。
- Python互換性：既存のManim（Python）スクリプトをTypeScriptに変換するツール（node tools/py2ts.cjs）を備え、移行コストを下げる。
- 出力・インタラクション：GIF/動画エクスポート、ドラッグ/ホバー/クリックなどのインタラクティブ操作をサポート。教育コンテンツの配信やインタラクティブ教材作成に向く。
- 開発状況：オープンソース（MIT）、活発にコミットされておりドキュメント・例が充実。ただしフル互換ではない箇所もあり、複雑なManim Pythonスクリプトは要調整の可能性あり。

例（基本的な使い方）:
```typescript
import { Scene, Circle, Square, Create, Transform, FadeOut } from 'manim-web';

async function squareToCircle(scene: Scene) {
  const square = new Square({ sideLength: 3 });
  const circle = new Circle({ radius: 1.5 });
  await scene.play(new Create(square));
  await scene.play(new Transform(square, circle));
  await scene.play(new FadeOut(square));
}
```

## 実践ポイント
- まず試す：npm install manim-web → npm run dev（リポジトリのexamples/を参照）
- 既存資産活用：Pythonで書いたManimスクリプトは node tools/py2ts.cjs input.py -o output.ts で変換を試す
- フロント統合：React/Vueコンポーネントを使えば既存サイトに自然に組み込み可能
- 日本市場での活用例：オンライン授業、学術プレゼン、技術ブログのアニメ（数式説明動画）や製品の可視化デモ
- 注意点：複雑なレンダリングやPython版特有の拡張機能は未対応な場合があるため、重要プロジェクトでは事前検証を行う

参考：manim-web（GitHub） — MITライセンス、ドキュメント・例が豊富。
