---
layout: post
title: "Cue Does It All, but Can It Literate? - CUEは何でもできるが、リテラル化できるか？"
date: 2026-01-16T11:20:34.225Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://xlii.space/cue/cue-does-it-all-but-can-it-literate/"
source_title: "CUE Does It All, But Can It Literate?"
source_id: 46588607
excerpt: "CUEで記事をビルドし、コードや図を実行・検証してドキュメントの劣化を防ぐ方法を学ぶ"
---

# Cue Does It All, but Can It Literate? - CUEは何でもできるが、リテラル化できるか？
ドキュメントが常に「正しいコード」を保証する──CUEで作る“実行可能な記事”入門

## 要約
CUEを使うと、ドキュメント中のコードや図をソースから直接生成・検証できるため、説明と実装のズレ（コピー&ペースト地獄）を防げる。cue cmdを使えば、記事を「ビルド」してCIのように検証できる。

## この記事を読むべき理由
「ブログや社内ドキュメントのコードが古い」「Emacs依存のorg-modeを避けたい」「VS CodeやCIと親和性のある方法が欲しい」──こうした課題を抱える日本のエンジニアや技術ライターにとって、CUEは実務的かつ移植性の高い解決策になるからです。

## 詳細解説
- 問題提起（Frankenstein問題）
  - 記事やチュートリアルではコード断片を分割して見せることが多いが、元の実装を直しても記事中の断片が更新されず、読者に壊れたコードを配ってしまうリスクがある。

- CUEの強み
  - CUEは型付け・検証ができる設定言語で、ファイル生成や外部コマンド実行も定義できる。文章を「ビルドターゲット」として扱い、依存関係（スニペットやレンダラ）を定義すれば、未検証の断片がある限り成果物は生成されない。

- どう動くか（要点）
  - tool/file や tool/exec といった組み込みで「ファイルを作る」「外部コマンドを実行する」ことを宣言。
  - 宣言だけでは副作用は起きない。実際に動かすには cue cmd を実行して、command: ブロックを順に実行する必要がある。
  - 重要な落とし穴：cue cmd が命令を拾うにはファイル名が *_tool.cue の形式であること（例: build_tool.cue）。

- ポリグロットなパイプライン
  - CUEは任意のCLIツールを呼べるため、Pikchrで図を描画したり、GHC/stackでHaskellスニペットをコンパイルしたり、任意言語の「レンダラ」を定義して記事生成パイプラインに組み込める。
  - これにより、画像の自動生成・コードの実行結果挿入・コンパイル検証などをドキュメント生成時に自動化できる。

- テストとしてのドキュメント
  - cue cmd をCIに組み込めば、記事は「合格するまで公開されない」ワークフローになる。図やコードが壊れていればビルドは失敗する。

## 実践ポイント
- 最低限の流れ
  1. CUEをインストールする（https://cuelang.org/ を参照）。
  2. パッケージファイルを作る（ファイル名は *_tool.cue にする）。
  3. tool/file と tool/exec を使って、生成したいファイルとレンダラを定義する。
  4. ローカルで cue cmd を実行して生成・検証する。CIにも組み込む。

- 最小例（雰囲気を掴むためのサンプル）
```cue
// cue
package example

import "tool/file"
import "tool/exec"

command: example: {
  for k, v in files {
    "(k)": file.Create & {
      filename: k
      contents: v
    }
  }
}

data: exec.Run & {
  cmd: ["sh", "-c", "echo '1.2.3'"]
  stdout: string
}

files: {
  "output.md": """
  My Awesome Project
  Current version: (data.stdout)
  """
}
```

- 実用のヒント
  - ファイル名は必ず *_tool.cue にする（例: build_tool.cue）。これを忘れると cue cmd が無視する。
  - レンダラは単なるCLIラッパーなので、既存のビルドツールや図版ツール（PlantUML, Pikchr, pandocなど）を流用できる。
  - CI例：push時に cue cmd を走らせ、生成物を検証してから公開するワークフローを作ると安全。
  - 日本の現場では、ドキュメントの多言語対応や社内テンプレート流用、VS Codeユーザーとの共有で特に恩恵が大きい。

CUEを使えば「ドキュメントは説明ではなく一つのビルドアーティファクトだ」という考え方に簡単に移行できる。まずは小さな記事一つをbuild_tool.cue化して、cue cmdで確実に生成・検証される体験をしてみてください。
