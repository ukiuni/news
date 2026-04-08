---
layout: post
title: "Open source security at Astral - Astralにおけるオープンソースのセキュリティ"
date: 2026-04-08T18:12:01.278Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://astral.sh/blog/open-source-security-at-astral"
source_title: "Open source security at Astral"
source_id: 966575810
excerpt: "Astral流の実践的OSSサプライチェーン防御：ハッシュ固定とSigstore活用"
image: "https://astral.sh/static/OpenGraph/Astral.jpg"
---

# Open source security at Astral - Astralにおけるオープンソースのセキュリティ
サプライチェーン攻撃に負けない！Astral流・現場で使えるCI/CDとリリースの防御術

## 要約
AstralがGitHub上で公開するツール群を守るために採用する、CI/CD・リポジトリ・リリース・自動化の実践的なセキュリティ対策を整理して公開した内容です。悪用されやすいトリガーの排除、アクションのハッシュ固定、シークレット隔離、署名・証明作成などが中心です。

## この記事を読むべき理由
日本でもOSSプロジェクトや企業のCI/CDがGitHubに集中しており、TrivyやLiteLLMのようなサプライチェーン攻撃事例は対岸の火事ではありません。実運用レベルで効果が立証された具体策を学べます。

## 詳細解説
- CI/CDの立ち位置  
  Astralは開発速度維持のため大量のGitHub Actionsを使う一方で、Actions自体の「デフォルトでの危険性」を踏まえ、ワークフロー自体をセキュアな観測可能環境に閉じる方針を採用しています。

- 危険なトリガーの禁止  
  pull_request_target や workflow_run 等、第三者PRで権限が漏れやすいトリガーを組織全体で禁止。多くのユースケースは非特権トリガー（例: pull_request）やログ／ジョブサマリで代替可能と判断しています。

- アクションのハッシュ固定と検査  
  ActionsはタグではなくコミットSHAへ固定（フルSHA必須）し、zizmorなどのツールで「偽装コミット（impostor commits）」やunpinned usesを検出。ネストされたアクションにもハッシュピンを徹底しました。

- ハッシュ固定だけでは不十分  
  固定されたアクションが外部から最新バイナリを取得してしまう「可変指標」問題は手動レビューで検出→ upstreamと協働してダウンロード先とそのハッシュをアクションに埋め込む等で対処。

- 最小権限・シークレット隔離  
  組織単位でデフォルト読み取りのみ、ワークフローごとは permissions: {} から開始。シークレットはリポジトリ全体ではなく「deployment environments」など環境単位で分離し、被害範囲を限定。

- 組織・リポジトリ管理の強化  
  管理者アカウントを限定、強力な2FA（最低TOTP、将来的にはWebAuthn/Passkeys）を義務付け、mainへの直接プッシュ禁止・ブランチ保護・特定ブランチ名禁止・タグ不変化などを組織レベルで強制。保護を無効化できないように権限も制限。

- 自動化（GitHub App）の活用  
  第三者PRにコメントを残す等、Actionsでは安全に実現できない処理はGitHub App（例：astral-sh-bot）で分離。App開発も通常のセキュリティ開発プロセスで扱う必要がある点を注意喚起。

- リリースの防御層  
  Trusted Publishingで長期的なレジストリ資格情報を不要にし、Sigstoreベースのアテステーションでビルド provenance を証明。GitHubのimmutable releasesとタグ保護、リリース環境の二名承認などで単一アカウントの悪用を防止。リリース時はキャッシュを使わない方針も採用。

- 依存関係の扱い（要点）  
  依存ライブラリやトランジティブ依存は信頼のチェーンを形成するため注意深く管理。元記事は対策の詳細につながる記述を続けています。

## 実践ポイント
- 自分のリポジトリで pull_request_target / workflow_run を禁止してみる。多くは pull_request で代替可能。  
- GitHub ActionsのusesをフルSHAでピン化し、unpinned-usesチェッカーをCIに組み込む（zizmor / pinact 等）。  
- ワークフローを permissions: {} から始め、必要最小限のジョブ単位で権限を拡張する。  
- シークレットは環境単位に分け、リリース用シークレットは別の承認フローで管理する。  
- 重要な自動化（コメント、外部操作）はGitHub Appへ切り出す。単一ワークフローに秘密を混ぜない。  
- リリースにはSigstore等のアテステーションとタグ保護を導入し、公開バイナリのチェックサムを配布物に明示する。  
- 組織・チームでは管理者数を絞り、強制2FA・ブランチ／タグ保護を組織レベルで設定する。

短期的にできる改善から始め、重要なリリース経路やCIのトリガー周りを優先して見直すのが有効です。
