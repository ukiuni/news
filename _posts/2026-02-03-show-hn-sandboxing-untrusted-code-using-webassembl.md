---
layout: post
title: "Show HN: Sandboxing untrusted code using WebAssembly - WebAssemblyで信頼できないコードをサンドボックス実行"
date: 2026-02-03T15:19:53.187Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mavdol/capsule"
source_title: "GitHub - mavdol/capsule: ⚙️ A secure, durable runtime for AI agents. Run untrusted code in isolated WebAssembly sandboxes."
source_id: 46871387
excerpt: "CapsuleでWebAssemblyを使いAIエージェントの外部コードを安全に厳格隔離して実行"
image: "https://opengraph.githubassets.com/18bb434329186b7b26674bcde5ea524dd6f5dd29486886968dd643e7bbb07047/mavdol/capsule"
---

# Show HN: Sandboxing untrusted code using WebAssembly - WebAssemblyで信頼できないコードをサンドボックス実行
魅せるタイトル: 「外部コードも怖くない——WebAssemblyでAIエージェントの作業を安全に隔離する『Capsule』入門」

## 要約
CapsuleはAIエージェントの各タスクを個別のWebAssemblyサンドボックスで実行し、CPU・メモリ・タイムアウトなどを厳格に制限して未検証コードの安全実行を可能にするランタイムです。

## この記事を読むべき理由
AIワークフローやプラグイン的な外部スクリプトを扱う場面が増える中、企業・開発チームは「どこまで外部コードを信頼して実行するか」を問われています。日本のプロダクトや研究現場でも、ユーザー提供コードや外部モデル連携の安全性を確保する実用的な選択肢として注目すべき技術です。

## 詳細解説
- アーキテクチャ概要  
  Capsuleは各タスクを個別のWasmモジュールとしてコンパイルして実行。ホスト側がCPU（Wasmの「fuel」）、メモリ、実行時間を管理し、失敗や過剰消費が他タスクに波及しないよう隔離します。

- タスク定義（Python / TypeScript）  
  Pythonでは関数に @task デコレータを付け、TypeScript/JavaScriptでは task() ラッパーでエントリを宣言。ランタイムは "main" タスクをエントリポイントとして実行します。

  ```python
  # Python
  from capsule import task

  @task(name="main", compute="LOW", ram="64MB", timeout="30s")
  def main() -> str:
      return "Hello from Capsule!"
  ```

  ```typescript
  // TypeScript
  import { task } from "@capsule-run/sdk";

  export const main = task({ name: "main", compute: "MEDIUM" }, async () => {
    return "Hello from Capsule!";
  });
  ```

- リソース管理と実行メタデータ  
  computeレベル(LOW/MEDIUM/HIGH/CUSTOM)でfuelを割り当て、各タスクは実行結果と実行メタ（duration_ms、retries、fuel_consumedなど）を含むJSONエンベロープを返します。これで監査・可観測性が確保されます。

- 入出力・I/Oの扱い  
  ファイルアクセスは allowed_files で許可したディレクトリに限定。TypeScriptはfetchなど標準APIが使え、Python向けにはサンドボックス内で動く専用HTTPクライアントが用意されています。

- 制約と互換性  
  TypeScript/JavaScriptの互換性が高くnpm資産が使いやすい一方、PythonはC拡張（numpy/pandas等）が現状サポート外。長時間・大規模処理向けに設計されていますが、ネイティブ拡張を使うワークロードは要検討です。

- 開発・導入の敷居  
  OSSで、ビルドにはRust（wasmtime等）、Python 3.13+、Node.js 22+などが必要。CLIやSDK経由でローカル試験が可能です。

## 実践ポイント
- まずは公式のQuick Startで hello.py / hello.ts を実行して挙動を確認する。  
- タスクごとに compute/ram/timeout を細かく設定し、失敗時は max_retries で挙動を制御する。  
- 外部ファイルアクセスは allowed_files で最小権限に絞る。  
- Pythonで数値計算ライブラリが必要なら、現状はTypeScript版や別プロセス実行を検討する。  
- 監査用に実行メタ（duration_ms、fuel_consumed 等）を必ずログに残す。  
- 日本の企業利用では、社内ルールに合わせて capsule.toml でデフォルト制限を設定し、サンドボックス運用を標準化する。

短時間で試せて、安全性と可観測性を両立できる点がCapsuleの肝。外部スクリプトやエージェント化された処理を扱う開発者は、一度検証してみる価値があります。
