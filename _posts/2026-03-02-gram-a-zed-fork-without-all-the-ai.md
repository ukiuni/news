---
layout: post
title: "GRAM: A Zed fork without all the AI - Zedの「AI抜き」フォーク：GRAM"
date: 2026-03-02T09:09:28.328Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gram.liten.app/"
source_title: "GRAM"
source_id: 715617135
excerpt: "AI機能を排し高速・ローカル重視のZedフォーク、GRAMがプライバシーと開発効率を両立"
---

# GRAM: A Zed fork without all the AI - Zedの「AI抜き」フォーク：GRAM
AI機能を省いて「速さとシンプルさ」を追求した新しいコードエディタ、GRAM

## 要約
GRAMはZedをベースにしたフォークで、AI機能を排しつつ高速性・拡張性・多数の内蔵機能（ドキュメント、DAPデバッガ、git統合など）を提供するエディタです。ソースはCodebergで公開され、M1+ macOSとLinux（AMD64）向けバイナリが配布されています。

## この記事を読むべき理由
日本企業や個人開発者の中には、AI依存やテレメトリを避けたい人や、軽快でローカル中心の環境を好む層が多く存在します。GRAMはそうしたニーズに応える選択肢であり、特にApple SiliconやLinuxサーバー開発者にとって実用的です。

## 詳細解説
- 基盤：Zedのフォーク。基本の操作感や拡張互換性を活かしつつ独自方針で開発。  
- AI非搭載の意義：外部AIサービスに依存せず、プライバシーと企業ポリシーに配慮した設計。日本の企業で導入しやすい。  
- パフォーマンス：軽量でレスポンス重視。大規模ファイルや低遅延編集を重視するワークフローに向く。  
- 拡張性：Zed用の拡張をそのまま利用可能（互換性は要確認）。標準で多言語サポート。  
- 内蔵機能：組み込みドキュメント、DAP（Debug Adapter Protocol）経由のデバッガ対応、gitによるソース管理など「バッテリー同梱」的な充実。  
- 配布と開発：ソースは codeberg.org/GramEditor/gram にホスト。M1+ macOSとLinux(AMD64)用バイナリあり。最近は Gram 1.0 リリース（2026-03-02）や開発哲学を語る記事が公開済み。

## 実践ポイント
- 今すぐ試す：公式サイトから対応バイナリをダウンロードして動作確認（M1/M2 MacユーザーやLinux開発環境で特に）。  
- デバッグ環境：DAP対応を使ってローカルでデバッグワークフローを検証。既存のDAPサーバ（例えばvscode-dap互換）と組み合わせ可能。  
- 拡張チェック：プロジェクトで使っているZed拡張がそのまま動くか試して互換性を確認する。  
- 移行検討：VS Codeや他エディタからの乗り換えは、git連携とデバッグ体験を中心に比較するとスムーズ。  
- セキュリティ／ポリシー観点：AIや外部テレメトリを使いたくない組織には検討価値が高い。ソースを直接確認して社内監査に備える。

出典・ダウンロード：公式サイト（https://gram.liten.app/）およびソース（codeberg.org/GramEditor/gram）。
