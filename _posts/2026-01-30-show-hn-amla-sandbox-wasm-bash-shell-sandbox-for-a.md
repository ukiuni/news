---
layout: post
title: "Show HN: Amla Sandbox – WASM bash shell sandbox for AI agents - Show HN: Amla Sandbox — AIエージェント向けWASMサンドボックス（bashシェル対応）"
date: 2026-01-30T15:08:06.259Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/amlalabs/amla-sandbox"
source_title: "GitHub - amlalabs/amla-sandbox"
source_id: 46824877
excerpt: "WASMで安全にLLMのスクリプト実行、ツール呼び出しを細かく制御して運用コストとリスクを同時削減"
image: "https://opengraph.githubassets.com/b49cf1b3201030e0995994bfab0f1581674e4ab592d709002f5be7e347299ffe/amlalabs/amla-sandbox"
---

# Show HN: Amla Sandbox – WASM bash shell sandbox for AI agents - Show HN: Amla Sandbox — AIエージェント向けWASMサンドボックス（bashシェル対応）
LLMに「安全なコード実行」を与えて、ツール呼び出しコストも減らす――Amla Sandbox活用ガイド

## 要約
Amla Sandboxは、LLMが生成するスクリプトをWebAssembly（WASM）上で安全に実行し、ツール呼び出しを能力（capability）で厳密に制御することで、トークンコスト削減と攻撃面の縮小を両立するサンドボックスです。

## この記事を読むべき理由
日本のプロダクト（特に金融や医療など規制の厳しい分野）でAIエージェントを使う際、モデルが直接ホストOSで任意コードを実行するリスクは重大です。Amlaは「Docker不要で軽量に隔離」しつつ、ツール単位で許可と制約を与えられるため、実運用検討に直結する選択肢になります。

## 詳細解説
- 基本思想：LLM→ツール→LLMの往復を減らすため、モデルに1本のスクリプトを書かせて一括で処理させる「コードモード」を採用。一方で単にevalするのではなく、WASMで実行してホストから切り離す。
- 実行基盤：QuickJSをWASM化し、WASIベースの最小Syscallで動作。wasmtimeランタイムを利用しメモリ安全性を担保。
- 能力ベースの制御：ツール呼び出しはMethodCapability/ConstraintSet/Paramで定義したルールに沿って検証される。例えば金額上限や通貨の列挙、クエリの先頭文字制約などを設定可能。
- ホスト連携モデル：サンドボックスはツール呼び出し時にホストへyieldし、ホスト側で能力チェック→実行→再開する形。これにより外部アクセス（ネットワーク等）は遮断される。
- VFS制約：書き込みは /workspace と /tmp のみ。ルートは読み取り専用。
- パフォーマンス：初回コンパイルは数百ms、プリコンパイルとキャッシュで以降は高速ロード。
- トレードオフ：Linuxフル環境やネイティブモジュール、GPUは不可。無限ループのJSはステップ制限だけでは止められないケースがある点に注意。
- ライセンス：Python側はMIT。ただしWASMバイナリは再配布禁止のプロプライエタリ部分あり（利用時の注意）。

コード例（導入と簡単な実行）:

```bash
# インストール（リポジトリ直インストール）
pip install "git+https://github.com/amlalabs/amla-sandbox"
```

```python
from amla_sandbox import create_sandbox_tool

sandbox = create_sandbox_tool()
# JavaScriptを実行
print(sandbox.run("console.log('hello'.toUpperCase())", language="javascript"))
# shellを実行
print(sandbox.run("echo 'hello' | tr 'a-z' 'A-Z'", language="shell"))
```

能力制約の例（Python API）:

```python
from amla_sandbox import Sandbox, MethodCapability, ConstraintSet, Param

caps = [
    MethodCapability(
        method_pattern="stripe/charges/*",
        constraints=ConstraintSet([Param("amount") <= 10000, Param("currency").is_in(["USD","EUR"])]),
        max_calls=100,
    )
]
sandbox = Sandbox(capabilities=caps, tool_handler=my_handler)
```

## 実践ポイント
- まずは「読み取り専用＋ /workspace 書き込み」モデルで既存エージェントを移行し、ツール呼び出しを1スクリプトにまとめてトークン使用量を削減する。
- 金銭や個人情報を扱うAPIは必ずMethodCapabilityで上限・ホワイトリストを設定する。
- 無限ループ対策や長時間実行防止は別途ホスト側でタイムアウトやステップ制限の監視を用意する。
- 配布や商用組み込み時はWASMバイナリのライセンス条件を確認する。
- フルVMが必要なら別ソリューション（e2bやModal）を検討するが、軽量な隔離と制約付きツール実行が目的ならAmlaは手早い選択肢。

以上。興味があれば公式リポジトリのExamplesとDocsを参照して、まずはローカルで簡単なツールを登録して試してみてください。
