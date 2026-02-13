---
layout: post
title: "The Many Flavors of Ignore Files - 無視ファイルの多様性"
date: 2026-02-13T07:30:27.604Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nesbitt.io/2026/02/12/the-many-flavors-of-ignore-files.html"
source_title: "The Many Flavors of Ignore Files | Andrew Nesbitt"
source_id: 808756358
excerpt: "gitignoreの差異でDockerやnpm公開が失敗、原因特定と実践的回避策を紹介"
image: "https://nesbitt.io/images/boxes.png"
---

# The Many Flavors of Ignore Files - 無視ファイルの多様性
知らないとビルドが遅くなり、パッケージが公開失敗する：.gitignore 互換を過信しないための実践ガイド

## 要約
.gitignore は単なる「ワイルドカードの列」ではなく、深い優先順位やアンカー規則、特殊なワイルドカードなど多数の細かい仕様が隠れている。各ツールは「gitignore 互換」と言うが、実装差で思わぬ違いが出る。

## この記事を読むべき理由
CI のキャッシュや Docker ビルド、npm パッケージ公開、エディタ拡張配布など、日本の開発現場で日常的に起きるトラブル（大きなビルドコンテキスト、公開漏れ、不要ファイルの混入）を未然に防げるから。

## 詳細解説
- 優先順位（4 層）  
  global excludes (~/.config/git/ignore) → .git/info/exclude → ルート .gitignore → 各サブディレクトリの .gitignore。深いディレクトリほど優先され、最後にマッチしたパターンが勝つ。原因追跡は git check-ignore -v <path> が有効。

- アンカー（/ を含むか否か）  
  スラッシュのないパターン（例: *.log）は実質的に **/ を前置した扱いで任意深さにマッチ。/ を含むパターンはその .gitignore のディレクトリにアンカーされる。ここが多くの再実装でズレる箇所。

- ワイルドカードの挙動  
  * はセグメント内（/ を跨がない）、? は1文字、** はセグメント単体でのみ「任意深さ」を意味する（foo/**/bar など）。Go やシェルの glob と微妙に違う実装差に注意。

- 文字クラスとエッジケース  
  [a-z] の範囲はバイト順序、先頭の ] や否定記号の扱い、POSIX クラスのサポートなど細かい仕様がある。

- ディレクトリ専用と否定（!）  
  trailing / はディレクトリ専用にする。! は再包含だが、既に親ディレクトリが除外されていれば作用しないため、中間ディレクトリを逐次再包含する必要がある（例: /* !/foo /foo/* !/foo/bar）。

- エスケープ、空白、追跡済みファイル  
  バックスラッシュで特殊文字をリテラル化。行末スペースは特別扱い。既に Git 管理下のファイルは .gitignore 追加だけでは無効（git rm --cached が必要）。

- 他ツールとの差分（実務インパクト）  
  Docker は階層的な .gitignore 的語彙を持たず、Go の filepath.Match を使うためアンカー挙動が異なる。npm は package.json の files による allowlist と .npmignore の優先関係、デフォルトで .gitignore を参照する挙動で公開漏れが発生しやすい。Mercurial は syntax: regexp を混在できるなど強力。ツールによって doublestar、否定、コメント等のサポート状況がバラバラ。

- エコシステムの試み  
  ripgrep の ignore crate や共通の .ignore は実用的な統一策。CommonMark が Markdown でやったように、仕様＋テストスイートがあれば互換性問題はずっと減る。

## 実践ポイント
- 問題解析：git check-ignore -v <path> でどのファイル・どのパターンが効いているか確認する。  
- npm 公開前：npm pack --dry-run で含まれるファイルを確認する（dist/ が除外されていないか等）。  
- Docker ビルド：.dockerignore の挙動は .gitignore と違うと仮定して明示的に書く（ビルドコンテキスト圧縮が重要）。  
- 再包含ルール：ネストした再包含は中間ディレクトリも明示的に再包含する（/* !/foo /foo/* !/foo/bar のパターンを理解する）。  
- トラッキング済みファイル：.gitignore 追加だけで済まない場合は git rm --cached を使う。  
- テストを作る：CI に ignore ファイルの振る舞いを検証する小さなフィクスチャを置き、ツールごとに期待結果をテストする（docker build, npm pack, git status 等）。  
- 可能なら共通ライブラリを選ぶ：プロジェクトで複数ツールを使うなら、ripgrep の ignore crate など成熟実装に合わせると差分を減らせる。

以上を押さえれば、知らぬ間に発生する「無視ファイル周りの失敗」をかなり減らせます。
