---
layout: post
title: "AI Hallucination Squatting: The New Frontier of Supply Chain Attacks - AIハルシネーション・スクワッティング：サプライチェーン攻撃の新境地"
date: 2026-02-03T13:05:58.160Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://instatunnel.my/blog/ai-hallucination-squatting-the-new-frontier-of-supply-chain-attacks"
source_title: "AI Hallucination Squatting: Weaponizing Fake Dependencies | InstaTunnel Blog"
source_id: 410393711
excerpt: "AIの幻覚で作られた偽パッケージが先行登録され、依存関係経由でマルウェア感染を招く危険"
image: "https://ibb.co/YBsqxTsH%22%3E%3Cimg%20src=%22https://i.ibb.co/3mZLnYZg/AI-Hallucination-Squatting-The-New-Frontier-of-Supply-Chain-Attacks.png"
---

# AI Hallucination Squatting: The New Frontier of Supply Chain Attacks - AIハルシネーション・スクワッティング：サプライチェーン攻撃の新境地
AIが「存在しないライブラリ」を自信満々で薦める隙を突き、攻撃者がその名前を先に登録してマルウェアを配布する――あなたの依存関係がAIの虚構で感染する時代が来ています。

## 要約
LLM（ChatGPTやCopilot等）が架空のパッケージ名を「 hallucinate（幻覚）」し、それを見越して攻撃者が実際に同名パッケージを公開することで、開発者がそのままインストールしてしまいサプライチェーンが侵害される新手法「AI Hallucination Squatting（別名：slopsquatting）」が急増しています。

## この記事を読むべき理由
日本の開発現場でもAI補助コーディングが急速に普及しており、誤情報を信じて依存関係を取り込むだけで企業システムや顧客データが漏洩するリスクがあります。早めの対策がコストと信頼を守ります。

## 詳細解説
- 仕組み：開発者がLLMに質問すると、モデルは「最もらしい」パッケージ名を生成することがあり（例：x-api-connector-py）。攻撃者はその名前を先にPyPIやNPMに登録し、悪意あるペイロードを仕込む。開発者が提示されたインストールコマンドをコピペすると即座に感染する。
- なぜ起きるか：LLMは事実を参照する知識ベースではなく、次のトークンを予測する統計モデルであるため、命名規則やパターンから存在を「推測」してしまう。古い/削除されたライブラリやニッチな要求への応答では特に発生しやすい。
- 特徴：「typosquatting（タイプミス狙い）」と異なり、人間のミス待ちではなく、AIの誤答（deterministicな繰り返し）を利用する点で攻撃効率が高い。研究では同じ偽名が複数回推奨される確率が高く、攻撃者はこれを監視して先回り登録する。
- 実例：研究者が「huggingface-cli」をPyPIに登録したところ、数か月で数万ダウンロードを記録し、大手企業のドキュメントにまで誤ったインストール手順が貼られていた。別の実験ではStack Overflowの質問を大量にLLMに投げ、架空パッケージが頻出したことが示された。
- 影響：APIキーや環境変数、SSH鍵の窃取、内部ネットワーク踏み台化など。企業のCI/CDやドキュメント経路を介した広範なサプライチェーン被害につながる。

## 実践ポイント
- まず検証（Verify, then Trust）：
  - AIが推奨したパッケージは必ず公式リポジトリ／GitHubレポジトリを確認する。
  - ダウンロード数・公開日時・公開者の信頼性をチェック。公開直後でダウンロードが極端に少ないものは疑う。
  - READMEやソースを読み、怪しい自動生成文や空のREADMEはNG。
- 組織的対策：
  - プライベートレジストリ／プロキシ（Artifactory、Nexus等）経由を必須にし、公開パッケージの新規導入ポリシーを設ける（例：公開から30日未満はブロック）。
  - スコープ付きパッケージ（@company/...）の利用を推奨し、サプライチェーンの可視化（SBOM）を導入する。
  - CIでパッケージ信頼度・署名・既知の悪意あるパッケージリストを自動チェック。
  - AI利用ポリシーを整備し、開発者に対して「AI出力は未検証の外部入力として扱う」教育を行う。
- ベンダーへの期待：
  - LLM側でRAG（実リポジトリ照合）を導入し、存在しないパッケージは推奨しない設計を求める。
  - 出典やパッケージ存在の検証を組み込む評価関数の改善。

以上を現場のチェックリストに落とし込み、AIを便利ツールとして使い続けるためには「速さより検証」を徹底してください。
