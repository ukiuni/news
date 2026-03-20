---
layout: post
title: "Delphi 13.1 Released, with ARM64 support - Delphi 13.1 リリース、ARM64対応"
date: 2026-03-20T19:25:11.794Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blogs.embarcadero.com/announcing-the-availability-of-rad-studio-13-florence-update-1/"
source_title: "Announcing the Availability of RAD Studio 13 Florence Update 1"
source_id: 378975923
excerpt: "Delphi 13.1、ARM64ECで既存Winアプリを最小修正でネイティブ化可能"
image: "https://blogs.embarcadero.com/wp-content/uploads/2026/03/florence-13-1-launch-webinar-replay-no-q-a.jpg"
---

# Delphi 13.1 Released, with ARM64 support - Delphi 13.1 リリース、ARM64対応
次世代Windows on Armに本格対応 — 既存コードでネイティブArmバイナリを狙える大規模アップデート

## 要約
EmbarcaderoのRAD Studio 13.1（Delphi/C++Builder 13.1）は、Windows on Arm向けのネイティブArm64ECコンパイラを始め、Android API 36 / iOS 26対応、FireMonkey用の新スタイルデザイナー、DelphiLSPへのLSIF導入など開発生産性と品質を大幅に強化しました。

## この記事を読むべき理由
日本の企業にも影響する「Windows on Arm実機/VM」や、Google/Appleのストア要件対応、既存のDelphi資産を活かした移行戦略が現実的になったため。レガシー資産を抱える開発者やモバイルアプリを運用するチームは必読です。

## 詳細解説
- Windows on Arm (Arm64EC): DelphiはLLVM 20ベースのArm64ECターゲットを追加。Armネイティブ実行で、x64エミュレーションと互換するArm64EC ABIを使い、既存のWin64コードを最小修正で再コンパイル可能。デバッガはLLDB、ランタイムはMicrosoft UCRTを利用。Intel専用アセンブリ依存箇所だけ注意が必要です。  
- モバイル対応：Android API Level 36 と iOS 26 をサポートし、ストア公開要件に準拠。Android向けのJAR/ビルド更新や.soライブラリ出力、予測バック操作のオプトアウト対応を含みます。  
- 開発体験強化：BookmarksアドオンがIDEに統合され自動番号・スタック型テンポラリブックマークなどで大規模コードの行き来が楽に。IDEスタイルもWindows 11向けVCLテーマを追加し自動切替対応。High DPI設計の改善で「96 DPIで保存」オプションも導入。  
- FireMonkey Style Designer：FMX専用の新しいスタイルデザイナー（単体アプリ）で色・タイポ・状態など上位概念からスタイル生成。デザイナーと開発者の協業を促進。  
- DelphiLSP + LSIF：コンパイラ依存を減らすLSIF対応で、事前生成インデックスを使った高速かつ安定した「移動先へジャンプ」「ホバー」等のコードインサイトを提供。コアライブラリは既にLSIFが付属可能。  
- C++/ツールチェーン・品質：Clang 20 周りの改善、clang-scan-deps導入、リンク時のUnicodeパス改善や最新Windows SDK対応。デバッガとIDE全体の品質改善も多数。  
- データベース／Web：FireDACでSAP ASE/DB2/MariaDB等の新バージョン対応、WebでSSEサポートやRAD Server LiteのTLS1.3対応など実運用向け強化。

## 実践ポイント
- まずは既存Win64プロジェクトをArm64ECでテストビルドし、Intel固有のアセンブリやWin32依存を洗い出す。  
- Android/iOSアプリはAPIレベル変更に合わせてビルド環境（SDK/JDK/署名）を更新、ストア提出期限に備える。  
- 大規模リポジトリではLSIFを生成してDelphiLSPの恩恵を受ける（コマンドオプションで出力可能）。  
- UI刷新はFireMonkey Style Designerでデザイナーと協業、VCLアプリは新Windows 11スタイルでモダン化を検討。  
- トライアルで13.1を試し、デバッガ改善やHigh DPI保存オプションをチーム開発ワークフローに組み込む。

（製品版はアップデートサブスクリプション経由で入手可能。移行計画は小さなテストから始めるのが安全です。）
