---
layout: post
title: "Microsoft confirms some Windows 11 PCs can't shut down, hibernate after latest Patch Tuesday - Microsoft、最新Patch Tuesday適用後に一部のWindows 11 PCでシャットダウン／休止ができない問題を確認"
date: 2026-01-19T12:55:37.182Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.neowin.net/news/microsoft-confirms-some-windows-11-pcs-cant-shut-down-hibernate-after-latest-patch-tuesday/"
source_title: "Microsoft confirms some Windows 11 PCs can't shut down, hibernate after latest Patch Tuesday"
source_id: 423143615
excerpt: "最新Patch Tuesdayで一部Windows 11がシャットダウンや休止不能、今すぐ影響確認を"
---

# Microsoft confirms some Windows 11 PCs can't shut down, hibernate after latest Patch Tuesday - Microsoft、最新Patch Tuesday適用後に一部のWindows 11 PCでシャットダウン／休止ができない問題を確認
夜間のシャットダウンができない…トラブルを避けるために今すぐ確認したい対処法

## 要約
Microsoftは、最新のPatch Tuesday配布後に一部のWindows 11マシンで「シャットダウン」や「休止（ハイバネート）」が正常に動作しない問題を認めています。影響を受ける環境では電源管理に関わる動作が不安定になります。

## この記事を読むべき理由
シャットダウン／休止はノートPCのバッテリー運用や企業の夜間メンテナンスで重要な機能です。通勤やリモートワークが多い日本のユーザーや、集中配信でWindows Updateを管理するIT管理者は早急な確認と対策が必要です。

## 詳細解説
- Patch TuesdayはMicrosoftが定期的に配布するセキュリティ／品質更新の集合体です。今回の配布によって一部環境でOSの電源状態遷移（稼働→スリープ→休止→シャットダウン）が期待どおりに完了しない事象が報告されています。  
- 原因としてよくあるパターンは、電源管理を扱うドライバー（ストレージ、チップセット、ネットワーク、ディスプレイなど）やACPI方面の相性問題、Fast Startup（ハイブリッドシャットダウン）周りの不整合、あるいは更新されたカーネルコンポーネントとの不整合です。Microsoftは該当問題を確認し、修正や回避策を案内する場合があります。  
- 影響は機種やドライバー構成によって異なり、全てのPCが該当するわけではありません。ログ（イベントビューア）や更新履歴で原因の手がかりが得られます。

## 実践ポイント
- まずは影響の確認：シャットダウン／休止ができないか、再現手順を把握する。Event Viewer（イベントビューア）でKernel-PowerやACPI関連のログを確認する。  
- 一時回避（管理者向け・安全確認のうえ実行）：
  - 即時シャットダウン（通常のUIでできない場合）:
```bash
shutdown /s /t 0
```
  - 再起動で回避できる場合もある:
```bash
shutdown /r /t 0
```
  - 休止を無効化して影響を回避する（休止が不要な場合）:
```bash
powercfg -h off
```
- 更新のロールバック／確認：
  - 設定 > 更新とセキュリティ > 更新の履歴 から最近の更新を確認し、疑わしい更新はアンインストールを検討する。企業環境ではWSUS/SCCMで該当更新を一時配信停止する。  
- ドライバーとファームウェアの確認：チップセット／ストレージ／ネットワークのドライバー、およびUEFI/BIOSの最新版をメーカー提供ページから確認して更新する。  
- 復旧時の注意：更新をアンインストールする前に重要データをバックアップし、社内ポリシーに従ってテスト環境で検証する。  
- 情報追跡：Microsoftの公式サポート情報やWindows Health Dashboard、各ベンダーのサポート情報を監視し、修正パッチやワークアラウンドが出たら速やかに適用する。

日本のノートPC利用者は通勤中や会議の合間に休止を多用する傾向があるため、影響が出ると実用上の不便が大きくなります。まずは影響有無の確認とログの取得、必要なら一時的な回避策を講じ、公式の修正を待ってください。
