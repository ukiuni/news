---
layout: post
title: "Show HN: Hippo, biologically inspired memory for AI agents - Hippo：生物学に着想を得たAIエージェント向けメモリ"
date: 2026-04-07T00:05:18.620Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/kitfunso/hippo-memory"
source_title: "GitHub - kitfunso/hippo-memory: Biologically-inspired memory for AI agents. Decay, retrieval strengthening, consolidation. Zero dependencies. · GitHub"
source_id: 47667672
excerpt: "ツール横断で重要記憶を残し不要を忘れる生物学的AIメモリHippo"
image: "https://opengraph.githubassets.com/db39bf05cf97a956017a5a5ab8d9a8933fe1c72b28dc38bdd5bd4035ef9ebcc6/kitfunso/hippo-memory"
---

# Show HN: Hippo, biologically inspired memory for AI agents - Hippo：生物学に着想を得たAIエージェント向けメモリ
ツールをまたいで“忘れる力”を設計する——Hippoでエージェントに人間らしい記憶を持たせる

## 要約
Hippoは「何でも保存する」代わりに「重要なものを残し、不要なものを忘れる」ことを目指すオープンソースのAIメモリ層。作業バッファ、エピソード記憶、意味記憶を使った学習・減衰・統合を提供し、複数のエージェント／ツール間で記憶を共有できます。

## この記事を読むべき理由
ツールを切り替えると文脈がリセットされる問題は、日本の開発チームやマルチツール運用でも頻出。Hippoを導入すればインシデントの再発防止や手順の継承、CI／運用ドキュメントの整備が自然に行えます。

## 詳細解説
- アーキテクチャ：短期の「バッファ（Working memory）」→タイムスタンプつきの「エピソード（Episodic）」→反復から作る「意味記憶（Semantic）」へと整理。定期的な「sleep（睡眠）」で再生・統合・減衰を行う。
- 減衰と強化：各メモリに半減期（デフォルト7日）を持たせ、未回収なら徐々に弱化。再呼び出しで半減期が延びる（Use it or lose it）。エラーや重要な教訓は半減期が長くなる設定。
- 検索・説明可能性：BM25キーワード検索とコサイン類似度（@xenova/transformersで任意使用）のハイブリッド。`hippo recall --why`でどの特徴が一致したかを確認できる。
- セマンティクスとスキーマ：類似エピソードをまとめて一般化し、頻出パターンは早く定着、ノイズは速く忘却される。
- 運用向け機能：セッションスナップショット、handoff（引き継ぎ）、作業バッファの上限や重要度による削除、衝突検出・追跡、Markdownでのインポート／エクスポート（ChatGPT/Claude/Cursorなど対応）。永続ストレージはSQLite＋人間可読なMarkdownミラーで、リポジトリに入れて共有可能。
- インテグレーション：Node.js（22.5+）で動作、ランタイム依存ゼロ。`hippo init`で既存エージェントフックや自動スケジュールを設定でき、チーム導入の障壁が低い。

## 実践ポイント
- まずは試す：`npm install -g hippo-memory` → `hippo init` で既存プロジェクトに導入し、日次の学習・sleepを有効化して自動で統合させる。
- インシデント管理に使う：デプロイ失敗や再発バグを`--error`で記録し、長めの半減期で保持。後続セッションで再発防止策を自動的に引き継げる。
- クロスツール共有：ChatGPTやClaude、Cursorからのインポート/エクスポートを活用してナレッジをロックインせずリポジトリで管理。
- 日本チーム向け運用案：CI（例：GitHub Actions）で夜間に`hippo learn --git`と`hippo sleep`を走らせ、コミットから自動で知見を抽出・統合する運用にする。
- 精度向上：埋め込み検索を使える環境なら`hippo embed`で検索品質が向上。リソースがない場合はBM25フォールバックで十分実用的。

短時間で「忘れるべきもの」と「残すべきもの」を分けられる仕組みは、増え続けるツール群と知識断片に悩む日本の現場に即効性のある改善をもたらします。興味があれば公式リポジトリ（https://github.com/kitfunso/hippo-memory）を覗いてみてください。
