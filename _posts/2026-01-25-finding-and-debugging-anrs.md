---
layout: post
title: "Finding and debugging ANRs - ANR（応答なし）検出とデバッグ"
date: 2026-01-25T08:23:21.057Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/NightMare8587/AnrLagCatcher"
source_title: "GitHub - NightMare8587/AnrLagCatcher"
source_id: 418138386
excerpt: "LagCatcherで50–200msの小さなジャンクを検出し原因行に即ジャンプ"
image: "https://opengraph.githubassets.com/2b611add5069ddbda71f23751440f10cf7fcad638e757239ee367eb47055e666/NightMare8587/AnrLagCatcher"
---

# Finding and debugging ANRs - ANR（応答なし）検出とデバッグ
魅力的なタイトル: 「一瞬の“カクつき”を見逃さない：Android向け軽量ANR検出ツール『LagCatcher』の使い方」

## 要約
LagCatcherはメインスレッドの小さな「ジャンク（50–200ms）」やフリーズを検出し、原因となったソース行を特定してAndroid Studioで直接開ける形式のログを出す軽量SDKです。ワンラインで導入でき、複数の感度レベルで詳細解析を行います。

## この記事を読むべき理由
日本のモバイル市場は多様な端末と高いUX期待が混在しており、短時間の描画遅延でもユーザー離脱につながります。アニメーションや決済フロー、ブラウジング体験を滑らかに保つために、早期に「小さなジャンク」を捕まえる手法は必須です。

## 詳細解説
- 目的：システムのANRダイアログ（5秒）よりも短い、ユーザ体験を損なう短時間の遅延（50–200ms）を検出する。
- 検出対象：ロジックブロック、重いXMLレイアウト膨張、Jetpack Compose周りの描画問題などを区別して分析する機能を持つ。
- 精度：発生箇所をプロジェクト内のソース行（FileName.kt:Line）で出力し、クリックでAndroid Studioに飛べる標準的なスタックトレース形式を生成する。
- 導入：ほぼゼロ設定で導入可能。推奨はJitPackで依存を追加し、Application.onCreateでデバッグビルドのみインストールする形。
- 感度（例）：
  - EASE ≈ 200ms（緩め、まずは大きなフリーズ検出）
  - HEAVY ≈ 100ms（標準推奨。視覚的ジャンクを捕える）
  - BRUTAL ≈ 50ms（アニメやゲーム向け）
  - NO_MERCY ≈ 20ms（60fps厳守、5msサンプリングでオーバーヘッドあり）
- 注意点：極端な感度（NO_MERCY）はサンプリング負荷が増えるため、ビルドやCIでの運用は慎重に。

Kotlin導入例：

```kotlin
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        if (BuildConfig.DEBUG) {
            // 感度は SeverityLevel.HEAVY など
            LagCatcher.install(this, SeverityLevel.HEAVY)
        }
    }
}
```

## 実践ポイント
- まずは開発・デバッグ環境でHEAVY（100ms）を有効化して意図しないジャンクを洗い出す。  
- 出力される FileName.kt:Line を使い、Android Studioで該当行を即確認。UIスレッド周りの同期や重い処理をオフロードする修正を優先する。  
- アニメや高FPSが重要な機能はBRUTAL/NO_MERCYで厳しく検査するが、計測オーバーヘッドに注意してCI運用を検討する。  
- 多機種で検証し、端末依存のUI膨張（XML）やComposeの描画負荷を拾い上げる。  

元リポジトリ: NightMare8587/AnrLagCatcher（GitHub）
