---
layout: post
title: "Completion is a Substrate, not a UI - 補完はUIではなく基盤である"
date: 2026-04-14T13:34:50.929Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.chiply.dev/post-icr-primer"
source_title: "Completion is a Substrate, not a UI | Charlie Holland's Blog"
source_id: 363172355
excerpt: "大量データ時代に探索コストを劇的に下げるICRの実践と設計手法"
image: "http://sveltekit-prerender/images/icr-primer-banner.jpeg"
---

# Completion is a Substrate, not a UI - 補完はUIではなく基盤である
タイプするだけで世界が狭まる：ICRが「探す」を再発明する理由

## 要約
Incremental Completing Read（ICR）は単なる便利機能ではなく、「候補を文字ごとに絞る」ことで探索コストをデータ量に依存しなくするインターフェース基盤だ。

## この記事を読むべき理由
大規模プロジェクトや大量のメール／ドキュメントを扱う日本のエンジニアにとって、ICRを理解し導入することは作業効率を根本的に変える投資になるから。

## 詳細解説
- ICRの定義（3要素）  
  - Read：プロンプトで値を取得する操作。  
  - Completing：入力に応じて候補集合を提示する。  
  - Incremental：各キー入力ごとに候補を再計算して即時に更新する。  
- なぜ別物か：ブラウズは候補数に弱く、検索はフィードバックギャップを生む。ICRは二者を融合し、入力中に候補を小さくすることで選択コストを一定化する。  
- 技術的要点：候補ソース／マッチャー／ソーター／注釈（annotator）／アクションは独立したレイヤーであり、Emacsやシェルはこれらを差し替え可能にしている。一方で多くの商用UIはこれらを固定してしまう。  
- スケーリングと認知：ICRは探索コストをデータ量から切り離すため、認知コストがほぼ $O(1)$（アナロジー）に近づく。Hick–Hymanの法則の $ \log_2(n+1) $ による選択コストを、ICRは「事前にnを縮める」ことで回避する。  
- 組み合わせ可能性：ファイル→アクション→別のICR、あるいはシェルの `fd | fzf | xargs` のように、ICRは小さなプリミティブを組み合わせて強力なワークフローを作れる。

## 日本市場との関連性
- 日本の企業でも巨大レポジトリ、長いメール履歴、要件ドキュメントの山が普通。探索コスト削減の効果が大きい。  
- VS Code、JetBrains、Neovimユーザーが多い日本の現場でも、ICR的UX（コマンドパレット、ファイル検索、Go-to Anything）は既に受け入れられており、さらにカスタマイズ可能なツール（fzf、Emacs＋Vertico/Ivy/Helm）が生産性差を生む。

## 実践ポイント
- まずは今のエディタでコマンドパレット／インクリメンタル検索を有効化する（例：VS CodeのCmd/Ctrl+P）。  
- シェルでの即戦力：fd + fzf を導入してファイル検索→編集をパイプで組む。  
- Emacsユーザは Vertico/Ivy/Helm を試し、matcher／sorter／actions 層を理解して差し替えてみる。  
- 自作ツールや社内ツールを作るなら、候補生成・マッチング・アクションを分離して「ICRを基盤にする」設計を検討する。  
- 大量データを扱うなら、ICR導入で体感的な「探す」コストが劇的に下がることを覚えておく。

この記事をきっかけに、単なる「入力補助」ではなく「探索の基盤」としてICRを検討してみてください。
