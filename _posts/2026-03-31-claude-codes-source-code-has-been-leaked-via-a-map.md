---
layout: post
title: "Claude Code's source code has been leaked via a map file in their NPM registry - Claude Code のソースが NPM のソースマップで流出した可能性"
date: 2026-03-31T10:28:49.605Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://twitter.com/Fried_rice/status/2038894956459290963"
source_title: "Claude Code's source code has been leaked via a map file in their NPM registry"
source_id: 47584540
excerpt: "NPMのソースマップに元コードや秘密が含まれ公開、依存先を今すぐ点検を"
---

# Claude Code's source code has been leaked via a map file in their NPM registry - Claude Code のソースが NPM のソースマップで流出した可能性

思わず確認したくなる一行: あるNPMパッケージのソースマップに「元のソース」が含まれて公開されてしまったと報告されています — あなたのプロジェクトも他人事ではありません。

## 要約
報告によれば、NPM に公開されたパッケージのソースマップ（.map）に元のソースコードが埋め込まれており、結果として実装（ソースコード）が外部から閲覧可能になった可能性があります。

## この記事を読むべき理由
多くの日本の開発者・組織が NPM を利用しており、ビルド工程で誤ってソースマップを公開すると知的財産や秘密情報（内部実装、API仕様、場合によっては鍵やトークン）が漏れるリスクがあります。手元のパッケージや公開設定をすぐ確認すべきです。

## 詳細解説
- ソースマップとは  
  バンドル／圧縮された JS をデバッグ可能にするために、圧縮後の行・列と元のソースを対応づけるメタデータ（.map ファイル）。  
- なぜ流出が起きるか  
  ビルドツールや設定によっては、sourceMap に元ソースを直接埋め込む（sourcesContent）ことがあり、そのまま npm publish すると公開レジストリに載る。さらに package に sourceMappingURL が残っているとブラウザや調査ツールから参照される。  
- 影響範囲  
  実装ロジック、未公開の関数名、コメント、場合によってはベアトークンやテスト用シークレット（ビルド時に埋め込まれた場合）が露出する。商用モデルや差し障りのあるアルゴリズムを扱うプロジェクトでは重大。  
- 発見方法  
  レジストリ上のパッケージを展開して .map を見る、ソースマップ内の sourcesContent フィールドを確認、またはブラウザの DevTools でソースが復元されるか試す。

## 実践ポイント
- すぐやること（公開者向け）  
  - npm パッケージに .map を含めていないか確認する（npm pack で確認）。  
  - ビルド設定で sourcesContent を無効化、またはソースマップを公開アーティファクトに含めない。  
  - package.json / .npmignore で .map を除外する。  
  - 万一の流出が疑われるなら該当バージョンを非推奨にし、鍵やシークレットをローテーションする。  
- 消費者・利用者向け  
  - 依存パッケージのバージョンを固定し、疑わしいバージョンがないか audit する。  
  - 公開パッケージから予期せぬ情報が見つかったらプロジェクトに報告し、必要なら使用を控える。  
- 組織的対策  
  - ビルドパイプラインに静的チェックを入れ、デプロイ前にソースマップや埋め込みシークレットを検出する（例: CI チェック、SAST、専用スキャン）。  
  - プライベートレジストリ運用や公開ポリシーを整備する。

以上を踏まえ、まず自分の公開パッケージ／依存関係を一度点検することを強くおすすめします。
