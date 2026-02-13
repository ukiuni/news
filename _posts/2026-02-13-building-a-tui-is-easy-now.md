---
layout: post
title: "Building a TUI is easy now - TUI開発は今や簡単に"
date: 2026-02-13T21:23:59.712Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hatchet.run/blog/tuis-are-easy-now"
source_title: "Hatchet · Building a TUI is easy now"
source_id: 47005509
excerpt: "Claude CodeとCharmで2日開発、ASCII流用で高速TUIを短期間で実用化する方法"
image: "/assets/og-PqKfvZWg.png"
---

# Building a TUI is easy now - TUI開発は今や簡単に
ターミナルで作る神速UI — Claude CodeとCharmで“2日開発”を実現する方法

## 要約
HatchetはClaude Code（ターミナル向けコーディングエージェント）とCharmスタックを組み合わせ、短期間で実用的なTUIを構築・安定化させました。ポイントは「既存フロントエンド参照」「モジュール設計」「エージェント駆動のテストループ」です。

## この記事を読むべき理由
日本の開発者はターミナル作業やIDE内完結を好む傾向があり、情報密度の高いTUIは生産性向上に直結します。本稿は初級者にも分かる形で、実践的な手順と注意点をまとめます。

## 詳細解説
- なぜTUIか：ブラウザUIと同じAPIを使っても、テキスト中心のTUIは「速さ」「情報密度」「コードとの連携」を強化。IDE→ブラウザの往復を減らせる利点が大きい。  
- 使った技術スタック：Charm社のライブラリ群（Bubble Tea、Lip Gloss、Huh）を採用。React系のようなUI設計に相当するTUI専用ライブラリで、テーマやスタイルの再利用が容易。  
- エージェント活用（Claude Code）：TUIの初期テストや操作フロー確認をClaude Codeに任せ、tmuxのcapture-pane等でレンダリング結果を取得して検証するワークフローが高速で効果的だった。  
- 既存フロント参照の重要性：既存のフロント実装（コンポーネント・フック・OpenAPI生成クライアント）を「参考実装」として与えると、エージェントがビジネスロジック優先でUIを組める。  
- 図（DAG）レンダリングの解決：React Flow相当をTUIに移植するのは難しいため、既存のASCIIグラフ実装（例: mermaid-ascii）を取り込み、Claude Codeに組み合わせさせて短期間で動くDAGビューを作成した。  
- テスト戦略：エージェントによる自動操作で「初回の広い網羅」を作り、手動テスト＋ユニットテストでクリティカル箇所を固める。結果としてイテレーションが収束しやすかった。

## 実践ポイント
1. Charmスタック（Bubble Tea / Lip Gloss / Huh）でまずプロトタイプを作る。  
2. 既存フロントを参照実装として用意し、APIクライアントはOpenAPIで自動生成する。  
3. Claude Codeのようなターミナル対応コーディングエージェントに、tmux+capture-paneで画面を見せつつ最初の操作・テストを任せる。  
4. 複雑な可視化は最初から作らず、既存のASCIIライブラリ（mermaid-ascii等）を流用して実装を速める。  
5. エージェント任せの後に必ず手動確認／ユニットテストを追加して安定化する。  
6. 小さく出してユーザーのフィードバックを得る（日本の現場でも「速さ」を評価されやすい）。

ライブデモ：https://tui.hatchet.run

以上を踏まえれば、TUIは想像よりずっと手軽に試作でき、実際の業務改善につながります。
