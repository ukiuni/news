---
layout: post
title: "An Honest Review of Google Antigravity - Google Antigravity の正直レビュー"
date: 2026-01-09T15:43:31.957Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/fabianfrankwerner/an-honest-review-of-google-antigravity-4g6f"
source_title: "An Honest Review of Google Antigravity - DEV Community"
source_id: 3135773
excerpt: "Agent主導で自動生成強力、だがバグ多発で本番導入は要注意"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F3m4zp72vmm1jd6zz52uv.png"
---

# An Honest Review of Google Antigravity - Google Antigravity の正直レビュー
未来のIDEか、それともバグだらけのプロトタイプか？Google Antigravityを1週間使って見えた光と影

## 要約
Google製のVS Code系IDE「Antigravity」は、Agent第一の新しいワークフローと最新モデル（Gemini 3 等）を統合し、コード生成からアセット作成、ブラウザ自動操作まで一体化した未来志向のツールだが、現状はバグや拡張互換性の問題が目立ち、まだ実戦的なメイン環境には厳しい。

## この記事を読むべき理由
VS Codeが日本でも圧倒的シェアを持つ中、GoogleがIDE市場に本気で介入すると開発者体験やツール競争が大きく動きます。新しい「Agent-First」設計やブラウザ統合は、日本のプロダクト開発／プロトタイピングにも即戦力となり得るため、その長所・短所を早めに把握しておく価値があります。

## 詳細解説
- コア技術と見た目  
  Antigravityは内部的にVS Code OSSをベースにしており、UIや名称を独自化している。記事では一部Windsurf由来と思しき痕跡（"Cascade"）が見つかったと報告されており、短期間で立ち上げるための技術取り込みが疑われる。

- 「Three Surfaces」設計  
  1) Editor：従来のコード編集画面。  
  2) Browser：統制されたChromeインスタンスを直接操作できる。  
  3) Agent Manager：タスクごとにエージェントを管理する別ウィンドウで、エージェントの状態（思考中・承認待ち・失敗）をInbox的に扱う。  
  この分離により「複数プロジェクトを並行管理して、必要なときだけエディタにフォーカスする」新しい開発フローが実現されている。

- モデルと実力（Gemini 3 等）  
  Gemini 3 / 2.5を使った自動生成は強力。著者は「古いゲームのクローン（物理・スプライト生成含む）」を一発で動く状態にまで作らせた例を挙げている。画像生成→ファイル注入→コード更新の一連の流れをAgentが自律的にやる点が大きな特徴。

- ブラウザ連携と検証機能  
  Chromeと密に連携し、エージェントがブラウザ上で操作（カーソルの動き、クリック等）を実行・録画し、エラー時のスクリーンショットや「Walkthrough」アーティファクトを残す実演機能がある。E2E的な自動検証やデモ作成に便利。

- 問題点（現状の短所）  
  - バグ多発：ボタンが効かない、サイドバーのアイコン消失などUX不安定。  
  - 拡張互換性：Svelte拡張が動作せずエディタ全体を壊す例あり。  
  - 基本的な操作の欠落：ファイルエクスプローラーで矢印キーが効かない等、基本UXの欠如が指摘されている。  
  - プロ向け機能未実装：Git Worktrees未対応など、マルチブランチ高速切替を期待する開発者には痛手。  
  - リソース消費：Electron＋常時ストリーミングでバッテリー消費と入力遅延が発生しやすい。  
  - 無料プレビューだがクォータ制限あり（記事では5時間毎にリセットする仕様を確認）。

- セキュリティ／信頼性の観点  
  コードやテレメトリをどこまでGoogleに預けるかは企業ごとに判断が必要。日本の受託開発や金融系ではオンプレやデータ保護ルールが厳しいため慎重な採用検討が望まれる。

## 実践ポイント
- 今すぐやるべきこと  
  - サイドプロジェクトやプロトタイプでまず試す：本番の締切がある案件は避ける。  
  - 拡張互換性を確認：自分の主要拡張（例：Svelte, TypeScript, LSP系）が動くか事前チェックする。  
  - リソース監視：開発中はCPU/メモリ・バッテリーの消費を監視する。長時間作業は避ける。  
  - クォータ挙動を把握：無料プレビューの制限（5時間リセットなど）をテストして運用設計する。  
  - セキュリティ方針確認：企業利用ならデータ送信先・ログの扱いを法務/情報システムと擦り合わせる。  
- どう使い分けるか  
  - 早期採用者／イノベーター：Agentワークフローや自動アセット生成を評価して継続的に試す。  
  - 安定性重視の現場：当面はVS Code＋成熟したAIツール（例：Cursor等）を併用し、Antigravityは補助的に使う。  
- フィードバックを送る  
  プレビュー段階なのでバグや拡張の互換性問題を報告すると改善が早まる可能性が高い。

結論：Antigravityは「やってくれそうな未来」を覗かせる強力な試作機。Geminiベースの自動生成やブラウザ統合は革新的だが、現時点ではバグと欠機能が目立つため、まずは実験用途で試し、安定運用はもう少し様子見が賢明。
