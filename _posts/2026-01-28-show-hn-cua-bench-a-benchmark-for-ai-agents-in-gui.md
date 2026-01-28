---
layout: post
title: "Show HN: Cua-Bench – a benchmark for AI agents in GUI environments - Cua-Bench — GUI環境で動くAIエージェントのベンチマーク"
date: 2026-01-28T16:05:21.674Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/trycua/cua"
source_title: "GitHub - trycua/cua: Open-source infrastructure for Computer-Use Agents. Sandboxes, SDKs, and benchmarks to train and evaluate AI agents that can control full desktops (macOS, Linux, Windows)."
source_id: 46768906
excerpt: "実機に近いGUIをAIが操作するCua基盤で即PoCを始めよう"
image: "https://opengraph.githubassets.com/968c1e1de987101a1426008d831e1e5ec21df427abe96772c46c1f7c6824c830/trycua/cua"
---

# Show HN: Cua-Bench – a benchmark for AI agents in GUI environments - Cua-Bench — GUI環境で動くAIエージェントのベンチマーク
実機デスクトップをAIに任せる時代へ。Cuaで「画面を見て操作する」エージェントを自分の環境で試そう

## 要約
Cuaは「コンピュータを操作できるAIエージェント」を開発・評価するためのオープンソース基盤で、隔離されたサンドボックス（Docker、QEMU、Apple Virtualization）・SDK・ベンチマーク（cua-bench）を提供します。GUI操作やコード実行を自動化するエージェントのトレーニングと評価がすぐに始められます。

## この記事を読むべき理由
日本でもRPA、UIテスト、自動化ツール、LLMを使った支援ツールの需要が高まっています。Cuaは「実機に近い環境で画面を操作するAI」をローカルで安全に試作・評価できるため、プロトタイプ作成や社内PoCに即役立ちます。

## 詳細解説
- 構成要素：cua-agent（エージェントフレームワーク）、cua-computer（デスクトップ制御SDK）、cua-bench（ベンチマーク／強化学習環境）、lume（Apple Silicon向け仮想化）など。
- サンドボックス：DockerやQEMU、AppleのVirtualization.Frameworkを使ってフルデスクトップを隔離実行。実機に近い挙動でUI操作を検証可能。
- ベンチマーク：OSWorld／ScreenSpot／Windows Arenaなどのシナリオ群でエージェント性能を評価し、操作の軌跡（trajectories）を学習データとしてエクスポート可能。
- 開発体験：Python（3.12/3.13）で簡単にエージェントを起動できるAPIを提供。以下は起動例（概念）：

```python
from computer import Computer
from agent import ComputerAgent

computer = Computer(os_type="linux", provider_type="cloud")
agent = ComputerAgent(model="anthropic/claude-sonnet-4-5-20250929", computer=computer)

async for result in agent.run([{"role":"user","content":"Open Firefox and search for Cua"}]):
    print(result)
```

- ライセンス・実装注意：プロジェクトはMITだが、一部コンポーネントにAGPLやCC-BYが含まれる点に注意。機密データや企業環境で使う際は自己ホスティングや隔離実行を推奨。
- 活動度：GitHubで活発にメンテされており、スター数・リリースも多い（コミュニティや拡張が期待できる）。

## 実践ポイント
- ローカルで試す：Dockerベースイメージを作成してcb runでベンチマークを回す（例：`cb image create linux-docker` / `cb run dataset ...`）。
- macOS（Apple Silicon）ではLumeでネイティブ近いVMが使えるため、mac固有のUIワークフロー検証が容易。
- 日本語対応：UIのロケールや日本語入力周りは挙動が変わるため、必ず日本語環境でテストしてから運用へ移行する。
- セキュリティ／コンプライアンス：個人情報を含む操作を学習データに含めない、またAGPL依存パッケージの利用可否を確認する。
- 活用アイデア：社内のGUIテスト自動化、カスタマーサポート向け操作補助、業務プロセスの自動化PoC、エージェントのデータ収集と強化学習用トラジェクトリー生成。

元リポジトリ（trycua/cua）は実用的なツール群とドキュメントが揃っているので、まずはサンドボックスで小さなシナリオを走らせて振る舞いを確認することをおすすめします。
