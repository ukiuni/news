---
  layout: post
  title: "FreeBSD Home NAS, part 3: WireGuard VPN, Linux peer, and routing - FreeBSDホームNAS（第3回）：WireGuard VPN、Linuxピア、ルーティング"
  date: 2026-01-04T12:10:52.317Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://rtfm.co.ua/en/freebsd-home-nas-part-3-wireguard-vpn-linux-peer-and-routing/"
  source_title: "FreeBSD: Home NAS, part 3 – WireGuard VPN, Linux peer, and routing"
  source_id: 1145873223
  excerpt: "FreeBSD NASでWireGuardを立て、PFとNATで自宅とオフィスを安全に接続"
  image: "https://rtfm.co.ua/wp-content/uploads/2025/11/freebsd_logo1.jpg"
---

# FreeBSD Home NAS, part 3: WireGuard VPN, Linux peer, and routing - FreeBSDホームNAS（第3回）：WireGuard VPN、Linuxピア、ルーティング
魅力タイトル: 自宅NASを安全に拡張する最短ルート ― FreeBSDでWireGuardを立ててオフィスと家をつなぐ実戦ガイド

## 要約
FreeBSD上のNASにWireGuardを導入して、自宅とオフィス（＋Linuxクライアント）を安全に接続する手順とポイントを分かりやすくまとめる。PF（Packet Filter）でのルールやルーティング、鍵管理、ルーター側のポートフォワード設定も扱う。

## この記事を読むべき理由
- 日本の在宅ワーカーや自宅サーバ運用者が、手元のFreeBSD NASを安全に外部や別拠点と接続するための実務的なノウハウが得られる。
- WireGuardは軽量でカーネル組み込み（パフォーマンスが高い）ため、低消費リソースの自宅サーバに最適。PFとの組み合わせで堅牢なネットワーク設計が可能になる。

## 詳細解説
1) WireGuardを選ぶ理由（要点）
- コードベース小・高速：カーネルで動作するためオーバーヘッドが小さい。
- P2Pモデル：サーバ／クライアントの概念はあるが、仕組み上は「ピア」を設定するだけ。
- 暗号はプロトコル内蔵：OpenVPNのような外部TLSライブラリ依存が少ない。

2) ネットワーク構成（例）
- オフィスLAN: 192.168.0.0/24（FreeBSD/NASが存在）
- 自宅LAN: 192.168.100.0/24（クライアント）
- VPNネットワーク: 10.8.0.0/24（WireGuard）
目的：FreeBSDをWireGuardの起点にして、双方のLAN間アクセス（ファイル共有、SSH等）を許可する。

3) FreeBSD側の主要手順（概略）
- パッケージとモジュールの準備
```sh
# pkg install wireguard-tools
# kldload if_wg
# sysrc wireguard_enable=YES
# sysrc wireguard_interfaces=wg0
```
- IPフォワーディングを有効に
```sh
# sysrc gateway_enable="YES"
# sysctl net.inet.ip.forwarding=1
```
- PF（Packet Filter）でWireGuardのハンドシェイク受けとVLAN間ルーティングを許可するルールを追加
  - UDP 51820（例）をFreeBSDへフォワード
  - wg0インターフェイス上の10.8.0.0/24からローカルLAN（192.168.0.0/24）やホーム側（192.168.100.0/24）へのトラフィックを許可
  - FreeBSD自身へのICMP/SSHはVPN経由も許可
（PFルールは「デフォルトブロック」→必要ポート明示許可の構成がベスト）

- 鍵の生成とwg0設定
```sh
# cd /usr/local/etc/wireguard
# wg genkey | tee server.key | wg pubkey > server.pub
# chmod 600 server.key
```
wg0.conf（サーバ側の最低限）
```ini
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = <server_private_key>
```
- 起動と確認
```sh
# wg-quick up wg0
# ifconfig wg0
# wg show
```

4) ルーター側（オフィスのTP‑Linkなど）
- グローバルIPが動的ならDDNSを設定（noip等）
- 外部UDPポート（例:51830）をFreeBSDの51820へNATフォワード（ポートマスクしておくと多少ぼかせる）

5) Linuxクライアント（Arch等）の設定
- インストールと鍵生成
```sh
# pacman -S wireguard-tools
# cd /etc/wireguard
# wg genkey | tee client.key | wg pubkey > client.pub
# chmod 600 client.key
```
- クライアント設定例（/etc/wireguard/wg-client.conf）
```ini
[Interface]
PrivateKey = <client_private_key>
Address = 10.8.0.2/32

[Peer]
PublicKey = <server_public_key>
Endpoint = office.example.ddns:51830
AllowedIPs = 10.8.0.1/32,192.168.0.0/24,192.168.100.0/24
PersistentKeepalive = 25
```
- サーバ側にクライアントの公開鍵とAllowedIPs（例 10.8.0.2/32）をPeerとして追加する。

6) ルーティングとPFのポイント
- WireGuardはIPベースでルーティングを追加するため、AllowedIPsで経路が作られる。クライアントがオフィスLANへアクセスするにはAllowedIPsにオフィスLANを追加するか、FreeBSD側で静的ルートを整備する。
- PFではwg0からのtransitを許可し、必要ならNATは行わず（拠点間ルーティングのみ）にするのが望ましい。

## 実践ポイント
- 小さく始める：まずはFreeBSD上でwg0を立ち上げ、ローカルから接続確認→PFルールを段階的に緩める。
- 鍵の管理：秘密鍵は必ず600、公開鍵のみ相手に渡す。複数クライアントはPeerエントリで管理。
- テスト手順
  1. FreeBSDでwg-quick up wg0 → ifconfig/wg showで状態確認。
  2. ルーター外部からUDPポート到達をnc/udpやオンラインポートチェックで検証。
  3. クライアントでwg-quick up → ping 10.8.0.1 → ping 192.168.0.x（オフィスLANの端末）。
- セキュリティ：管理ポート（SSH等）はVPN経由のアクセスだけに限定すると堅牢性が上がる。
- 運用上のコツ：Office側のグローバルIPが変わる可能性がある場合はDDNS + 非標準ポートで多少のプローブ回避／識別しやすさを両立する。
- ログと監視：pfのログとwg showで接続状態を定期確認。ZFSミラーにバックアップを保存する用途なら転送帯域や暗号負荷を監視しておく。

この構成はFreeBSDの堅牢性、WireGuardの軽快さ、PFの細かな制御を組み合わせた実用的な自宅／拠点VPNパターンです。まずは小さく動かして、PFルールとAllowedIPsを必要最小限にしてから段階的に拡張してください。
