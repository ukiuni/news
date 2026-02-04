---
layout: post
title: "Show HN: Ghidra MCP Server – 110 tools for AI-assisted reverse engineering - Ghidra MCP サーバー — AI支援リバースエンジニアリングのための110のツール"
date: 2026-02-04T10:27:07.790Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/bethington/ghidra-mcp"
source_title: "GitHub - bethington/ghidra-mcp: Production-grade Ghidra MCP Server — 132 endpoints, cross-binary documentation transfer, batch analysis, headless mode, and Docker deployment for AI-powered reverse engineering"
source_id: 46882389
excerpt: "Ghidra MCP Serverで110の解析ツールがAI連携し、バイナリ解析を自動化・高速化"
image: "https://opengraph.githubassets.com/ed00a1ac4198cb7f8d2935846cebb8521bfd542e37cbc56de088e1128967a3c2/bethington/ghidra-mcp"
---

# Show HN: Ghidra MCP Server – 110 tools for AI-assisted reverse engineering - Ghidra MCP サーバー — AI支援リバースエンジニアリングのための110のツール

魅力的タイトル: GhidraがAIと手を組むとこうなる――「Ghidra MCP Server」でバイナリ解析が自動化・高速化する理由

## 要約
Ghidra MCP Serverは、Ghidraの解析能力をModel Context Protocol(MCP)経由で外部AIや自動化ツールに公開するプロダクション向けブリッジで、110以上の解析ツールとバッチ操作、クロスバイナリ文書伝搬などを備えます。

## この記事を読むべき理由
日本でも組込みファームウェア解析、脆弱性調査、マルウェア解析、レガシーソフトのリバースなど需要が高く、Ghidra を AI や自動化パイプラインに組み込むことで作業効率と再現性が大きく上がります。本ツールはCI連携やヘッドレス運用が可能で、現場での実務導入に直結します。

## 詳細解説
- 何をするか：GhidraMCP.jar（Ghidraプラグイン）と bridge_mcp_ghidra.py（Pythonブリッジ）で、Ghidraの関数解析、デコンパイル、メモリマップ、ストリング抽出、構造体生成などをHTTP/MCP経由で操作可能にします。  
- 主要機能：110のMCPエンドポイント（関数一覧、デコンパイル、コールグラフ、型操作、ラベル/リネーム、バルク編集、スクリプト管理、クロスバイナリ関数ハッシュと文書の伝搬など）。バッチ操作でAPIコールを大幅削減し原子トランザクションをサポート。  
- 運用面：ヘッドレスモードやDocker展開、バッチ解析、バージョン対応の自動デプロイ、詳細なログ機能があり「開発→テスト→デプロイ→検証」の循環を自動化できます。  
- 技術要件：Java 21、Maven、Ghidra 12.x、Python 3.8+。GhidraのJARをlibにコピーしてビルド（mvn package）、bridgeを起動してGhidra側でMCPサーバを有効化します。  
- AI連携：LLMやClaude等のAIに対して標準化された解析コンテキストを渡せるため、プロンプトに解析結果や関数ドキュメントを供給してAIによる要約／修正提案／自動命名が可能になります。

## 実践ポイント
- まずはローカル検証：リポジトリをクローンし、Ghidraの必要JARをlibにコピーしてビルド、bridge_mcp_ghidra.py（stdio推奨）で起動して手元のバイナリを解析してみる。  
- Docker/CI化：ヘッドレスでのバッチ解析をCIに組み込み、定期スキャンやリリース前の解析パイプラインに組み込むと効果が高い。  
- クロスバイナリ文書化：関数ハッシュ索引を作成して別バージョンへドキュメントを適用すれば、アップデート後の再解析コストを大幅に削減できる。  
- 小さく始める：まずは「関数一覧→デコンパイル→ラベル自動付与」の自動化から。バルク操作を使うとAPI呼び出し回数が劇的に減る。  
- セキュリティ注意：解析対象が商用/機密バイナリの場合は取り扱いと環境分離（オフライン/隔離環境）を徹底する。

元リポジトリ（導入手順・詳細ドキュメント）：https://github.com/bethington/ghidra-mcp
