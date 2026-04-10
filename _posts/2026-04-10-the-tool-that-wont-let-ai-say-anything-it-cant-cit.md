---
layout: post
title: "The tool that won't let AI say anything it can't cite - AIが出典を示せないことを言わせないツール"
date: 2026-04-10T07:01:47.855Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/grainulation/grainulator"
source_title: "GitHub - grainulation/grainulator: Research that compiles. · GitHub"
source_id: 47714239
excerpt: "出典で主張を厳格に検証し、根拠薄ならAI出力を遮断する開発者向けツール"
image: "https://opengraph.githubassets.com/8d4debe05b5296eb9ca0bf601aa7dbc2577666a512c3a459b4be46010c0454fe/grainulation/grainulator"
---

# The tool that won't let AI say anything it can't cite - AIが出典を示せないことを言わせないツール
AIに「根拠のない結論」を言わせない──研究成果を型（claims）で組み立てる新しいワークフロー

## 要約
Grainulatorは、AIによる調査・意思決定支援を「型付きの主張（claims）」と証拠トレースで管理し、根拠が弱ければ出力をブロックする研究コンパイラ／プラグインです。Claude向けプラグイン＋PWAデモで即試用可能です。

## この記事を読むべき理由
AIが生成する結論の「出典・信頼度」をちゃんと担保したい日本のエンジニアやプロダクト担当者にとって、有益な実務ツールです。規制対応、社内レビュー、設計判断の記録化に直結します。

## 詳細解説
- コア概念：すべての所見は「claim（主張）」として型付きで保存される（types: constraint, factual, estimate, risk, recommendation, feedback）。各claimは証拠の「tier（stated → web → documented → tested → production）」で格付けされる。  
- コンパイラ：claimsを7パスで解析（型カバレッジ、証拠強度、衝突検出、バイアススキャンなど）し、信頼度スコアを算出。不整合が残ると出力を止め、要解決にすることで誤情報出力を抑止する。  
- ワークフロー／スキル：/init, /research, /challenge（敵対的検証）, /witness（裏付け）, /blind-spot（抜け穴検出）, /brief（決定用ブリーフ生成）などの13種のプロンプトワークフローを備える。  
- 自律エージェント：grainulatorサブエージェントはコンパイラ出力を読んで次のアクション（研究→挑戦→裏取り）を自律選択し、決定準備まで走らせられる。  
- デモ＆実装：PWA（grainulator.app）でブラウザ内推論（WebLLM: SmolLM2-360M）や50トピックのデモが動作。実運用はClaudeプラグインとして組み込み、Node.js >= 20が要件。READMEにある手順でclaude plugin install grainulatorで導入可能。  
- エコシステム：wheat（主張エンジン）、mill（書式変換）、silo（ナレッジ格納）など8ツールで構成。各ツールはNode組み込みのみで動き、外部依存を最小化している。  
- エンタープライズ配慮：プロジェクトの .claude/settings.json で有効化、MDM経由配布、あるいは CLAUDE_CODE_PLUGIN_SEED_DIR によるエアギャップ導入が可能。

## 実践ポイント
- まずはデモを試す：grainulator.appで挙動を確認（ローカル推論と逐次的な主張公開が分かる）。  
- 導入手順（簡易）：Node.js >= 20 を用意 → Claudeのマーケットプレイスにプラグイン追加 → claude plugin install grainulator。  
- 小さく始める：/research や /challenge を使い、1〜2スプリントで主張→裏付け→ブリーフ生成の流れを体験。  
- 社内適用：設計判断やコンプライアンス資料をclaimベースで残すと監査・レビューが楽になる。  
- セキュリティ運用：air-gapped運用や管理者承認ダッシュボード（farmer）を活用して企業ポリシーに合わせる。

元リポジトリ：https://github.com/grainulation/grainulator（READMEにインストール／トラブルシュートあり）
