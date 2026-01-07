---
  layout: post
  title: "How We Built a Website Hook SDK to Track User Interaction Patterns - ユーザー行動を追うWebsite Hook SDKをどう作ったか"
  date: 2026-01-07T15:08:05.264Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://blog.crowai.dev/blog/website-hook-sdk-evolution/"
  source_title: "Building the Website Hook SDK: A Story of Iteration and Hard Decisions | blog.crowai.dev"
  source_id: 468819913
  excerpt: "軽量イベント中心SDKで帯域・プライバシー問題を解決しつつ、実務で使える8つの教訓を公開"
  image: "https://blog.crowai.dev//_astro/banner.D3U0RnqZ.jpg"
---

# How We Built a Website Hook SDK to Track User Interaction Patterns - ユーザー行動を追うWebsite Hook SDKをどう作ったか
無駄を削ぎ落としたトラッキングの教科書：CROWが辿った8つのフェーズと実務で使える教訓

## 要約
「視覚的なセッションリプレイ」から出発し、最終的に軽量なイベント中心SDKへ収束した開発の道筋と意思決定の記録。トレードオフ（帯域、プライバシー、開発コスト）をどう扱ったかが学べます。

## この記事を読むべき理由
日本のプロダクトやECサイトでは、モバイル回線やユーザープライバシーへの配慮が必須です。本記事は「何を最初に作るべきか」「どこを削るか」を実例で示すため、限られたリソースで実装すべきトラッキングの優先順位が明確になります。

## 詳細解説
- 背景  
  CROWはウェブや店内CCTV、SNSを組み合わせて顧客行動を解析するプラットフォーム。Website Hook SDKはクライアント側で振る舞い（ページビュー、クリック、エラーなど）を収集してCloudflareのエッジへ送る役割を担います。

- 初期ビジョンと転換  
  初めはFullStory/Hotjar的なセッションリプレイ（定期的にDOMをスクリーンショット化して送信）を目指しましたが、スクショはデータ量が大きく、実用性が限定的でした。結果として「視覚的再現」ではなく「イベント＋セッション」を中心に据える方針に転換しました。

- フェーズ別の技術的ポイント（抜粋）
  1. スクリーンショット収集（html2canvas）  
     - 利点：見た目を正確に残せる。  
     - 欠点：画像サイズが巨大、サーバ側処理が必要。
  2. エッジ統合（Cloudflare Worker）  
     - 画像アップロードを試す。設定が無視されるバグ（固定100ms）を発見 → 設定が実際に反映されるかを必ずテストする重要性。
  3. ポインタ（マウス）トラッキング  
     - バッファ＋バッチ送信で負荷を抑える。初期は15msで大量リクエスト発生 → 1秒間隔に調整し実用化。スクショはオプション化。
  4. API簡素化  
     - 設定項目を削減し、合理的なデフォルトに固定。多数のオプションは導入側の負担になる。
  5. アーキテクチャ整理  
     - fetch→kyへ（リトライやクリーンなAPI）、fire-and-forget（失敗は黙認してUXを最優先）、共通ユーティリティ抽出。
  6. 統合トラッキング（挫折）  
     - スクショと座標を同期する双バッファ、ミューテックス等の高度実装を試行。しかしニーズに合わず削除。
  7. リセットと削除  
     - 781行を削除。動くコードでも「不要なら消す」判断を下す。保守コストの削減が目的。
  8. イベント中心アーキテクチャへ（最終形）  
     - セッション管理（localStorageでsessionId/anonymousId保持）、イベントバッファと5秒フラッシュ、オートキャプチャ（pageview/click/error）、プライバシー（パスワード/カードマスキング、Do Not Track対応）、beforeunloadでのクリーンアップ。

- システム全体  
  クライアント → Cloudflare Edge（web-ingest-worker）→ D1（DB）→ キュー→ バックエンド処理（AI解析）。テスト用に「rogue-store」というデモECで実装検証。

## 実践ポイント
- まずはシンプルに：まずはページビュー・クリック・コンバージョンなどの基本イベントから始める。過剰な機能は後で追加可能。
- 不要なコードは躊躇せず削除：保守コストは積み重なる。迷ったら削る判断を検討する。
- 設定は最小限に：合理的なデフォルトを用意し、カスタムが必要な少数に限定する。
- 失敗はユーザーに影響させない：送信失敗は黙殺し、UXを優先する（fire-and-forget）。
- バッチングを活用：イベントをまとめて送るだけでネットワークコストと電力消費を大幅に削減できる。
- 設定の効果を自動テストする：設定が実際に反映されないバグは起きやすい。CIやE2Eで検証を入れる。
- 日本の現場向け注意点：モバイル回線の帯域制限、APPIやCookie規制、ユーザーのプライバシー感度を尊重するため、マスキングやDo Not Track対応は必須に。

統合は簡単（React例）
```javascript
// JavaScript
"use client";
import { useEffect } from "react";
import { initInteractionTracking } from "@b3-crow/website-hook-sdk";

export function InteractionTracker() {
  useEffect(() => {
    initInteractionTracking({ logging: true });
  }, []);
  return null;
}
```

以上の教訓は「技術的にできること」と「実際に価値を生むこと」を分けて考える実務的な指針になります。必要なら、この記事の各フェーズで使われた具体的な実装パターン（バッファ設計、retry戦略、セッションID生成など）を詳しく掘り下げて解説します。どのトピックを深掘りしますか？
