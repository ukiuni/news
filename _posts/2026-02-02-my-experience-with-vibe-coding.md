---
layout: post
title: "My experience with vibe coding - vibeコーディングの体験談"
date: 2026-02-02T17:02:18.775Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://haskellforall.com/2026/02/my-experience-with-vibe-coding"
source_title: "Haskell for all: My experience with vibe coding"
source_id: 1190075811
excerpt: "AIと共にGHCJSビルド障害を解決試行、脆いLLMパッチとmacOS依存の真因を暴いた実務レポート"
image: "https://haskellforall.com/imgs/logo.jpg"
---

# My experience with vibe coding - vibeコーディングの体験談
魅力的なタイトル: 「AIと一緒にコードを書く“vibeコーディング”は本当に現場で使えるのか？— Nix と GHCJS の実例から学ぶ」

## 要約
著者はClaude CodeでNix上のGHCJSビルド障害を解決しようとしたが、LLMが出した「動くけど壊れやすい」パッチに失望。根本原因はmacOS固有のツールチェーン問題で、適切な人間の判断とCI運用が最終解決を導いた。

## この記事を読むべき理由
日本でもApple SiliconやNixを使う開発者が増加中。AI支援開発の恩恵と限界を、実際のビルド障害（再現性のないGHCJSビルド失敗）を通して学べるため、実務でAIを導入する際の判断材料になります。

## 詳細解説
- 背景：著者はNixpkgsをアップグレードした後、GHCJSのビルドで「ghc/utils/unlit/fs.h が見つからない」というエラーに遭遇。問題はマシン間で再現性がなく、一方では成功していた。
- vibeコーディングの流れ：Claude Code Proに相談し、対話的にコマンド実行やパッチ適用を試行。著者は手出しを最小限にしてClaudeに任せる方針だったが、途中で非推奨な案（x86_64でビルドするなど）を修正する介入が必要に。
- LLMの出した解：Claudeは/nix/store直書きやビルドフェーズの丸ごとコピペで回避する「動くが脆い」パッチを提案。こうした手法はNixの再現性やメンテナンス性を損なう。
- なぜダメか：固定された/nix/storeパスはgcで消える・他環境で動かない、ビルドフェーズのベンダリングは upstream の変更を取り込めず将来的に壊れる。LLMは一見妥当なコードを生成するが、設計上のトレードオフや維持コストを判断できないことがある。
- 実際の原因と正しい解：根本はmacOSの新しいバージョンで発生するgccのプリプロセス失敗（重複するLC_RPATH等）。現実的な対処は（1）該当のNixpkgs PRをマージする、（2）問題のコマンドだけclangに切り替える等の局所的修正、または（3）古いmacOS上でCIビルド成果物をキャッシュして配布する（著者はGarnix CIでの回避を採用）。

## 実践ポイント
- LLMが出したコードは「動作確認＋設計チェック」必須。特にNixでは/store直書きやビルドフェーズの丸ごと置換を避ける。
- 再現性を最優先に：固定パスを使わない、override/overrideAttrsで差分を小さく保つ。
- 問題切り分けは人間が担う：LLMを使って探索させつつ、根本原因の確認（OS差異、ツールチェーンのバグ、CI環境差）を行う。
- CIとビルド成果物の共有を活用：macOS系問題はローカル環境差が出やすいので、安定したランナーでビルドしてアーティファクトを配るのが現実的。
- チーム導入の注意：日本の現場でも「vibeコーディング＝魔法」ではない。コスト（トークン・プラン）とメンテナンス負荷を評価し、人間によるレビュー体制を必須にする。

以上。vibeコーディングは短時間でアイデアを出すのに有用だが、保守性と再現性を求める現場では人間の設計判断とCI運用が欠かせません。
