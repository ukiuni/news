---
layout: post
title: "Show HN: uBlock filter list to blur all Instagram Reels - uBlockフィルターでInstagramのReelsをすべてぼかす"
date: 2026-03-02T20:59:11.163Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gist.github.com/shraiwi/009c652da6ce8c99a6e1e0c86fe66886"
source_title: "Nuke Insta Slop · GitHub"
source_id: 47223147
excerpt: "簡単uBlockフィルターでInstagramのReelsを一括ぼかし、タイムラインの騒音を即消去"
image: "https://github.githubassets.com/assets/gist-og-image-54fd7dc0713e.png"
---

# Show HN: uBlock filter list to blur all Instagram Reels - uBlockフィルターでInstagramのReelsをすべてぼかす
Reelsを一網打尽に“ぼかす”ことでアルゴリズムのゴミを可視化し、タイムラインを静かに取り戻す方法

## 要約
uBlock Origin用の簡潔なフィルター群で、InstagramのReelsタブや動画コンテンツ（フォローしていない投稿含む）をぼかして視覚的に排除する手法を紹介する。

## この記事を読むべき理由
日本でもInstagramの短尺動画が職場や集中の妨げになる場面が増えています。簡単に導入できるuBlockフィルターで視覚的ノイズを減らし、生産性や体験の制御が可能です。

## 詳細解説
このgistはuBlockの「コスメティックフィルター」を使い、特定のDOM要素にスタイルを強制適用して動画やReelsのアクセスポイントを目立たなくします。主な技術ポイントは次の通りです。

- ドメイン指定のコスメティックフィルター形式：`instagram.com##selector`。
- Reelsへのリンクを消す／目立たなくするために`a[href="/reels/"]`をターゲット。
- フォローしていない投稿の検出は、投稿内に「Follow」ボタンを含む要素を`:has(div:has-text(/^Follow$/))`でマッチさせ、opacity／filterでぼかす。
- 動画判定は`div[aria-label="Video player"]`などアクセシビリティ属性を使っているため、ほぼ確実に動画コンテンツに適用される。
- 視覚的に「消す」のではなく「ぼかす（blur + grayscale）」ことで、アルゴリズムの埋め草の量を把握できる設計。

前提条件・制限：
- uBlock Originのコスメティックフィルターが必要。ブラウザやuBlockのバージョンにより擬似クラス（:has, :has-text）の動作が異なることがある。
- 友人の動画も含めて全動画に作用するため、重要な動画を見逃す可能性がある（元作者も警告）。

フィルター例（そのままuBlockの「My filters」に貼れます）:

```text
instagram.com##a[href="/reels/"]
instagram.com##article:has(div:has-text(/^Follow$/)):style(opacity: 0.2 !important; filter: blur(2em) grayscale(100%) !important; pointer-events: none !important;)
instagram.com##article:has(div[aria-label="Video player"]):style(opacity: 0.2 !important; filter: blur(2em) grayscale(100%) !important; pointer-events: none !important;)
```

## 日本市場との関連性
- 日本のSNS利用は通勤・休憩時間と強く結びつき、短尺動画の過剰露出が時間の浪費につながるケースが多い。企業のリモートワーク環境や個人の集中管理に役立つ。
- インフルエンサー文化が強い日本では、非フォロワー動画や広告的なアルゴリズム表示を抑えることで、業務や学習における雑音を低減できる。

## 実践ポイント
- 導入手順：uBlock Origin → ダッシュボード → 「My filters」に上記フィルターを貼って「Apply changes」。
- カスタマイズ：ぼかし強度（blur(2em)）やopacityを調整して視認性を変える。特定ユーザーを除外したい場合はセレクタをユーザー固有のクラスやリンクに合わせて条件追加。
- テスト：PCデスクトップで動作確認を行い、モバイルアプリやWebViewでは効かない点に注意。
- 注意：重要な動画を見逃す可能性があるため、一時的に無効化するプロファイルを作ると便利。

必要なら、導入手順をスクリーンショット付きで簡潔に案内しますか？
