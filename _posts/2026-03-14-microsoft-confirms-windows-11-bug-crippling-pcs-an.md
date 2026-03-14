---
layout: post
title: "Microsoft confirms Windows 11 bug crippling PCs and making drive C inaccessible - Microsoft、Windows 11の不具合を確認 — Cドライブが「アクセス不可」に"
date: 2026-03-14T22:07:24.069Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.neowin.net/news/microsoft-confirms-windows-11-bug-crippling-pcs-and-making-drive-c-inaccessible/"
source_title: "Microsoft confirms Windows 11 bug crippling PCs and making drive C inaccessible - Neowin"
source_id: 382880542
excerpt: "KB5077181適用でCドライブがアクセス不可に、今すぐ更新履歴とバックアップ確認"
---

# Microsoft confirms Windows 11 bug crippling PCs and making drive C inaccessible - Microsoft、Windows 11の不具合を確認 — Cドライブが「アクセス不可」に

「C:\ が開けない」Windows 11の深刻バグ、今すぐ確認すべきこと

## 要約
2026年2月のPatch Tuesday（KB5077181）適用で、一部Windows 11（24H2/25H2）のPCが「C:\ is not accessible – Access denied」となり、ファイルやアプリ（Outlook、ブラウザ等）にアクセスできなくなる不具合が報告され、Microsoftが調査中です。

## この記事を読むべき理由
日本ではSamsung製ノートが米州・韓国ほど多くないものの、社内持ち込みや個人輸入機などで影響を受ける可能性があります。業務で使う端末が突然「実質的に動作不能」になるリスクは誰にとっても無視できません。

## 詳細解説
- 影響更新：2026年2月のセキュリティ更新 KB5077181（および以降の更新）を適用したWindows 11 24H2／25H2が対象。Windows 10やWindows 11 23H2以前は影響外とされています。  
- 症状：エクスプローラーで「C:\ is not accessible – Access denied」が出る、アプリが起動できない、ファイルアクセスや権限昇格ができない、更新のアンインストールやログ採取も失敗するケースあり。事実上PCが“機能不全”になる。  
- 対象端末：報告は主にSamsung製（Galaxy Book4など）で、ブラジル、ポルトガル、韓国、インドなど複数地域から。MicrosoftはSamsung Share関連の可能性を示唆していますが原因は未確定。  
- 対処状況：Microsoftは公式ドキュメントで問題を認め調査中。ユーザーがドライブ所有権を強制変更して解決したとの報告もあるが、非常にリスクが高く推奨されません。

## 実践ポイント
- まず確認：設定 → Windows Update → 更新履歴 で KB5077181 等の更新が入っているか確認。Windows のバージョンは「winver」で確認して24H2/25H2か確認。  
- 未適用なら：Windows Update を一時停止（Pause updates）して様子を見る。業務端末は特に慎重に。  
- 既に適用で問題が出た場合：可能なら更新をアンインストール（設定 → Windows Update → 更新履歴 → 更新プログラムをアンインストール）またはシステム復元／回復オプションを検討。ただし一部環境では戻せない報告あり。  
- 危険な対処は避ける：Cドライブの所有権やACLを安易に変更するのはデータ損失や起動不能を招く可能性があるため、最終手段・専門家対応のみ。  
- 事前準備：重要データのバックアップ（イメージ/外付け）、回復ドライブ作成を今すぐ実施。影響が出たらメーカー（Samsung）とMicrosoftサポートに連絡。  
- 情報収集：Microsoftの公式ドキュメントやSamsungのサポート情報を注視し、修正パッチが出るまで急なアップデートは控える。

必要なら、あなたの端末のWindowsバージョンと更新履歴の確認手順を短く案内しますか？
