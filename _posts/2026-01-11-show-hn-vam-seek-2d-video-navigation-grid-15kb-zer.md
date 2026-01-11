---
layout: post
title: "Show HN: VAM Seek – 2D video navigation grid, 15KB, zero server load - 2Dビデオシークマーカー（15KB・サーバ負荷ゼロ）"
date: 2026-01-11T03:38:00.953Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/unhaya/vam-seek"
source_title: "GitHub - unhaya/vam-seek: 2D Video Seek Marker - Client-side video navigation grid library"
source_id: 46572304
excerpt: "15KBでサーバ負荷ゼロ、サムネグリッドで瞬時に見たいシーンへワープ"
image: "https://opengraph.githubassets.com/2abc31b0088b1bea0cd3124d791a18f8bab1bdd81ca51857234e36e28406a1e3/unhaya/vam-seek"
---

# Show HN: VAM Seek – 2D video navigation grid, 15KB, zero server load - 2Dビデオシークマーカー（15KB・サーバ負荷ゼロ）
サムネで一目瞭然：15KBの軽量ライブラリで「見たいシーン」へ瞬時にワープする動画グリッドUX

## 要約
VAM Seekはクライアント側でフレームを抽出してサムネイルグリッドを作る、約15KBのJavaScriptライブラリです。従来の1次元シークバーをやめ、視覚的に動画をナビゲートできます（サーバ負荷ゼロ、LRUキャッシュ、React/Vueサンプルあり）。

## この記事を読むべき理由
長時間の講義録やストリーミング、プロモ動画で「目的のシーンを探す」ストレスは日本のプロダクトでも共通課題です。サーバ資源を増やさずにUXを大幅改善できるため、スタートアップ〜大手まで導入候補になります。

## 詳細解説
- 概要動作  
  VAM Seekはブラウザの video + canvas を使い、指定タイムポイントをシークして描画したフレームをサムネ化することでグリッドを生成します。サーバでサムネイルを作らないためインフラコストがかかりません。ライブラリ本体は dist/vam-seek.js の1ファイル（約15KB）。

- クライアント側フレーム抽出（簡略）  
  1. 非表示の video 要素にソースをセット  
  2. video.currentTime を目的時刻に変更して seeked イベントで canvas に描画  
  3. toDataURL で画像化して LRU キャッシュへ保存

- タイムスタンプ計算（VAMアルゴリズム）  
  グリッド上の位置 (x, y) から連続的にタイムスタンプを計算します。概念は次の通りです：
  $$\text{rowIndex}=\left\lfloor\frac{y}{\text{gridHeight}}\times\text{rows}\right\rfloor$$
  $$\text{colContinuous}=\frac{x}{\text{gridWidth}}\times\text{columns}$$
  $$\text{cellIndex}=\text{rowIndex}\times\text{columns}+\text{colContinuous}$$
  $$\text{timestamp}=\min(\text{cellIndex}\times\text{secondsPerCell},\ \text{duration})$$

- パフォーマンスとUX  
  - LRUキャッシュ（デフォルト200フレーム）で再描画を抑制  
  - requestAnimationFrame で滑らかなマーカー移動（60fps目標）  
  - キーボード操作やReact/Vue統合サンプルを提供

- デモとバックエンド  
  デモ用にFastAPI + FFmpeg のバックエンドが付属しますが、本番では不要。注意点として、video 要素がクロスオリジンの場合は CORS/同一オリジンの制約によりフレーム取得が制限されます。

- ブラウザ互換性  
  Chrome 80+, Firefox 75+, Safari 14+, Edge 80+（モバイルでは挙動が異なる場合あり）

## 実践ポイント
- すぐ試す（CDN経由）
```javascript
// CDNで読み込み後に初期化
const vam = VAMSeek.init({
  video: document.getElementById('myVideo'),
  container: document.getElementById('seekGrid'),
  columns: 5,
  secondsPerCell: 15,
  onSeek: (time, cell) => console.log(`Seeked to ${time}s`)
});
```
- 設定のコツ  
  - columns: 3〜10、短い動画は columns を小さく。  
  - secondsPerCell: シーン切替の頻度に合わせて調整（ニュースは短め、講義は長め）。  
  - cacheSize: メモリ許容に応じて増減。200 は一般的な出荷設定。

- 運用上の注意  
  - 動画が外部CDNにある場合、CORSヘッダが必要。クロスオリジンでcanvasに描画するとセキュリティ制限で取得不可。  
  - 商用利用はライセンス確認（個人/教育/研究は無償、商用は有料）。

- 日本向けユースケース例  
  - eラーニング：講義内の重要箇所へ直接ジャンプ  
  - 広告クリエイティブレビュー：良シーンを即座に確認  
  - 企業内記録（会議/監視）検索性向上

ライブラリは軽量で導入がシンプルなため、まずは社内プロトタイプで試し、CORS/ブラウザ制約を確認することを推奨する。ライセンスや商用利用の詳細はリポジトリで要確認。
