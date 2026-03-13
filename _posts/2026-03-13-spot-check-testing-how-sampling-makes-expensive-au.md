---
layout: post
title: "Spot-Check Testing: How Sampling Makes Expensive Automated Tests Practical - サンプリングで高コストな自動テストを現実的にする「スポットチェックテスト」"
date: 2026-03-13T01:05:13.928Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.code101.net/spot-check-testing"
source_title: "Spot-Check Testing: How Sampling Makes Expensive Automated Tests Practical | Code101.net"
source_id: 385252034
excerpt: "CIでランダムにページを選びLighthouseを段階的に監視する手法、失敗は再試行し結果を永続化"
image: "/images/spot-check-testing/main.webp"
---

# Spot-Check Testing: How Sampling Makes Expensive Automated Tests Practical - サンプリングで高コストな自動テストを現実的にする「スポットチェックテスト」

魅力的なタイトル: CIを遅くするLighthouseを諦めない方法──「スポットチェック」で全ページを賢く監視する

## 要約
高コストなLighthouseやアクセシビリティ監査を毎回全ページで回す代わりに、CIごとにページをサンプリングして徐々に全ページをカバーする手法（スポットチェック）を紹介する。失敗は必ず再テストし、結果を永続化することで信頼性を保つ。

## この記事を読むべき理由
LighthouseやPa11yを全ページで毎回実行するとCIが遅延・不安定になる。日本のプロダクトでもページ数が増えれば同じ問題に直面するため、実用的かつ低コストで品質を高める手法がすぐに役立つ。

## 詳細解説
- 問題点: Lighthouseはヘッドレスブラウザを複数立ち上げるため時間・リソースを大量消費。並列化は結果の歪みを招く。
- アイデア: 各CI実行で全ページではなく「少数のページ」を選んで監査し、複数回のCIで最終的に全ページを検査する（スポットチェック）。
- サンプリング戦略（トレードオフ）:
  - ランダム：バラエティが出るが全カバーまで時間がかかる
  - 逐次（シーケンシャル）：最短で全カバーだが類似ページが固まりやすい
  - トラフィック重み付き：重要ページを多くテストできるがデータ管理が必要
  - 固定代表リスト：決定的だが陳腐化・死角が生まれる
- 著者の実装（要点）:
  - 常にホームを含める
  - 前回失敗したページは必ず再テストする
  - 残りをランダムにシャッフルして未検証ページを優先して選ぶ
  - 結果（passed / failing）をJSONで永続化し、CI間で読み書きする
- ページ発見はビルド出力のsitemap.xmlをパースして自動化
- ランニングはリソース競合を避けるため直列実行推奨
- Lighthouse適用: デスクトップ／モバイル両方で監査し閾値を設定（例: performance:95, accessibility:100）
- 時間的ラチェティング（Temporal Ratcheting）: ベースラインを記録して、段階的に閾値を厳しくしていくことで徐々に品質を向上させる

実装例（選択アルゴリズム、TypeScript）:

```typescript
const RANDOM_PAGE_COUNT = 3;

function selectPages(
  results: Pa11yResults,
  allPages: string[]
): string[] {
  const selected = new Set<string>(["/"]);
  // Add failing pages first
  for (const page of results.failing) selected.add(page);
  // Remaining pages
  const remaining = allPages.filter(p => !selected.has(p));
  // Shuffle remaining
  for (let i = remaining.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [remaining[i], remaining[j]] = [remaining[j], remaining[i]];
  }
  const untested = remaining.filter(p => !results.passed.includes(p));
  const tested = remaining.filter(p => results.passed.includes(p));
  const candidates = [...untested, ...tested];
  for (const page of candidates) {
    if (selected.size >= RANDOM_PAGE_COUNT + 1) break;
    selected.add(page);
  }
  return [...selected];
}
```

永続化JSON例:

```json
{
  "failing": [],
  "passed": ["/", "/about", "/contact"]
}
```

Lighthouse閾値例:

```javascript
const THRESHOLDS = {
  performance: 95,
  accessibility: 100,
  "best-practices": 100,
  seo: 100,
};
```

## 実践ポイント
- CIで「失敗は必ず再テスト」「ホームは常にテスト」をルール化する
- 結果をJSONで永続化し（リポジトリ or S3 等）、CI開始時に読み込む
- sitemap.xmlからページ検出を自動化してメンテ不要にする
- ヘッドレス監査は直列実行し、1回あたりのページ数（N）を調整してCI時間を制御する
- 閾値を設定し、時間的ラチェティングで段階的に厳しくする（改善を標準化）
- まずは小さなサイトでN=3程度から試し、日本のプロダクト規模に合わせてチューニングする

元記事の実践的なアルゴリズムはコードベースやCIパイプラインに容易に組み込め、Lighthouseやアクセシビリティ監査を現実的に運用する手助けになる。
