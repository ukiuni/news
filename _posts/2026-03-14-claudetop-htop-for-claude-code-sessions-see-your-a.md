---
layout: post
title: "Claudetop – htop for Claude Code sessions (see your AI spend in real-time) - Claudetop — Claude Codeセッション向けhtop（AI支出をリアルタイム可視化）"
date: 2026-03-14T19:51:34.272Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/liorwn/claudetop"
source_title: "GitHub - liorwn/claudetop: htop for your Claude Code sessions — real-time cost, cache efficiency, model comparison, and smart alerts · GitHub"
source_id: 47380203
excerpt: "Claude CodeのリアルタイムAI課金を端末で可視化し無駄を即発見できるCLIツール"
image: "https://opengraph.githubassets.com/b9b717cdeb1cecfe17735a3e269d1b0f7d70aa45dfeeab09f3d1e2636ce90823/liorwn/claudetop"
---

# Claudetop – htop for Claude Code sessions (see your AI spend in real-time) - Claudetop — Claude Codeセッション向けhtop（AI支出をリアルタイム可視化）
AI課金のムダを即発見！Claude Codeのトークン・コストを端末で「見える化」するclaudetop

## 要約
claudetopはClaude Codeセッションの実時間コスト、キャッシュ効率、モデル別比較、アラートなどをステータスラインで表示するCLIツール。請求の「何に使ったかわからない」を解消する目的で作られています。

## この記事を読むべき理由
日本でもクラウドAI利用が増え、想定外の課金やモデル選定ミスが開発コストを圧迫します。claudetopは開発中のAIコスト可視化と早期検出を手軽に導入できるため、スタートアップ／企業エンジニア問わず役立ちます。

## 詳細解説
- 何をするか：Claude Codeのステータスラインに「現在のモデル／セッション時間／リアルタイム消費額／時給換算／月額予測／キャッシュヒット率／モデル別コスト試算／スマートアラート」を表示します。  
- なぜ有効か：Anthropicのモデルはトークンの読み書きやキャッシュ効率で料金差が出やすく、セッション単位で可視化できれば無駄遣いを素早く把握できます（例：コンパクションでトークンが隠れて請求が跳ねるなど）。  
- 主な機能：リアルタイムコスト追跡、モデル比較（Opus / Sonnet / Haiku等）、キャッシュ効率メトリクス、しきい値でのスマートアラート、セッション履歴と集計（claudetop-stats）、タグ付けやデイリーバジェット設定、プラグイン拡張（~/.claude/claudetop.d/）。  
- 動作要件：Claude Code（ステータスライン対応）、jq、bc等が動く環境。価格はリポジトリのpricing.jsonで管理され、更新で反映されます。  
- 拡張性：プラグインは数行のシェルスクリプトで作成可能。CIステータスやSpotify表示、チケット番号などを任意に追加できます。

## 実践ポイント
- インストール（端末で実行）:
```bash
# bash
curl -fsSL https://raw.githubusercontent.com/liorwn/claudetop/main/install.sh | bash
```
- まずはclaudetopを起動してセッションを数回観察し、キャッシュ比率と時給換算を確認する。  
- デイリーバジェットを設定して超過アラートを受け取る:
```bash
export CLAUDETOP_DAILY_BUDGET=50
```
- 高コストが続くモデルは試算機能で代替モデル（Sonnet/Haiku）に切替可能か検証する。  
- プロジェクト単位でタグ付け（例：CLAUDETOP_TAG=auth-refactor）し、機能ごとのコストを追跡する。  
- 日本のチーム運用では「CIや自動エージェントが暴走していないか」「夜間バッチで無駄に回っていないか」をclaudetopで定点観測すると効果的。

claudetopは「見えない請求」を可視化して即対応できるツールです。導入は軽量なので、まず試して日々のAI利用を数値で把握してください。
