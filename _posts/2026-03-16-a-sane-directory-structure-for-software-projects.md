---
layout: post
title: "A Sane Directory Structure for Software Projects - ソフトウェアプロジェクトの合理的なディレクトリ構成"
date: 2026-03-16T03:07:25.786Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://trop.in/blog/a-sane-directory-structure-for-software-projects"
source_title: "A Sane Directory Structure for Software Projects — Andrew Tropin"
source_id: 1525903494
excerpt: "この記事の詳細をチェック"
image: "https://trop.in/assets/smiling-face.webp"
---

# A Sane Directory Structure for Software Projects - ソフトウェアプロジェクトの合理的なディレクトリ構成
迷わないコードベースを作るディレクトリ設計術 — 長く保守できる「覚えやすさ」を優先する

## 要約
複雑化するプロジェクトでも「予測可能で混ざらない」ディレクトリ構成を提案する記事。モジュール名とファイルパスの一貫性、言語/サブシステムごとの中間ディレクトリ、src/tests/dev/envの明確な分離が肝。

## この記事を読むべき理由
日本の現場でもマルチ言語化・モノリポ化が進み、意図しないテストコード混入やビルドの不可逆な副作用に悩むことが増えています。本記事の方針はオンボーディング、CI設定、リリース安定性をすばやく改善できます。

## 詳細解説
- モジュール名とファイルパスの対応  
  多くの言語でロードパス（search/load paths）があるため、モジュール名はファイルパスと対応させるのが基本。これによりコンパイラ・IDE・新参者がどこを探せばいいか予測可能になる。

- モジュール命名ルール（推奨）  
  例：(project domain module) のように3要素以上で命名すると衝突が減り可読性が上がる。最初の要素はプロジェクト名かドメイン、最後は具体的な概念。基本は単数形。

- トップレベルでの副作用禁止  
  ソースファイルに起動時に自動実行される副作用（ファイル生成、ネットワークアクセスなど）を置くと、ビルドや読み込み時に予期しない結果を招く。トップレベルは定数・関数定義のみにし、実行は明示的に行う。

- 言語（またはサブシステム）ごとの中間ディレクトリ  
  guile、hoot、c、scheme-common のように中間層を置くとマルチ言語プロジェクトが整理しやすい。共通モデルは language-common のように独立させる。

- トップレベル構成（推奨）
  - env/ : 開発・リリース環境定義（パッケージ、チャネル）
  - src/ : 本番コード（さらに言語/サブシステムで分割）
  - tests/: テスト（src を鏡像する構成にする）
  - dev/ : ベンチマーク、REPLスニペット、実験コード
  さらに doc/, target/, tmp/ を用意して生成物・一時物を明確にする。

- テストファイルの機械的対応  
  tests のパスは src と機械的に対応させる。例：
  - src/guile/my-project/markdown/parser.scm → tests/guile/my-project/markdown/parser-test.scm

- ビルド/ロードパス管理例
  環境変数で明示しておくと accidental inclusion を防げる：
  ```bash
  GUILE_LOAD_PATH="./src/guile:./src/scheme-common"
  ```

## 実践ポイント
- まずトップレベルを4+3（src/tests/dev/env + doc/target/tmp）で分ける。すぐリポジトリに反映。
- モジュールは可能な限り「プロジェクト.グループ.モジュール」の形でファイルパスに対応させる。命名は単数形を基本に。
- ソースのトップレベルに副作用コードを書かない。実行用スクリプトは dev/ や bin/ に置く。
- tests を src と同じ構造で配置し、IDE/CI がテストを見つけやすくする。
- CI/ビルドで使うロードパスは明示的に設定して、dev/test コードが混入しないようにする。

この設計は冗長に見えるが「探す時間の削減」「誤った依存の流入防止」「新規参加者の学習コスト低減」に直結します。まずは小さくルールを決め、プロジェクト全体で統一してみてください。
