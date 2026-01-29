---
layout: post
title: "OTelBench: AI struggles with simple SRE tasks (Opus 4.5 scores only 29%) - OTelBench：AIは単純なSRE作業でも苦戦（Opus 4.5 の成功率はわずか29%）"
date: 2026-01-29T17:02:49.393Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://quesma.com/blog/introducing-otel-bench/"
source_title: "Benchmarking OpenTelemetry: Can AI trace your failed login? - Quesma Blog"
source_id: 46811588
excerpt: "OTelBenchで14モデル検証、Opus 4.5は成功率29%で観測性自動化は危険"
image: "https://quesma.com/_astro/thumbnail_piotr.CjJxCeZg.jpg"
---

# OTelBench: AI struggles with simple SRE tasks (Opus 4.5 scores only 29%) - OTelBench：AIは単純なSRE作業でも苦戦（Opus 4.5 の成功率はわずか29%）
クリックせずにはいられないタイトル：AIが「ログを見る」を代替できる？OTelBenchが暴いた観測性の現実

## 要約
最先端LLM14種に対してOpenTelemetryの実装タスク（23件、11言語）をベンチマークした結果、最高のClaude Opus 4.5でも成功率は29%にとどまり、多くが「ビルドは通るが正しいトレースを出さない」失敗をした。

## この記事を読むべき理由
日本のクラウド／マイクロサービス環境でも、サービス障害の切り分けに分散トレーシングは必須。AIに任せて安心できるかを知ることで、現場の工数設計や採用ツール選定に直結します。

## 詳細解説
- 背景：分散トレーシングは「1回のユーザー操作」が複数サービスを跨いだ際にTraceIDでつなぎ、呼び出し関係（スパン）を可視化する仕組み。OpenTelemetry（OTel）はその事実上の標準で、Semantic Conventions、各言語のSDK、Collector、そして自動計装のエコシステムを持つ。  
- ベンチマーク概要：14モデルを対象に、Go/Java/C++/Python/JS/PHP/Ruby/Rust/Erlang/.NET/Swiftの計11言語で23タスクを評価（合計966実行、コスト約$522）。各タスクは実運用を想定した短め（約300行）のマイクロサービスで、AIは端末で編集・ビルド・実行して計測。  
- 主な失敗パターン：  
  - 文脈（Context）伝播の誤り：別ユーザー操作を同一トレースに結合してしまう（例：成功パスとエラーパスを1つのTraceIDに混在）。  
  - スパン命名や親子関係の不整合：コンパイルは通っても階層構造が崩れ、実用的な可視化にならない。  
  - 言語バラツキ：C++が37%と高め、Goは20%（中心的言語として重要）、Java/Ruby/Swiftは全滅に近い。  
  - コスト・速度のトレードオフ：最安のGemini 3 Flashは19%でコスト効率は良好だが精度は低め。  
- 結論的観察：OTelの実装は「単純作業」ではあるが長期的な文脈追跡と多言語対応が要求され、現行LLMだけでは本番信頼には遠い。

## 実践ポイント
- まずAIに全部頼らない：生成された計装はビルドだけで合格判定せず、TraceID・スパン構造・エラー経路を必ず手動で検証する。  
- テストを自動化する：正常系・異常系（エラーやタイムアウト）を含むE2Eテストでトレースを検証するCIを導入する。  
- OTelBenchを試す：QuesmaOrg/otel-bench（Harborベース）をローカルで回し、特定モデルの挙動を再現・評価する。  
- 優先度付け：まずは認証・支払いなど「障害コストの高い」サービスから確実に手動で正しい計装を入れる。  
- モデル選定はコストと失敗リスクで判断：安価なモデルが速度・コスト面で魅力でも、観測性ミスのコストは高いことを念頭に。  
- コミュニティに参加：OTelBenchはOSS化されているため、日本の実案件ベースのケースを追加して精度向上に貢献するのも有効。

参考：OTelBenchの結果・コードは QuesmaOrg/otel-bench と OTelBenchサイトで公開。AIに任せる前提でなく「補助ツール」としてどう活かすかが今の現場の分かれ道です。
