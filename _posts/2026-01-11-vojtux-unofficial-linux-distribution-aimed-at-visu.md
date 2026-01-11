---
layout: post
title: "Vojtux – Unofficial Linux Distribution Aimed at Visually Impaired Users - 視覚障害者向け非公式Linux配布「Vojtux」"
date: 2026-01-11T08:03:07.455Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/vojtapolasek/vojtux"
source_title: "GitHub - vojtapolasek/vojtux: Scripts and documentation about accessible version of Fedora"
source_id: 46525271
excerpt: "視覚障害者向けにOrca自動起動やOCR搭載で、すぐ使えるFedora派生Vojtux"
image: "https://opengraph.githubassets.com/e43f6a00b49fce27dc77e2c8710563c83e00f35b5e4ecaba75010666288c6483/vojtapolasek/vojtux"
---

# Vojtux – Unofficial Linux Distribution Aimed at Visually Impaired Users - 視覚障害者向け非公式Linux配布「Vojtux」
視覚に障害のある人が「すぐ使える」ことを優先したFedora派生の実験的ディストリ。目指すのは最終的に「Vojtuxが不要な世界（= Fedora自体が完全にアクセシブル）」。

## 要約
VojtuxはFedora（現状はMate Spinベース）を最小限に改良して、スクリーンリーダーやOCR、キーボード操作など視覚障害者向けの使いやすさを強化したライブISOとパッケージ群を提供するプロジェクトです。カスタマイズはできるだけパッケージ化して upstream に還元する方針を取っています。

## この記事を読むべき理由
- 日本でもアクセシビリティ対応は重要なテーマ（公共・企業の要件、ユニバーサルデザイン）。実用的な手法や設計方針が学べる。  
- Fedoraベースで再現しやすく、自分でローカライズ（日本語化・日本語OCR追加）して使えるため、実務やコミュニティ活動に直接役立つ。

## 詳細解説
- 目的と設計哲学  
  - 最終目標は「NO VOJTUX NEEDED」— upstream（Fedora）自体が十分アクセシブルになること。  
  - 原則は「元ディストリに極力近く」「壊れている箇所を無理に直さない」「変更は再利用可能なパッケージで配布」。これによりメンテナンス負荷を抑え、改善はできるだけ上流に還元する。

- 技術スタックと主要機能  
  - ベース: Fedora（現行リリース例としてFedora 43 のライブイメージ）／デスクトップは軽量でアクセシビリティの比較的良い MATE。  
  - 配布形式: ライブISO（GitHub制限により外部ホスティング＋ハッシュ付き）と、vojtux-appsというCoprリポジトリで提供されるRPM群。  
  - アクセシビリティ強化: Orcaスクリーンリーダーをログイン画面から自動起動、QTのアクセシビリティ有効化、LightDM GTK greeter採用（Orcaの起動問題回避）。  
  - 同梱／プリインストールツール例: Tesseract（OCR）、LIOS（OCRアプリ）、ocrmypdf、Audacity、VLC、Chromium、tmux、Ifuse/jmtpfs（スマホ接続）、各種ファームウェア。  
  - カスタムスクリプトとショートカット: ログイン音量復元、物理モニタのトグル、Orca再起動や音量操作などのキーボードショートカットを提供（例: Alt+Super+o で Orca 再起動）。  
  - セキュリティ設定: ライブ作成時に一時的にSELinuxを緩める設定が含まれる（ビルドや動作上の理由）。

- ビルド手順（概要）  
  - 開発環境は対象のFedoraバージョンと合せることが推奨。主な手順は lorax/ livemedia-creator 等を使ったKickstartベースのISO作成。  
  - 代表的コマンド（リポジトリからクローンしてビルド）:

```bash
# bash
sudo dnf install lorax-lmc-novirt
git clone https://github.com/vojtapolasek/vojtux
cd vojtux
ksflatten -c ks/vojtux_en.ks -o vojtux.ks
sudo livemedia-creator --make-iso --no-virt --iso-only \
  --anaconda-arg="--noselinux" \
  --iso-name vojtux_43.iso --project vojtux --releasever 43 \
  --ks vojtux.ks --tmp live/tmp
```

- 既知の注意点  
  - 現状は英語キックスタートが中心。チェコ語ファイルなどは古いまま。日本語ローカライズは手を入れれば可能だが現状未実装。  
  - ライブISOは大きいためGitHubで配布せず外部ホスト。ダウンロード後はハッシュで検証を推奨。

## 実践ポイント
- まずはVMで試す: ISOをダウンロード→ハッシュ検証→VMで動かしてOrcaやショートカット、OCRの動作を確認。  
  - ハッシュ検証例:
```bash
# bash
sha256sum -c vojtux_43.iso.sha256
```
- 日本語化の基本手順（短縮）:  
  - Fedora上で日本語ロケールを追加、Orcaの日本語ボイス（音声合成）や日本語入力（IBus）を組み込む。  
  - Tesseractに日本語データを追加（tessdata-ja）してOCRの言語を切替える。  
- コントリビュートの方法: テスト報告、ドキュメント翻訳、日本語用Kickstartの作成、必要なRPM（日本語音声/辞書/入力メソッド）のパッケージングやvojtux-appsへの提供。  
- 実務での活用提案: 公的機関や社内のアクセシビリティ検証環境として活用し、フィードバックをupstreamに上げることで継続的な改善を促す。

Vojtuxは「アクセシビリティ改善のための現実的な実験場」として価値が高く、日本語対応を加えれば現場で即戦力になる可能性が高い。興味があればローカライズやパッケージ提供での参加が有益。
