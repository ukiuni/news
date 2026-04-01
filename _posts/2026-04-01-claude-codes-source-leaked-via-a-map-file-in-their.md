---
layout: post
title: "Claude Code's source leaked via a map file in their NPM registry - ClaudeのコードがNPMレジストリのmapファイル経由で流出"
date: 2026-04-01T00:50:09.608Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://x.com/Fried_rice/status/2038894956459290963"
source_title: "Claude Code's source leaked via a map file in their NPM registry"
source_id: 409593692
excerpt: "NPMのソースマップ誤公開でClaudeのソースが流出、公開前チェック必須"
---

# Claude Code's source leaked via a map file in their NPM registry - ClaudeのコードがNPMレジストリのmapファイル経由で流出

魅力的な日本語タイトル: NPMの「.map」が招いた流出リスク — Claudeのソースが丸見えに？

## 要約
報告によれば、Claude（あるAIプロジェクト）のソースコードが、NPMに公開されたソースマップ（.map）ファイルを通じて流出した可能性があります。ソースマップの扱いミスが原因です。

## この記事を読むべき理由
日本のフロントエンド開発やOSSを扱う現場でも、無頓着なソースマップ公開は重大な情報漏えいやサプライチェーンリスクにつながります。対策を知らないままだと、自社プロジェクトやライブラリが同じ目に遭う可能性があります。

## 詳細解説
- ソースマップとは：ブラウザでデバッグするために、圧縮・難読化された配布ファイル（例：bundle.min.js）を元のソースにマッピングするためのファイル（example.js.map）。通常、minified JSの末尾に「//# sourceMappingURL=...」で参照されます。
- 流出パターン：ソースマップ内のsourcesContentプロパティに元のソースを埋め込むと、レジストリに公開されたパッケージから誰でも元コードを復元可能になります。公開パッケージに.mapを含めたまま公開すると、minifiedの「隠れた」元コードが丸見えになるわけです。
- 技術的ポイント：
  - .mapファイルは単なるテキスト（JSON）で、sourcesやsourcesContentを含む。
  - webpackのdevtool設定には "source-map"（完全に含める）や "nosources-source-map"（ソースは含めない）などの差がある。
  - NPMパッケージは一度公開するとキャッシュやミラー経由で広がるため、回収が難しい。
- 影響範囲：機密ロジック、APIキー（ビルド時に埋め込まれた場合）、内部設計、特許やアルゴリズムの実装などが露出し得る。

## 実践ポイント
- パッケージ公開前に内容を確認する：
  - npm packで作成したtgzを展開して*.mapを確認する。
  - bash例:
```bash
# パッケージの中身を確認
npm pack <package>@<version>
tar -tf <package>-<version>.tgz
```
- ビルド設定を見直す：
  - webpackなら devtool を "nosources-source-map" か false にする（開発用は別）。
  - ビルドで sourcesContent を埋め込まない設定にする。
- 配布物から.mapを除外：
  - .npmignore に *.map を追加する、または公開用ビルドで生成しない。
- CIで自動チェック：
  - publish前にアーティファクト内に.mapや秘密情報が含まれていないかスキャンする（grep/JQや専用ツール）。
- レジストリ運用：
  - 重要なパッケージはプライベートレジストリを使う。公開済みに気づいたら速やかにバージョン撤回と鍵のローテーションを行う。
- ツール導入：
  - Snyk、GitHub Advanced Security、npm auditなどで供給網リスクを監視する。

短く言えば：publicに出す前にビルド成果物を必ずチェックし、ソースマップの取り扱いを運用ルールに組み込みましょう。
