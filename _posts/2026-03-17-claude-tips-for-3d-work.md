---
layout: post
title: "Claude Tips for 3D Work - Claudeの3D作業Tips"
date: 2026-03-17T06:54:07.039Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.davesnider.com/posts/claude-3d"
source_title: "Claude tips for 3D work - Dave Snider"
source_id: 47365299
excerpt: "スクリーンショット検証ループでClaudeに3D修正を任せ、視覚的問題を自動で見つけて直す方法を学ぶ"
image: "https://files.davesnider.com/2026MAR/ZKeO2SgcsKAh-fel.png"
---

# Claude Tips for 3D Work - Claudeの3D作業Tips
AIに3Dを任せる前に知っておきたい、視覚フィードバックで回す“検証ループ”の作り方

## 要約
Claudeはコード生成に強いが、3D空間の視覚的判断は苦手。スクリーンショットを使った自動化ループで「見て確かめる」仕組みを作ると、劇的に実用性が上がる。

## この記事を読むべき理由
日本でもWebGL/Three.jsやSTLを扱うプロダクトやプロトタイピングは増加中。AIに任せる際の落とし穴と現場で使える実践的ワークフローが学べる。

## 詳細解説
- 問題点：Claude（LLM）はテキストや2D画像の理解は得意だが、CADや3Dの空間推論（可視性、ブーリアンの結果、視点依存の問題）は誤認しやすい。STLを「読める」と主張してもバイナリ中身を正確に理解できないことがある。
- 解決の考え方：人が目で確認する作業をAI側にもさせるために、アプリの状態を読み取り、カメラを動かし、デバッグ用の可視マーカー（例：赤い球）を置き、複数角度でスクリーンショットを取得して検証する「反復検証ループ」を作る。
- 具体的要素：ジオメトリ生成→STL生成→レンダリングキャプチャ→project.jsonで位置確認→問題箇所をズームして再チェック→修正の繰り返し。Playwright等で操作を自動化し、Claudeに「自分で操作して検証して戻って来る」ルーチンを与えるのが肝。

例：記事が使っているコマンド（自動化ツール類）
```bash
# ジオメトリ再生成
npx tsx scripts/generate-geometry.ts

# プリセット角度レンダリング
npx tsx scripts/capture-view.ts --angle iso
npx tsx scripts/capture-view.ts --angle top

# ズームやカメラ指定
npx tsx scripts/capture-view.ts --angle left --zoom 3
npx tsx scripts/capture-view.ts --pos "100,80,150" --look-at "0,25,50"

# 特定アイテムを指定してレンダリング
npx tsx scripts/capture-view.ts --trayId nrme206 --angle bottom --zoom 2
```

## 実践ポイント
- まず「検証ツール」を先に作る：スクリーンショット取得、カメラ制御、赤いマーカー配置、JSONで位置出力を用意する。
- Claudeに期待するのは「全自動で正解を出すこと」ではなく、「自分で操作して検証→修正→再検証」を回す能力。必ず自動ループを与える。
- 小さな単位で差分を作る（箱・トレイ・蓋などファイル分割）し、問題箇所を絞って回す。
- 日本の製造・CAD案件では、STLなどバイナリを盲信せず、可視化と検証工程を自動化してAIとの共作フローを確立することが重要。

以上。この記事を参考に、まずは小さな検証ループを作ってClaudeとの共同作業を試してみてください。
