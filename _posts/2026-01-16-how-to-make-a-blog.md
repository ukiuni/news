---
layout: post
title: "How to make a Blog - ブログの作り方"
date: 2026-01-16T17:56:43.693Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.erikwastaken.dev/posts/2026-01-16-how-to-make-a-blog.html"
source_title: "How to make a Blog"
source_id: 425259582
excerpt: "コードほとんど不要でMake+Pandocで作る超軽量静的ブログ構築法"
---

# How to make a Blog - ブログの作り方
make + pandocで作る「最小限の静的ブログ」入門 — コードをほとんど書かずに自分のブログをビルドする

## 要約
make（Makefile）とpandocだけで、Markdownの投稿をHTMLに変換して静的ブログを自動生成する手順を解説します。最小限の仕組みで「差分だけを再ビルド」する効率的なワークフローが身に付きます。

## この記事を読むべき理由
- 日本の個人開発者や小規模チームでも、重たい静的サイトジェネレータを使わずに高速で運用可能。
- makeの基本が分かればCIやデプロイの自動化にも応用でき、運用コストを下げられる。

## 詳細解説
背景：makeは1976年に登場したビルドツールで、ターゲット・前提ファイル・レシピ（ルール）に基づき「再ビルドが必要なものだけ」を自動で更新します。pandocは汎用ドキュメント変換器でMarkdown→HTMLの変換とテンプレート適用を得意とします。この2つを組み合わせると、シンプルで効率的な静的ブログ生成が可能です。

基本構成（例）
- posts/（Markdownファイル）
- templates/（HTMLテンプレート）
- css/（スタイル）
- out/（生成物）

pandocで単一ファイルを変換するコマンド例：
```bash
pandoc --standalone --template=templates/post.html -o foo.html foo.md
```

Makefileの基本ルール例：ターゲット foo.html を foo.md とテンプレートから生成する。
```makefile
foo.html: foo.md templates/post.html
	pandoc --standalone --template=templates/post.html -o foo.html foo.md
```

多数の投稿を手作業でルール追加せずに扱うため、makeのワイルドカード／関数を使います。主要ポイント：
- wildcardでposts/*.mdを列挙
- 置換関数で出力パス（out/posts/*.html）に変換
- パターンルールで自動生成

例（変数＋パターンルール）：
```makefile
OUT_DIR := out
sources := $(wildcard posts/*.md)
posts := $(subst .md,.html,$(sources))
posts := $(subst posts/,$(OUT_DIR)/posts/,$(posts))

# トップターゲット
blog: $(posts) $(OUT_DIR)/index.html $(OUT_DIR)/atom.xml $(OUT_DIR)/css/style.css

# パターンルール：out/posts/%.html を posts/%.md から生成
$(OUT_DIR)/posts/%.html: posts/%.md templates/post.html
	pandoc --standalone --template=templates/post.html -o $@ $<
```

自動変数：$@ はターゲット名、$< は最初の前提ファイルを指します。

静的資産（CSS）の扱いは単純コピーで済みます：
```makefile
$(OUT_DIR)/css/style.css: css/style.css
	cp $< $@
```

ファイルではないターゲット（例：clean, publish）は.PHONYで宣言して常に実行されるようにします：
```makefile
.PHONY: blog clean publish
clean:
	rm -rf $(OUT_DIR)
publish: blog
	tar -C $(OUT_DIR) -czf $(OUT_DIR).tar.gz .
	# ここにデプロイコマンドを追加
```

## 実践ポイント
- 必要ツール：pandoc と make（多くのUNIX系環境で利用可能）。WindowsではWSLやmsys2で同様に動作。
- まずは最小構成で試す：1投稿のMarkdown・テンプレート1つ・CSSのみでMakefileを作り、makeを実行する。
- 新しい投稿を追加してもMakefileを触らないために、wildcard + パターンルールを必ず導入する。
- ローカル確認は簡易HTTPサーバで：`python -m http.server --directory out` 等で動作確認。
- CI連携：GitHub ActionsやGitLab CIにmakeコマンドを組み込めば、Pushで自動ビルド→デプロイが可能。
- 日本語対応：pandocのテンプレートに<meta charset="utf-8">や日本語フォントのCSSを入れると文字化けを防げます。
- まずはテンプレートを既存の静的サイト用に流用し、後で必要に応じてHakyllや他のフレームワークに移行しても良い。

短く言えば、make + pandoc は「軽量で分かりやすい」静的ブログの最短ルートです。まずは一度小さなリポジトリで試し、ルールと自動化の感触を掴んでみてください。
