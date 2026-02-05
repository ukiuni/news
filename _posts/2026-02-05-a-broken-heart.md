---
layout: post
title: "A Broken Heart - 壊れたハート"
date: 2026-02-05T13:00:36.243Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://allenpike.com/2026/a-broken-heart/"
source_title: "A Broken Heart - Allen Pike"
source_id: 46844393
excerpt: "SafariでNoto Color Emojiが一文字で約1600ms遅延、原因特定と即時回避法を解説"
image: "https://allenpike.com/images/2026/profile-banner.jpg"
---

# A Broken Heart - 壊れたハート

Safariがハート絵文字で100倍遅くなる？即効で使える原因特定と回避策

## 要約
あるダッシュボードがSafariで激遅になった原因は、Googleの「Noto Color Emoji」（COLRv1）フォントに含まれる絵文字で、単一文字でレイアウトが約1600msかかるというSafari側の問題でした。コーディングエージェントを使った二分探索で原因を特定し、最小再現例を作って報告しています。

## この記事を読むべき理由
日本のサービスでも絵文字はUIに頻出で、macOS/iOSユーザーは多い。絵文字フォントの選定一つでパフォーマンスが劇的に変わるため、開発・運用で致命的な落とし穴を避けられます。

## 詳細解説
- 症状と調査の流れ：最初はReactの再レンダリングを疑ったが効果なし。Safariのパフォーマンスプロファイラでレイアウト処理がCPUを占有していることを確認。
- デバッグ手法：コーディングエージェント（記事ではClaude）に手伝わせ、変更を二分探索的に外していき、最小の差分を見つけることで犯人を特定。
- 真の原因：Noto Color EmojiはCOLRv1（カラーフォント）を使い、SafariではフォールバックでSVG系の処理（CoreSVG）が走ってしまい、単一の絵文字で複数回のレイアウトが各1600msになる現象が発生。
- 最小再現例（記事での例）：

```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Color+Emoji" rel="stylesheet">
  <style>body { font-family: "Noto Color Emoji"; }</style>
</head>
<body>💔</body>
</html>
```

- 結論：Safari（現時点）ではNoto Color Emojiが重い可能性があるため、フォント順や代替手段で回避するのが現実的。

## 実践ポイント
- まずSafariで必ず動作・パフォーマンス確認を行う（特にmac/iOSターゲットのUI）。
- font-familyでは「Apple Color Emoji」を先に置くなど、Noto Color Emojiを優先しない順序にする。
- 絵文字が多用されるUIでは、SVG/アイコンフォントや画像ベースの代替を検討する。
- ブラウザバグか判断に迷ったら最小再現例を作ってWebKit/Safariへ報告する（バグ報告は修正を早める）。
- AIエージェントは探索の高速化に有効だが、最終確認と最小ケース化は人がやること。

以上。
