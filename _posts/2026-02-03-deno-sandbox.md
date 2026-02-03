---
layout: post
title: "Deno Sandbox - Deno サンドボックスの紹介"
date: 2026-02-03T18:34:10.968Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://deno.com/blog/introducing-deno-sandbox"
source_title: "Introducing Deno Sandbox | Deno"
source_id: 46874097
excerpt: "Deno Sandboxで未検証コードを秘密漏洩ゼロで即実行・本番デプロイ可能"
image: "https://deno.com/blog/introducing-deno-sandbox/og.webp"
---

# Deno Sandbox - Deno サンドボックスの紹介
LLMが生み出したコードをそのまま実行しても安全ですか？Deno Sandboxなら「秘密」と「通信先」を封じて、安全に即実行・そのままデプロイできます

## 要約
Denoが発表したSandboxは、軽量なLinuxマイクロVMで未検証のコードを隔離し、シークレットは環境に渡さず、許可したホストへの通信だけを許すことで機密漏洩を防ぎつつ、そのままDeno Deployへデプロイ可能にするサービスです。

## この記事を読むべき理由
日本でもLLMを使ったプロダクトやユーザー生成コードを扱うサービスが増えています。APIキーや顧客データを守りつつ「即実行・即デプロイ」できる仕組みは、SaaS、FinTech、社内ツールの安全性と開発効率を両立します。

## 詳細解説
- 分離と起動
  - SandboxはDeno Deploy上で動く軽量LinuxマイクロVM。起動は1秒未満でエフェメラル（最大30分、延長可）。
  - 用途：AIエージェントのコード実行、プラグイン、エフェメラルCI、開発環境スナップショット。

- シークレットの扱い（重要）
  - シークレットはサンドボックス内に実体として注入されない。コードからはプレースホルダーしか見えず、本当の鍵は「許可された外向き接続」が発生したときのみプロキシ経由で使用される。
  - これにより、プロンプトインジェクションでキーを盗ませても無意味になります。

- ネットワーク出口制御
  - allowNetで通信先ホストを明示的に制限。未許可ホストへのリクエストはVM境界でブロックされる。
  - 実装はアウトバウンドプロキシ（policy chokepoint）で、将来的に接続分析やフックも予定。

- 開発→本番ワークフロー
  - sandbox.deploy()でサンドボックスのそのままのコードをDeno Deployに1コールで移行。別CIや再ビルド不要。

- 永続性と再利用
  - Volumes（読み書きストレージ）とSnapshots（読み取り専用のツールチェインイメージ）で「一度セットアップして使い回す」運用が可能。

- 主要スペックと課金（要チェック）
  - リージョン例：Amsterdam, Chicago。vCPU 2、メモリ0.75–4GB、最大30分。課金はCPU時間・メモリ・ストレージ単位の従量制。

コード例（JS SDK）:
```javascript
import { Sandbox } from "@deno/sandbox";

await using sandbox = await Sandbox.create();
await sandbox.sh`ls -lh /`;
```

シークレットとホスト制限の例:
```javascript
import { Sandbox } from "@deno/sandbox";

await using sandbox = await Sandbox.create({
  secrets: {
    OPENAI_API_KEY: { hosts: ["api.openai.com"], value: process.env.OPENAI_API_KEY },
  },
  allowNet: ["api.openai.com", "*.anthropic.com"],
});
await sandbox.sh`echo $OPENAI_API_KEY`; // プレースホルダー表示
```

サンドボックスから本番へ:
```javascript
const build = await sandbox.deploy("my-app", { production: true, build: { mode: "none", entrypoint: "server.ts" } });
const revision = await build.done;
console.log(revision.url);
```

## 実践ポイント
- まずは小さなワークロード（AIエージェントの短時間実行など）で試す。起動速度が速いのでUX確認が簡単。
- シークレットは必ずSandboxの秘密管理に預け、allowNetで最小限のホストだけ許可する。
- CIやテストの一部をサンドボックスで回すと、環境差による問題を減らせる（Snapshots活用）。
- 日本の事業者はAPPIや契約上の要件での「データ流出リスク低減」をアピールできる点を評価すると良い。
- コスト管理：CPU時間・メモリ単位の従量制。Proプランの無料枠を確認して試用を始める。

公式ドキュメント／SDKでハンズオンすると効果が早く実感できます（docs.deno.com/sandbox）。
