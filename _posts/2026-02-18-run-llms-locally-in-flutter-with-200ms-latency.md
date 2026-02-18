---
layout: post
title: "Run LLMs locally in Flutter with <200ms latency - FlutterでLLMをローカル実行、<200msの低遅延"
date: 2026-02-18T00:24:25.401Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ramanujammv1988/edge-veda"
source_title: "GitHub - ramanujammv1988/edge-veda"
source_id: 47054873
excerpt: "FlutterでLLMを端末常駐化し、熱・電池を監視してプライベートに<200msで動く導入法"
image: "https://opengraph.githubassets.com/6e36ad5e50312f2448c79fa2d6fe81a0c089a1fd2915c01d45118e0374c4a303/ramanujammv1988/edge-veda"
---

# Run LLMs locally in Flutter with <200ms latency - FlutterでLLMをローカル実行、<200msの低遅延
スマホだけで“長時間・安定・プライベート”に動くオンデバイスAI — Edge‑Vedaの全貌と日本での実用シナリオ

## 要約
Edge‑VedaはFlutter向けの「監視付きオンデバイスAIランタイム」。モデルを端末に常駐させ、熱・メモリ・バッテリを監視しながら長時間安定して動かす設計が特徴です。

## この記事を読むべき理由
モバイル第一の日本市場では「プライバシー」「オフライン稼働」「通信コスト削減」「ユーザー体験の安定化」が重要。Edge‑Vedaはこれらを満たす実装・運用哲学を提供します — 開発者が現実のデバイス制約下でLLM/音声/視覚機能を実用化するための実践知が得られます。

## 詳細解説
- 目的と差別化  
  - ベンチマーク短期性能ではなく「長時間の振る舞い」を最優先に設計。クラッシュや熱スロットリングを回避してグレースフルに低劣化するのが狙い。デフォルトでネットワークに問い合わせずプライベート。

- アーキテクチャ（簡潔）  
  - Flutter (Dart) アプリ ←→ Edge‑Veda FFI（XCFramework）  
  - Persistent Workers：Text/Vision/Whisper用の永続アイソレートでモデルを一度ロードしてメモリに常駐。Dart FFIが同期的なため、UI凍結を避けるために背景アイソレートで実行。  
  - Scheduler & RuntimePolicy：デバイスの熱／メモリ／バッテリを監視し、優先度に応じて処理を縮小（FPS、解像度、トークン量の段階的削減）。復帰にはクーリングタイムを設けて振動を防止。  
  - 観測性：JSONLのパフォーマンストレースや構造化ログでオフライン解析が可能。

- 主な機能  
  - テキスト：ストリーミング生成、マルチターン会話、オートサマリでコンテキスト管理  
  - 音声：whisper.cppをMetalで加速、3秒単位のストリーミング転写（非同期アイソレート）  
  - 視覚：VLMを常駐してカメラフレームを逐次解析（フレームは drop‑newest のバックプレッシャー）  
  - RAG/Embeddings：組み込みのVectorIndex（DartでHNSW）、エンベディング生成→検索→注入→生成のパイプライン  
  - 構造化出力と関数呼び出し：スキーマ制約付き生成やツールレジストリで安全なツール呼び出しが可能

- モデル選定と適合性  
  - ModelAdvisorとDeviceProfileで端末のRAM/チップ世代を判定し、MemoryEstimatorでモデルが載るかスコアリング。canRun()でダウンロード前チェックが可能。

- パフォーマンス設計の特徴  
  - モデルを再ロードしない「常駐ワーカー」により繰り返しの初期化コストを削減 → レイテンシ低下と安定性向上。  
  - 予算契約（p95レイテンシ、バッテリ、熱、メモリ）を宣言してスケジューラが強制することでSLOを守る運用を可能に。

## 実践ポイント
- 導入の最初の一歩（pubspecと初期化例）
```dart
// dart
dependencies:
  edge_veda: ^2.1.0

final edgeVeda = EdgeVeda();
await edgeVeda.init(EdgeVedaConfig(
  modelPath: '/path/to/model.gguf',
  contextLength: 2048,
  useGpu: true,
));
```
- すぐ試す機能：generateStream(), ChatSession（マルチターン）、WhisperSession（マイク→逐次転写）、RagPipeline+VectorIndex
- 実機で必ず検証：エミュレータは熱・バッテリ挙動を再現しない。特に日本の普及機種（ミドルレンジAndroidやiPhoneの複数世代）でcanRun()→実行するワークフローを組むこと。
- 運用TIPS：Adaptive budgetで自動調整を始め、アプリのユースケースに応じてConservative/Balanced/Performanceプロファイルを切り替える。熱警告→段階的劣化の挙動をユーザーに明示するとUXが向上。
- 日本市場での応用例：オフライン翻訳・会話アシスタント、機密情報扱う業務アプリ（医療/金融）、通信が不安定な現場でのフィールドワーク支援。

参考：ベンチマークや詳細実装はリポジトリのREADMEとBENCHMARKS.mdを確認して、実機データを元にモデル選定と予算設定を行ってください。
