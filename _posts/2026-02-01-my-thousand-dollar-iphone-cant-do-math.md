---
layout: post
title: "My thousand dollar iPhone can't do math - 私の千ドルiPhoneが“計算できない”"
date: 2026-02-01T23:03:45.877Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://journal.rafaelcosta.me/my-thousand-dollar-iphone-cant-do-math/"
source_title: "My thousand dollar iPhone can&#x27;t do math"
source_id: 46849258
excerpt: "iPhone16 Pro MaxのNeural Engine不具合でLLM出力が桁違いに壊れる"
image: "https://journal.rafaelcosta.me/content/images/2026/01/ios-26-iphone-16-pro-trust-this-computer-alert-mac-crop-1.png"
---

# My thousand dollar iPhone can't do math - 私の千ドルiPhoneが“計算できない”
最新iPhoneのNeural Engineが暴走？開発者が見つけた“数値が桁違いになる”謎

## 要約
開発者がローカルLLM（MLX/Gemma）をiPhoneで動かしたところ、iPhone 16 Pro Maxだけ中間テンソルの数値が桁違いになり出力が完全に壊れる。iPhone 15やMacでは正常に動作したため、最終的にハードウェア（Neural Engine/Metal周り）の不具合を疑って端末交換に至った。

## この記事を読むべき理由
- 日本でもiPhoneは主要な開発・テスト端末。オンデバイスLLMやAppleの機械学習APIが広がる中、ソフト寄りの不具合に見えて実はハード故障という落とし穴は誰にでも起こり得ます。  
- プライバシー重視でローカルモデルを採用する日本のプロダクトでも、同様のトラブル対応が必要になる可能性があります。

## 詳細解説
- 背景：投稿者はMiniMax（M2.1相当）やMLXを使い、レシート分類・支出トラッキングを行う簡易アプリを作成。最初にAppleの「Apple Intelligence」経由の手法を試すがモデルダウンロードが進まず断念。次にMLXをアプリ内に組み込みローカル実行を試した。  
- 問題の症状：同一コード・同一モデル・同一プロンプト（例："What is 2+2?"、温度0で決定的に）を実行すると、iPhone 16 Pro Maxでは生成が「意味不明」になりCPU使用率は最大になって長時間止まらない。一方でiPhone 15 ProやMacでは正しい応答を返す。  
- デバッグ手法：モデル層ごとに中間テンソル（MLXArray/Tensor）をログに出力し、同プロンプトでデバイス間比較。初期入力は一致するが、ある層以降で値が桁違いに発散していることを確認。  
- 技術的考察：iPhone 16に載るA18のNeural Engine向けにMetalでコンパイルしたテンソル演算のどこかで誤算（スケーリングミス、アクセラレータの欠陥、あるいはMetalコンパイラパスのバグ）が起きている可能性が高い。ソフト側（モデル実装）では再現せず、ハード/ドライバ層の疑いが強まった。投稿者はAppleCare経由で交換し、iPhone17で正常動作を確認している。

## 実践ポイント
- まず端末を疑う：同一コードが別端末で動くならハード／ドライバ層の問題を疑う。  
- 再現環境を揃える：温度など決定性のある設定（temperature=0、同量子化モデル）で比較実行。  
- 層ごとの中間テンソルをログ出力：どのレイヤで値が狂うかを特定すると原因切り分けが早い。  
- 切り分け候補：CPU実行／GPU実行／Neural Engine（Metal）実行で挙動比較。GPU/Neural Engineでのみ発生するならアクセラレータ周り。  
- ユーザー対策：開発中は複数世代の実機で確認、クリティカルな処理はフォールバック経路（CPU実行や別実装）を用意する。  
- 事後対応：ログと再現手順を用意してAppleサポート/AppleCareに持ち込むと交換の判断がつきやすい。

この記事から得られる教訓は単純です：ソフトが壊れているように見えても、最後に疑うべきは物理レイヤ（ハード／ドライバ）です。日本の開発現場でもオンデバイスMLの普及とともに、同種の切り分け技術は必須になります。
