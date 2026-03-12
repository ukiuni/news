---
layout: post
title: "Lowdown Manpage Support - Lowdown の manpage サポート"
date: 2026-03-12T14:37:43.105Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kristaps.bsd.lv/lowdown/mdoc.html"
source_title: "Lowdown Manpage Support"
source_id: 916863709
excerpt: "Markdownだけで意味論的なman/mdocを自動生成し、man作成の敷居を劇的に下げるツール"
---

# Lowdown Manpage Support - Lowdown の manpage サポート
Markdownでmanページを書ける？lowdownが面倒なroff世界をやさしく変える

## 要約
lowdown 3.x の新機能で、man/mdoc を生成するために「manらしいMarkdown」を書くだけで意味論的な mdoc/man を出力できるようになった。面倒な roff/macros を覚えずに manページを作成できる。

## この記事を読むべき理由
日本のOSS開発者やシステム管理者にとって、READMEだけでなく適切な manページを用意することは品質やユーザビリティ向上に直結する。lowdown を使えば初学者でも敷居が低くなり、パッケージ配布や社内ツールのドキュメント整備が楽になる。

## 詳細解説
- 背景：従来のmanページはroff（man/mdoc）マクロで記述する必要があり、マクロや書式ルールが複雑で執筆が敬遠されがちだった。mdoc は意味論重視、man はスタイル寄りの記述。
- lowdown のアプローチ：Markdownを「manらしく」書くと、lowdown の出力オプション（-tmdoc / -tman）と新しい --roff-manpage により、文脈を理解して意味のある mdoc/man を生成する。つまり「見た目はmanの要素でMarkdownを書く」だけで済む。
- 主要ルール：
  - ドキュメント先頭に title と section を metadata として置ける（指定なければ NAME の最初の項目、デフォルトセクションは 7）。
  - 各 man セクション（NAME, SYNOPSIS, DESCRIPTION, SEE ALSO 等）は Markdown の見出しで表現。中身を空にしたセクションは省略する。
  - SYNOPSIS はコードスパンやコードブロックで記述（ユーティリティ呼び出しは1段落1行、関数はプロトタイプをそのまま）。
  - man内で特別扱いされる要素（関数名、オプション、引数、他のman参照など）は強調（emphasis）や二重強調でマーキングすると lowdown がそれらを適切に mdoc/man の対応要素に変換する。
- 制限と注意点：自動変換は完璧ではなく、等号の扱いや変数と関数の区別があいまいになる場合がある。出力は mandoc のリンターでチェックし、問題があれば手直しか upstream へ報告するのが推奨。

## 実践ポイント
- 書き方のテンプレ（最小例）
```markdown
---
title: progname
section: 1
---

# NAME
progname - 一行説明

# SYNOPSIS
`progname [-a] [--opt arg] FILE`

# DESCRIPTION
*progname* は次のように動く。
*-a* : 何かをするフラグ。
*--opt arg* : 引数 arg を受け取るオプション。

# SEE ALSO
other(1)
```
- 生成コマンド例：
  - lowdown -tmdoc --roff-manpage -o progname.1 progname.md
  - lowdown -tman --roff-manpage -o progname.1 progname.md
- 配布時の注意：生成した .1 等を /usr/share/man/... に置き、必要なら makewhatis/mandb を更新して man で見えるようにする。パッケージに組み込む場合はパッケージポリシーに従う。
- チェックリスト：生成物は mandoc（または man）で表示確認、リンターで警告を潰す、変換ミス（等号や複雑な型表現）がないか目視で確認する。

lowdown は「Markdownで書ける」メリットを活かして manページ作成のハードルを下げるツール。まずは小さなユーティリティの man を一本書いて試してみることを勧める。
