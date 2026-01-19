---
layout: post
title: "A Tale of UDP tracking: Hytale server auto stop and start with systemd - UDPトラッキング物語：systemdでHytaleサーバーを自動停止・起動"
date: 2026-01-19T11:55:06.714Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nwildner.com/posts/2026-01-19-hytale/"
source_title: "A Tale of UDP tracking: Hytale server auto stop and start with systemd - my random ideas"
source_id: 1708386896
excerpt: "UDPトラフィック検知で非稼働時にHytaleを自動停止・起動、省エネ運用手順を解説"
---

# A Tale of UDP tracking: Hytale server auto stop and start with systemd - UDPトラッキング物語：systemdでHytaleサーバーを自動停止・起動
遊んでいないときはサーバーを自動で止めて省エネにする――UDPを「数える」だけで実現する手早いsystemd運用術

## 要約
Hytaleサーバーを、UDPパケットの流量を監視して一定時間無通信なら自動停止し、最初のUDP到着で自動起動する仕組みをsystemdの.socket＋サービス＋監視スクリプトで構築する手順を紹介する。

## この記事を読むべき理由
- 常時稼働させたくない個人/小規模ゲームサーバーを省エネかつ安全に運用したい読者に直結する実用テク。
- root権限を与えずに「一般ユーザー権限」でUDPトラフィックの変化を検出する現実的な回避策が学べる。

## 詳細解説
目的は「接続者がいない間にHytaleサーバーを自動で停止してワールド時間を止める」こと。実装の要点は次の3つです。

1. systemdの.socketでUDPポート（例: 5520/udp）をリッスンし、最初のパケット到着でサーバーを起動させる。
2. サーバープロセスの稼働中にグローバルなUDPパケット数をポーリングし、増加がなければ一定時間（例120秒）で停止するwatchdogスクリプトを走らせる。
3. 「一般ユーザー」で見られる情報ソースとして /proc/net/snmp を利用し、ルート権限を必要とせずにUDPダイジェスト数を取得する。

実際のファイル例（パスは適宜書き換えてください）。

systemd socketユニット:
```ini
# hytale.socket
[Unit]
Description=Hytale UDP Server Socket

[Socket]
ListenDatagram=5520
Accept=no

[Install]
WantedBy=sockets.target
```

systemd serviceユニット（Hytale本体）:
```ini
# hytale.service
[Unit]
Description=Hytale Server
After=network.target

[Service]
Environment=HOME=/home/nwildner
WorkingDirectory=/home/nwildner/hytale
ExecStart=/usr/bin/java -XX:AOTCache=Server/HytaleServer.aot -jar Server/HytaleServer.jar --assets Assets.zip
TimeoutStartSec=300
Restart=no

[Install]
WantedBy=multi-user.target
```

watchdogスクリプト（UDPパケットの増減を見て停止する）:
```bash
#!/bin/bash
SERVICE="hytale.service"
SOCKET="hytale.socket"
TIMEOUT=120

get_pid() {
  systemctl --user show --property=MainPID --value "$SERVICE"
}

get_udp_packets() {
  awk '/^Udp:/ {getline; print $2}' /proc/net/snmp
}

pid=$(get_pid)
[ "$pid" -eq 0 ] && exit 0

last_packets=$(get_udp_packets)
last_activity=$(date +%s)

while kill -0 "$pid" 2>/dev/null; do
  packets=$(get_udp_packets)
  if [ "$packets" -gt "$last_packets" ]; then
    last_packets="$packets"
    last_activity=$(date +%s)
  fi

  current_time=$(date +%s)
  delta_time=$(( current_time - last_activity ))

  if [ "$delta_time" -gt "$TIMEOUT" ]; then
    echo "Idle timeout reached, stopping $SERVICE"
    systemctl stop --user "$SOCKET"
    sleep 10
    systemctl stop --user "$SERVICE"
    sleep 10
    systemctl start --user "$SOCKET"
    exit 0
  fi

  sleep 5
  pid=$(get_pid)
done
```

watchdogのsystemdユニット:
```ini
# hytale-watchdog.service
[Unit]
Description=Hytale Idle Watchdog

[Service]
Type=simple
ExecStart=/home/nwildner/hytale/watchdog.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

有効化コマンド（ユーザー空間）:
```bash
systemctl --user enable --now hytale.socket
systemctl --user enable --now hytale-watchdog.service
```

設計上のポイントと注意点
- /proc/net/snmp を使うのは、一般ユーザーでアクセスできてグローバルなUDP受信数を得られるため。プロセス単位やポート単位の正確なカウントはできない（同一ホストで他UDPサービスが動いていると誤検知の可能性）。
- ss/tcpdump/conntrackは権限やUDPの性質上、一般ユーザー運用では都合が悪い／情報が取れない場合がある。
- systemdの.socketで起動はできるが「稼働中の通信を追跡して自動停止」する機能はsystemd単体では賄えないため、外部スクリプト（watchdog）で補完している。
- 停止→再起動の操作に短いsleepを挟むのは、systemd内部でsocketとserviceが競合してしまう現象を回避するため。

クライアント側の注意
- Hytaleサーバーの初期起動に約15秒かかるため、クライアント側が10秒でタイムアウトする設定だと「最初だけ接続失敗」が生じる。ユーザー体験の改善にはサーバー側/クライアント側のタイムアウト調整が必要。

## 実践ポイント
- PATHやユーザー名（例: /home/nwildner）は自分の環境に合わせて必ず書き換える。
- TIMEOUTの秒数は用途に応じて調整（短くすると誤停止しやすく、長くすると省エネ効果が薄れる）。
- 同一ホストでDNSや別のUDPサービスを動かす場合は、この方法だと誤検知する可能性がある。必要ならroot権限でconntrackやtcpdump、またはファイアウォールでポートごとのカウントを検討する。
- まずは手動でsocketを起動→最初のUDP到着でサービスが上がること、watchdogが停止することを確認してから自動有効化する。
- 初回接続の「no server available」問題はサーバー起動待ち時間の調整（クライアント側）で緩和できる点をユーザーに伝えると親切。

以上を実装すれば、root権限をなるべく使わずに、UDPの流量変化だけでHytaleサーバーを自動的に省エネ運用する仕組みが手に入ります。
