---
layout: post
title: "Show HN: Ghost Pepper – Local hold-to-talk speech-to-text for macOS - Ghost Pepper：macOS向けローカル完結のホールド・トゥ・トーク音声→テキスト"
date: 2026-04-06T23:59:49.031Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/matthartman/ghost-pepper"
source_title: "GitHub - matthartman/ghost-pepper: Hold-to-talk speech-to-text for macOS. 100% local, powered by WhisperKit and local LLM cleanup. Hold Control to record, release to transcribe and paste. · GitHub"
source_id: 47666024
excerpt: "Control長押しで即ローカル文字起こしし入力欄へ自動貼付、機密データに安心のmacアプリ"
image: "https://opengraph.githubassets.com/cbded00964b5c52380f7ee0060b2342999b4f9d13cb7aca92acafa34af1b217a/matthartman/ghost-pepper"
---

# Show HN: Ghost Pepper – Local hold-to-talk speech-to-text for macOS - Ghost Pepper：macOS向けローカル完結のホールド・トゥ・トーク音声→テキスト

魅力的なタイトル: ローカルで即変換・貼り付け。プライバシー重視のmacOS音声入力アプリ「Ghost Pepper」

## 要約
Controlキーを押して話し、離すとローカルで音声を文字起こししてアクティブな入力欄に貼り付けるmacOS用アプリ。音声処理も後処理（LLMによる文の整形）もすべてマシン内で完結するのが最大の特徴。

## この記事を読むべき理由
クラウドに音声を送らずに高精度な文字起こしと自然な後処理ができるため、プライバシーや社内データ扱いが厳しい日本企業や個人開発者にとって即戦力になるからです。Apple Silicon上でローカル実行するためレスポンスも実用的です。

## 詳細解説
- 使い方：Controlを押して話す（ホールド）、離すとトランスクリプトが生成されてアクティブなテキストフィールドへ自動貼付。メニューバー常駐で起動時に自動立ち上げも可能。
- アーキテクチャ：音声認識は WhisperKit（オープンモデル）で、生成されたテキストの「フィラー除去」「自己修正」などの整形は LLM.swift を使ったローカルLLMで行う。モデルはHugging Faceからダウンロードしてローカルにキャッシュ。
- モデル選択とトレードオフ：軽量モデルは高速だが英語専用、より大きいモデルやParakeet v3で多言語対応。後処理用のQwen 3.5系は0.8B/2B/4Bなどサイズで速度と品質が変わり、0.8Bは1–2秒、4Bは数秒かかるが精度重視。
- セキュリティと動作環境：macOS 14以上、Apple Silicon（M1以降）推奨。マイクとアクセシビリティ権限が必要。トランスクリプトはディスクに保存されずメモリ内で処理される設計。
- ビルド／配布：公式のDMGで簡単導入、ソースからは Xcode プロジェクトを開いてビルド可能。企業向けにはMDM経由でアクセシビリティ権限を事前承認できる。

## 実践ポイント
- まずはDMGを入れてマイク／アクセシビリティ権限を許可して試す。  
- 速度重視なら軽量Speech／0.8BのQwenを選び、品質重視なら大きめのCleanupモデルを選択。  
- 常にローカル処理なので機密情報の入力や社内会議のメモ取りに適す。  
- 管理下のMacではMDM（Jamf等）でPPPC設定を用意すると導入がスムーズ。  
- 開発者はGhostPepper.xcodeprojを開いてカスタム機能やプロンプトを編集可能。
