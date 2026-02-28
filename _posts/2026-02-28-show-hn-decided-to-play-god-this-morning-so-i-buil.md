---
layout: post
title: "Show HN: Decided to play god this morning, so I built an agent civilisation - エージェント文明を作ってみた（Werld）"
date: 2026-02-28T14:42:46.613Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/nocodemf/werld"
source_title: "GitHub - nocodemf/werld: agentic life simulation from inception"
source_id: 47195530
excerpt: "ローカルで動く進化シムでNEAT風脳を持つ自律エージェント文明を覗く"
image: "https://opengraph.githubassets.com/ea0e50ddaec2be39c87dcc38ada8f4bb2e5deb7054e803bd20135e4c79f5f0ea/nocodemf/werld"
---

# Show HN: Decided to play god this morning, so I built an agent civilisation - エージェント文明を作ってみた（Werld）
魅惑の“デジタルペトリ皿”──自律エージェントが勝手に進化する世界を覗いてみませんか？

## 要約
ローカルで動くエージェントベースの進化シミュレーション「Werld」は、Watts–Strogatz小世界ネットワーク上でNEAT風の可変構造ニューラルネット（脳）を持つ個体が感覚・行動・繁殖・死亡を通じて開かれた進化を遂げる実験環境です。シミュレータは純粋なPython（stdlibのみ）、可視化はNext.jsダッシュボードでSQLiteを介して連携します。

## この記事を読むべき理由
- エージェントベースモデルや進化的学習の「何が自律的に出現するか」を実験的に観察したい人に最適。  
- クラウド不要でローカル実行できるため、企業や教育機関でデータ・プライバシーを守りつつ試せる。  
- NEATや小世界トポロジ、進化アルゴリズムを実装・拡張するハンズオン素材としても有用。

## 詳細解説
- 基盤トポロジ：Watts–Strogatzの小世界グラフを採用し、格子や人工的制約を敷かずに現実らしい局所性＋短経路性を再現。  
- エージェント：感覚チャネル、メモリ、連続的なエフェクタを持ち、29個のゲノム特性で行動や知覚が決まる。通信（フェロモン類似）や季節変化も組み込まれている。  
- 脳（Cortex）：NEATスタイルでトポロジーが変化する可変ニューラルネット。構造が進化して複雑化／単純化する様子を観察できる。  
- 進化プロセス：生殖・突然変異・選択が自然選択の形で働き、エージェントの行動パターンやコミュニケーションが「発見」される設計。  
- 実装と運用：シミュレータはPython 3.10+でstdlibのみ。自動チェックポイント、SIGTERM安全、データは data/simulation.db に保存。ダッシュボード（Next.js、13セクション）は ../data/simulation.db を4秒毎にポーリングして可視化。  
- リポジトリ構成（抜粋）：main.py（エントリ）、config.py（パラメータ）、engine/、agents/、reasoning/（NEAT）、persistence/（SQLite）、dashboard/（Next.js）。

## 実践ポイント
- 試す手順：Python 3.10+ でシミュレータを起動 -> python main.py。短時間試行は --ticks 5000、再開は --resume、クラッシュ自動復帰は --watchdog。  
- ダッシュボード：cd dashboard && npm install && npm run dev、http://localhost:3000 を開く（先にシムを起動）。  
- カスタマイズ：config.py を編集してトポロジー・突然変異率・感覚ゲイン等を変え、挙動の違いを比較する。  
- 研究・教育での活用案：NEATや進化計算の教材、ローカルでの探索実験、エージェントの行動解析パイプライン構築に好適。  
- 貢献：CLAUDE.md にアーキテクチャ詳細、CONTRIBUTING.md に開発ガイド。フォークして新しいゲノム特性や観測指標を追加すると面白い結果が得られます。

興味が湧いたらリポジトリ（nocodemf/werld）をチェックして、まずは短いランで“何が出てくるか”を眺めてみてください。
