---
layout: post
title: "Remarkable Pro Colors - Remarkable Pro の色表現"
date: 2026-02-01T21:53:01.561Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.thregr.org/wavexx/rnd/20260201-remarkable_pro_colors/"
source_title: "2026-02-01: Remarkable Pro Colors"
source_id: 1033486140
excerpt: "Remarkable Proのくすんだ色をPCで忠実に再現するICC＋パレット＋GIMP手順"
---

# Remarkable Pro Colors - Remarkable Pro の色表現
Remarkable Proの“くすんだ色”をPCで忠実にプレビューする簡単ワザ

## 要約
Remarkable Proの限定パレットとディザ処理で出る独特の色味を、著者が撮影＋ICCプロファイル＋パレットで再現する手法を公開。GIMP等でソフトプルーフ→ディザリングするだけでかなり近づく。

## この記事を読むべき理由
タブレット上で見た色とPCにエクスポートした画像が合わず不満を感じている人、Remarkable Proを写真表示やイラスト用途で使いたい人に実務的な対処法を示すから。

## 詳細解説
- 問題点：Proは表示色が限られ（離散パレット）ディザ処理されるため、PC表示と閲覧体験が一致しない。白は灰色寄り、バックライトで黒がやや青寄りになるなど特性がある。  
- カラー抽出：DSLRでタブレットと白基準カードを並べて撮影（中間の間接光、背面光は中くらい）。キャリブレータ済みLCDと肉眼で比較して抽出。  
- パレット／色味：主要なペン色を抽出しパレット化（作者は.gplで配布）。代表的な色例として黒系 #3a4861、灰 #7f7e82、白（実質）#a8aaa7、青 #3c5483 等を採取。  
- プロファイル作成：argyll等でテストチャート→ICC作成の手法を応用。完成したICCはソフトプルーフ用で「perceptual」レンダリングが相性良。完全再現ではないが実用的。  
- 注意点：Pro側の自動コントラスト→量子化ディザ処理を完全に再現するには専用ビューアやプラグインが要るため、ICCは「より良い目安」であり青寄りのシフト等残る。

## 実践ポイント
- 配布ファイル：rmpro-v0.icc（カラー・プロファイル）、rmpro-palette.gpl（GIMPパレット）を入手しておく。  
- GIMPでの簡易手順：
  1. Image → Color Management → Soft-proof profile で rmpro-v0.icc を選択。  
  2. レンダリング意図を「Perceptual」に設定。  
  3. View → Color Management → Proof colors を有効化。  
  4. 必要に応じて Hue/Contrast を調整し、最後にディザ（量子化）処理をかけて比較する。  
- 画像調整のコツ：重要領域がパレットで潰れないようにコントラストを抑え、色相を少しシフトしてProの近い色に乗せると見栄えが良くなる。  
- 運用上の留意点：Proは描画精度（ペンの追従・筆圧）や同期/UI周りに不満があるため、作業用途と鑑賞用途を分けて運用するのが現実的（例：Proは参照・閲覧、別機種で細かい作画）。  

興味があれば配布ファイル名（rmpro-v0.icc / rmpro-palette.gpl）を元に検索して入手し、手元のワークフローに組み込んでみてください。
