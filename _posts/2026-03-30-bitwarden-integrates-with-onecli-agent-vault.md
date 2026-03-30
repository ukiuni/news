---
layout: post
title: "Bitwarden Integrates with OneCLI Agent Vault - BitwardenがOneCLI Agent Vaultと統合"
date: 2026-03-30T16:44:13.303Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.onecli.sh/blog/bitwarden-agent-access-sdk-onecli"
source_title: "Bitwarden Integrates with OneCLI Agent Vault"
source_id: 47575950
excerpt: "Bitwarden×OneCLIでキーを渡さず承認経由でAPI連携する安全なエージェント運用"
image: "https://www.onecli.sh/blog/bitwarden-agent-access-sdk-onecli.png"
---

# Bitwarden Integrates with OneCLI Agent Vault - BitwardenがOneCLI Agent Vaultと統合
魅力的なタイトル: エージェントに「鍵を見せない」認証の勝ち筋──Bitwarden×OneCLIで実現する安全なAIエージェント運用

## 要約
Bitwardenの「Agent Access SDK」が公開され、OneCLIがその前段ゲートウェイとして動作することで、AIエージェントがAPIキーを直接保持せずに人の承認を経て安全に外部APIへアクセスできる仕組みが提供されます。

## この記事を読むべき理由
エージェント運用が増える日本の現場でも、APIキー漏洩やプロンプトインジェクションによる秘匿情報の流出が大きなリスクです。本統合は「鍵を渡さないまま認証を実行する」実運用に直結する解決策を示します。

## 詳細解説
- Agent Access SDK（Bitwarden側）
  - エージェントは「鍵を要求」し、ユーザーがCLI経由で承認するまで鍵は解放されない。承認がない限り平文の鍵はエージェントに渡らない。
  - 企業向けの鍵管理と承認ワークフローを組み合わせた設計。

- OneCLIの役割
  - エージェントと外部APIの間にプロキシ（ゲートウェイ）を置き、送信するHTTPリクエストに対してBitwardenから取得した認証情報をネットワーク層で注入する。
  - これにより、エージェントやLLMプロバイダは鍵を「見る」ことがない。
  - ポリシー適用（レート制限など）やアクセスの監査ログをOneCLI側で一元管理できる。

- 技術的メリット
  - 秘密の在り処はVaultに固定、実行時もエージェントのメモリに残らないため抽出リスクが低い。
  - 承認と利用の両方に監査が残るためコンプライアンス対応が容易。
  - HTTPを使う任意のエージェントフレームワーク（カスタム含む）に適用可能。

- 短い設定例（OneCLIにBitwardenを追加し、ホスト毎にレート制限を作る）
```bash
# Bitwardenをプロバイダとして追加
onecli provider add bitwarden --vault-url "https://vault.bitwarden.com"

# サービス単位でレート制限ルールを作成
onecli rules create \
  --name "Stripe rate limit" \
  --host-pattern "api.stripe.com" \
  --action rate_limit \
  --rate-limit 10 \
  --rate-window 1h
```

## 実践ポイント
- 小規模でも「鍵を渡さない」運用を試す：テスト環境でOneCLIをプロキシとして立て、Bitwarden承認フローをワークフローに組み込む。
- ポリシーを先に設計：どのAPIにどのレート制限／承認要件を掛けるかを決め、OneCLIルールとして実装する。
- 監査と通知を有効化：承認記録（Bitwarden）と利用ログ（OneCLI）をSIEMや運用チケットに連携して可視化する。
- オープンソースで試す：両プロジェクトはOSSなので、まずはalpha版でPOCを回してリスクと運用コストを評価する。
