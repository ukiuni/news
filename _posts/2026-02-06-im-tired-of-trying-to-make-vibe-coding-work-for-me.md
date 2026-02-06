---
layout: post
title: "I'm tired of trying to make vibe coding work for me - 「雰囲気コーディング」を無理に続けるのに疲れた"
date: 2026-02-06T09:24:48.321Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://youtu.be/ly-GM3aYgfQ?si=QRuDvEuzlfIRENfX"
source_title: "I&#39;m tired of trying to make vibe coding work for me - YouTube"
source_id: 407987421
excerpt: "雰囲気作りに疲れたなら、VS Codeで摩擦を減らして成果を数値化する実践法を試そう"
image: "https://i.ytimg.com/vi/ly-GM3aYgfQ/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGGIgYihiMA8=&amp;rs=AOn4CLDCskRMnKfaOuELhabRoiYScowfTA"
---

# I'm tired of trying to make vibe coding work for me - 「雰囲気コーディング」を無理に続けるのに疲れた
雰囲気重視の“vibe coding”に疲れたエンジニア向け：本当に集中できる開発環境を取り戻す方法

## 要約
「雰囲気（vibe）を整えればコードが捗る」という流行に疲れた人へ。本当に効果のある集中法と、見た目重視の落とし穴を簡潔に解説します。

## この記事を読むべき理由
日本でも「見た目の良いセットアップ」「作業BGM」「おしゃれなテーマ」がSNSで話題になりがちです。けれども、それが生産性向上に直結するとは限らない――忙しい日本のエンジニアや副業プログラマが無駄な試行錯誤を減らし、実務で効く方法を知るために読むべき記事です。

## 詳細解説
- vibe codingとは：音楽プレイリスト、デスク周りの美化、エディタテーマやフォント、照明など「雰囲気」を整えることで集中を促すという考え方。SNSでの見栄えも相まって人気化しています。
- なぜ効かないことがあるか：
  - 過度な最適化で「設定ジプシー」になり、本来の作業時間が削られる。
  - 新しい環境に慣れるための認知コストが高く、集中の回復に時間がかかる。
  - タスクの種類（設計・実装・レビュー）によって必要な集中の質が違い、同じ雰囲気で全部をカバーできない。
- 科学的視点：短く区切った深い集中（ディープワーク）と、報酬系を刺激する短い成功体験の組み合わせが有効。BGMや照明は補助であり、唯一無二の解決策ではない。
- ツール面の具体例（VS Codeユーザー向け）：
  - Zen ModeやFocus ModeでUIノイズを減らす。
  - 統合ターミナルと出力パネルをワンキーで切り替えられるキーバインドを設定し、コンテキスト切替コストを下げる。
  - テーマ変更は「作業前の儀式」になりがちなので、1〜2セットに絞る。

## 実践ポイント
1. まずは1週間だけ「雰囲気の変更を禁止」して実績（完了タスク数・時間）を測る。効果が分からなければ見た目改善は後回しに。
2. タスク別に環境を決める：設計は無音、実装は軽いBGM、レビューは完全に別ウィンドウ等。
3. 小さく試す：1つだけ変更（例：通知オフ）を1週間続けて効果を評価する。
4. VS Codeの簡単設定例（Zen Mode とトグルキー）：

```json
// settings.json
{
  "zenMode.centerLayout": true,
  "zenMode.hideTabs": true,
  "zenMode.restore": true,
  "workbench.activityBar.visible": false
}
```

5. 測定を習慣化：タイマー（ポモドーロ）と簡単なログ（今日やったこと）で可視化する。

短期的な「雰囲気」を追うより、作業ごとに最小限の摩擦を取り除くことが長期的な生産性を上げます。まずは小さな変更を一つずつ試して、数字で判断してください。
