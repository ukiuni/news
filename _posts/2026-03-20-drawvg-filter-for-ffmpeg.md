---
layout: post
title: "Drawvg Filter for FFmpeg - FFmpeg用 drawvg フィルター"
date: 2026-03-20T09:20:57.254Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ayosec.github.io/ffmpeg-drawvg/"
source_title: "FFmpeg - drawvg - FFmpeg - drawvg"
source_id: 47413879
excerpt: "FFmpeg 8.1のdrawvgでVGS描画を使い動的マスクやトランジションを簡単生成"
---

# Drawvg Filter for FFmpeg - FFmpeg用 drawvg フィルター
動画編集をプログラムで制御！FFmpegの新フィルターdrawvgで自由自在にベクター描画を重ねる方法

## 要約
FFmpeg 8.1で導入されたdrawvgフィルターは、VGS（Vector Graphics Script）という軽量スクリプト言語でベクター描画をフレーム上にレンダリングし、動的なオーバーレイ・トランジション・マスクなどを手軽に作れます。

## この記事を読むべき理由
- 動画にプログラム的な装飾・マスク・トランジションを加えたい人（配信素材、自動化パイプライン、動画処理ツール開発者）にとって強力な武器になるため。  
- 日本の制作現場やサービスでも、FFmpegを使った自動処理が増えており、描画制御の自由度が格段に上がります。

## 詳細解説
- 基本概念: drawvgはVGSスクリプトを読み、Cairoでラスタライズして各フレームに描画します。VGSはSVGやPostScriptに触発されたコマンド群（rect, circle, moveto, lineto, arcn, setcolor, fill, stroke など）と、簡潔な制御構造（repeat, if, setvar）を提供します。  
- 動的表現: VGS内でFFmpegの式（w,h,t,ts,PIや関数 sin, mod, randomg など）を使えるため、フレームタイムやメタデータに応じたアニメーションや計算が可能です。  
- メタデータ参照とピクセル読み出し: cropdetectなどのフィルターが追加したフレームメタデータは getmetadata コマンドで参照できます。ピクセル色は p(x,y) で読み取り、ピクセルベースのエフェクト（ピクセライズやカラーベースの描画）を実装できます。  
- マスクとトランジション: drawvgでアルファマスク画像をレンダリングし、alphamerge→overlayの組合せでカスタムトランジションを作れます。xfadeにない任意位置のサークルトランジションなどが代表例です。  
- 他フィルターとの連携: boxblurやdisplaceと組み合わせて波形変形やディスプレイスマップを作るなど、既存のFFmpegフィルターと組み合わせることで表現の幅が広がります。  
- 実装上の注意: フレームごとにスクリプトが評価・レンダリングされるため、複雑なスクリプトは処理負荷が高くなります。必要に応じて解像度を落とす、ループやキャッシュ的な構造で負荷を抑える工夫をしましょう。

## 実践ポイント
- 必要環境: FFmpeg 8.1以上（drawvg追加バージョン）を使う。  
- まずは短いスクリプトで試す（例：進捗円を描く）:

```text
# progress.vgs
setvar T 3
setvar R (h / 6)
translate (w - R - 5) (R + 5)
moveto 0 0
arcn 0 0 R (3 * PI / 2 - (PI * 2 * mod(t - ts, T) / T)) (-PI / 2)
setcolor red@0.6
fill
```

```bash
ffmpeg -an -ss 12 -t 3 -i bigbuckbunny.mov -vf "crop=iw-1,drawvg=file=progress.vgs,format=yuv420p" -c:v libvpx-vp9 output.webm
```

- メタデータ参照例: cropdetectの結果を反映するには getmetadata cdx lavfi.cropdetect.x のように取得して矩形を描く。  
- マスク作成: マスクはalphamergeでアルファチャネル化し、overlayで合成する（複数動画を結合するトランジション作成に便利）。  
- 出力互換性: 最終的な互換性のために format=yuv420p を使うケースが多い。Web向けならlibvpx-vp9やH.264の組合せを検討。  
- 参考と練習: 公式のPlaygroundやサンプルスクリプトを読み、既存例を改変して動きを確かめるのが早道。

短時間で「動く」サンプルを作り、用途に合わせてスクリプトを拡張すれば、社内ツールや動画パイプラインへすぐに導入できます。
