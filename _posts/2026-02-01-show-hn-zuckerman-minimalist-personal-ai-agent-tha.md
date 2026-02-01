---
layout: post
title: "Show HN: Zuckerman – minimalist personal AI agent that self-edits its own code - Zuckerman — 自分のコードを自己編集するミニマルな個人AIエージェント"
date: 2026-02-01T16:12:02.916Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/zuckermanai/zuckerman"
source_title: "GitHub - zuckermanai/zuckerman: A personal AI that starts minimal, self-improves in real-time, and shares its discoveries with other agents."
source_id: 46846210
excerpt: "実行中にコードを自己編集し即進化、TypeScript製でホットリロード対応の個人用AI"
image: "https://opengraph.githubassets.com/dd4d6d2bc346a1505b3ddf1341db937c1c6ec26b471c51b66751084dce2f37a0/zuckermanai/zuckerman"
---

# Show HN: Zuckerman – minimalist personal AI agent that self-edits its own code - Zuckerman — 自分のコードを自己編集するミニマルな個人AIエージェント

自分で書き換えて成長する「ミニマルな個人AI」。最小限で始め、実行中に自己編集して即時進化し、改善を共有する実験的なエージェント群の提案。

## 要約
ZuckermanはTypeScriptで書かれた軽量な個人AIフレームワークで、設定やツール、場合によっては自分のコードまでプレーンテキストで編集し、ホットリロードで即時に反映することを目指すプロジェクトです。

## この記事を読むべき理由
- 大規模なエージェント群（例：OpenClaw）に比べ、導入障壁が低く実験に向くため、個人やチームで「自動化／カスタムAI」を試すのに最適。  
- 日本のプロダクトや業務プロセスに合わせた小さな自律エージェントを安全にプロトタイプする手法として有用。

## 詳細解説
- 基本方針：超ミニマルで起動→実行中に自己改良→改善を共有、というシンプルなループを重視。  
- 技術スタック：主にTypeScript、CLIとElectronフロントエンドの二重UI。Voice（TTS/STT）や複数メッセンジャー（Discord/Slack/Telegram等）に対応。  
- アーキテクチャ（概念）：  
  - World（src/world/）: 軽量OS層。通信、実行、ランタイム生成、設定ローダーなどを担う。  
  - Agents（src/agents/）: 各エージェントはフォルダ単位で定義され、コアモジュール・ツール・セッション・人格（プロンプト）を持つ。  
  - Interfaces（src/interfaces/）: ユーザーや外部とやり取りする入口（CLI/Electronなど）。  
- コア機能：プレーンテキストでの設定/コード管理、即時ホットリロード、機能のバージョン管理、複数エージェント運用、共有プラットフォームへの提案/採用フロー。  
- セキュリティ：認証・ポリシーエンジン・サンドボックス（Docker）・シークレット管理等の基礎は用意されているが、自己改良機能は慎重な運用が必須（権限やプロンプト注入のリスクあり）。  
- ライセンス：AGPL-3.0。商用利用や公開時のライセンス影響に注意。

## 実践ポイント
- ローカルでまず試す（サンドボックス環境を推奨）。  
- すぐ使えるコマンド（リポジトリで実行）:
```bash
git clone https://github.com/zuckermanai/zuckerman.git
cd zuckerman
pnpm install
pnpm run dev
```
- エージェントの振る舞いは src/agents のプレーンテキストファイルを直接編集すれば即時反映されるので、プロンプトやツール追加で素早く試作できる。  
- 実運用前に：APIキーや権限は最小化、Docker等で隔離、変更履歴とレビュー運用を必ず設ける。AGPLの適用範囲も確認すること。  
- 日本語の業務自動化やチャット連携に適用する際は、ローカル辞書／形態素処理との組み合わせや、社内ポリシーに沿った権限設計を優先する。

短時間でプロトタイプを回したいエンジニアやチームにとって、Zuckermanは「自分で育てるAI」を体験する良い入り口になります。
