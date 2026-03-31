---
layout: post
title: "Universal Claude.md – cut Claude output tokens by 63% - Universal CLAUDE.md：Claudeの出力トークンを63%削減"
date: 2026-03-31T02:05:41.754Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/drona23/claude-token-efficient"
source_title: "GitHub - drona23/claude-token-efficient: Universal CLAUDE.md - cut Claude output tokens by 63%. Drop-in. No code changes. · GitHub"
source_id: 47581701
excerpt: "ドロップインでCLAUDE.mdを置くだけ、出力トークン約63%削減してコスト削減"
image: "https://opengraph.githubassets.com/75687e05daefaef5a1e8f47e1297d28a9215042fb75b49a4ce31ff8467d120dc/drona23/claude-token-efficient"
---

# Universal Claude.md – cut Claude output tokens by 63% - Universal CLAUDE.md：Claudeの出力トークンを63%削減
1ファイル置くだけでClaudeの「冗長なおしゃべり」を封じ、出力トークンを大幅削減する実用テクニック

## 要約
プロジェクトルートにCLAUDE.mdを置くだけで、Claude Codeの冗長な前置き・締め・フォーマットノイズを抑制し、出力トークンを約63%削減できる（ただしファイル自体が入力トークンを消費するため、高出力量のワークロードで有効）。

## この記事を読むべき理由
トークン課金型のAIを開発や自動化で多用する日本の開発チームにとって、出力の無駄を減らすことはコストとログノイズの両方を減らす近道。設定・コード変更不要の“ドロップイン”で導入できる点も魅力。

## 詳細解説
- 仕組み：Claude Codeはプロジェクトルートやグローバル、サブディレクトリのCLAUDE.mdを自動読み込みし、応答ルールを順守する。ユーザー指示が優先される「オーバーライドルール」あり。
- 主なルール例：先頭の賛辞・冗長な締め言葉の禁止、質問の再掲禁止、ASCII 出力強制（スマートクォート/特殊文字禁止）、根拠のない推測を避け「わからない」と明言、不要な提案禁止、最小実装のコード提示など。
- トレードオフ：CLAUDE.md自体が毎メッセージで入力トークンを消費するため、出力削減が入力コストを上回る高頻度・大量出力ケースで効果的。単発問い合わせでは逆にコスト増の可能性あり。
- ベンチマーク（リポジトリの方向性指標）：5つのサンプルプロンプトで合計出力語数を465→170に削減（約63%）。個別例：コードレビューで120語→30語（75%削減）。
- 運用上の注意：構造化出力（JSON等）や厳密なパーサ要件がある場合はAPIのスキーマ機能を併用する方が安全。複数プロジェクトや自動化パイプライン向けにプロファイル分割が推奨される（global/project/subdirで使い分け）。

使い方は簡単：
```bash
# Option 1 - Universal
curl -o CLAUDE.md https://raw.githubusercontent.com/drona23/claude-token-efficient/main/CLAUDE.md

# Option 2 - Clone + pick profile
git clone https://github.com/drona23/claude-token-efficient
cp claude-token-efficient/profiles/CLAUDE.coding.md your-project/CLAUDE.md
```

## 実践ポイント
- まずは出力が多い自動化ジョブ（CI、エージェントループ、コード生成パイプ）で試す。  
- グローバルにはトーンやASCIIルール、プロジェクトごとに安全制約やファイル改変ルールを置く。  
- 実運用前にトークン消費のビフォー/アフターを計測し、ネット効果を確認する。  
- 既知の失敗モード（例：エラーを無視する、余計な修正を加える）に合わせた具体的なルールを追加する。  
- 詳細説明が必要な場合は明示的に「詳しく説明して」と指示すれば従う。
