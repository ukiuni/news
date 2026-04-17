---
layout: post
title: "Show HN: Spice simulation → oscilloscope → verification with Claude Code - SPICEシミュレーション → オシロスコープ → Claude Codeによる検証"
date: 2026-04-17T02:34:21.389Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lucasgerads.com/blog/lecroy-mcp-spice-demo/"
source_title: "SPICE simulation → oscilloscope → verification with Claude Code — Lucas Gerads"
source_id: 47801255
excerpt: "SPICE波形と実機オシロをClaudeで照合し検証を自動化する新ワークフロー"
---

# Show HN: Spice simulation → oscilloscope → verification with Claude Code - SPICEシミュレーション → オシロスコープ → Claude Codeによる検証
魅力タイトル：AIに「波形を見せる」時代へ──SPICEから実機検証までを自動化する新ワークフロー

## 要約
SPICEシミュレーションの波形をオシロスコープとファイル経由でAI（Claude Code）に与え、モデル検証や組み込みデバッグを自動化する実験的ワークフローの紹介。データ整形や測定のズレをAIに任せて高速に反復できる点が主眼。

## この記事を読むべき理由
日本のハード開発現場や趣味の電子工作でも、シミュレーションと実機を素早く突き合わせて検証するニーズは高い。手作業での波形整形や比較に時間を取られているなら、本手法は検証コストを下げるヒントになる。

## 詳細解説
- 全体像：SPICEで回路を設計→（MCPサーバー経由で）SPICEの出力やオシロスコープ波形をファイル化→Claude Codeに渡して解析・照合。  
- なぜ有効か：Claudeは自然言語でのやり取りに強いが、即時フィードバック（生データ）を与えるとモデル・回路設計の改善に強みを発揮する。波形のタイム軸正規化、整列、ピーク検出などの前処理が面倒なタスクを自動化できる。  
- 実装の要点：
  - オシロスコープは物理的接続をAIが「見ている」わけではないので、接続情報を明示的に与えること（デバイスマップや配線図）。  
  - 生データは直接チャットに投げず、ファイルとして保存してAIに間接的に扱わせる（コンテキスト汚染とサイズ問題の回避）。  
  - マイクロコントローラ操作は、ピン割当（pinout/pinmux）を明示し、Makefileに build/flash/ping/erase といった標準ターゲットを用意してAIに使わせる。AIにコマンドを勝手に組ませない。  
- リポジトリ例（元著者）：
  - lecroy-mcp：LeCroyオシロ用MCPサーバ  
  - spicelib-mcp：SPICEラッパーMCPサーバ  
  - rc-filter-demo-files：デモ用セットアップ  

## 実践ポイント
- まずは小さな回路（RCフィルタ等）でワークフローを試す。  
- オシロ/シミュレーション出力はCSV等で保存し、AIにはファイル参照させる。  
- リポジトリにMakefileとピンマップを備え、AIが既存ターゲットを呼べるようにする。  
- モデル調整→シミュ→実機計測→AI解析のループを短く回し、差分からSPICEモデルをチューニングする。  
- 日本語ドキュメントや現地計測慣習（電源規格、部品入手性）を併記しておくと実運用が楽になる。

元記事のアプローチは、個人開発から産業用途までスケール可能で、測定・検証の反復速度を劇的に上げられる可能性があります。
