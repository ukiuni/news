---
layout: post
title: "\"Configuration over Code\" in AI Agent Frameworks - AIエージェントフレームワークにおける「コードより設定」"
date: 2026-01-20T12:38:27.177Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ConnectSafelyAI/agentic-framework-examples/tree/main/linkedin-to-sheets-export/agentic/mastra"
source_title: "agentic-framework-examples/linkedin-to-sheets-export/agentic/mastra at main · ConnectSafelyAI/agentic-framework-examples · GitHub"
source_id: 422072775
excerpt: "設定だけでLinkedIn→Sheets連携のAIエージェントを高速かつ安全に構築・再利用する手法"
image: "https://opengraph.githubassets.com/5a21764fdb91de81af7594d41ca703d21f2ddaf70eebadc9fa57e1af8f8fbb9b/ConnectSafelyAI/agentic-framework-examples"
---

# "Configuration over Code" in AI Agent Frameworks - AIエージェントフレームワークにおける「コードより設定」

魅力的なタイトル: コードを書かずにエージェントを作る時代へ――設定ファイルで素早く作るAIワークフロー（LinkedIn→Sheets例で学ぶ）

## 要約
「設定（configuration）を中心にしてAIエージェントを組む」アプローチは、開発速度・再現性・運用性を大きく改善する。ConnectSafelyAI の agentic-framework-examples（linkedin-to-sheets-export）の構成は、これを実践する良いハンズオン例だ。

## この記事を読むべき理由
日本の企業やスタートアップでも、LLMや自動化エージェントを短期間で安全に導入したいニーズが高まっている。コードを増やさず設定で運用する設計は、社内ガバナンスや運用負荷を下げ、迅速なPoCやスケールに直結するため必読。

## 詳細解説
- 背景概念  
  従来は「機能を追加するとコードを書く」→ 複雑化・バグ・レビュー負荷が増える。対して「設定ファイル（YAML/JSON）でエージェント構成・ツール連携・プロンプトテンプレート・実行ポリシーを定義する」方法は、変更を宣言的に扱えるためCI/CD・レビュー・ロール分担が楽になる。

- repositoryの例（linkedin-to-sheets-export）  
  この例は「LinkedInから情報を取得してGoogle Sheetsに出力する」ワークフローをエージェントとして示している。ポイントは、下記をコードではなく設定で表現している点：
  - 使用するツール（LinkedInコネクタ、Sheets API）の登録
  - プロンプトテンプレートや出力フォーマットの定義
  - エラー時のリトライやフェールオーバー動作
  - 認証情報（環境変数で分離）とスコープ管理
  これにより、同じフローを別のデータソースや別の出力先に「設定差し替え」で転用できる。

- 技術的な利点
  - 再現性：設定ファイルをそのままバージョン管理できる
  - テスト容易性：設定ごとのユニット/統合テストが書きやすい
  - セキュリティ：秘密情報を設定の外（シークレットマネージャ）に切り分けられる
  - ガバナンス：コンプライアンスルール（データ保持、アクセス範囲）を設定ベースで監査可能

- 注意点・制約
  - 設定だけでは高度なロジックやデータ前処理は表現しづらい場面がある（その場合は小さなコードプラグインを使う）
  - 外部APIの利用規約（例：LinkedInのスクレイピング規約）や日本の個人情報保護法に注意が必要
  - ランタイムのオーケストレーションやスケール設計は別途考慮が必要

## 実践ポイント
- 小さく始める：まずは1つのタスク（例：プロフィールから氏名・職歴を抽出してスプレッドシートへ）を設定で定義して動かす
- 設定テンプレートを用意する：プロンプト、ツール定義、エラーポリシーをテンプレ化してチームで共有
- 環境ごとのオーバーライド：dev/stage/prod を設定で切り替え、認証情報はシークレットで管理する
- テストとモニタリング：設定単位でのユニットテスト・実行ログ・レート制御を必ず組み込む
- 法令・利用規約遵守：LinkedIn等のデータ取得は利用規約と個人情報保護を確認し、同意があるデータのみを扱う運用ルールを作る

短く言えば、設定中心のエージェント構成は「速く・安全に・再現可能に」AIワークフローを回す鍵。日本企業の実務でも、まずは小さな取り組みから導入して運用ルールと監査ラインを整えることをおすすめする。
