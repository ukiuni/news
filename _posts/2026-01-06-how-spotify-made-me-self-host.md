---
  layout: post
  title: "How Spotify Made Me Self Host - Spotifyが私をセルフホストへ導いた"
  date: 2026-01-06T20:53:56.838Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://layandreas.github.io/personal-blog/posts/how-spotify-made-me-self-host/"
  source_title: "How Spotify Made Me Self Host | Personal Blog"
  source_id: 46517636
  excerpt: "Spotify値上げを契機にJellyfinとWireGuardで低コストなセルフホストを構築"
  image: "https://layandreas.github.io/personal-blog/%3Clink%20or%20path%20of%20image%20for%20opengraph,%20twitter-cards%3E"
---

# How Spotify Made Me Self Host - Spotifyが私をセルフホストへ導いた
サブスク疲れを抜け出す最短ルート：Spotify値上げで始めたJellyfin + WireGuardセルフホスティング入門

## 要約
Spotifyなどのストリーミングの値上げ・UX低下をきっかけに、Hetzner上にJellyfinとWireGuardでメディアをセルフホストした事例紹介。低コストでプライバシーと操作性を取り戻す実践ガイド。

## この記事を読むべき理由
日本でもサブスクの値上げや広告挿入、パスワード共有取り締まりなどが話題になる中、手持ちの音楽・動画コレクションを低コストで安全に配信する選択肢として、セルフホスティングは実用的な代替案になり得る。特に技術者や自宅でメディアを楽しむ人には具体的な構成例が参考になる。

## 詳細解説
- 背景
  - 著者はSpotifyの値上げと無料プランの制約（シャッフル強制・シーク制限）に失望し、既存のメディアコレクションを活かして自前サーバに移行。
  - ストリーミング各社は価格改定や広告導入でUXが悪化しがち。コスト対価値を重視する観点からセルフホスティングを検討した。

- 全体アーキテクチャ
  - デプロイ先：Hetzner VPS（例: CAX21 — 4 vCPU / 8GB RAM / 20TBトラフィック / 80GB SSD）
  - ストレージ：Hetzner Storage BoxをSMBでマウントし、メディアを共有・ローカルからもアクセス可能に
  - メディアサーバ：Jellyfin（OSS）。Plexはプロバイダ制限で非推奨。
  - リモートアクセス：WireGuardでVPNトンネルを構築。家庭内はルータ側でWireGuard設定を入れてLAN機器が透過的に利用可能に。

- WireGuardの構成ポイント
  - サーバ側は内部VPNアドレス帯（例: 10.13.13.1/24）を割り当て、ListenPortは51820/udp。
  - PostUp/PostDownでiptablesルールを立ててJellyfinのポート（例: 8096）をVPN経由で許可する。
  - クライアントは端末ごとに鍵ペアとAllowedIPsを割り当て、各デバイスの内部IPを固定する。

- Docker構成の要点
  - WireGuardをコンテナで立て、Jellyfinはそのネットワークスタックを共有（network_mode: "service:wireguard"）することで外部にJellyfinポートを直接公開せずVPN経由のみでアクセス可能にする手法。
  - ストレージは読み取り専用でマウントして権限を分離。

- 注意点・デメリット
  - ライブラリ規模は商用ストリーミングに及ばない。メンテナンスとセキュリティ対応が必要。
  - 国際的なVPS（Hetzner）は日本からのレイテンシや配信帯域、法令順守の面で差異があるため、国内プロバイダ（さくらのVPS、ConoHa等）も選択肢に入れるべき。

## 実践ポイント
- まず在庫確認：手持ちメディアの量とフォーマット、サブタイトルやメタデータの整備から始める。
- プロバイダ選定：トラフィック量重視ならHetzner、国内低遅延を重視するなら国内VPSを検討。
- 手順（最短）
  1. VPSを立てる（例: 4vCPU/8GB）
  2. Storage Boxか外部ストレージをSMB/NFSでマウント
  3. WireGuardを先に構築してVPN経由のアクセスを確立
  4. JellyfinをDockerでデプロイし、メディアをマウントしてライブラリ作成
  5. 各端末は個別のWireGuardクライアント設定を作成
- セキュリティと運用
  - Jellyfinの管理アカウントは強固に、定期的にアップデートを行う
  - VPNの鍵はバックアップし、不要なピアは削除
  - 公開する場合はTLSや認証強化を検討する
- 参考設定（簡略）
  - WireGuardサーバ（例）
```ini
[Interface]
Address = 10.13.13.1/24
ListenPort = 51820
PrivateKey = <SERVER_PRIVATE_KEY>
PostUp = iptables -A INPUT -i wg0 -p tcp --dport 8096 -j ACCEPT; iptables -A FORWARD -i wg0 -j ACCEPT
PostDown = iptables -D INPUT -i wg0 -p tcp --dport 8096 -j ACCEPT; iptables -D FORWARD -i wg0 -j ACCEPT
```
  - docker-compose（要点）
```yaml
version: "3.9"
services:
  wireguard:
    image: linuxserver/wireguard:latest
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - SERVERPORT=51820
      - SERVERURL=<YOUR_SERVER_IP_OR_DOMAIN>
    ports:
      - "51820:51820/udp"
    volumes:
      - ./wireguard/config:/config
  jellyfin:
    image: jellyfin/jellyfin:latest
    network_mode: "service:wireguard"
    volumes:
      - ./jellyfin/config:/config
      - /mnt/storagebox:/media:ro
    depends_on:
      - wireguard
```

まとめ：手間は必要だが、コストとプライバシー、操作性を重視するならセルフホスティングは現実的な選択肢。日本の環境に合わせてプロバイダやネットワーク設計を調整すれば、実用的なメディア環境を自前で作れる。
