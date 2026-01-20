---
layout: post
title: "A static site generator written in POSIX shell - POSIXシェルで書かれた静的サイトジェネレータ"
date: 2026-01-20T11:31:33.616Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://aashvik.com/posts/shell-ssg"
source_title: "an ssg written in shell"
source_id: 1265170926
excerpt: "POSIXシェルだけでMarkdown→HTMLやタグ管理までこなす軽量SSG『gen.sh』を解説"
---

# A static site generator written in POSIX shell - POSIXシェルで書かれた静的サイトジェネレータ
シェルだけでブログを作る楽しさ──POSIXで動く超軽量SSG「gen.sh」の中身を覗く

## 要約
POSIX準拠のシェルスクリプトで書かれたサイトジェネレータ「gen.sh」は、最小限の外部依存（任意でcomrak）でMarkdown→HTML、タグ・フィード・サイトマップ・ドラフト管理までこなす、個人サイト向けのワンパスビルドツールです。

## この記事を読むべき理由
- 小さく単純なブログを、重いフレームワークに頼らず低コストで運用したい日本の個人開発者や技術学習者に実用的なアイデアを与えます。  
- POSIXシェルのテキスト処理だけで「現実に動く」静的サイト生成が可能だと分かり、シェルスクリプト力向上の教材になります。

## 詳細解説
- 構成概念  
  - 入力：posts/（Markdown）、include/（静的資産）、template/（HTMLテンプレート）  
  - 出力：public/ 配下に各記事の index.html、/index.html、/tags、/drafts、RSS/Atom/JSONフィード、sitemap を生成。  
  - ワンパス実行でインクリメンタルビルドはなし（単純さ優先）。

- メタデータの扱い  
  - 各Markdownは固いヘッダ（行番号依存）を持つ。2行目が日付、3行目がタイトル、4行目が説明、5行目がタグ、6行目がカテゴリ、といった固定フォーマットで sed によって抽出。  
  - この単純な設計は実装を容易にする反面、柔軟性・堅牢性に欠ける（編集ミスで壊れやすい）。

- Markdown処理とHTML後処理  
  - comrak（任意）を使い CommonMark 拡張を多数有効にしてレンダリング。raw HTMLや数式、シンタックスハイライト等をサポート。  
  - comrak 出力を sed -z -E で更に整形。例：複数の <img> を横並びにラップしたり、title を figcaption に変換、拡張子から音声/動画タグに置換、相対パスを /assets/post_slug/* に書き換える等のポストプロセスを行う。

- テンプレートエンジン  
  - 簡潔さのために独自テンプレート言語は使わず envsubst（環境変数置換）でテンプレートに埋め込む。これによりテンプレートは平易でシェル内の変数が直接差し込まれる。

- タグ処理の工夫（POSIX制約への対処）  
  - POSIXシェルに配列が無いため、タグ→記事一覧管理は文字列連結＋get_tag_index関数やevalを駆使した実装。実用的だが eval に伴うリスクと可読性の低下に注意。

- その他  
  - ドラフトはメタデータで判定し /drafts にまとめる。  
  - RSS/Atom/JSON および sitemap を生成（筆者はAtomだけ残す予定）。  
  - ビルド速度は軽量で、例として29投稿で数百ミリ秒で完了する実測あり。

## 実践ポイント
- まず試す手順（短め）  
  1. gen.sh を取得して読み解く（行番号メタデータ、テンプレートの変数名を確認）。  
  2. comrak を入れるか、代替Markdownレンダラを使う（comrakは多機能）。  
  3. posts/, include/, template/ を用意して ./gen.sh を実行してみる。  
- 日本での応用アイデア  
  - 個人技術ブログやポートフォリオを軽量に公開（GitHub Pagesや自己ホスト）する際に最適。CIで毎回スクリプト実行する運用が楽。  
  - 社内の小さなドキュメントサイトなら外部依存を減らして運用・監査を簡単にできる。  
- 改良すると良い点（実務的な注意）  
  - 固定行番号のメタデータは壊れやすいので、運用用途ならYAML frontmatter＋パーサに移行する。  
  - eval や文字列ベースのタグ管理はセキュリティ／保守性で問題になり得る。Bash の配列や小さなDB（sqlite）に置き換える案を検討。  
  - 大規模化するなら増分ビルド（キャッシュ）を実装すると高速化できる。

短く言えば、gen.sh は「楽しく学べる」「実用に足るが割り切りが必要」な一品。シェルで何でもやってみたい人にとっては実践的なリファレンスになります。
