---
layout: post
title: "Mastodon: Don't use \"mastodon\" or \"mstdn\" in domain names - Mastodon：ドメイン名に「mastodon」や「mstdn」を使わないでください"
date: 2026-04-16T13:07:22.642Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mastodon/mastodon/commit/d6f8ac97e808821180e9ae0c66879b7a2d64e690"
source_title: "Add trademark warning to `mastodon:setup` task (#38548) · mastodon/mastodon@d6f8ac9 · GitHub"
source_id: 1481728469
excerpt: "セットアップでmastodon/mstdn含むドメインを警告、今すぐ確認"
image: "https://opengraph.githubassets.com/6638519063d42048b6d29a6912d5dd7c5013f5dd4244739c5dd056dd42759d91/mastodon/mastodon/commit/d6f8ac97e808821180e9ae0c66879b7a2d64e690"
---

# Mastodon: Don't use "mastodon" or "mstdn" in domain names - Mastodon：ドメイン名に「mastodon」や「mstdn」を使わないでください
Mastodonのセットアップで「mastodon」や「mstdn」を含むドメインを検出して警告する変更 — 公式商標の扱いに注意を促す小さなけれど重要な改修。

## 要約
Mastodonのセットアップタスクに、環境変数LOCAL_DOMAINに`mastodon`または`mstdn`が含まれる場合に商標警告を出し、続行するか確認して中断する仕組みが追加されました。商標ポリシー参照リンクも表示します。

## この記事を読むべき理由
- 自分でインスタンスを立てたい日本の技術者・愛好者が、知らずに公式ブランド名を含むドメインを使って法的トラブルや運用上の問題を招かないようにするため必読です。
- セットアップ時の挙動変更は即座に影響するため、手順や回避方法を知っておくと安全です。

## 詳細解説
- 変更箇所は mastodon のセットアップ用 Rake タスク（lib/tasks/mastodon.rake）。LOCAL_DOMAIN 環境変数の値に対して文字列検索を行い、`'mastodon'` または `'mstdn'` を含むときに警告を出すようになっています。
- 表示されるメッセージは商標が制限されている旨と、公式の商標ポリシー（https://joinmastodon.org/trademark）への案内。ユーザーが「続行しない」を選べばセットアップを中断します。
- 技術的には単純な文字列チェック（include?）での防止策で、完全な法的チェックではなく開発者側からの注意喚起機能です。既存のコードには Unicode ドメインに対する punycode 入力の注意書きもあります。

例（簡略化した該当ロジック）:
```ruby
if env['LOCAL_DOMAIN'].include?('mastodon') || env['LOCAL_DOMAIN'].include?('mstdn')
  prompt.warn 'The Mastodon name is a trademark and its use is restricted.'
  prompt.warn 'You can read the trademark policy at https://joinmastodon.org/trademark'
  next prompt.warn 'Nothing saved. Bye!' if prompt.no?('Continue anyway?')
end
```

## 実践ポイント
- 新規インスタンスを立てるときはドメイン名に「mastodon」「mstdn」を含めない（例：myinstance.example.jpのような固有名を使う）。
- 日本語ドメインや全角文字を使う場合は punycode（xn--...）での登録と入力を確認する。
- 既に公式名を含むドメインで運用している場合は、速やかに別ドメインへの移行や名称変更を検討する。法的懸念があるなら弁護士に相談する。
- ローカルでセットアップを実行する際は env（.env.production 等）を見直し、rake mastodon:setup のプロンプトに従う。

短く言えば：公式名はブランドであり扱いに注意。セットアップ時の警告は運用トラブルを未然に防ぐための親切なチェックです。
