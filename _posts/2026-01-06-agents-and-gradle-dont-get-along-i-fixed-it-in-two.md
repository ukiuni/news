---
  layout: post
  title: "Agents and Gradle Dont Get Along - I Fixed It in Two Commands - エージェントとGradleは相性最悪だった — 2つのコマンドで解決した話"
  date: 2026-01-06T17:52:33.611Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://nek12.dev/blog/en/how-to-give-ai-agents-kotlin-library-source-search-in-gradle-for-claude-and-codex"
  source_title: "How to Give AI Agents Kotlin Library Source Search in Gradle for Claude and Codex | nek12.dev"
  source_id: 469526887
  excerpt: "Gradleの複雑なキャッシュをksrcで2コマンドに短縮し、依存ソース参照を即解決！"
---

# Agents and Gradle Dont Get Along - I Fixed It in Two Commands - エージェントとGradleは相性最悪だった — 2つのコマンドで解決した話

Gradleの複雑なキャッシュ構造でAIエージェントがライブラリのソースを見つけられない問題を、CLIツール「ksrc」でわずか2コマンドに短縮する話。

## 要約
Kotlin（特にマルチプラットフォーム）の依存先ソースをGradleキャッシュから探すのは手間がかかる。nek12.devの作者は「ksrc」というCLIを作り、検索→参照を2コマンドで完了できるようにした。

## この記事を読むべき理由
日本のAndroid／Kotlinマルチプラットフォーム開発者や、AIアシスタント（Claude/Codex）と組み合わせて自動化を進めたい現場にとって、依存ソースの迅速な参照はデバッグ、生産性、レビュー品質の向上に直結するため必読。

## 詳細解説
問題点
- Gradleは依存をハッシュ付きの階層にキャッシュするため、パッケージ名から目的のソースを直接探すのが難しい。
- AIエージェントは大きなファイルツリーを掘り下げるとコンテキストやトークン消費が増え、 hallucination（想像でのコード生成）や検索失敗が起きやすい。
- 実際の手順は「依存を見つける → バージョン確定 → sources.jar を探す → 展開 → grep」と多数の手順が必要だった。

ksrcのアプローチ
- ksrc は Gradle キャッシュを横断検索し、必要ならソースを自動ダウンロード／展開して、該当ファイルの該当行をすばやく返すCLI。
- 基本操作は2つのコマンド：search（依存＋キーワードで候補を列挙）と cat（ファイルを行指定で表示）。
- 結果はエージェントが扱いやすいフォーマットで出力され、ClaudeプラグインやCodex向けのスキルも用意されているため、エージェントが自動的に利用できる。

例（概念）
```bash
# 該当アーティファクト内をキーワードで検索
bash$ ksrc search "pro.respawn.apiresult:core*" -q "recover"

# 見つけたファイルの指定行だけ表示
bash$ ksrc cat pro.respawn.apiresult:core:2.1.0!/commonMain/pro/respawn/apiresult/ApiResult.kt --lines 480,515
```

導入効果
- 手動での15ステップ相当の作業を2コマンドに圧縮できる。
- AIエージェントとの統合で、対話的に「このライブラリのこの関数はどう使う？」を即確認できる。
- ソースが無ければ自動で取得／展開するフローが組み込まれているため、プロジェクトごとに都度タスクを書く必要が減る。

## 実践ポイント
- まずはバイナリをダウンロードしてPATHに追加。作者は単一ファイル配布＆セットアップスクリプトを用意している（Homebrew対応は今後）。
- 日常ワークフロー：
  1. ターミナルで ksrc search して候補を見つける。
  2. ksrc cat で該当ファイルの該当行を開く（VS Codeのターミナルやエディタのアウトプットに表示すると便利）。
- CI/レビュー活用：コードレビュー自動化ツールやBotに組み込み、依存APIの参照エビデンスを自動取得させるとレビュー品質が上がる。
- エージェント連携：ClaudeやCodex用のスキルを導入すれば、エージェントが人手なしでライブラリ探索を行えるようになる。
- マルチプラットフォーム開発（Android＋iOS＋JS）では特に有用。Gradleの複雑な出力先を意識せずにソースへ辿り着ける。

短く言えば、ksrcは「Gradleのゴチャゴチャを透過してソースへ直行するための橋渡し」。Kotlin開発の生産性を一段引き上げる実用ツールなので、まずは試してみる価値が高い。
