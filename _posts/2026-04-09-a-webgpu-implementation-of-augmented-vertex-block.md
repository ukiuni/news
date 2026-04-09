---
layout: post
title: "A WebGPU Implementation of Augmented Vertex Block Descent - Augmented Vertex Block Descent の WebGPU 実装"
date: 2026-04-09T14:08:29.783Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jure/webphysics"
source_title: "GitHub - jure/webphysics: WebGPU physics engine based on the AVBD solver · GitHub"
source_id: 47702541
excerpt: "WebGPUで動くTypeScript製AVBD実装、ブラウザで高性能物理を試せるデモ"
image: "https://opengraph.githubassets.com/c1fc9d5df4542ca9fd43df4d8fa7a692946484ead3f9f87cb5118dd45fffa1c9/jure/webphysics"
---

# A WebGPU Implementation of Augmented Vertex Block Descent - Augmented Vertex Block Descent の WebGPU 実装
魅せるブラウザ物理シミュレーション：WebGPUでAVBDを動かす実験プロトタイプ

## 要約
WebGPU 上で Augmented Vertex Block Descent (AVBD) を実装した実験的なリジッド／ソフトボディ物理エンジン。Chrome 対応の TypeScript 実装で、LBVH ブロードフェーズから色付け（coloring）、AVBD の反復ソルブまで論文アルゴリズムに忠実に近いパイプラインを構築している。

## この記事を読むべき理由
Web 上で高性能な物理シミュレーションを実現する技術（WebGPU + AVBD）の現在地が分かる。ブラウザアプリ、教育用シミュレーター、軽量ゲームやプロトタイピングに直結する知見が得られ、日本の開発現場でも活用余地が大きい。

## 詳細解説
- 背景：AVBD（Augmented Vertex Block Descent）は2025年の論文で提案された、拘束付き剛体/柔体の並列化に強い反復型ソルバ。WebGPU の並列計算能力と相性が良い。
- パイプライン（実装は論文の Algorithm 1 に準拠）：
  1. 衝突検出：現在の位置 $x^t$ からブロードフェーズ→ナローフェーズで候補ペアを検出（LBVH を構築・走査）。実装ファイル例: src/physics/gpu/broadPhase.ts, src/lvbh/GPULBVHBuilder.ts
  2. ナローフェーズ：接触面（manifold）生成とウォームスタート用接触状態の保持（src/physics/gpu/contactGeneration.ts）。
  3. ボディ毎拘束リスト構築：接触・ジョイント・スプリングから束を集める（src/physics/gpu/avbdState.ts）。
  4. 色付け（coloring）：同色のボディを並列に処理するための貪欲カラーアルゴリズム（src/physics/gpu/avbdState.ts）。
  5. 慣性目標 $y$ と原始状態初期化：ウォームスタートで dual/剛性係数も初期化。
  6. AVBD 反復：色ごとの primal solve（近似ヘッセ行列の扱い含む）、その後並列で dual と剛性更新を適用し、最後に速度を再構築。
- 実装上の注意点：
  - 基本は論文準拠だが、同色競合時のダブルバッファ更新は未実装で「インプレース」更新を行っている点が差異。
  - 現時点では Chrome のみ安定的に動作すること、プラグ・アンド・プレイには程遠い実験段階であることを明記。
- 技術スタック：TypeScript / WebGPU（ブラウザ GPU 計算）、デモと開発用スクリプトがリポジトリに存在。

## 日本市場との関連性
- 日本のブラウザベース開発（Web アプリ、教育、製造やロボットの軽量シミュレーション）で、ネイティブに近い速度の物理演算をブラウザで実現できる点は魅力的。
- WebGPU の普及（Chrome を筆頭に日本でも徐々に対応ブラウザが増加）に伴い、社内ツールやプロトタイピング環境に取り込みやすい。
- ゲーム開発や Web CAD、産業シミュレーションのフロントエンド実装で、TypeScript ベースなら既存のフロントエンドチームでも採用しやすい。

## 実践ポイント
- リポジトリを試す：npm install → npm run dev でローカル起動（Chrome 推奨）。まずはデモで挙動を確認。
- 学ぶ順序：衝突検出（LBVH）→接触生成→色付け→AVBD の反復というパイプライン順でコードを追うと理解が早い。
- 日本のプロジェクトでの採用検討：
  - ブラウザ互換性を確認（対象ユーザーのブラウザが WebGPU 対応か）。
  - 安定性向上とダブルバッファ更新など論文で推奨される差分を実装して検証する。
- 応用案：オンライン物理学教材、ブラウザ上でのモーションプランニング可視化、軽量リアルタイム群衆シミュレーションなど。

元記事（実装・デモ）は GitHub: jure/webphysics（TypeScript 実装、ライブデモあり）。試してみて、安定化や日本語ドキュメント化・チュートリアル作成を進めるとコミュニティ貢献にもなる。
