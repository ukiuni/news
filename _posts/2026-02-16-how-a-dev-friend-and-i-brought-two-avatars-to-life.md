---
layout: post
title: "How a DEV Friend and I Brought Two Avatars to Life - DEVの友達と僕が2体のアバターを動かした話"
date: 2026-02-16T16:25:45.221Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/itsugo/how-a-dev-friend-and-i-brought-two-avatars-to-life-chp"
source_title: "How a DEV Friend and I Brought Two Avatars to Life - DEV Community"
source_id: 3256702
excerpt: "VRoidで作った2体のアバターに自然な会話と動作を短時間で実装する手順と設計法を具体的に解説"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Feifm5cpen8arsfq86w8x.png"
---

# How a DEV Friend and I Brought Two Avatars to Life - DEVの友達と僕が2体のアバターを動かした話
夜の20分で生まれた会話するアバター — 小さなコラボが生んだ「動くキャラクター」の作り方

## 要約
ネットで出会ったインドと日本の開発者が、VRoidで作ったアバターに自然な立ち振る舞いと対話を与えるまでの試行錯誤を共有した話です。技術的には「モデル→ポーズ修正→アニメーション重ね→会話オーケストレーション」が鍵でした。

## この記事を読むべき理由
VR/3Dアバター、VTuber、ビジュアルノベルなどが身近な日本市場で、少人数かつ非同期コラボでも「動くキャラ」を素早く作る実践知が得られます。初心者でも取り組める手順と設計のヒントが学べます。

## 詳細解説
- 初期フェーズは「簡単な形で画面構成を検証」することから。大きな設計よりまず動くものを作るのがコツ。
- アバターはVRoid Studioで作成→エクスポート→読み込み。ここでよくある問題はデフォルトのTポーズ（手を広げたまま）で「モデルはあるがキャラに見えない」点。ニュートラル姿勢（両手下ろし）に戻すだけで印象が大きく変わります。
- アニメーションは段階的に追加：挨拶、会話中の小さなジェスチャー、ため息など。直接デフォルトジェスチャを上書きしようとして失敗する経験から、アニメーションシステム固有のルールを尊重する重要性を学んでいます。
- 会話の中身（脚本）は技術より難しい場合がある：短さ、自然さ、ユーモアの塩梅は何度も調整が必要。
- 大事なのは「振る舞いのオーケストレーション」。会話やアニメーションをデータとして定義し、シーンがそのシーケンスを解釈する設計にすると拡張性が上がります。例：

```javascript
const DIALOGUE = [
  { speaker: "A", text: "I'm Web Developer Hyper. I like to make fun things.", animation: "VRMA_03_peace_sign.vrma" },
  { speaker: "B", text: "Hello! I'm Itsugo. And I like turning ideas into something real.", animation: "VRMA_04_shoot.vrma" },
];
```

- 同期の難しさ（アニメ完了検知）への対処：アニメが終了イベントを必ず教えてくれるとは限らないため、「アニメ完了待ち OR タイムアウト」のどちらか早い方で次へ進める実装にして堅牢化しています。簡潔な実装例：

```javascript
async function playAndWait(animation, timeoutMs = 3000) {
  const finishPromise = waitForAnimationEnd(animation);
  const timeoutPromise = new Promise(res => setTimeout(res, timeoutMs));
  await Promise.race([finishPromise, timeoutPromise]);
}
```

- コラボの不可視要素（コードの読みやすさ、コメント、ジェスチャ強度調整など）を丁寧にやることが長期的な価値を生む、という点も強調されています。

## 実践ポイント
- まずはVRoidで簡単なモデルを作り、読み込んで「ニュートラル姿勢」に直す。これだけで「キャラ感」が増す。
- 振る舞いはコードにハードコーディングせず、JSONや配列で定義してシーンに解釈させる。
- アニメ完了は「イベント待ち + タイムアウト」の組合せで実装しておく（フリーズ対策）。
- 台詞は短く自然に。複数回リライトしてテンポを確かめる。
- 日本ではビジュアルノベルやVTuberコンテンツとの親和性が高いので、次の展開（対話型ストーリー／インタラクティブ体験）を視野に入れると良い。

元記事は小さな実験から生まれたコラボの記録ですが、実践的な設計思考（データ駆動の対話管理、フェイルセーフな同期）を学べる良い教材です。
