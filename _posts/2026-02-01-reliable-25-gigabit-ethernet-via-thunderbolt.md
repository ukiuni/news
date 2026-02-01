---
layout: post
title: "Reliable 25 Gigabit Ethernet via Thunderbolt - Thunderbolt経由で実現する信頼できる25GbE"
date: 2026-02-01T11:35:03.995Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kohlschuetter.github.io/blog/posts/2026/01/27/tb25/"
source_title: "Reliable 25 Gigabit Ethernet via Thunderbolt | Dr. Christian Kohlschütter"
source_id: 46786575
excerpt: "Thunderbolt経由の安価25GbEを冷却とFW更新で実用化"
image: "https://kohlschuetter.github.io/blog/assets/posts/2026/01/27/tb25/px25g_product_shot.jpeg"
---

# Reliable 25 Gigabit Ethernet via Thunderbolt - Thunderbolt経由で実現する信頼できる25GbE
驚くほど小型・静音で携帯できる“Thunderbolt → 25GbE”アダプタを分解して発見した「実用化できる冷却＆ファーム更新手順」

## 要約
Thunderbolt接続の小型25GbEアダプタ（PXブランド相当）は実測でほぼ25Gbpsを出す一方、放熱不足で不安定になる。筐体を開けると中身はMellanox ConnectX‑4 LxのOCPカード＋Thunderbolt変換基板で、外付けヒートシンクとLinux上でのファーム更新で安定化できる。

## この記事を読むべき理由
- ノートPC中心の日本のモバイル／在宅ワーク環境で「単一ケーブルで25GbE」を手軽に使える可能性があるため。  
- 市販の高価なThunderbolt→25GbE製品を避け、安価な流通品を実用レベルにする具体策（冷却・FW更新）を示すから。

## 詳細解説
- 製品概要：Amazon等で見かける「Thunderbolt 25G」アダプタは安価で単一ケーブル給電。価格は単ポート・デュアルポートで概ね$157〜くらいから流通。動作はmacOSでPlug‑and‑Play（mlx5 DriverKit）だが、詳細設定は限定的。  
- 性能：iperf3で片方向約20.7 Gbps、双方向合計で約25 Gbps前後を確認（Thunderbolt 3/4経由の実装上の現実的上限に近い）。  
- 問題点：筐体温度が非常に高く（触れないレベル）、一部で接続消失やmacOSカーネルパニックを経験。内部はMellanox ConnectX‑4 Lx（OCP 2.0）カードと「Thunderbolt3→OCP」変換基板の二枚構成で、サーバ向けカードが流用されているため発熱が集中する。  
- 分解・解析：フロントのねじを外すと基板が取り出せる。デュアル版では金属ヒートスプレッダが欠損している個体もあり、追加冷却が効果的。ConnectX‑4カードは中古で安く入手可能だが、Thunderbolt変換基板が価値の中心。  
- 改善策（冷却）：ケース外側に大型ヒートシンクを“サンドイッチ”で貼る（例：120×69×27 mm 程度、熱伝導率の高い1mmサーマルパッド使用）。分解不要で筐体温度を少なくとも約15 K下げ、筐体周囲を40°C未満、チップ温度を約75°C前後に抑えられる。  
- 改善策（FW更新）：安定性向上のためConnectX‑4の最新ファームを書き込む。これはmacOS上では困難なため、Thunderbolt対応のWindows/Linux機（あるいはUSB4）で実施する。主な手順は以下の通り（要root・Boltデーモン有効化、FWファイルはNVIDIA/Mellanox配布から取得）。

```bash
# 例（Linux上での流れ）
sudo su
apk add mstflint bolt dbus polkit pciutils
/etc/init.d/dbus start
boltctl                 # 接続デバイスのUUIDを確認
boltctl enroll <UUID>   # デバイスを認可
echo 1 > /sys/bus/pci/rescan
lspci -v                 # MellanoxデバイスのPCIアドレスを確認（例 07:00.0）
mstflint -d 07:00.0 -i ./fw-ConnectX4...bin burn
# 書込み後は mstfwreset または再起動
```

- 注意点：Thunderboltハブやドックを経由すると帯域を共有するため、可能なら直接接続する。長いケーブルはUSB4/Thunderbolt 40Gbps対応を推奨。ヒートシンクを付けると携帯用ケースに収まらなくなる点も考慮。

## 実践ポイント
- まずは手元のMacでPlug‑and‑Playで挙動確認（iperf3で転送確認）。異常発熱や接続落ちがあれば分解または外付け冷却を検討。  
- 冷却は「大きめの外付けヒートシンク＋高導熱パッド」で分解不要の簡易対策が効果的。  
- 安定化の肝はファーム更新。Linux/Windowsマシン（Thunderbolt対応）でmstflintとboltctlを使ってファームを書き換えると信頼性が向上する。  
- 国内購入時はレビュー少なめ・個体差ありを想定し、保証・返品対応を確認すること。業務で使うなら冗長化（dual‑portで別経路）や正式メーカー品も検討を。

以上を踏まえれば、安価なThunderbolt→25GbEアダプタを実用レベルに持っていける可能性が高いです。
