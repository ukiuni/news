---
layout: post
title: "A verification layer for browser agents: Amazon case study - ブラウザエージェントの検証レイヤー：Amazonケーススタディ"
date: 2026-01-28T16:04:31.451Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sentienceapi.com/blog/verification-layer-amazon-case-study"
source_title: "A verification layer for browser agents: Amazon case study"
source_id: 46790127
excerpt: "検証レイヤーで小型ローカルLLMがAmazon購買自動化を安全・確実にする実践ガイド"
image: "https://sentienceapi.com/og-image.png"
---

# A verification layer for browser agents: Amazon case study - ブラウザエージェントの検証レイヤー：Amazonケーススタディ
「小さなローカルLLMでAmazon操作を成功させる秘訣：検証レイヤーが信頼性を作る」

## 要約
構造化スナップショット＋Jest風の明示的アサーションで、視覚モデル不要でも小型ローカルLLMを安全に実行器として使える。検証があればモデルサイズよりも信頼性が確保でき、トークン効率も設計で改善できる。

## この記事を読むべき理由
- コスト／レイテンシ／データ保護の観点でローカル実行を検討する日本の開発者にとって、実務的な自動化設計パターンが分かる。  
- UI自動化やRPA、テスト自動化で「モデルの暴走」を防ぐ実装手法がすぐ使える。

## 詳細解説
- 問題点：スクリーンショット中心（ピクセル制御）はターゲット曖昧、遷移検出失敗、状態が変わらないまま「進行」してしまうなどの失敗が定常化する。  
- 提案：ページを「構造化スナップショット（役割／テキスト／ジオメトリ＋重要度）」として扱い、各アクション後に明示的なアサーションで合否を判定する。これが「Jest for agents」。  
- アーキテクチャ（3モデルスタック）：
  - Planner（推論）→ 構造化JSONプラン（手順＋検証要件）  
  - AgentRuntime：スナップショット取得→検証（assert_/check）→トレース記録  
  - Executor（小型LLM）：DOMアクション（CLICK/TYPE）を選択  
  - Verifier（Sentienceランタイム）：各ステップを通過可否でゲート
- 検証の実装例：predicate（例：url_contains, exists）をスナップショットに評価し、失敗時は失敗アーティファクト（スクショ／トレース）を残す。フルーエントな再試行ハンドル（.once()/.eventually()）で非同期UIにも対応。  
- 実験（Amazon購買フロー：検索→1番目クリック→カート→チェックアウト）：
  - Demo 0（クラウドLLM＋構造化）：トークン約35,000→19,956（約43%削減）  
  - Demo 3（ローカル自律：DeepSeek planner + ~3B級ローカル executor + 検証）：再実行で7/7ステップ成功、トークン11,114、成功率高。  
- 挙動制御：意図が明確な場合は決定的オーバーライド（例：第一商品選択、アップセル引き下げ）で安全に誘導。プランの脆弱なセレクタは検証で即露呈し、サイレントフェイルを防ぐ。

## 実践ポイント
- ページ制御は「構造化スナップショット」主体に切り替える（DOMテキスト＋役割フィルタ）。  
- すべてのアクション直後に明示的アサーションを入れる（exists / url_contains 等）。  
- Planner（大きめ）とExecutor（小さめ）を分離してコストとレイテンシを最適化する。  
- 意図が明白な操作は決定的オーバーライドで安全性を担保する。  
- 要素フィルタでプロンプトサイズを減らしトークンコストを削減する。  
- ステップ毎のトレース／スクリーンショット／動画を残してデバッグ可能にする。

短く言えば：「検証を設計に組み込めば、小型ローカルモデルでも実用的な自動化が可能」。日本のプロダクトやRPA現場でもすぐ試せる実践的なアプローチです。
