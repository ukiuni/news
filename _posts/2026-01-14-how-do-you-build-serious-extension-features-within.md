---
layout: post
title: "How do you build serious extension features within the constraints of VS Code’s public APIs? - VS Codeの公開APIの制約内で、本格的な拡張機能をどう作るか？"
date: 2026-01-14T19:19:16.320Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://docs.getpochi.com/developer-updates/dynamic-rendering-stratergies-for-ai-edits/"
source_title: "NES Series (Part 4): Dynamic Rendering Strategies for AI Code Edits - Pochi"
source_id: 426833581
excerpt: "VS Code公開APIで浮動画像や差分装飾を使い邪魔しないAI編集を実現"
image: "https://docs.getpochi.com/og-image/cover-nes-part-4-og-image"
---

# How do you build serious extension features within the constraints of VS Code’s public APIs? - VS Codeの公開APIの制約内で、本格的な拡張機能をどう作るか？
魅力的日本語タイトル: VS Code拡張で「邪魔しないAI編集」を作る技術 — NESが採った3つの描画戦略

## 要約
PochiのNESは、VS Codeの公開APIだけでAI生成のコード編集候補を「視認性を保ちつつ邪魔しない」形で表示するために、編集位置や提案の規模に応じて3種類の描画戦略を切り替えている。

## この記事を読むべき理由
VS Codeが主戦場の日本の開発者には、AI補助の品質は「正確さ」だけでなく「開発の流れを壊さない提示方法」が重要。拡張を作る／選ぶ立場なら、どの表示手法がいつ有効かを知っておくと導入判断や実装設計で差がつきます。

## 詳細解説
背景と課題
- エディタは常に変化しており、拡張側でカーソル位置を制御できない。提案をそのまま出すと、カーソルジャンプ、強制スクロール、大きな差分のインライン表示で開発者の集中を壊すリスクがある。
- VS Codeは「LLM編集プレビューの専用API」を持たない代わりに、状況ごとに最適化された表示プリミティブ（インライン補完API、テキスト装飾API、画像デコレーションなど）を提供している。

NESのDynamic Rendering Strategy（3つのパス）
1. インライン補完（Inline Completion）
   - 編集がカーソル直下に収まる小さな変更（括弧補完や数文字の置換）では、VS Codeのインライン補完APIで自然に流れに乗せる。最も非侵襲。
2. インライン差分プレビュー（Inline Diff Preview）
   - 変更がファイル内の別箇所に及ぶが行単位で示せる場合、置換箇所を赤でハイライト、挿入内容を緑で表示する「差分装飾」を使い、カーソルを移動させずに変更内容を見せる。
3. 浮動差分イメージ（Floating Diff Image）
   - 新しいヘルパ関数の挿入やブロック単位のリファクタなど多行・構造的な提案は、ターゲット近くに浮かぶ画像プレビューで提示する。こうすることでビューをスクロールさせずに文脈を伝えられる。

大きな技術ポイント（画像プレビューを作るための実装要素）
- テーマ整合：アクティブなVS Codeテーマ(JSON)からトークン色を抽出してエディタと見た目を一致させる。
- シンタックスハイライト：vscode-textmate相当の仕組み（TextMateグラマー）でトークン化し、実際の色付けルールを適用する。
- 画像レンダリング：canvaskit-wasmなどを使いフォントサイズ・行間を反映してコードを描画し、差分の赤緑ハイライトを合成。生成した画像をデコレーションAPIで表示する。
- 性能配慮：レンダリングは非同期で行い、軽量な差分判定や条件分岐で不要な処理を避ける。

設計思想
- 「見せすぎず、伝わる量だけ見せる」ことが肝。提示方法は編集の位置とサイズに合わせ最小の注意喚起で十分な文脈を与えるように選ぶ。

## 実践ポイント
- 提案の適用対象（カーソル直下か否か、単一行か複数行か）を最初に判定し、表示パスを分岐させるロジックを必ず作る。
- 小規模変更はVS CodeのInline Completion API、大きな変更はDecoration API（テキスト装飾／画像デコレーション）を使い分ける。
- 画像プレビューを作るなら、ユーザーのテーマ・フォント情報を読み込み、TextMateベースのトークン化→canvaskitでの描画というパイプラインを検討する（既存ライブラリを探すと実装工数が減る）。
- レスポンスとレンダリングは非同期にし、UIスレッドをブロックしない。表示は「プレビュー」であり、ワンクリックで適用できる仕組みを用意する。
- 日本のチーム運用ではレビューやCIと組み合わせやすい表示（差分プレビューの明確さ）を優先すると採用されやすい。

以上を押さえれば、VS CodeのAPI制約内でも「開発者の流れを壊さない」AI編集体験を実装できる。
