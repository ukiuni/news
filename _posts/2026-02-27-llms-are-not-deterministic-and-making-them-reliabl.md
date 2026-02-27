---
layout: post
title: "LLMs Are Not Deterministic. And Making Them Reliable Is Expensive (In Both the Bad Way and the Good Way) - LLMは確定的ではない。信頼性を作るのは高くつく（悪い意味でも良い意味でも）"
date: 2026-02-27T12:58:11.557Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/marcosomma/llms-are-not-deterministic-and-making-them-reliable-is-expensive-in-both-the-bad-way-and-the-good-5bo4"
source_title: "LLMs Are Not Deterministic. And Making Them Reliable Is Expensive (In Both the Bad Way and the Good Way) - DEV Community"
source_id: 3275292
excerpt: "LLMは確定せず運用コスト急増―誤答対策と評価ループで信頼性を築け"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fsjm314ox7knil293i7jh.png"
---

# LLMs Are Not Deterministic. And Making Them Reliable Is Expensive (In Both the Bad Way and the Good Way) - LLMは確定的ではない。信頼性を作るのは高くつく（悪い意味でも良い意味でも）
LLMは「賢いが不確かな部品」――デモと実運用の溝を埋めるには、見えないコストとエンジニアリングが必要だ

## 要約
大規模言語モデル（LLM）は確定的ではなく確率的なトークン予測器に過ぎない。信頼できるプロダクトにするには、生成→評価→再試行などの制御ループを積み上げる必要があり、それが実運用コストを大きくする。

## この記事を読むべき理由
デモやAPI呼び出しの「安さ」に惑わされると、運用で想定外のコストや不安定さに直面する。日本のサービスや規制対応が厳しい業界（金融や医療、法務）では、信頼性と費用のバランス設計が不可欠だから。

## 詳細解説
- 本質：LLMは文脈から次のトークンを確率分布からサンプリングする仕組み。内部に「真理判定」や確実な推論エンジンはない。
- デモ vs 実運用：デモは単発の呼び出しで見栄えするが、実際は誤答（hallucination）や制約無視が頻発する。モデル自体を“確定的”にすることはできない。
- 解決法は「モデルの上に制御を置く」こと：入力整形→生成→生成物の評価→ルーティング（合格なら返答、不合格なら再試行／別モデル）というパイプラインを回す。
- コストの再定義：トークン単価が安くても、ひとつのユーザー要求が複数のモデル呼び出し（生成、評価、整形、ツール呼び出し、メモリ参照）を要求するため、システム全体のコストは高くなる（「ネジは安いが飛行機は高い」比喩）。
- 「高くなる悪い方」と「高くなる良い方」：運用が下手なら金を燃やしても信頼性は上がらない。一方、評価器や冗長性、観測性に投資すれば信頼できるシステムが得られるが費用はかかる。
- 実務観点：LLM運用は分散システム工学に近い。データ品質、レイテンシ、スキーマ設計、プロンプトのバージョン管理、トレースとベンチマークが重要。
- 小モデルを活用する戦略：分類やルーティングは軽量モデルで、推論や生成は大型モデルで行えばコスト削減と信頼性の両立が可能。ただし「どこをダウングレードして安全か」は設計上の判断が必要。

## 実践ポイント
- 受け入れ基準（acceptance gate）を作る：出力が状態や金銭、信頼を壊す可能性がある箇所は“良い enough”を許さない。
- 評価ループを明確化：生成→自動評価→再生成（閾値で判定）を標準パターンにする。
- モデルファミリ設計：分類・正規化は小モデル、生成・推論は大モデルと分担する。
- 冗長性と観測性：ログ、トレース、メトリクス、プロンプト・モデルのバージョン管理を必須にする。
- コスト計測を「1回答あたり」で行う：トークン単価ではなく、実際のワークフロー全部で見積もる。
- 優先順位付け：法務・決済・顧客信用に関わる部分は厳格検証、UIや探索的機能は緩めでOKと線引きする。

以上を踏まえると、LLM導入は「安さの幻想」を捨て、どこに信頼を置き、どこにコストを払うかを設計することが成功の鍵になる。
