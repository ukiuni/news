---
layout: post
title: "We Built a Video Rendering Engine by Lying to the Browser About What Time It Is - ブラウザに「時間」を偽装して動画を作る方法"
date: 2026-03-03T09:45:08.420Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.replit.com/browsers-dont-want-to-be-cameras"
source_title: "Replit — We Built a Video Rendering Engine by Lying to the Browser About What Time It Is"
source_id: 47203827
excerpt: "ブラウザの時間を仮想化して任意ページをフレーム単位で決定論的にMP4化する手法"
image: "https://cdn.sanity.io/images/bj34pdbp/migration/d01f4f249ff1c45cdc6cb49090cfcf7c629a0cdc-1400x787.jpg"
---

# We Built a Video Rendering Engine by Lying to the Browser About What Time It Is - ブラウザに「時間」を偽装して動画を作る方法
ブラウザに時間の進み方を信じさせて、任意のウェブページをフレーム単位で安定したMP4に変換する技術

## 要約
Replitは「ブラウザの時間」を完全に仮想化して任意のページをフレーム単位でレンダリングする仕組みを作り、アニメーションや音声を決定論的にMP4に書き出せるようにした。

## この記事を読むべき理由
ブラウザは本来リアルタイムで動くため、スクリーンキャプチャだけではフレーム落ちや音声ズレが起きる。Web上のあらゆる表現（CSSアニメ、canvas、外部ライブラリなど）を壊さずに確実に動画化したいサービス設計や動画自動生成AIを扱う日本の開発者に実用的な知見を与える。

## 詳細解説
- 仮想クロック：ページに注入するスクリプトで setTimeout/setInterval/requestAnimationFrame/Date/Date.now/performance.now を差し替え、時間を外部で1フレームごとに進める。これによりページ側は常に均一なフレーム間隔を前提に動作する。
- フレームループ（概念）：
```javascript
// javascript
async function nextFrame() {
  await seekCSSAnimations(currentTime);
  await seekMedias();
  currentTime += frameInterval;
  fireIntervalAndTimeouts(currentTime);
  fireRAFCallbacks(currentTime);
  await captureFrame(); // スクリーンショット
  nextFrame();
}
```
- コンポジタのウォームアップ：レンダリング開始前の待機でChrome内部バッファが枯渇する問題を回避するため、見えない「スキップフレーム」を30fps程度で吐いて内部状態を温める。
- 動画要素対策：headless環境の<video>再生は非決定論的なため多段処理を採用。MutationObserverで検出→サーバーでFFmpegを使ってfragmented MP4にトランスコード→mp4box.jsでブラウザ内デマックス→WebCodecs（ネイティブ優先、WASMフォールバック）でデコード→canvasに描画して仮想クロックに同期。
- 音声の取り扱い：ヘッドレスから出力を録るのは不安定なため、Web AudioやHTMLMediaElementの主要APIをフックして「再生しようとしているソース、開始時刻、ボリューム、ループ情報」を捕捉し、オリジナル音声をサーバーでダウンロードしてFFmpegでタイミング・音量・フェードを再構成・ミックスする（atrim/aloop/adelay/volume/afade → amix）。
- 決定論のための安全策：OffscreenCanvasやtransferControlToOffscreenを無効化、サブリソースはSSRF対策で検証、リソース集中的な処理のため単一実行（concurrency=1）運用など。既存プロジェクト（WebVideoCreator）を踏襲しつつTypeScript/Puppeteer向けに再実装している。

## 実践ポイント
- 任意ページを動画化するなら「時間の仮想化」が第一歩：主要タイミングAPIを差し替える設計を検討する。  
- <video>や音声はそのまま頼ると破綻する：fragmented MP4 + mp4box.js + WebCodecs（またはWASM）+ canvas描画の流れを用意する。  
- 音声は再生意図をフックしてサーバーで再合成する方が確実。  
- OffscreenCanvas等の回避策、SSRFチェック、リソース隔離（単一レンダ実行／メモリ制限）を必須で組み込む。  
- 参考実装（WebVideoCreator等）を調査してから、自社のクラウド環境向けにPuppeteer/FFmpeg周りを最適化すると工数削減になる。

興味があれば、仮想クロックの差し替えや動画要素の多段パイプラインに関する小さなサンプルコードを提示できます。どの部分を深掘りしますか？
