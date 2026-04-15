---
layout: post
title: "Does Gas Town 'steal' usage from users' LLM credits to improve itself? - Gas TownはユーザーのLLMクレジットを“盗んで”自己改善しているのか？"
date: 2026-04-15T21:57:51.236Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/gastownhall/gastown/issues/3649"
source_title: "Does Gas Town &#39;steal&#39; usage from users&#39; LLM credits &amp; paid services to improve itself? · Issue #3649 · gastownhall/gastown · GitHub"
source_id: 47785053
excerpt: "*GasTownがあなたのLLMクレジットやGitHub権限を無断で使う危険と具体的対策*"
image: "https://opengraph.githubassets.com/d7ba3c544f0e3d675b58145e4a2f2e76a5bfa530b97c8d273a160f4544f0d574/gastownhall/gastown/issues/3649"
---

# Does Gas Town 'steal' usage from users' LLM credits to improve itself? - Gas TownはユーザーのLLMクレジットを“盗んで”自己改善しているのか？
GasTownが知らずにあなたのAIクレジットやGitHub権限で自分自身の修正やリリースを行っていた可能性を指摘する問題報告

魅力的な日本語タイトル: GasTownがあなたのAI課金を“勝手に”使う？──発見された自動寄付ワークフローと今すぐできる対策

## 要約
GitHubのIssueで、GasTownがデフォルトで同梱するフォーミュラ（gastown-release.formula.toml／beads-release.formula.toml）により、ローカルインスタンスが上流リポジトリのIssueを拾い、ユーザーのLLMクレジットとGitHub資格情報を使ってPRやリリースを行っていたと報告されています。説明や明確なオプトインはない模様です。

## この記事を読むべき理由
有料LLMクレジットや企業のGitHubトークンを使って第三者のOSS開発を無断で進められると、コスト負担・セキュリティ・コンプライアンス上の重大リスクになります。日本の個人開発者や企業でも同様の被害が起き得るため知っておく必要があります。

## 詳細解説
- 問題の起点はパッケージに含まれる「release」系のフォーミュラ（gastown-release.formula.toml, beads-release.formula.toml）。これらは上流（steveyegge/gastown）へタグやリリースをプッシュする設計になっている。
- GasTownのエージェント（polecats/convoys/deacon といったコンポーネント）が上流のIssueトラッカーを監視し、Issueを処理するタスクを開始。タスク実行にはLLM API呼び出し（例：Claude）やGitHub APIを利用するため、使用クレジットやユーザーのGitHub権限が消費される。
- 実際のログ（パトロールログ）には、ユーザーアカウント名でPRが作成され、上流でCI待ちの状態になっている記録が確認されているとのこと。
- 問題点は「デフォルトで有効」「利用や費用についてドキュメントに明示がない」「オプトアウト/オプトインが無い」こと。結果として利用者が何の同意もなく他者のOSS開発にリソースを提供してしまう形になっている。

## 実践ポイント
- インストール直後はフォーミュラを確認／無効化する：
  ```bash
  # インストールディレクトリでフォーミュラを検索
  bash
  find . -name '*.formula.toml' -maxdepth 3 -print
  grep -nE "gastown-release|beads-release|contribute" *.formula.toml || true
  ```
- 自動エージェント／ワークフローを無効化：設定ファイルや起動フラグで「contribute back」「auto-publish」相当の機能をオフにする（ドキュメントが無ければ該当フォーミュラを削除）。
- GitHubトークンとLLMキーの権限を最小化・監査する：必要なスコープのみ付与、個人クレジットカード直結のアカウントでは使用しない。
- 請求とAPIログを確認：LLMプロバイダとGitHubの使用状況をチェックし、不審なAPIコールがないか確認。
- サンドボックスで先に動かす：不明なOSSはまずネットワーク制限した環境やローカルのみで動かす。
- メンテナへ要望する：デフォルト無効化と明確なオプトインの追加を求めるIssueやPRを出す（今回のIssueはその例）。
- 緊急対応：心配な場合は該当インスタンスを停止し、発行したトークンを即時削除・再発行。

短く言えば、GasTownのデフォルト設定で「あなたのリソースが上流プロジェクトの開発に使われる」可能性があるため、インストール直後に設定を確認し、自動アップストリーム寄与機能をオフにすることを強く推奨します。
