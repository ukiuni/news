---
layout: post
title: "A Claude plugin that forces you to write code - コードを書かせるClaudeプラグイン"
date: 2026-01-25T00:49:53.987Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mlolson/claude-spp"
source_title: "GitHub - mlolson/claude-spp: Simian Programmer Plugin for Claude"
source_id: 419603068
excerpt: "実際にタイピングさせて人のコーディング比率を強制するClaudeプラグイン"
image: "https://opengraph.githubassets.com/fd788580d6bd343ce52002751284d8aba8b371d847bc26667ac60d7fb4205202/mlolson/claude-spp"
---

# A Claude plugin that forces you to write code - コードを書かせるClaudeプラグイン
あなたを“タイピングさせる”AI──怠け癖を直すSimian Programmer Plugin（SPP）

## 要約
SPPはClaude用のプラグインで、人間が実際にコードを書く割合をプロジェクトごとに強制・追跡します。割合が下回るとClaudeは自動でコードを書かず、「どうやって直すか」をガイドしてユーザーに実装させる仕組みです。

## この記事を読むべき理由
AIコード補完が当たり前の今、学習や品質維持のため「人が手を動かす」習慣を意図的に作るツールは重要です。日本の教育現場やチームでの技術継承・オンボーディング、コンプライアンス管理にも有用です。

## 詳細解説
- モード：5段階のモード（Lazy/Curious/Clever/Wise/Crazy）で「人間／AIの比率」を指定（例：Clever = 人間25%／AI75%）。
- 比率の追跡方法：コミットメッセージに "Co-Authored-By: Claude" を含めたものをAI側コミットとカウント。デフォルトはコミット単位で過去7日間を参照。行数ベースの追跡オプションもあり。
- 制止と代替動作：比率が目標を下回るとClaudeは直接コードを書かず、spp-human-task（help human code）スキルで
  - 高レベル目標の提示
  - コードの指針（どこを直すか）
  - テスト手順の提示
 という形でユーザーを導き、完了後にレビューも行います（例として失敗テストの原因特定→修正手順提示の出力あり）。
- 運用コマンドとフロー：
  - Claudeプラグイン追加とインストール、CLIのグローバルインストール（npm i -g claude-spp）、プロジェクト初期化（spp init）。
  - 便利コマンド：spp stats / spp modes / spp mode [n] / spp pause / spp resume / spp reset。
  - gitのpost-commitフックでコミット後に現在の比率とメッセージを表示。
- 実装面：リポジトリはTypeScript主体、MITライセンス。トラッキングは初期化時点の最新コミットから開始します。

## 実践ポイント
- 試す手順（短縮）：
```bash
# Claudeにプラグイン追加（Claude上）とCLIインストール
/plugin marketplace add mlolson/claude-spp
/plugin install spp@mlolson
npm i -g claude-spp
cd /path/to/project
spp init
```
- チーム導入のコツ：AI補助は有効だが、学習フェーズやレビュー重視のブランチでは「Wise/Clever」など人側比率を高めに設定する。
- ワークフロー改善：小さく意味のあるコミットを心がけ、AIコミットは必ず Co-Authored-By ヘッダで明示する。IDEのAI自動サジェストを無効化すると効果的。
- 用途例：新人のコーディング学習、ペアプロの補助、開発ルールの運用（「人が理解していること」を担保するポリシー）。

短く言えば、SPPは「AIに頼りすぎる癖」を技術的に矯正し、人が手を動かす習慣を復活させるツールです。興味があるなら実プロジェクトでモードを切り替えつつ試してみてください。
