---
layout: post
title: "Netflix Void Model: Video Object and Interaction Deletion - 動画オブジェクトと相互作用の削除"
date: 2026-04-07T02:28:49.000Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Netflix/void-model"
source_title: "GitHub - Netflix/void-model · GitHub"
source_id: 47627998
excerpt: "NetflixのVOIDは物体と影響領域（影・崩壊）を同時に消去し高品質な自動VFX化を実現"
image: "https://opengraph.githubassets.com/939b79384ba3362624d3084b70aa7df4942130285a385c0d2e5f60e3a65ce6f3/Netflix/void-model"
---

# Netflix Void Model: Video Object and Interaction Deletion - 動画オブジェクトと相互作用の削除
動画から「物体」だけでなく、その物理的・視覚的な影響ごと一括で消す——NetflixのVOIDが切り拓く映像編集の近未来

## 要約
VOIDは動画内の対象物を削除すると同時に、その対象が引き起こした物理的・視覚的な相互作用（落下、押し出し、影など）も再構築して消す動画インペインティング手法です。CogVideoXをベースにした2段階推論と、SAM2＋VLM（Gemini）による「quadmask」生成パイプラインが特徴です。

## この記事を読むべき理由
日本の制作現場や配信事業者にとって、手作業のVFXコスト削減、プライバシー対応、局所的な差し替え・ローカライズ作業の自動化に直結する技術だからです。短時間で高品質な差分生成が求められる場面が増えている日本市場で実用性が高い注目技術です。

## 詳細解説
- 基本コンセプト  
  - 単に対象ピクセルを埋めるのではなく、対象が与えた「影響領域」まで特定して自然な結果を生成する。例：ギターを持つ人を消すと、ギターが自然に落ちる挙動まで再現。

- マスク表現（quadmask）  
  - 1ピクセルあたり4値（0,63,127,255）で意味付け。  
    - 0: 主たる除去対象、63: 重なり、127: 影響領域（相互作用）、255: 背景（維持）

- パイプライン（大枠）  
  1. Mask生成（VLM-MASK-REASONER）  
     - SAM2でセグメンテーション、VLM（Gemini）で相互作用領域を推論。GUIで対象ポイント選択 → 自動処理でquadmask出力。  
  2. 推論（VOID）  
     - Pass 1: CogVideoXベースのインペインティング（大半のケースで十分）。  
     - Pass 2: 光学フローでワープした潜在表現を使う「warped-noise」補正で時間的一貫性を向上。  
  3. 手動補正（任意）  
     - quadmaskエディタでフレーム単位の修正が可能。  

- 入力フォーマットとプロンプト  
  - 各シーケンスはフォルダにまとまる（input_video.mp4、quadmask_0.mp4、prompt.json）。prompt.jsonの"bg"は「除去後の背景を描写する」こと（除去行為自体は書かない）。

- 実行要件と入手先  
  - GPU大容量（例：A100相当の40GB以上推奨）。SAM2、Gemini APIキー、CogVideoXやVOIDのsafetensorsはHuggingFace等から取得。リポジトリはMIT/Apache系ライセンス。

- 学習データ生成（研究向け）  
  - HUMOTO（人体相互作用）＋Blenderや、Kubricベースの合成パイプラインで「対比動画＋quadmask」を生成。HUMOTOは利用申請が必要。

## 実践ポイント
- まずノートブックで試す（リポジトリ付属のQuick Startが最速）。  
- 必須：40GB級GPU、SAM2のインストール、Gemini APIキー、CogVideoXのダウンロード。  
  ```bash
  # 例
  pip install -r requirements.txt
  export GEMINI_API_KEY=your_key_here
  ```
- モデルチェックポイント（void_pass1.safetensors / void_pass2.safetensors）とCogVideoXの配置を確認する。  
- 自動生成マスクが不正確ならquadmaskエディタで局所修正してから再推論。  
- 利用用途はVFX短縮、プライバシー対応、番組編集の差し替え等。実運用では法務・権利・倫理面の確認を必ず行う。  

参考リポジトリ: https://github.com/Netflix/void-model
