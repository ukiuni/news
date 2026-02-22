---
layout: post
title: "How I use Claude Code: Separation of planning and execution - Claude Codeの使い方：企画と実装を分離する"
date: 2026-02-22T01:40:01.574Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://boristane.com/blog/how-i-use-claude-code/"
source_title: "How I Use Claude Code | Boris Tane"
source_id: 47106686
excerpt: "plan.mdと注釈サイクルで合意を作り、AI実装を壊さず高速化する方法"
image: "https://boristane.com/assets/blog/how-i-use-claude-code/og.png"
---

# How I use Claude Code: Separation of planning and execution - Claude Codeの使い方：企画と実装を分離する
AIにコードを書かせる前に「計画書」を徹底させるだけで、開発が壊れず速くなる理由

## 要約
Claude Codeを使う際の核は「計画（Plan）と実行（Implement）の厳格な分離」。まず深掘り調査→計画書作成→編集で注釈を入れて合意を作る、合意できたら一気に実装する、というワークフローが効果的だと説明します。

## この記事を読むべき理由
AI支援開発が増える中で「AIに任せたら周辺仕様を壊した」といった失敗は日本のプロジェクトでも頻出します。本記事は実践的な対策（計画の可視化、レビューサイクル、実装ガード）を示すので、プロダクト品質と開発効率を両立したいエンジニア／チームに役立ちます。

## 詳細解説
- フェーズ構成：Research → Plan → Annotate（注釈サイクル）→ Todo → Implement → Feedback。
- Research：対象フォルダや機能を「deeply／in great detail」と指示してClaudeに読み込ませ、必ず永続的な research.md を出力させる。要点は表層読みを防ぎ、チーム側が理解を検証できる成果物にすること。
- Planning：実装方針・コードスニペット・影響ファイル・トレードオフを含む plan.md を生成させる。既存の参照実装（OSSの良例等）を添えて具体性を与えると精度が上がる。
- Annotation Cycle：plan.md をエディタで開き、行単位で注釈（制約や修正、ドメイン知識）を入れる→Claudeに反映させる、を1〜6回繰り返す。「実装するな（don’t implement yet）」の明示的ガードが必須。
- Todoリスト化：実装前に細かなタスク分解を作らせ、プランを進捗トラッカーにする。実装中はここで完了マークを付けさせる。
- Implementation：合意したら一括実装コマンド（例：「implement it all」相当）で進める。実装中は継続的に型チェック／テストを回す、不要なコメントや any を避ける等ルールを事前に定義する。
- フィードバック：実装フェーズは短い指示で修正（「幅を広げて」「2px詰めて」等）。視覚的な問題はスクショで示すのが有効。
- コントロール維持：Claudeの提案は逐一受け入れず、Accept／Modify／Skip／Overrideで選別。APIシグネチャや重要な設計は硬い制約を設定する。
- セッション運用：研究→計画→実装を単一の長セッションで回す運用が有利。計画ドキュメントが永続的状態として残れば、コンテキストコンパクションの影響も抑えられる。

## 実践ポイント
- 常に「deep read」を指示し、research.md を出させる。成果物で理解を検証する。  
- plan.md を必須にして、エディタで必ず注釈を入れる（これが最も価値が出る工程）。  
- 「実装禁止」の明示（実装前ガード）をルール化する。  
- 実装前に粒度の細かい todo チェックリストを作る（進捗はここで管理）。  
- 実装命令は一括で出し、実行中は継続的に型チェック／テストを回す。  
- 参照実装を渡すと設計精度が上がる（既存パターンの踏襲を明示）。  
- 重要なAPIや既存インターフェースは「変更禁止」として明確にする。

このワークフローをチームのルールに落とし込めば、AIが書いたコードに振り回されずに速く安全に開発できます。
