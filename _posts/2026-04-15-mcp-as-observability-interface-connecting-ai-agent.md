---
layout: post
title: "MCP as Observability Interface: Connecting AI Agents to Kernel Tracepoints - MCPを観測性インターフェースに：AIエージェントとカーネルトレースポイントを直結する試み"
date: 2026-04-15T14:37:41.984Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ingero.io/mcp-observability-interface-ai-agents-kernel-tracepoints/"
source_title: "MCP Observability Interface: AI Agents + Kernel Tracepoints"
source_id: 47778617
excerpt: "MCPでAIがeBPF経由のGPUトレースを直接解析し、未知の遅延原因を即特定する手法を紹介"
---

# MCP as Observability Interface: Connecting AI Agents to Kernel Tracepoints - MCPを観測性インターフェースに：AIエージェントとカーネルトレースポイントを直結する試み
AIエージェントがダッシュボード越しではなく、カーネルレベルの生データを直接問える世界へ。

## 要約
MCP（Model Context Protocol）がAIエージェントとインフラ間の標準インターフェースになりつつあり、Datadogのラップ方式とIngeroのMCPネイティブ（eBPFでCUDAトレースを直接公開）という2つのアプローチが対照的に示された。生データ直結は詳細な根本原因解析を可能にする一方で、認証やデータ露出の新たなリスクも生む。

## この記事を読むべき理由
GPUやオンプレの運用・AI推論基盤を扱う日本の開発者・SREは、AIによる自動化と細粒度なトレース取得が運用効率と障害解析を劇的に変える点を押さえておくべきだから。

## 詳細解説
- MCPの役割：AIクライアントが「ツール」を呼び出すための軽量プロトコル。Datadogは既存の観測プラットフォームをMCPでラップしてAIに渡すアプローチを実装。利点は既存積み上げの有効活用。  
- MCPネイティブの考え方：IngeroはeBPFを用いてCUDAランタイム／ドライバAPIをuprobesでトレースし、結果をSQLiteに格納、7つのMCPツール（例：get_trace_stats, get_causal_chains, run_sql, get_stacks）でAIに直接提供。ダッシュボード集約で失われる因果連鎖やコールスタックがそのまま処理できるため、特定のリクエストだけ遅くなるような問題（例：vLLMで最初のトークンが14.5x遅延）の根本原因を素早く特定できた。  
- 使い分け：集計指向（SLO確認など）はラップ型が向く。根本原因解析や未知の問いに答える「観測性」はネイティブ型が強い。  
- セキュリティ：Qualysの指摘の通り、MCPサーバで静的シークレット利用が多い点は重大。GPUトレースはタイミングやメモリレイアウトから機密情報を漏らす可能性があるため、発見・呼び出しのログ、最小権限、監査トレースが必須。IngeroはMCP呼び出し自体も同じeBPFパイプラインでトレースする設計。  
- 今後の波及：ネットワーク（eBPF）、セキュリティ（syscallトレース）、コスト（実資源計測）など、ダッシュボードを介さず生データをAIに渡すパターンが拡大する見込み。

## 実践ポイント
- 試す（ローカル）：リポジトリをクローンして組み立て、用意された調査DBにMCPクライアントで接続可能。
```bash
git clone https://github.com/ingero-io/ingero.git
cd ingero
make build
./bin/ingero mcp --db investigations/pytorch-dataloader-starvation.db
```
- ローカルAIで調査（例：Ollama/ollmcp）
```bash
pip install ollmcp
# /tmp/ingero-mcp-dataloader.json を作ってから
ollmcp -m qwen3.5:27b -j /tmp/ingero-mcp-dataloader.json
```
- セキュリティチェック：MCPサーバは静的シークレットを避け、発見・呼び出しを必ずログ、MCP操作自体をトレース可能にする。アクセスは最小権限で。  
- 運用への示唆：既存のDatadog等を活かしつつ、原因解析が重要なワークロード（GPU推論、低レイテンシ経路）ではeBPFベースのネイティブ観測を検討すると良い。

（参考）IngeroはOSSで調査DBと実装が公開されているため、まずはローカルで動かして観測データにAIを直接問う体験を推奨。
