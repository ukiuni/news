---
layout: post
title: "2026 is the Year of Self-hosting - 2026年はセルフホスティングの年"
date: 2026-01-11T23:04:38.455Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://fulghum.io/self-hosting"
source_title: "2026 is the year of self-hosting"
source_id: 46580326
excerpt: "ミニPC＋Tailscale＋CLIで手軽に自宅クラウド運用を実現"
image: "https://fulghum.io/glances.png"
---

# 2026 is the Year of Self-hosting - 2026年はセルフホスティングの年
家の1台で「自前クラウド」が楽しくなる理由——CLIエージェントで誰でも始められるセルフホスティング入門

## 要約
CLIエージェント（例：Claude Code）＋小型低消費電力PC＋Tailscaleの組み合わせで、自宅サーバーの導入が格段に簡単かつ実用的になった。パスワード管理や写真、メディアなど日常サービスを自前で安全に運用できる年が来た、という主張。

## この記事を読むべき理由
日本でもプライバシーやコスト、サービスのロックイン回避に関心が高まっている今、難しい設定作業を減らして「使える」自宅サーバーを手軽に構築できる手法は即実践価値がある。家庭用回線・機器の事情を踏まえた実用的な手順と注意点が得られる。

## 詳細解説
- 「なぜ今か」  
  1) 小型で静音・低消費電力なミニPCが安価に手に入る（例：Beelink系）  
  2) Tailscale等でポート開放や複雑なネットワーク設定をほぼ不要にできる（NAT越え／VPN代替）  
  3) Claude CodeのようなターミナルネイティブなCLIエージェントが、DockerやComposeの細かい書式を代行してくれるため導入工数が大幅に減る

- 実際の流れ（要点）  
  1) ミニPCにUbuntu Server（例：22.04 LTS）をインストール  
  2) Tailscaleを入れてリモートから安全にSSH接続できるようにする  
  3) サーバ上でClaude Codeなどエージェントを動かし、「Dockerを入れてComposeファイルを作って」と自然言語で指示する  
  4) Caddyによるリバースプロキシ（自動TLS）、各サービスを個別コンテナで起動、データ永続化、起動時自動復旧などを設定

- 典型的に動かすサービス  
  - Vaultwarden（Bitwarden互換の自己ホスト型パスワード管理）— iOSのデフォルトパスワードマネージャとしての運用も可能  
  - Immich（Google Photos代替）— モバイルアップロード、顔認識、タイムライン等をローカルで提供  
  - Plex（メディア）— ハードウェアトランスコードが必要ならPlex Passを検討  
  - Uptime Kuma（簡易監視）、ReadDeck（あとで読む系）、Caddy（自動TLSのリバースプロキシ）  
  - 運用補助：Lazydocker（ターミナルでのDocker操作UI）、Glances（リソース監視）

- パフォーマンスの実例  
  ミニPCで13コンテナを稼働させ、メモリ4GB程度・低CPUで安定動作という事例がある。重い処理（大規模トランスコードや大規模ML推論）は別途考慮。

## 実践ポイント
- 最初の一本は「Vaultwarden」を入れると成功感が高い（既存のパスワードを移行して日常運用に直結するため）。  
- 必須セットアップ（順）  
  1) OS（Ubuntu Server 22.04等）  
  2) Tailscale（外部アクセスを簡素化）  
  3) Docker / Docker Compose（コンテナ管理）  
  4) Caddy（リバースプロキシ＋自動TLS）  
  5) Claude Code等のエージェント（設定自動化）  
- データ永続化：コンテナのボリュームは必須。外付けNVMe/HDDを用意して定期バックアップ（別PC/クラウド）を取る。  
- 安全対策：OS・コンテナの自動更新ルール、ファイアウォール、TailscaleのACL、Vaultwardenの強力なマスターパスワード運用。  
- 電源対策：停電時のデータ破損を避けるため小型UPSの導入を検討。  
- 回線・ISPの注意点：住宅用回線のグローバルIP・ポート制限や上り帯域を確認。Tailscaleで多くは解決するが、ファイルアップロードや外部配信は帯域がボトルネックになり得る。  
- ローカル法規／利用規約：家庭でのサーバ公開がISPの規約に抵触しないか事前に確認する。

このアプローチは「インフラ専門家になりたくないけど、自前でサービスを持ちたい」人向け。日本の読者なら、まずは静音で省電力のミニPC＋Tailscaleで始め、VaultwardenやImmichの導入で手応えを得るのが近道。
