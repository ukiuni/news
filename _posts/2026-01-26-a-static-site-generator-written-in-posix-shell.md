---
layout: post
title: "A static site generator written in POSIX shell - POSIXシェルで書かれた静的サイトジェネレータ"
date: 2026-01-26T07:52:56.034Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://aashvik.com/posts/shell-ssg/"
source_title: "an ssg written in shell"
source_id: 46690463
excerpt: "POSIXシェル一ファイルでMarkdownをHTML化しRSSやタグ管理まで行う超軽量SSG"
---

# A static site generator written in POSIX shell - POSIXシェルで書かれた静的サイトジェネレータ
シェルスクリプトだけでブログを丸ごと生成する—“ちょっとクセあるけど愛せる”超軽量SSGの作り方

## 要約
POSIXシェル（主にbash系）で書かれた一つのファイル gen.sh が、Markdown→HTML変換（comrak任意）・タグ集計・RSS/Atom/JSONフィード・サイトマップ・ドラフト管理までこなす軽量静的サイトジェネレータを実現している。

## この記事を読むべき理由
大きなフレームワークやNode依存を避けたい個人サイト/ブログ運営者や、シェルでのテキスト処理を実践的に学びたいエンジニアにとって、依存最小・運用コスト低めなアプローチが参考になるため。日本の個人開発者や技術ブログ運営にも相性が良い。

## 詳細解説
- 構成想定：posts/（Markdown）・include/（静的資産）・template/（HTMLテンプレ）を読み、public/ を出力先にする一発生成（インクリメンタルは無し）。
- Markdownレンダラ：comrak（任意）を利用。CommonMark拡張やシンタックスハイライト、フロントマター区切り対応で機能豊富。
- メタデータ：各Markdownの先頭数行をsedで柔軟に抽出（date/title/desc/tags/cats等）。YAMLパーサは使わず正規表現で済ませる設計。
- テンプレート：envsubstで環境変数を置換。テンプレ側はシンプルに${var}で埋める。
- HTML後処理：comrak出力をsed -z -Eで加工。複数画像を横並びにラップ、画像のタイトルを<figure>/<figcaption>に変換、画像拡張子からaudio/videoタグに置換、相対パスを/assets/post_slug/*へ書き換えるなど。
- タグ処理：POSIXシェルの配列非対応をevalや動的変数名で回避し、タグ一覧とタグごとの投稿リストを構築。タグページを生成。
- ドラフト：カテゴリ（cats）にdraftを含めると公開リストから除外し /drafts を生成。
- フィード類：RSS/Atom/JSONとサイトマップを生成（やや冗長だが一通り対応）。
- 性能：キャッシュ無くても小規模サイトでは高速。例：29ポストで約700msで生成（著者の計測）。

## 実践ポイント
- すぐ試す：リポジトリを作り、gen.sh・template・posts を配置してローカルで実行してみる。comrakを入れればMarkdown拡張が有効。
- CI運用：GitHub Actions／GitLab CIでgen.shを走らせて public を公開するワークフローが簡単（Node不要）。
- 安全性：evalや動的変数を多用するため、外部投入データはサニタイズ（タグ名やファイル名に注意）すること。
- 拡張案：インクリメンタル化（mtime比較）やテンプレートをもっと強力にする（mustache等導入）の検討。日本語サイト特有の文字コードや日付書式に注意。
- 学習用途：sed/awk/envsubst/comrakの組合せは、テキスト処理とUNIX哲学を学ぶ良い教材になる。

短く言えば、依存を絞って「自分で全部見通せる」静的サイトビルドを求める人に強くおすすめ。シンプルな個人サイトや学習プロジェクトに最適。
