---
layout: post
title: "Move over, Vibe-Coding: I built an AI editor for STRESS-CODING - 「バイブコーディングはもう古い：ストレス・コーディング用AIエディタを作った」"
date: 2026-04-08T10:16:18.968Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/phalkmin/move-over-vibe-coding-i-built-an-ai-editor-for-stress-coding-4243"
source_title: "Move over, Vibe-Coding: I built an AI editor for STRESS-CODING - DEV Community"
source_id: 3460935
excerpt: "まばたきでコードが徐々に破壊される監視ジョークIDEを実装解説"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Ffx87tqdppj1fmoh1j4gh.png"
---

# Move over, Vibe-Coding: I built an AI editor for STRESS-CODING - 「バイブコーディングはもう古い：ストレス・コーディング用AIエディタを作った」
あなたのまばたきでコードが壊れる？監視社会を茶化したAIエディタ「Quantum Collapse」の話

## 要約
Webカメラでまばたきを検出し、まばたきするとコードを「ひそかに改変」して作業者を不安に陥れるジョークIDE「Quantum Collapse」を技術的に紹介する記事。監視ツールとAI時代の職場体験を風刺している。

## この記事を読むべき理由
日本でもリモートワーク増加でカメラ・生体トラッキングや生産性監視の話題が現実味を帯びているため、技術的な実装と倫理的含意を理解しておく価値がある。開発スタックや検出手法は実務でも参考になる。

## 詳細解説
- 概念：画面を見ていればコードは無事。まばたきや視線離脱を検出すると「波動関数を収縮」させるようにコードを徐々に改変し、保存や動作を阻害する（例：変数名を絵文字に、セミコロンを別記号に置換、関数名を特撮モンスター名にするなど）。安定度（Stability Meter）が下がると保存不可に。
- 顔検出／まばたき検出：Google MediaPipe（Face Landmarker）をブラウザ上で動かし、200msのまばたきを検知。クライアント側でリアルタイム処理し遅延ゼロを意図。
- 変更エンジン：「どこが変わったかわからない」ことを重視した差分変換ロジック（変数名・句読点・関数名の非破壊的な改変）。意図的に微妙な壊し方をする設計思想。
- 開発スタック：React 19 + TypeScript（型安全を保ちつつ混乱を演出）、Vite 8、Framer Motion（グリッチ演出）、PrismJS（シンタックスハイライト）。AIツールとしては企画・設計にGemini（Web/CLI）のPlan Mode、前段にCodexでフロント調整、デプロイはGoogle Cloud Run。  
- 補足：著者はジョーク／風刺を主眼にしており、同時に監視ソリューションの実情を皮肉っている — 企業向け監視とエンタープライズ基盤で運用されるギャップがアイロニー。

## 実践ポイント
- 技術的に試すなら：React+TypeScript+Viteの雛形にMediaPipe Face Landmarkerを組み込み、まばたき閾値（例：200ms）で処理をトリガーする実装をまず作ると理解が深まる。UIはFramer Motionで演出可能。  
- セキュリティ／プライバシー対策：カメラ権限を必要最小限にし、監視系ツール導入前に社内ポリシーと同意を明確化する。  
- 倫理的判断：ジョークでも実装の技術やUX設計を知ることで、監視ツールのリスク（心理的負荷、誤検出による生産性低下）を議論できる。  
- リソース確認：公開リポジトリやデモ（元記事参照）を見てコード設計を学ぶと実装パターンが掴める。
