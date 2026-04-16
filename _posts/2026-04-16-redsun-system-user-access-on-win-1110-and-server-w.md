---
layout: post
title: "RedSun: System user access on Win 11/10 and Server with the April 2026 Update - RedSun：2026年4月アップデートでWindows 11/10/Serverのシステム権限取得"
date: 2026-04-16T05:16:07.221Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Nightmare-Eclipse/RedSun"
source_title: "GitHub - Nightmare-Eclipse/RedSun: The Red Sun vulnerability repository · GitHub"
source_id: 47788473
excerpt: "2026年4月更新WindowsでRedSunがファイル復元を悪用しシステム権限を奪う危険、対策必須"
image: "https://opengraph.githubassets.com/891723666bf6a56458ceade2bf8f69b6b2c56f5055dbe37db55df80711b67de3/Nightmare-Eclipse/RedSun"
---

# RedSun: System user access on Win 11/10 and Server with the April 2026 Update - RedSun：2026年4月アップデートでWindows 11/10/Serverのシステム権限取得
Windows Defenderの「クラウドタグ付きファイルを元の場所に戻す」挙動を悪用する脆弱性、RedSunの概要と日本企業が取るべき対策を分かりやすく解説します。

## 要約
RedSunは、Windows 11/10およびServerの2026年4月アップデート環境で、アンチマルウェア製品のファイル復元挙動を突いてシステムファイルを書き換え、権限昇格を引き起こす可能性がある脆弱性を指します。公開リポジトリにはPoCがあるものの、ここでは手順は扱いません。

## この記事を読むべき理由
日本の企業や開発者の多くがWindowsを業務基盤にしているため、エンドポイント防御の仕様に起因する権限昇格は実務的リスク。パッチ適用や運用見直しで被害を防げます。

## 詳細解説
- 何が起きるか（高レベル）
  - 一部のアンチマルウェア製品が「クラウドタグ付き」と判断したファイルに対し、検査後にそのファイルを元の場所へ「書き戻す」挙動を持つことがある。
  - RedSunはこの書き戻しプロセスを悪用し、意図的に標的ファイルを上書きすることでシステム権限を取得する可能性を示しています。
- 技術的な要点（非実行的説明）
  - 問題のコアは「検査・復元のフロー」と「復元時の整合性／アクセス制御の不足」。復元処理が適切な権限チェックや検証を行わないと、攻撃者が任意ファイルをシステム領域へ戻す契機を得る可能性があります。
  - 影響範囲はWindows 11/10およびサーバー系で、特定の更新環境下で顕在化する点が報告されています。
- 公開リポジトリについて
  - GitHub上にリポジトリ（RedSun）が存在しPoCコードが示されているようですが、実運用環境での再現や悪用は重大なリスクが伴うため、ここでは再現手順は割愛します。

## 実践ポイント
- まず更新を確認：Microsoftや利用しているアンチウイルスベンダーの公式アドバイザリとパッチ情報を優先的に確認・適用する。
- エンドポイント設定の見直し：AV/EDRのファイル復元ポリシーやクラウド連携の挙動を運用チームと確認し、必要なら保守モードや厳格な検証設定に変更する。
- 最小特権と分離：管理アカウントの常用を避け、重要サーバーはアクセス制御とネットワーク分離を強化する。
- ログと検知：ファイル書き換えや不審な復元イベントを検知するルールをSIEM/EDRで整備する。
- 社内周知と対応手順：ペネトレーションやPoCの実行は管理下でのみ行う指針を明確化し、インシデント対応フローを更新する。
- バックアップと復旧計画：システムファイルの改竄に備えたバックアップと迅速な復旧手順を確認しておく。

出典（参照元）：GitHub リポジトリ「Nightmare-Eclipse/RedSun」（公開情報に基づく要約）。
