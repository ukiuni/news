---
layout: post
title: "Fix macOS 26 (Tahoe) exaggerated rounded corners - macOS 26（Tahoe）の過剰な角丸を修正する"
date: 2026-01-19T21:02:49.738Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/makalin/CornerFix"
source_title: "GitHub - makalin/CornerFix: CornerFix is a lightweight macOS menu bar app that restores sharp display edges by overlaying customizable “caps” on the screen corners. Safe, SIP-friendly, and easy to use, it lets you toggle, resize, and recolor caps to reclaim the squared look Apple removed in macOS 26. Multi-monitor support included."
source_id: 46683589
excerpt: "CornerFixでmacOS26の過剰な角丸を安全に補正し、スクエア寄りの画面に戻せます"
image: "https://opengraph.githubassets.com/a137743eff72c53af7dcfafe84c168e7711a4ed4007ac6daa991d0d2e2cce30d/makalin/CornerFix"
---

# Fix macOS 26 (Tahoe) exaggerated rounded corners - macOS 26（Tahoe）の過剰な角丸を修正する
角が「スクエア」に戻る！macOS 26の過度な角丸を視覚的に取り戻す軽量ツール「CornerFix」

## 要約
CornerFixは、macOS 26で導入された過度なディスプレイ角丸を、画面端にクリック可能なオーバーレイ「キャップ」を重ねて視覚的に補正する軽量なメニューバーアプリです。SIPに安全で、マルチモニタやダーク/ライト自動判別に対応します。

## この記事を読むべき理由
macOSのUI変更で画面端のシルエットが変わり「違和感」を覚える人が多く、日本でもデザイン作業や画面レイアウトに厳しいプロや好みでスクエア寄りに戻したいユーザーが増えています。システムファイルをいじらず安全に見た目だけを戻す方法として実用的だからです。

## 詳細解説
- 何をするか：CornerFixは各ディスプレイの角に小さな「キャップ」ウィンドウを常時最前面で表示し、ディスプレイの外周を直線的に見せます。アプリやウィンドウそのものの角丸は変わりません（あくまでディスプレイのシルエットを補正）。
- 実装と安全性：SwiftUIで作られたメニューバーアプリで、特別な権限やシステム改変を行わないためSIP（System Integrity Protection）に安全です。オーバーレイは .screenSaver ウィンドウレベルを使っているため通常のウィンドウの上に表示されますが、これより上に描画するアプリがあると重なりが発生する場合があります。
- 機能：
  - 各ディスプレイごとに常時表示のクリックスルーオーバーレイ
  - キャップのサイズをピクセル単位で調整可能（小さくすると角丸の内側、逆に大きくすると角を強く隠す）
  - ダーク/ライトに合わせた自動色モード、またはカスタムカラー指定（柄の強い壁紙用）
  - フルスクリーンやSpacesとの互換性、マルチモニタ対応
- 開発・動作環境：macOS 13+（開発ではmacOS 14–26で確認）、Xcode 15+。リポジトリの Swift ファイルをプロジェクトに追加してビルドするだけでメニューバーに表示されます。
- 制約：アプリのウィンドウ角丸は変えられません。ほかに .screenSaver より高いウィンドウレベルで描画するユーティリティや記録ソフトと重なる可能性があります。ライセンスはMIT。

## 実践ポイント
- まず試す：GitHubのリポジトリをクローンし、Xcode 15でビルド。リリースがない場合でもソースから動きます。
- 設定の目安：キャップサイズは環境により好みが分かれるが、外付けディスプレイや高解像度では 8–24px を試すと調整しやすい。壁紙に模様がある場合はカスタムカラーで端の色を合わせると自然に見えます。
- トラブルシュート：キャップが見えない・重なる場合は、他のユーティリティ（録画ソフトや画面効果系アプリ）を停止して確認。表示がおかしいときは再起動またはアプリ再起動で改善することが多い。
- 日本の現場での応用：UIデザインや動画編集で厳密なフレーミングが必要な場面、プレゼンやスクリーンショットの見栄え調整に有効。クリーンなスクリーンシルエットを好む個人ユーザーにも手軽な解決策。

CornerFixはシンプルでリスクの低い「見た目のリカバリ」手段として実用的。macOS 26の見た目が気になるなら、まずソースを試して自分の作業環境に合う設定を見つけてみてください。
