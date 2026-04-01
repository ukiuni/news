---
layout: post
title: "Show HN: Zerobox – Sandbox any command with file, network, and credential controls - Zerobox：ファイル・ネットワーク・資格情報を制御する軽量サンドボックス"
date: 2026-04-01T19:24:22.133Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/afshinm/zerobox"
source_title: "GitHub - afshinm/zerobox: Lightweight, cross-platform process sandboxing. Sandbox any command with file, network, and credential controls. · GitHub"
source_id: 47574871
excerpt: "ZeroboxでAPIキーを露出させずにローカルAIやCIを細かく制御して安全に隔離実行できる方法"
image: "https://opengraph.githubassets.com/790a97a89d614b0bbada19a3facef8b3f670f375e6d6b0f671c820037349ffed/afshinm/zerobox"
---

# Show HN: Zerobox – Sandbox any command with file, network, and credential controls - Zerobox：ファイル・ネットワーク・資格情報を制御する軽量サンドボックス

ローカルでAIエージェントやビルドを「安全に」走らせる方法がここに――APIキーをプロセスに見せずに使える軽量サンドボックス、Zerobox。

## 要約
Zeroboxは「拒否（deny）前提」のクロスプラットフォームなプロセスサンドボックス。ファイル読み書き、ネットワーク、環境変数、APIキーの注入を細かく制御でき、AIエージェントやCIでの誤操作やシークレット漏洩を防ぐ。

## この記事を読むべき理由
日本企業でもLLMや外部APIを扱う開発が増え、ローカル実行やCIでのシークレット漏洩・不正アクセスリスクが高まっています。Zeroboxは低オーバーヘッドで導入しやすく、実務での安全策になるため知っておく価値があります。

## 詳細解説
- 基本思想：デフォルトで書き込み／ネットワーク／環境変数をブロックし、許可された操作だけを明示的に通す（deny-by-default）。
- 資格情報の扱い：プロセス内には置き換え済みのプレースホルダーを渡し、実際のキーはプロキシ層で「許可されたホスト」に対するリクエストのみ差し替えられる。プロセスが直接キーを取得することはない。
- ファイル・ネットワーク制御：--allow-read／--allow-write／--allow-net などのフラグでパスやドメイン単位で許可・拒否。--deny-* が優先される。
- 環境変数制御：デフォルトで PATH, HOME 等のみ継承。--allow-env／--deny-env／--env で細かく設定可能。
- SDK：TypeScript向けのDeno風APIを提供。ツール単位で異なるサンドボックスを作り、読み取り専用・書き込み限定・ネット限定などを組み合わせられる。
- 実装・プラットフォーム：macOSはSeatbelt、Linuxはbubblewrap+seccomp+namespaces。シングルバイナリで Docker/VM不要。オーバーヘッドは通常約+10ms・数MB程度。
- 使いどころ：AI生成コード実行、ビルドやテストの外部アクセス制限、LLMエージェントの各ツール呼び出しの分離など。

簡単な使用例：
```bash
# ネットワーク・書き込み禁止でスクリプトを実行
zerobox -- node -e "console.log('hello')"

# 特定ディレクトリだけ書き込み許可
zerobox --allow-write=./dist -- node build.js

# APIキーを特定ホストだけに注入（プロセスはキーを見ない）
zerobox --secret OPENAI_API_KEY=sk-xxx --secret-host OPENAI_API_KEY=api.openai.com -- node agent.js
```

TypeScript SDK例：
```typescript
import { Sandbox } from "zerobox";

const sandbox = Sandbox.create({
  secrets: {
    OPENAI_API_KEY: { value: process.env.OPENAI_API_KEY, hosts: ["api.openai.com"] }
  },
  allowWrite: ["/tmp/output"],
  allowNet: ["api.openai.com"]
});

const out = await sandbox.sh`node agent.js`.text();
```

## 実践ポイント
- まずローカルで試す：curl一発でインストール可能（macOS/Linux）。軽量なのでローカル検証に最適。
- AIエージェント実行時は、出力先だけ許可する（--allow-write=/tmp/output）＝ファイル破壊リスクを低減。
- シークレットは必ず --secret + --secret-host で限定的に渡す。Node内部でプロキシを使う場合は --use-env-proxy が必要なケースあり。
- CIではテストにネットワークを切って実行し、偶発的な外部アクセスを防ぐ。
- パフォーマンス影響は小さいが、重いジョブでベンチを取って運用ルールを決める。
