---
layout: post
title: "Pocketbase lost its funding from FLOSS fund - PocketBaseがFLOSS/fundの資金提供を断念"
date: 2026-02-18T18:11:28.665Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/pocketbase/pocketbase/discussions/7287"
source_title: "(Cancelled) ~FLOSS/fund sponsorship~ and UI rewrite · pocketbase/pocketbase · Discussion #7287 · GitHub"
source_id: 47062561
excerpt: "PocketBase、FLOSS資金撤回でUI刷新計画が不確実に—Shablonで再設計挑戦中"
image: "https://opengraph.githubassets.com/dd7cda569f8b046fdfeb64dcd95541904749d2863d481ea1122d8b4f260888bf/pocketbase/pocketbase/discussions/7287"
---

# Pocketbase lost its funding from FLOSS fund - PocketBaseがFLOSS/fundの資金提供を断念
魅力的なタイトル: 「人気軽量BaaSの危機？PocketBase、資金提供キャンセルでUI大改造の行方が見えない」

## 要約
PocketBaseの主要メンテナが、FLOSS/fundからのスポンサー資金を規制上の問題と個人情報取り扱いの懸念で辞退。もともとの計画だったフルタイムでのUI書き換えと安定版リリースの予定に不確実性が生じたが、メンテナは依然として独自の軽量フロントフレームワーク「Shablon」でUI再設計を進めている。

## この記事を読むべき理由
PocketBaseはMVPや小～中規模サービスのバックエンド候補として日本でも注目度が高い。資金流入やUI設計方針の変化は、導入・拡張を検討する開発者やプロダクトマネージャーに直接影響します。

## 詳細解説
- 資金撤回の背景：FLOSS/fundは送金をインド経由のワイヤートランスファーで行う提案をしており、メンテナは跨域の書類手続きと個人情報（特にメール等の共有チャネル）の取扱いに懸念を示し、申請撤回を決定。結果的に「1年専従で開発する」という当初見通しは白紙化。
- UIの課題と目標：現状のダッシュボードはカスタマイズ性が乏しく、フィールド拡張、OAuthプロバイダ追加、プロダクション表示のカスタマイズ、UIプラグイン連携などが難しい。目指すのは「外部スクリプトからSPAルータやリアクティビティに介入できる」拡張性。
- フレームワーク選定の苦悩：Svelte等のコンパイラ型は拡張時に利用者へNodeビルドを強いるため避けたい。Vue／Lit等は候補だが依存と将来の互換性リスクがある。
- Shablonの試み：メンテナが作成した0依存の小さなJSフレームワークで、コンポーネント概念を排して生のDOMに最小限のリアクティブ機能を付加するアプローチ。内部の状態管理はProxyベース（signalライク）。ライフサイクル管理はグローバルなMutationObserverを用いる設計で、深い構造での性能評価が課題。
- 開発方針：最終安定版到達後は依存を減らし「完成」状態に近づける方針。現状はUI周りで実験的な取り組みを継続し、当面は機能凍結を行う予定。

## 実践ポイント
- PocketBaseを採用済み／検討中のチームは、予定された安定版リリースに依存しない運用計画を用意する（マイグレーションやカスタムUIの代替を想定）。
- カスタムUI／プラグインを作る場合は、Nodeビルド不要で動的に読み込める設計（ランタイムでのインジェクション、固有プレフィックスでのCSS）を優先すると統合が楽。
- Shablonや関連ディスカッションをウォッチし、互換性やパフォーマンス面での結論を待ってから本番導入を判断する。
- オープンソース資金獲得に関心がある日本のプロジェクトは、国際送金・個人情報規制（例：個人情報保護法や越境移転の要件）を事前にチェックしておくと安心。

元スレッド（GitHub Discussions）でのやり取りは継続しているので、最新情報はリポジトリのDiscussionを確認することを推奨。
