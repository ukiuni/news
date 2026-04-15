---
layout: post
title: "Show HN: Libretto – Making AI browser automations deterministic - Libretto — AIでブラウザ自動化を決定論的にするツールキット"
date: 2026-04-15T17:41:11.882Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/saffron-health/libretto"
source_title: "GitHub - saffron-health/libretto: The AI toolkit for building and maintaining browser automations · GitHub"
source_id: 47780971
excerpt: "Librettoで画面操作をAPI化し、AIで安定化するブラウザ自動化ツール"
image: "https://opengraph.githubassets.com/3001e7841d4ee781480e3e93029d4938acb6a7427a329b66650a8e3cc07a1926/saffron-health/libretto"
---

# Show HN: Libretto – Making AI browser automations deterministic - Libretto — AIでブラウザ自動化を決定論的にするツールキット
魅力的なタイトル: 「ブラウザ自動化の“ゆらぎ”を消す――LibrettoでAI×ブラウザ操作を安定化する方法」

## 要約
Librettoは、コード側エージェントに“生きたブラウザ”を与え、スクショ＋HTMLのスナップショット解析やネットワークキャプチャでUI自動化を安定化・高速化するオープンソースのツールキットです。

## この記事を読むべき理由
日本のプロダクトやSIで多い「画面操作に依存した連携」が壊れやすい問題を、AIによるスナップショット解析やネットワーク逆解析で解決できる可能性があるからです。特に医療・保険・金融系の既存Webサービス連携で有用です。

## 詳細解説
- 目的と設計思想  
  - Librettoは「エージェント（コード）が実際のブラウザを操作しつつ、視覚情報はLLMに任せて最小限のコンテキストで解析する」仕組みを取ります。これによりエージェントのトークン消費を抑えつつ、UI変化にも対応しやすくします。

- 主な機能  
  - ライブブラウザ操作：ヘッド付き/ヘッドレスでページを開き、手動操作も混ぜてワークフローを作成可能。  
  - スナップショット解析：PNG＋HTMLをLLMで解析し、セレクタ抽出や失敗原因の診断を行う（モデルはOpenAI/Anthropic/Gemini/Vertex等に対応）。  
  - ネットワークキャプチャ：ブラウザのリクエストを記録してAPIを逆解析し、UI操作を直接API呼び出しに変換して高速化・安定化。  
  - アクション録画＆再生：ユーザーのブラウザ操作を記録してPlaywrightスクリプトへ変換。  
  - セッション／プロファイル管理：.libretto以下に各セッションの状態（ネットワークログ、アクション、スナップショット）を保存。プロファイルで認証状態を再利用可能。  

- ワークフロー例（用途）  
  - UI操作をして得られた手順を自動でPlaywrightスクリプト化。  
  - 画面の壊れたセレクタを再現・診断して自動修正。  
  - UI→APIに置き換えて速度と信頼性を改善、同時にセキュリティ上のリスク（Cookie等）を解析。

- 技術スタックと開発者体験  
  - TypeScript主体、CLIで操作（npx libretto ...）。テストや開発用スクリプトが整備されており、既存のエージェントやPlaywrightワークフローに組み込みやすい。

## 実践ポイント
- まず手元で試すコマンド（初回セットアップ）:
```bash
# bash
npm install libretto
npx libretto setup      # 初回セットアップ（Chromium取得、モデルのピン留め）
npx libretto open https://example.com
npx libretto snapshot --objective "ログイン画面のボタンを特定" --context "メールアドレス入力済み"
```
- LLMキーは環境変数（OPENAI_API_KEY 等）か .env に置く。設定は .libretto/config.json に保存される。  
- 既存のUI自動化が壊れる・遅いなら、ネットワークログからAPI化を検討する（Librettoが一部自動化を支援）。  
- セキュリティとプライバシー：キャプチャされるデータ（スクショ/ネットワーク/クッキー）はローカルの .libretto に保存されるため、機密データの取り扱いポリシーを整備すること。  
- 日本の現場での活用案：レガシーなWebベースの医療・保険システム、業務用SaaSの画面連携、自動テストの復元力向上に特に効果が見込めます。

ライブラリとドキュメントは GitHub（saffron-health/libretto）で公開中。興味があるならまず npx libretto setup で手を動かしてみてください。
