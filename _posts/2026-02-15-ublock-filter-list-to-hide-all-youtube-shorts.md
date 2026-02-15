---
layout: post
title: "uBlock filter list to hide all YouTube Shorts - YouTube Shorts を非表示にする uBlock フィルターリスト"
date: 2026-02-15T16:01:39.270Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/i5heu/ublock-hide-yt-shorts"
source_title: "GitHub - i5heu/ublock-hide-yt-shorts: Maintained - uBlock Origin filter list to hide YouTube Shorts"
source_id: 1676691170
excerpt: "ワンクリックでYouTube Shortsを画面から消すuBlockフィルター導入法"
image: "https://opengraph.githubassets.com/b2e648597cd4dc221e747f21dd20b9b8b9d44c423c0076fb75734987ab8fc6d6/i5heu/ublock-hide-yt-shorts"
---

# uBlock filter list to hide all YouTube Shorts - YouTube Shorts を非表示にする uBlock フィルターリスト
魅せられるタイトル: 「YouTube Shortsを二度と見たくない人へ──ワンクリックで“短尺コンテンツ”を消す方法」

## 要約
uBlock Origin 用のコミュニティ保守フィルターで、YouTube 上の Shorts 表示（サムネ・タイムライン・再生候補など）を画面上から隠します。コメント非表示用の別リストも提供されています。

## この記事を読むべき理由
日本でも短尺動画（Shorts）は急速に増加し、おすすめの雑多さや視聴体験の分断を感じる人が増えています。ブラウザレベルでコントロールする手軽な対処法を知っておくと、作業効率や集中力維持に直結します。

## 詳細解説
- 何をするものか：uBlock Origin の「フィルターリスト」として読み込むだけで、YouTube の Shorts コンテンツに関連する要素（ショート動画のカード、サムネイル、ショート専用プレイヤーなど）を CSS セレクタやネットワークリクエストのフィルタで非表示にします。コメントを隠すオプションも別リスト（comments.txt）で用意。
- 技術的ポイント：これは広告ブロッカーの「カスタムフィルター」を利用した方法で、要素非表示（cosmetic filters）や URL ブロックを組み合わせることで表示を消します。実際の動画の配信自体を止めるのではなく、ブラウザ側で見えなくするアプローチです。
- メンテナンスと信頼性：元のリスト作成者が活動を停止した後、i5heu がフォークして保守しています。YouTube の DOM やクラス名変更で動作が崩れるため、公開リポジトリで更新が続く限り有効です。ライセンスは MIT、Google/YouTube とは無関係のコミュニティプロジェクトです。

## 実践ポイント
1. uBlock Origin をブラウザに入れる（未導入の場合）。
2. Dashboard > Filter lists を開く。
3. 一番下の「Import...」欄に以下を貼る：
   - Shorts 非表示リスト: https://raw.githubusercontent.com/i5heu/ublock-hide-yt-shorts/master/list.txt
   - コメントも隠したい場合: https://raw.githubusercontent.com/i5heu/ublock-hide-yt-shorts/master/comments.txt
4. 更新を待ってページをリロードするだけで Shorts 表示が消えます。
5. 注意点：YouTube の仕様変更で効かなくなることがあるため、GitHub リポジトリをスターやウォッチして更新状況を確認すると安心です。

短時間で効果を実感できる実用的な手段なので、まずは試してみてフィード体験を取り戻しましょう。
