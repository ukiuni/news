---
layout: post
title: "Aqua: A CLI message tool for AI agents - Aqua：AIエージェント向けCLIメッセージツール"
date: 2026-02-23T04:15:59.796Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/quailyquaily/aqua"
source_title: "GitHub - quailyquaily/aqua: Aqua, a cli message tool for AI agents"
source_id: 47117169
excerpt: "AquaはE2EE・P2PでAIエージェントをローカル/分散環境で安全に直接連携させるCLIツール"
image: "https://opengraph.githubassets.com/a8364eba2ac2b5e7329aef731461584cee0ec584ef4045dc4683b007026b996c/quailyquaily/aqua"
---

# Aqua: A CLI message tool for AI agents - Aqua：AIエージェント向けCLIメッセージツール
SSH不要でAI同士が直接・暗号化してやり取りできる「Aqua」で、ローカル／分散環境のエージェント連携を始めよう

## 要約
AquaはP2Pでエージェント間メッセージをやり取りする軽量CLI。エンドツーエンド暗号化、耐久的な受信箱/送信箱、リレー経由のネットワーク越え接続を備え、AIエージェント同士の安全な通信プロトコルを提供する。

## この記事を読むべき理由
日本企業や開発者はプライバシーとオンプレ寄りの運用を重視する場面が多く、クラウド依存を減らしてエージェント間通信を安全に実装できるAquaは実務導入の選択肢になり得るから。

## 詳細解説
- アーキテクチャ概要  
  AquaはCLIとプロトコルの組合せで、各ノードがピアIDを持ち、連絡先を検証してメッセージを交換する。メッセージはE2EEで保護され、ノード側に耐久的なinbox/outboxを保持するため、オフライン受信や再送が可能。

- ネットワーク／接続モデル  
  直接通信が可能なら直接接続、NATやファイアウォール越えが必要な場合はCircuit Relay v2（TCP/QUIC）で中継。公式リレーも用意されており、--relay-mode autoで自動フォールバックする。

- セキュリティと検証  
  ピアのアイデンティティ管理と連絡先の検証コマンドがあり、信頼チェーンを作れる点が特徴。メッセージはエンドツーエンド暗号化されるため中継者は中身を見られない。

- CLIと開発者向け要素  
  主要コマンド：init / id / serve / contacts / send / inbox / outbox。デフォルトデータディレクトリは ~/.aqua。Go製で、SKILL.mdやAGENTS.mdにエージェント向け統合例あり。

## 実践ポイント
- インストール（推奨：リリースバイナリ）
```bash
# バイナリ自動インストール
curl -fsSL -o /tmp/install.sh https://raw.githubusercontent.com/quailyquaily/aqua/refs/heads/master/scripts/install.sh
sudo bash /tmp/install.sh
```

- ソースから（Goが必要）
```bash
go install github.com/quailyquaily/aqua/cmd/aqua@latest
```

- 最短サンプル（2台での手順）
```bash
# 各ノードでIDを作成
aqua id alice     # 出力に peer ID
# サーバー起動（ローカル）
aqua serve
# 相手のアドレスを contacts に登録・検証して送信
aqua contacts add "<peer_addr>" --verify
aqua send <peer_id> "hello"
aqua inbox list --unread --limit 10
```

- NAT越え／リレー  
  --relay-mode auto を使えば直接接続→リレーの自動切替。独自リレーを立てるか、公式リレーを利用可能。

- 日本向け運用アドバイス  
  機密データを扱う場合はオンプレ側にAquaノードを置いて連絡先検証を厳格化すること、リレー運用は社内で握るか公式を信頼するか方針を決めることが重要。

元リポジトリ（導入手順やSKILL.md）を参考に、まずはローカルでid→serve→contacts→sendの流れを試してみることを推奨する。
