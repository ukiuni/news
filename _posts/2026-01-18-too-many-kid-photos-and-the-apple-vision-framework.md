---
layout: post
title: "Too many kid photos and the Apple Vision Framework - 子ども写真が増えすぎた問題とApple Visionフレームワーク"
date: 2026-01-18T18:09:50.735Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://shutterslim.com/blog/2026/01/18/vision-framework-image-similarity/"
source_title: "Too many kid photos, the Apple Vision Framework and the #2 spot in the German App Store - ShutterSlim"
source_id: 423682661
excerpt: "Apple Visionで12,000枚・150GBの子ども写真を高速に整理する方法"
---

# Too many kid photos and the Apple Vision Framework - 子ども写真が増えすぎた問題とApple Visionフレームワーク
子ども写真を一気に片付けるApple Vision活用術 — 12,000枚・150GBを削除してドイツApp Storeで2位に躍進

## 要約
写真ライブラリの「見た目がほぼ同じ」写真をピンポイントで削除するために、AppleのVisionフレームワークの「Feature Print」を使って画像の意味的類似度を計算し、大量の重複・類似写真を効率的に整理した事例。

## この記事を読むべき理由
スマホ／デジカメで写真が増え続ける日本のユーザーにとって、ローカルで高速かつプライバシー重視に写真整理できる手法は実用的。古いMacや小容量SSDでも現実的に運用できる工夫が参考になる。

## 詳細解説
- 問題点  
  単純なハッシュ比較やピクセル等価だけでは、微妙に異なるが内容は同じ（例：同じラクダに連写した15枚）写真は検出できない。必要なのは「意味的類似性（semantic similarity）」。

- VisionのFeature Print  
  AppleのVisionフレームワークにある VNGenerateImageFeaturePrintRequest は、画像をニューラルネットに通して高次元の「feature print」（VNFeaturePrintObservation）を生成する。類似画像は近いベクトルを返し、ベクトル間のユークリッド距離で似ているかを判定できる。距離が0に近いほど同一に近い。実装例（Swift）:

  ```swift
  // swift
  let request = VNGenerateImageFeaturePrintRequest()
  let handler = VNImageRequestHandler(cgImage: image, options: [:])
  try handler.perform([request])
  guard let featurePrint = request.results?.first as? VNFeaturePrintObservation else { return }
  var distance: Float = 0
  try featurePrint1.computeDistance(&distance, to: featurePrint2)
  ```

  実運用では、著者はラベリングで閾値を調整して $0.35$ をデフォルトに設定した。$0.2$ だと見逃しが多く、$0.5$ だと別物が混ざるというバランス。

- 計算量の工夫  
  全ての組合せ比較は $$\frac{n(n-1)}{2}$$ に等しく、例として $n=35{,}000$ のとき約6億回の計算になるため現実的でない。そこで「時間クラスタリング」を導入：撮影時刻に10分以上のギャップができたら別グループに分け、グループ内のみ比較する方式。実例では5,300クラスタに分かれ、中央値は2–3枚なので比較数は数十万に削減できた。大きなイベント（結婚式379枚→約71,000組）は例外的に重いが全体として十分現実的。

- キャッシュと再走査  
  Feature print生成は高コストなので、SQLite 等に「写真ID＋更新日時」をキーにしてfeature printをキャッシュし、ペアごとの類似度結果も保存する。こうすると2回目以降は差分だけ処理し、数分で再走査が終わる。

- ベスト写真の自動選定  
  重複群からどれを残すか自動で選ぶため、スコアリングを導入。著者の重み付けは以下（概念）:
  - シャープネス 25%（エッジ検出の分散）
  - 顔の品質 30%（Visionのランドマーク検出）
  - 構図 15%（ルール・オブ・サードの簡易判定）
  - 解像度 20%
  - 新しさ（編集済み） 10%

  全体スコアは加重平均で算出し、レビュー作業を「確認→次へ」とキーボード中心に高速化できる。

- 安全策と限界  
  削除はまずアプリ内のゴミ箱へ。最終的に空にするとPhotos.appの「最近削除」に移行するため30日以内の復元が可能。Visionのモデルはブラックボックスで学習データや最適化基準が不明な点、しきい値調整が必要な点が限界だが、照明やトリミング、軽微な回転に対する頑健さは期待より高いと報告されている。

- 成果  
  著者は約12,000枚・約150GBを削除し、アプリをApp Storeに出したところドイツのApp Storeで2位を記録した。

## 実践ポイント
- 閾値の出発点は $0.35$ 前後を試す（ライブラリ特性で調整）。  
- 比較は撮影時刻で10分程度のウィンドウに分けると爆発的な組合せを避けられる。  
- Feature printは生成コストが高いので写真ID＋更新日時でSQLiteにキャッシュする。  
- 自動選定は顔に重みを置くとユーザ満足度が上がる（目が開いている等）。  
- 削除は段階的に：アプリ内ゴミ箱→Photosの最近削除で二重保護。  
- 最初は小規模サンプルで閾値と重みをチューニングしてから全体適用する。

このアプローチは、プライバシー重視でローカル処理を好む日本のユーザーや、容量の小さいMacを使う開発者／写真愛好家に実用的な解決策を提供する。
