---
layout: post
title: "Gleam v1.15.0 released - Gleam v1.15.0 リリース"
date: 2026-03-16T18:53:38.989Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gleam.run/news/upgrading-hex-security/"
source_title: "Upgrading Hex security | Gleam programming language"
source_id: 1382766549
excerpt: "Gleam v1.15.0でHexがOAuth2化、MFA必須化とLSP/JS連携強化"
---

# Gleam v1.15.0 released - Gleam v1.15.0 リリース
Gleamのセキュリティ強化と開発体験改善で、BEAM/JS連携がさらに実用的に

## 要約
Gleam v1.15.0では、HexのOAuth2ベース認証への移行に伴うセキュリティ強化を中心に、言語サーバーやJavaScript FFI、パッケージ公開チェックなど多数の品質／開発体験改善が導入されました。

## この記事を読むべき理由
日本でもElixirやBEAM系の採用が増える中、パッケージ管理（Hex）と開発ツールの安全性・使いやすさは実務上重要です。社内ID連携やMFAポリシーとの親和性、JS連携の強化は日本のプロジェクトでも即戦力になります。

## 詳細解説
- Hex認証の刷新  
  - Hexが旧トークン方式からOAuth2へ移行。MFAが必須化され、クライアントはパスワードを直接扱わず、アクセストークンは短寿命化。企業のIdP（SSO）統合も可能。Gleamは新方式のみを使い、既存のレガシートークンは初回接続時に取り消されます。ローカルに保存するHexトークンの暗号化パスワードは最低8文字必須に。
- Hexエラーの改善  
  - 存在しない依存や公開権限不足など、よくある失敗に対してより分かりやすいカスタムエラーを導入。
- 言語・LSPの使い勝手向上  
  - caseガードで文字列結合が利用可能に。guardでの型ミスに対する明確なエラーメッセージ。LSPでガード内のリネーム/定義へジャンプ/参照検索/ホバーがサポート。
  - 抽出（Extract）アクションが無名関数に対応、モジュール使用箇所からのリネーム、型引数の自動追加提案、文字列プレフィックスでのリネーム/参照検索対応など、多数のコードアクション改善。
  - フォールディング、より精度の高い補完、シグネチャヘルプでの型引数名表示など編集体験の向上。
- JavaScript FFI強化  
  - BitArray向けのJS側API（型判定・内部データ取得）とTypeScript定義を追加。Gleamで定義した型をJS/TS側で安全に扱いやすくなりました。
- パッケージ公開ルール整備  
  - デフォルトのREADMEやREADME未設定のパッケージはpublishを拒否するチェックを導入し、Hex登録パッケージの品質向上を図る。
- 設定の一貫性など小規模改善  
  - gleam.tomlのキー名をsnake_caseに統一（旧書式は非推奨で互換性あり）。CLIのhelpコマンド強化でローカルだけで詳しい手順確認が可能に。

## 実践ポイント
- まずGleamをv1.15.0へアップデートする。Hex連携時にレガシートークンが取り消されるため、初回は再認証が必要。
- Hexのローカルトークン用パスワードは8文字以上に設定する（組織のパスワードポリシーと合わせる）。
- 企業利用ではHexのOAuth/SSO統合を検討し、MFA運用を有効にすることで公開・書き込み操作の安全性を高める。
- パッケージ公開前にREADMEを整備し、デフォルト生成のまま公開しない（publishチェックでブロックされる）。
- VS CodeなどのLSP対応エディタを使って、新しいリネーム／抽出／補完／フォールディング等の機能を活用し、リファクタリング生産性を上げる。
- JS/TS連携が必要なプロジェクトはBitArrayの新APIや生成されるTypeScript型を試し、既存のnpmライブラリとのインタopを検証する。
- プロジェクトやチームでGleamを継続的に使うなら、開発者コミュニティやErlang Ecosystem Foundationへの支援を検討する（インフラ保守に寄与）。

参考：リリースはErlang Ecosystem Foundationと協力して行われています。
