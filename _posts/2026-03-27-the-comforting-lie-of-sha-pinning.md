---
layout: post
title: "The Comforting Lie Of SHA Pinning - SHAピンニングの安心という幻想"
date: 2026-03-27T22:03:59.458Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.vaines.org/posts/2026-03-24-the-comforting-lie-of-sha-pinning/"
source_title: "The Comforting Lie Of SHA Pinning"
source_id: 949207684
excerpt: "SHAピンだけで安心すると、フォーク経由の悪意コミットでActionsが乗っ取られる危険"
image: "http://www.vaines.org/posts/2026-03-24-the-comforting-lie-of-sha-pinning/featured.png"
---

# The Comforting Lie Of SHA Pinning - SHAピンニングの安心という幻想
あなたのGitHub Action、SHAで守れていると思ってない？見た目は同じでも“フォーク由来の悪意あるコミット”に差し替えられる実例

## 要約
GitHub Actionsで「コミットSHAでピン留めすれば安全」という常識は危険。SHAは内容を指すが、リポジトリスコープで検証されないため、フォーク経由で攻撃者のコミットに差し替えられる危険がある。

## この記事を読むべき理由
Trivy等のサプライチェーン侵害が示すように、日本の開発現場でも外部アクションやパッケージに依存するワークフローが増加中。見た目だけのベストプラクティスに頼ると、レビューやCIで秘密情報が漏洩するリスクがあります。

## 詳細解説
- 背景：近年のトピックス（Trivyやnpmの事例）は、サプライチェーンが「信頼と慣習」でつながっていることを露呈した。対策として「依存をピン留め（pin）せよ」、GitHub Actionsでは「タグではなくコミットSHAを使え」という推奨が広まった。  
- なぜ安心できないか：人は「owner/repo@SHA」を見ればそのリポジトリの特定コミットだと想像するが、GitHub Actionsのランナーはコミットオブジェクトをグローバルに解決する。フォークに同じコミットオブジェクトが存在すれば、そのコミットを実行してしまう。つまりPRでSHAだけ差し替えられれば、見た目のowner/repoは同じまま攻撃コードが実行される。  
- タグ vs SHAのトレードオフ：タグはリポジトリスコープだが移動（mutable）する。SHAは内容指向で不変に見えるが、複数リポジトリに到達可能な点で「スコープされていない」。結果として「タグは人に優しいが移動のリスク」「SHAは機械的に不親切で人のチェックを無理にする」という新たな弱点が生じる。  
- サプライチェーンの現実：Secretsがワークフローで暗黙的に利用できる点、レビューが差分やowner名にしか注目しないことなど、人間側の運用ミスとプラットフォーム挙動の組合せが被害を生む。

## 実践ポイント
- SHAを使う場合でも「そのSHAが本当に指定したowner/repoに属するか」をAPIやgit ls-remoteで検証するプロセスを入れる。  
- 外部アクションはMarketplaceや公式配布元、署名付きリリース（sigstore/cosign等）を優先する。  
- 重要ワークフローでの第三者アクション利用を減らし、自前で管理する（リポジトリ内にコピーするか、内部ライブラリ化）。  
- ワークフローの権限を最小化し、シークレットアクセスを不要化する。Pull Requestからのワークフロー実行に制限をかける。  
- レビュー時チェックリストを運用し、「SHAがどこから来たか」「そのコミットが指定リポジトリに存在するか」を必須項目にする。  
- 可能ならリポジトリ側でタグの不変化（immutable tags）や署名付きタグ運用を検討する。  

短く言えば、「SHAピンニングだけで安心するな」。ツールと運用の両方で「出所（provenance）」を検証する仕組みを組み込むことが最短の被害軽減策です。
