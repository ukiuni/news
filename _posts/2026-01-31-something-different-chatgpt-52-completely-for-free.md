---
layout: post
title: "Something different, ChatGPT 5.2 completely for free, no account needed. Using their official /translate page. - 「違う形で：ChatGPT 5.2を完全無料・アカウント不要で使う方法（公式/translateページを利用）」"
date: 2026-01-31T16:01:10.308Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jonathanyly/freegpt"
source_title: "GitHub - jonathanyly/freegpt: This Extension injects into the translation page of chatgpt (offical chatgpt page), replacing it with a fully functional (its heavily vibecoded (with chatgpt) im not a frontend dev) chatpgt UI. You can choose the model, system and developer prompt in the settings."
source_id: 413998397
excerpt: "公式/translateを改変し、ChatGPT‑5.2を無料・アカウント不要で使う方法"
image: "https://opengraph.githubassets.com/b9487d3e813990fa177bedbeb04c662150eaedf4f569e594683109a1563d2925/jonathanyly/freegpt"
---

# Something different, ChatGPT 5.2 completely for free, no account needed. Using their official /translate page. - 「違う形で：ChatGPT 5.2を完全無料・アカウント不要で使う方法（公式/translateページを利用）」
ChatGPTの翻訳ページがそのまま“完全なチャットUI”に変わる拡張 — まずは試してみたくなる手軽さ

## 要約
GitHubの「freegpt」は、ChatGPTの公式翻訳ページ（/translate）にUIを差し替え、ネットワークレベルで会話リクエストを書き換えてモデルやsystem/developerプロンプトを差し替えるChrome拡張。設定はローカルに保存され、gpt-5-2系などのモデル選択が可能。

## この記事を読むべき理由
日本の開発者やテック愛好家にとって、公式ページを活用して手元でプロンプト実験やモデル切替を手軽に試せる点は魅力。ローカルでプロンプトを簡単に管理でき、翻訳用途やプロンプト調整の学習コストを下げるため実務・学習の入り口として有用。

## 詳細解説
- 仕組み：拡張は翻訳ページにUIを注入し、ブラウザのネットワーク処理で発生する /conversation リクエストを横取りして、送信前にmodelやsystem/developer promptの値を差し替える。つまりページの見た目だけでなく、サーバーに送るリクエスト内容を改変する方式。
- 主な機能：
  - モデル選択：gpt-5-2／gpt-5-2-thinking等を切替可能（ただし実際の可用性はOpenAI側の制約に依存）。
  - カスタムsystem prompt／developer prompt：AIの振る舞いと返信後追加指示を設定可。
  - Markdownレンダリング：コードブロックや強調が見やすく表示。
  - 設定の永続化：localStorageに保存。
- 技術構成：content.js（UI注入・設定管理）、injector.js（リクエスト差替え）、manifest.json、styles.css。インストールはソースをクローンしてChromeの「拡張機能」→「デベロッパーモード」→「パッケージ化されていない拡張機能を読み込む」でフォルダを指定するだけ。
- 注意点：公式UIやAPIの挙動・利用規約は随時更新されるため、動作保証はなし。企業利用や機密データの投入は情報漏洩リスク・規約違反の可能性があるため慎重に。

## 実践ポイント
- 試す場所：https://chatgpt.com/en-EN/translate/ に拡張を入れるとカスタムUIに置き換わる。
- すぐやれること：設定でsystem/developerプロンプトを用意して、同じプロンプトで比較実験（モデルA vs モデルB）を行うと違いが掴みやすい。
- セキュリティ／コンプライアンス：社内規程やOpenAI利用規約を確認し、機密情報は送らない。社内利用ならIT管理者に相談を。
- 継続的チェック：拡張は非公式かつ軽量なため、OpenAI側の変更で動かなくなることがある。定期的にリポジトリの更新を確認する。
