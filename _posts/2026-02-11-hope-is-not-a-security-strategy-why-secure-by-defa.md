---
layout: post
title: "Hope Is Not a Security Strategy: Why Secure-by-Default Beats Hardening - 希望はセキュリティ戦略ではない：ハードニングよりも「デフォルトで安全」を選ぶ理由"
date: 2026-02-11T07:16:37.429Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tuananh.net/2026/02/09/hope-is-not-a-security-strategy/"
source_title: "Hope Is Not a Security Strategy: Why Secure-by-Default Beats Hardening - Tuan-Anh Tran"
source_id: 1289177666
excerpt: "AIエージェント時代、microVM/WASMでデフォルト隔離しないと重大事故を招く理由を解説"
---

# Hope Is Not a Security Strategy: Why Secure-by-Default Beats Hardening - 希望はセキュリティ戦略ではない：ハードニングよりも「デフォルトで安全」を選ぶ理由
「共有カーネル＋祈り」はもう通用しない――AIエージェント時代の“当たり前”を変えるセキュリティ戦略

## 要約
AIエージェントは非決定的（underdeterministic）で、従来のハードニングやポリシーだけでは対処できない。解は「デフォルトで隔離（secure-by-default）」する設計――microVM／WASMなどで信頼の境界を引くこと。

## この記事を読むべき理由
日本の企業・開発チームでもAIツール導入が進む中、従来の「イメージを固めて監視する」アプローチではリスクが残る。規制対応や金融・製造など重要インフラを扱う現場ほど、隔離を前提にした設計が急務です。

## 詳細解説
- エージェントの問題点：出力や振る舞いを事前に列挙できないため、ポリシーで「悪い挙動」を完全に防げない（underdeterminism）。  
- 従来の対応：イメージハードニング、seccomp／eBPF／runtime検出、監視→対応。だがこれらはすべて同一カーネル上で動作し、カーネルが破られれば無力化される。  
- 解決策：ハイパースケール由来の考え方を取り入れ「すべて未信頼として隔離する」。gVisor／Firecracker／microVM、WASMベースのサンドボックス（例：WASMランタイム、MCPサンドボックス）で強い境界を作る。  
- 運用の現実：採用が進まない理由は導入の面倒さ・開発者体験の悪さ。だが技術自体（microVM, gVisor, Firecracker, WASM）は成熟しつつあり、目的は「簡単に使える形で標準化」すること。

## 実践ポイント
- エージェントやツール呼び出し(MCP)は必ずサンドボックス化する（microVM/WASMを優先）。  
- カーネル上の検出器（eBPF等）だけに依存しない。検出＋隔離の二重防御を設計する。  
- 既存クラスターは段階的に「隔離ノード／ランタイム」を導入し、密度最適化と境界確保を両立する。  
- 開発者体験を改善するため、CI/CDに隔離ランタイムを組み込み、テンプレ化して採用障壁を下げる。  
- 小規模から試す：FirecrackerやWASMベースのサンドボックスをPoCで評価し、性能・運用コストを把握する。

以上。セキュリティは「祈り」ではなく「設計」で決まります。
