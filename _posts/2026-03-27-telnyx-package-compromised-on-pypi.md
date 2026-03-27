---
layout: post
title: "Telnyx package compromised on PyPI - Telnyx Python SDKがPyPIで改ざんされました"
date: 2026-03-27T21:04:13.327Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://telnyx.com/resources/telnyx-python-sdk-supply-chain-security-notice-march-2026"
source_title: "Telnyx Python SDK Security Notice: Malicious PyPI Versions Identified (March 2026)"
source_id: 47540388
excerpt: "PyPIのTelnyx公式SDKがマルウェア混入、即確認と秘密鍵ローテーションが必須"
image: "https://images.ctfassets.net/2vm221913gep/79q4hqxMz9w2xhBjDDA0Gl/5f1653ceb354443ad952a67afc93eadb/58db2ca1-0d1d-40c8-9ef5-a79897cb9ce9.jpeg"
---

# Telnyx package compromised on PyPI - Telnyx Python SDKがPyPIで改ざんされました
PyPIで配布されたTelnyx公式Python SDKの一部がマルウェア化 — 今すぐ確認すべき“影響範囲”と実践対応ガイド

## 要約
2026年3月27日にTelnyxのPython SDKで不正なバージョン（4.87.1 / 4.87.2）がPyPIに一時公開され、マルウェアが混入しました。公式プラットフォーム自体は影響を受けていませんが、該当バージョンを取り込んだ環境は侵害の可能性があります。

## この記事を読むべき理由
国内でもPyPI経由でライブラリを運用するプロジェクトは多く、依存関係の“サプライチェーンリスク”は日本の開発現場でも現実的な脅威です。CI/CDやコンテナで自動的にライブラリを引いている現場ほど被害を受けやすく、即対応が必要です。

## 詳細解説
- 何が起きたか：03:51〜10:13 UTC（3月27日）の間にtelnyx==4.87.1と4.87.2がPyPIに公開され、悪意あるコードを含んでいました。両バージョンは当日中に削除・隔離済み。TelnyxのAPIやインフラ本体は不正侵入されていません（SDK配布経路のみが被害）。
- 影響範囲：直接インストール、無固定（unpinned）での依存解決、あるいはトランジティブ依存でこれらのバージョンを取得した環境が対象。
- マルウェアの性質：C2サーバ（83.142.209.203:8080）への接続や、WAVファイルを使ったステガノグラフィ（隠蔽型）でのペイロード配送といった兆候が報告されています。
- 関連背景：TrivyやLiteLLMなど他のOSS配布チャネルも標的となった同一のサプライチェーン攻撃キャンペーンの一部と見られます。

## 実践ポイント
- まずバージョン確認：
```bash
pip show telnyx
```
- 影響があれば即ダウングレード：
```bash
pip install telnyx==4.87.0
```
- ただちに行うべき事：
  - 環境内で使用している全てのシークレット（APIキー、DB資格情報、クラウドトークン、SSH鍵、環境変数）をローテーションする
  - CI/CD、Dockerイメージ、ビルドキャッシュを点検し、脆弱バージョンを取り込んでいないか確認する
  - ネットワークログ／プロセスログを監査し、外部接続（特にC2のIP 83.142.209.203:8080）や不審なWAVファイル処理をチェックする
  - 不審があれば隔離・フォレンジック調査を実施
- 予防策：
  - 依存のバージョン固定（requirements.txtやPoetryのlockファイル）を徹底する
  - 署名付きパッケージや内部ミラー（プライベートPyPIプロキシ）の導入を検討する
  - 依存性スキャン・SBOMの運用、CI段階でのパッケージ検査を組み込む

必要なら、環境の確認やログの見方、CI設定のチェックポイントを手短に案内します。どの作業を優先したいですか？
