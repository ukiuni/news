---
layout: post
title: "Claude Cowork runs Linux VM via Apple virtualization framework - ClaudeのCoworkはAppleの仮想化フレームワークでLinux VMを実行"
date: 2026-01-15T20:19:25.705Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gist.github.com/simonw/35732f187edbe4fbd0bf976d013f22c8"
source_title: "linux-container-environment-report.md · GitHub"
source_id: 46613304
excerpt: "Apple仮想化で動くClaudeの隔離Linux VMの仕組みと安全対策を簡潔解説"
image: "https://github.githubassets.com/assets/gist-og-image-54fd7dc0713e.png"
---

# Claude Cowork runs Linux VM via Apple virtualization framework - ClaudeのCoworkはAppleの仮想化フレームワークでLinux VMを実行
Mac上でAIが「隔離されたLinux」を立ち上げる仕組み──あなたのMacで何が起きているかを簡潔に解説

## 要約
Claudeの「Cowork」機能は、AppleのVirtualizationフレームワーク（VZVirtualMachine）を使ってApple Silicon上でARM64のUbuntu 22.04 VMを起動し、厳格にサンドボックスされた環境でコード実行やファイル操作を行う仕組みを採用している。

## この記事を読むべき理由
ローカルで動くAIアシスタントが実際にどのように「隔離」しているかは、プライバシーや社内ポリシー、開発ワークフローに直結します。特にMac（Apple Silicon）を業務で使う日本の開発者・運用担当者にとって、技術的な安全策と制約を理解しておくことは重要です。

## 詳細解説
- 基本構成
  - VMはUbuntu 22.04.5 LTS（aarch64）で、カーネルはLinux 6.8系。ホストはApple Silicon／macOS 13以上が必要。
  - VMバンドル（rootfs.img＋10GBのセッションディスク）はclaude.aiから配布され、SHA256で整合性確認できる設計。
  - ネイティブ（Swift）モジュールがVMのライフサイクルを管理し、Node.js向けにバインディングを公開（createVM / startVM / stopVM / vmIsProcessRunning 等のAPI）。

- サンドボックスの中身（セキュリティ）
  - Bubblewrap（bwrap）で名前空間（ネットワーク、PIDなど）を分離。親プロセス終了でコンテナも死ぬ（die-with-parent）。
  - seccompフィルタとカスタムBPFでシステムコールを厳しく制限。NoNewPrivs有効、すべてのケーパビリティ削除。
  - ネットワークは全てローカルのプロキシ経由（socatで /tmp/claude-*.sock をフォワード、HTTP: localhost:3128、SOCKS5: localhost:1080）で制御・監査可能。
  - 永続領域はワークスペース用のbindfsマウントのみで、セッション自体はエフェメラル（作業フォルダは残る）。

- 環境・ツール
  - インストール済み主要ツール：Python 3.10、Node.js 22、npm、GCC 11、OpenJDK 11 等。Go/Rust/Dockerは含まれないため、特定のビルドやコンテナ作業は制限される。
  - リソース例：4コアARM64、約3.8GiB RAM、10GBディスク（session用）など。

- 実行・通信
  - VM内部でタスクを実行し、結果はRPCクライアント（ClaudeVMDaemonRPCClient）を通じてホストに返る。UIはclaude.ai側で管理され、ローカルで安全に処理を行う形。

## 実践ポイント
- 開発者／運用向けチェックリスト
  - macOS 13＋Apple Siliconが必須：社内の端末ポリシーに反しないか確認する。
  - VMバンドルのSHA256を検証して改ざん防止を行う。
  - seccomp/BPFやNoNewPrivsを採用しているかを監査し、必要なら追加ログを取得する。
  - ネットワークはプロキシ経由かつソケットでフォワードされるため、プロキシログやソケットの監視ポイントを設定する。
  - 永続化されるフォルダ（outputs/uploads）を特定し、機密データの取り扱いルールを決める。

- 日本の現場での意味合い
  - Apple製端末が多いチームでは「ローカルで動くが隔離された」AIワークフローを取り入れやすい。規制・コンプライアンス観点では、エフェメラルなセッションと厳格なネットワーク制御が評価点になる。
  - 一方でGo/Rust/Dockerが無い制約はCI的な検証や再現性に影響するため、ワークフロー設計時に考慮が必要。

短くまとめると、ClaudeのCoworkは「Appleの仮想化で動く、堅牢に設計されたローカルVMを使ったサンドボックス」です。実際の導入や監査では、VMバンドルの整合性、seccomp/プロキシ設定、永続フォルダの扱いを重点的に確認してください。
