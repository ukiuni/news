---
layout: post
title: "I Tried Vibing an RSS Reader and My Dreams Did Not Come True - RSSリーダーを「vibeコーディング」してみたが夢は叶わなかった"
date: 2026-04-07T10:00:39.686Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.jim-nielsen.com/2026/vibe-dreams-didnt-come-true/"
source_title: "I Tried Vibing an RSS Reader and My Dreams Did Not Come True - Jim Nielsen’s Blog"
source_id: 834268837
excerpt: "AIで一晩で作ったRSSリーダー試作は速かったが、CORSや配布で挫折し学びが多かった"
image: "https://cdn.jim-nielsen.com/blog/2026/vibe-rss-mac-app-2.png"
---

# I Tried Vibing an RSS Reader and My Dreams Did Not Come True - RSSリーダーを「vibeコーディング」してみたが夢は叶わなかった
魅力的すぎてついクリックしたくなるタイトル: 「AIで一晩で作ったRSSリーダー、夢の体験にはほど遠かったけど学びは大きかった話」

## 要約
AI（LLM）を使って「雰囲気で」RSSリーダーのプロトタイプを作った試行記。macOSネイティブ→PWA→Electronと試し、速く作れる一方でCORS、デバッグ、配布、品質の壁に直面したという結論。

## この記事を読むべき理由
LLMを使った高速プロトタイピングが現実の製品化でどんな落とし穴に当たるか、日本のエンジニアやプロダクト担当が短時間で概念実証を行う際に役立つ実践的な示唆が得られます。

## 詳細解説
- アプローチ：バックエンドは既存のFeedbin APIを利用。フロントはまず未知のmacOSネイティブ（Xcode/Swift）に挑戦し、LLMのサポートで最短で動くものを作成。  
- 問題点：ネイティブ開発は学習コストが高く、AIが複雑なUI改修や細かいバグ修正で失敗しやすい。作者はデバッグ能力不足と学習意欲の低さが継続を阻害したと振り返る。  
- Web版の限界：PWAで一覧＋外部サイトを埋め込む案はCORS／X‑Frame‑Optionsで挫折。iframeで元ページをそのまま表示できないサイトが多い。  
- Electron採用：CORS回避やデスクトップでの一体感を得るためElectronでプロトタイプを作成。左に未読リスト、右にプレビューという典型的構成で「動くけど理想ではない」状態に。  
- セキュリティと配布：鍵情報をmacOSキーチェーンに入れるなど基本は押さえつつも、他人に配布する自信はないと著者。ネイティブなら配布・署名・App Store対応の学習が必要。  
- 本質的教訓：LLMは「ゼロから何か」を作るスピードを劇的に上げるが、品質向上・設計の熟考・長期運用は別問題。短時間で得た「何か」を「良いもの」にするのが依然として難しい。

## 実践ポイント
- まずは既存API（例：Feedbin）でプロトタイプを作ると早い。  
- ブラウザで元ページを埋める必要があるならCORSとX‑Frame‑Optionsを最初に確認。回避はプロキシかElectronを検討。  
- LLMに頼る時は「小さな反復」と「自分でデバッグできる範囲」を設計する。AIに任せ切りにしない。  
- ユーザに配布するなら認証情報の保護（キーチェーン等）、署名や配布方法（App Store/Notarization）を計画する。  
- 「試作→熟成」にかかる時間を見積もり、最初から運用・保守のコストを織り込む。

（参考）著者は最終的に「vibe codingは速いが、真の製品化には時間と深い理解が必要」と結論づけ、ReederやFeedbinのような既存ツールへの感謝を記しています。日本の個人開発者やプロダクト担当にも示唆に富む実例です。
