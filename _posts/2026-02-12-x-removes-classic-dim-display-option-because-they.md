---
layout: post
title: "X removes classic Dim display option because they “don’t have capacity” for 3 colors - Xが「3色は対応できない」として“Dim”表示を削除"
date: 2026-02-12T16:28:19.615Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.dexerto.com/entertainment/x-removes-classic-dim-display-option-because-they-dont-have-capacity-for-3-colors-3318084/"
source_title: "X removes classic Dim display option because they “don’t have capacity” for 3 colors - Dexerto"
source_id: 443445365
excerpt: "Xが夜間の中間色「Dim」を廃止、目疲れやアクセシビリティ問題が波紋を呼ぶ"
image: "https://www.dexerto.com/cdn-image/wp-content/uploads/2026/02/12/x-dim-mode-removed.jpg"
---

# X removes classic Dim display option because they “don’t have capacity” for 3 colors - Xが「3色は対応できない」として“Dim”表示を削除
夜のブラウジング疲れを救ってくれた“中間色”がウェブから消えた——あなたの目と開発現場に与える影響

## 要約
X（旧Twitter）がウェブ版で長年あった「Dim」テーマ（青みがかった中間の暗色）を2026年2月12日の更新で削除。ヘッド・オブ・プロダクトは「現状は2色以上の対応はできない」と説明しているが、波紋が広がっている。

## この記事を読むべき理由
多くの日本ユーザーは深夜にOLED端末で閲覧することが多く、純黒は目の疲れや視認性の問題を引き起こす。UIの色数削減はUX／アクセシビリティに直結するため、一般ユーザーもエンジニアも知っておくべき変更です。

## 詳細解説
- Dimの経緯：2016年にNight Modeとして導入、2019年に名称変更。白のDefaultと漆黒のLights outの“中間”として親しまれてきた。  
- 削除の範囲：今回の変更はウェブ版のみ。Android/iOSアプリでは現状Dimは残っている。  
- 運営の説明：Xのプロダクト責任者ニキータ・ビア氏が「我々には今、2色以上をサポートするキャパシティがない」とツイート。代替としてウェブの黒を「やや明るくする」検討を示唆したが時期は未定。  
- 反応と懸念：ユーザーは「大企業で3色表示が無理なのか」と疑問視。特にOLEDでは純黒の高コントラストが夜間の目の刺激となるため、アクセシビリティの観点から問題視されている。  
- 背景の文脈：2023年にイーロン・マスク氏がDim削除を示唆していた流れの延長で、UI統一や保守コスト低減を狙う方針の一環と見られる。技術的にはCSSのテーマ切替やprefers-color-schemeで複数テーマは容易だが、プロダクト判断で削減された可能性が高い。

## 実践ポイント
- 一般ユーザー向け
  - ウェブでDimが消えたら：モバイルアプリではまだ使えるのでアプリを利用するか、ブラウザ拡張（例：Dark Reader、Stylus）で中間トーンを再現する。  
  - 目の負担対策：夜間はOSのブルーライトカットや画面輝度を下げ、フォントサイズ／コントラスト調整を行う。  
  - フィードバックを送る：Xの設定や公式アカウントへ要望を送ることでユーザー声を可視化する。  
- 開発者／プロダクト担当向け
  - テーマ設計の教訓：ユーザーに選択肢を与えること（ダーク／ライト／ミドル）はUX上有益。prefers-color-schemeだけでなく複数カラーパレットの提供を検討する。  
  - OLEDやアクセシビリティでの検証を必ず行う（夜間テスト、コントラスト比、色覚多様性対応）。  
  - コスト低減の名目でテーマを削る場合は代替手段の提示と移行期間を設ける。

短いですが、変化は日常の使い勝手と健康に直結します。ウェブ運営側の決定が個々の閲覧体験にどう影響するか、今後も注視しましょう。
