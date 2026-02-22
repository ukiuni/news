---
layout: post
title: "How We Fixed YAML Comment Preservation in Ruby (And Why We Sponsored It) - RubyでYAMLのコメントを保持する仕組みを直した話（そしてなぜスポンサーしたか）"
date: 2026-02-22T09:09:21.444Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.discourse.org/2026/02/how-we-fixed-yaml-comment-preservation-in-ruby-and-why-we-sponsored-it/"
source_title: "How We Fixed YAML Comment Preservation in Ruby (And Why We Sponsored It)"
source_id: 915540791
excerpt: "Discourseが支援したpsych-pureでYAMLコメントを消さず自動編集できる"
image: "https://blog.discourse.org/content/images/size/w1200/2026/02/Discourse-Header-YAML-Preservation.png"
---

# How We Fixed YAML Comment Preservation in Ruby (And Why We Sponsored It) - RubyでYAMLのコメントを保持する仕組みを直した話（そしてなぜスポンサーしたか）

YAMLのコメントが自動編集で消えて運用ドキュメントが台無しになる問題を、Discourseがスポンサーした純Ruby実装で解決した話。

## 要約
Rubyの標準YAML（Psych）はコメントを破棄するが、psych-pureはコメントをASTノードに紐づけてシリアライズ時に復元する。Discourseはこれを安定化させ、運用スクリプトでコメントを失わないワークフローを実現した。

## この記事を読むべき理由
運用自動化でYAMLを扱う日本のSRE/運用エンジニアやDevOpsチームは、コメントが失われると「歴史的コンテキスト＝トライバルナレッジ」を失いインシデント対応や移行が遅れる。現場で実用的に使える解決策が紹介されているため即試せます。

## 詳細解説
- 問題点：Rubyでよく使われるPsychはYAML仕様上「コメントは表現上の詳細」として破棄して良いとされるため、プログラムで読み込み→書き出しするとコメントが消える（例: runbookが実行されるたびに注釈が消える）。
- これまでの試行：
  - 文字列置換（正規表現）：YAML構造が複雑だと壊れる。
  - Psychの非公開AST操作：脆弱で保守困難。
  - Pythonのruamel.yaml移植：大規模な工数。
- 解決策（psych-pure）：純Rubyでコメントをパース時に近傍のASTノードへ付与し、シリアライズ時にコメントをそのまま出力する設計。Discourseは既存の開発者（Kevin Newton）をスポンサーしてライブラリの安定化とエッジケース修正を進め、1,736ファイルに対するテストでパース失敗ゼロまで到達。
- 実装例：Discourseはpsych-pureを使うラッパーYamlHelperを作成し、既存のrunbookをほぼ変更せずコメントを保持できるようにした。テストスイートも整備（クラスタ管理、DBフェイルオーバー、キー回転など11テスト）。
- 挙動で注意する点：ノードごとに付随するコメントは、該当キーを削除するとコメントも一緒に削除される（意図した動作）。その他のコメントは元のまま保持される。
- 付帯ツール：yaml-janitor（フォーマット整形＋コメント保持のリンター／修正ツール）が公開されている。

## 実践ポイント
- まずはローカル／ステージングで試す：バックアップを取り、psych-pureで既存ファイルをロード→保存して差分を確認する。
- インストールと簡単な利用例：
```bash
# bash
gem install psych-pure yaml-janitor
```
```ruby
# ruby
YamlHelper.edit_file('container.yml') do |data|
  data['env']['NEW_KEY'] = 'value'
  data['templates'] << 'new_template.yml'
end
```
- 削除時のコメント挙動に注意：キー削除で付随コメントも消えるのが仕様なので、重要コメントは別ファイルやトップレベルの注釈に移すことを検討する。
- 自動化導入の流れ：yaml-janitorで整形→psych-pureベースのスクリプトで編集→CIで差分検査、というパイプラインにすると安全。
- コミュニティ貢献：企業スポンサーやPRでこうしたライブラリを支えると、日本の運用コミュニティ全体の負担が減る。

元記事はDiscourseの技術ブログ。日本の現場でもすぐ役立つ実用的な解決法です。
