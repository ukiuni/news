---
layout: post
title: "Don't run OpenClaw on your main machine - メインマシンでOpenClawを実行してはいけない"
date: 2026-02-27T18:32:28.542Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.skypilot.co/openclaw-on-skypilot/"
source_title: "Don't Run OpenClaw on Your Main Machine | SkyPilot Blog"
source_id: 47183503
excerpt: "OpenClawは個人PCで情報漏えいリスクが高く、クラウドVMでの隔離運用を推奨"
image: "https://blog.skypilot.co/openclaw-on-skypilot/assets/banner.png"
---

# Don't run OpenClaw on your main machine - メインマシンでOpenClawを実行してはいけない
魅惑のAIアシスタント、でも「自分のPCで動かす」にはリスクが大きすぎる — 安全に試すためのクラウド隔離ガイド

## 要約
OpenClawはメッセージ経由でシェルやブラウザ、ファイルにアクセスする強力なセルフホストAIエージェントだが、プロンプト注入や実際の脆弱性により個人PCでの稼働は危険。クラウドVMでの隔離運用が現実的な対策。

## この記事を読むべき理由
日本の開発者や個人利用者も短期間で導入が進む可能性が高く、誤った運用はSSH鍵やブラウザセッション、企業VPN情報などを一発で漏らすリスクがあるため、導入前の安全設計が必須。

## 詳細解説
- OpenClawの挙動（要点）
  - チャット経由でシェル実行、ブラウザ自動操作（Playwright）、ファイル読み書き、100以上のサービス連携、ベクトルメモリ、スケジュール実行を行う。
- なぜ危険か
  - エージェントはユーザーと同等のアクセス（事実上のroot権限に近い）を持ち、プロンプト注入で悪意ある命令を実行してしまう。
  - 実被害事例：CVE-2026-25253（未認証のWebSocketでトークン抽出）、21,000以上の露出インスタンス、Moltbookデータ漏洩、サプライチェーン攻撃など。
- 隔離オプション（比較）
  - Docker：マウントを限定できるがホストとネットワークを共有、逃走脆弱性は稀だが存在。
  - 専用ハード：物理的隔離が強力だが初期コストと管理が必要。
  - クラウドVM（推奨）：個人データを持ち込まず、侵害時の影響範囲をVM内に限定。簡単に破棄・再作成できる。
- SkyPilotを使う利点
  - VMのプロビジョニング、セットアップ、ライフサイクルをYAMLで自動化。WebUIはローカルバインド＋SSHトンネルで公開ポートを回避。

## 実践ポイント
1. 絶対にメインPCで直接動かさない。まずはクラウドVMで検証。
2. SkyPilotでの簡単な流れ（例）
```bash
# SkyPilotインストール（例: AWS用）
pip install 'skypilot[aws]'
sky check

# OpenClaw起動（openclaw.yamlを用意）※ANHTROPIC_API_KEYは環境変数で渡す
sky launch -c openclaw openclaw.yaml --env ANTHROPIC_API_KEY

# ローカルブラウザでWebChatにアクセスするためのSSHトンネル
ssh -L 18789:localhost:18789 openclaw
# ブラウザで http://localhost:18789 を開く（起動時に表示されるトークンを入力）
```
3. チャネル連携（VM上で実行）
```bash
ssh openclaw
openclaw onboard
# 個別ログイン例
openclaw channels login --channel whatsapp
openclaw channels login --channel telegram
```
4. 運用管理
```bash
# 一時停止（ディスク保存）
sky stop openclaw
# 再開
sky start openclaw
# 完全削除（ディスクも消える）
sky down openclaw
```
5. セキュリティ運用の基本
  - WebChatは必ずSSHトンネル経由で利用し、ポートは公開しない。
  - ANTHROPICなどのAPIキーはVMへ環境変数で渡し、不要ならすぐ撤去。
  - 使用しないときはsky stopで停止、使い終わったらsky downで破棄。重要データはS3やrsyncで外部保存。
  - 小規模利用なら2CPU/4GBのインスタンスで十分（コスト目安：約$0.03–0.05/時）。

以上。安全な隔離運用を前提に、まずはクラウドVMで小さく試してから拡張することを推奨。
