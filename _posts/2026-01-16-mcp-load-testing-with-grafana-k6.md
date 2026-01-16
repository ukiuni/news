---
layout: post
title: "MCP load testing with Grafana k6 - Grafana k6で実装するMCP負荷テスト"
date: 2026-01-16T11:22:27.812Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://infobip.com/developers/blog/implementing-mcp-load-tests-with-grafana-k6"
source_title: "Implementing MCP load tests with Grafana k6  - Infobip Developers Hub | Infobip Developers Hub"
source_id: 425521440
excerpt: "k6でMCP負荷を再現し、ツール呼び出し由来のHTTPスパイクやタイムアウトを発見"
image: "https://www.infobip.com/developers/wp-content/uploads/2026/01/Grafana-dashboards-k6-load-testing-AI-tool-calls-image-with-blue-and-green-hues.jpg"
---

# MCP load testing with Grafana k6 - Grafana k6で実装するMCP負荷テスト
AIエージェントの“考える時間”と突発的なリクエストを再現する、現場で使える負荷試験の実践レシピ

## 要約
k6を拡張してMCP（AIエージェント→ツール連携を扱うプロトコル）レベルで負荷を測定すると、1つのMCP呼び出しが複数のHTTPリクエストを生む実態が分かり、帯域やタイムアウト、セッション保持の問題を検出・改善できる。

## この記事を読むべき理由
日本のプロダクトでもAIエージェントを本番投入すると、突発的な「考える時間（idle）」やツール呼び出しに伴うHTTPスパイクで思わぬ障害が起きます。MCPレベルでの負荷試験は容量計画だけでなく、タイムアウト設定やセッション設計といった運用改善につながります。

## 詳細解説
- ツールと手法の選定  
  Grafana k6を採用し、JavaScriptで「ラamping VUs（仮想ユーザー増減）」を定義してAIエージェントの挙動を模擬します。k6は拡張可能で、Infobipはxk6-infobip-mcp拡張を作成してMCP呼び出しを扱えるようにしました。

- ランプシナリオ例（要点）  
  100個のエージェントを次の3段階でシミュレート：30秒かけて徐々に増加→30秒維持→10秒で優雅に停止。設定例：
```javascript
export const options = {
  scenarios: {
    llm_spike_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 100 },
        { duration: '30s', target: 100 },
        { duration: '10s', target: 0 },
      ],
      gracefulStop: '5s',
    },
  },
};
```

- ランダムな「考える時間」の再現  
  各仮想ユーザーの呼び出し末尾でランダムに待機することで、会話の間（LLMがどのツールを呼び出すかを決める“thinking”）を模倣します。
```javascript
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';
sleep(randomIntBetween(5, 10));
```

- 重要な観察点：MCP vs HTTPの差分  
  テストで得られた結果例では、約17 MCP/s が約52 HTTP/s を生み出すなど、MCP呼び出し1件が複数のHTTPリクエストを発生させるケースが明確に確認されました。従って単にHTTPのみを測ると本質を見誤ります。

- レポート活用（端末出力とHTML）  
  k6は端末出力で手早く要点を確認でき、HTMLレポートで帯域やエラー発生タイミングを相関させられます。例えば帯域がボトルネックなら転送レートが頭打ちになりますが、増加が続くなら別の原因（タイムアウトやインスタンス切替など）を疑います。

- 実際に発見された問題と対策  
  1) タイムアウト：ロードバランサー側のタイムアウトが短く、長時間処理するMCPツールでコネクション切断が発生。対策として「段階的タイムアウト」を採用し、外部LBを最長に、内部処理は短めに設定して接続を保つ設計に。  
  2) インスタンスホッピングと遅延：リクエストが短時間で別インスタンスへ移ることでキャッシュ（RAM）の“warm”状態が失われ、SSE切断や高遅延が発生。対策として「スティッキーセッション」を導入（MCP Session IDヘッダーまたはクライアントIPによるルーティングの両方をサポート）して安定化。

- 今後の拡張案  
  k6のdisruptor拡張で冗長系の自己回復検証、あるいはMCP出力データ量をLLMトークン換算して無駄なトークンコストを可視化する仕組みなどが挙がっています。

## 実践ポイント
- まずはk6でラamping-vusシナリオを作って「突発＋idle」を再現する。上の設定で手早く試せます。  
- MCPレベルのメトリクス（mcp_calls, mcp_call_duration など）を必ず収集し、HTTPのみの指標に頼らない。  
- レポート（HTML）で転送レートやピーク時の相関を確認し、帯域かアプリの処理が原因かを切り分ける。  
- 見つかった症状に対しては：  
  - LBやプロキシのタイムアウトを見直し、長い処理パスには段階的タイムアウトを採用する。  
  - セッションステートが有効なケースはスティッキーセッションを検討（Session ID／IPの両対応で互換性を確保）。  
- 既製の拡張（xk6-infobip-mcpなど）を使ってMCPをk6に組み込み、テストコードを公開リポジトリで共有すると再利用性が高まる。

短いまとめ：MCPのようなAIツール呼び出し系は「1リクエスト＝1HTTP」ではない。k6で実際の会話パターンを再現してMCPレベルで評価すれば、運用に直結する隠れた問題を早期に発見できます。
