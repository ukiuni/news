---
layout: post
title: "Claude Opus 4.7 costs 20–30% more per session - Claude Opus 4.7 はセッション当たり20〜30%高くなる"
date: 2026-04-17T16:15:43.343Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.claudecodecamp.com/p/i-measured-claude-4-7-s-new-tokenizer-here-s-what-it-costs-you"
source_title: "I Measured Claude 4.7&#x27;s New Tokenizer. Here&#x27;s What It Costs You."
source_id: 47807006
excerpt: "Claude Opus 4.7は英語・コードでトークン増、セッション費用約20–30%増で要見直し"
image: "https://beehiiv-images-production.s3.amazonaws.com/uploads/asset/file/e5042662-e001-4de8-8c26-224b260a6303/thumbnail.png?t=1776374689"
---

# Claude Opus 4.7 costs 20–30% more per session - Claude Opus 4.7 はセッション当たり20〜30%高くなる
Claude 4.7の新トークナイザで「同じ仕事」がなぜ高くなるのか？実測データで読むコストと効果

## 要約
AnthropicのClaude Opus 4.7はトークナイザ変更で英語・コード中心の入力に対して $1.3\text{–}1.45\times$ 程度トークンが増え、長い対話セッションではセッション単価が約20–30%上昇する一方、厳密な指示遵守は小幅（サンプルで+5pp）に改善した。

## この記事を読むべき理由
日本のエンジニア／SaaS運用者は、同じAPI課金で「いつものワークフロー」が突然割高になり得る点を押さえておくべきです。トークン増加は料金だけでなく、レート制限・キャッシュ戦略にも影響します。

## 詳細解説
- 測定方法：Anthropicの無料カウントAPI（POST /v1/messages/count_tokens）で同一テキストを Claude Opus 4.6 と 4.7 に投げ、差を比較。
- 実測結果（代表）：
  - 技術文書：$1.47\times$
  - CLAUDE.md（実ファイル、5KB）：$1.445\times$
  - 実利用サンプル7件の加重比：$1.325\times$
  - CJK（日本語／中国語）はほぼ変化なし（約 $1.01\times$）
  - 英語＋コード寄りのワークロードほどトークン増が大きい
- トークナイザの変化点（推察）：
  - 4.7は英語・コードで「より細かいトークン分割」を採用しており、chars-per-token が低下（例：英語で 4.33→3.60）。
  - 結果、頻出の英語単語やコードのマージが少なくなり、トークン数増。
- 指示遵守の検証：
  - IFEvalベンチ（制約付き生成）からサンプリング20件で評価：厳密評価の合格率が 85%→90%（+5pp）に向上。効果は小さくサンプルサイズは限定的。
- セッションコスト試算（例：長期のバグ修正 80ターン）：
  - Claude 4.6 想定合計：約 \$6.65
  - Claude 4.7 想定合計：約 \$7.86–\$8.76
  - 増分は概ね 20–30%（理由：会話履歴キャッシュの読み取りが多く、履歴自体が膨らむため）
- キャッシュ影響：
  - モデル切替でキャッシュパーティションが変わりコールドスタート時の書込コストが増大。頻繁なキャッシュ書換えやTTL切れで痛手が大きい。

（参考：計測で使われた最小コード）
```python
python
from anthropic import Anthropic
client = Anthropic()
for model in ["claude-opus-4-6", "claude-opus-4-7"]:
    r = client.messages.count_tokens(
        model=model,
        messages=[{"role": "user", "content": sample_text}],
    )
    print(f"{model}: {r.input_tokens} tokens")
```

## 実践ポイント
- 予算設計：英語／コード中心のワークロードはトークン消費を $1.3\text{–}1.45\times$ 想定して予算を上げる。  
- レート管理：Maxプランのレート枠は同割合で早く尽きるため、ウィンドウ運用を見直す。  
- キャッシュ運用：モデル切替やCLAUDE.md編集の頻度を減らし、TTL戦略でキャッシュ書込回数を抑える。  
- 評価検証：重要なワークフロー（フォーマット厳守やツール呼び出し）が4.7で本当に改善するか、短いA/Bで確認する。  
- 代替策：コスト重視なら4.6運用継続、厳密な指示遵守が重要なら移行検討。移行前に貴社コンテンツでトークン増分を計測して判断する。

以上。必要ならあなたの代表的なプロンプト／ファイルで実測するための手順（簡単なスクリプト）を用意しますか？
