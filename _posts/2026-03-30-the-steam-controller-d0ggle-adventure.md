---
layout: post
title: "The Steam Controller D0ggle Adventure - スチームコントローラー「D0ggle」冒険譚"
date: 2026-03-30T06:47:12.538Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://im-just-lee.ing/steam-controller-d0ggle-54682aa4/"
source_title: "The Steam Controller D0ggle Adventure"
source_id: 785689449
excerpt: "廃盤のSteamドングルをSMD交換で確実に復活させる実践記"
---

# The Steam Controller D0ggle Adventure - スチームコントローラー「D0ggle」冒険譚
Steam Controllerの“壊れたドングル”を自力で復活させたハードウェア・ハックの一部始終

## 要約
Steam Controllerの無線ドングル（通称d0ggle）が壊れたところから、チップの特定・フラッシュ地獄・最終的なSMDチップ交換で復活させるまでの実録。プロトコル解析やツール選定など、実践的なハードウェア改修のノウハウが詰まっている。

## この記事を読むべき理由
- 廃盤になった周辺機器を自力で直す方法が具体的に分かる（部品選定〜フラッシュ手順〜SMDリワーク）。
- 初心者でも理解できるように、ソフト／ハード両面のトラブルシューティング手順が学べる。
- 日本でも入手困難な周辺機器の代替策や、買い替え前の修理判断材料になる。

## 詳細解説
- 症状と初動：ドングルの外装が取れてPCBむき出し、USB差込部の接触不良でLinuxのdmesg/lsusbに断続的に認識が出る状態からスタート。多層基板の微細クラックによる断線が多い点に注意。
- チップ特定：基板上のチップ表記はNRF24LU1P。NordicのUSBマイコンで、過去のLogitech Unifyingなどにも使われた実績あり。データシートを元にISP/SPIパッドやInfoPageの存在を確認。
- フラッシュ試行の挫折：AliExpressの安価なNRF24ボードはファームロックや16KB版（必要なのは32KB）で使えず、SPI経由でも読み書き不可。既存のオープンソースツール（NRF24LU1prog, Bastilleのnrf-research-firmware）はハード／ソフト両面で互換性問題がある（特定LogitechモデルやPython2依存など）。
- 代替ドングル問題：Logitechの一部モデル（C-U0007等）は書き換え可能だが、ブートローダーやモデル差で実用的な交換は確実性に欠ける。
- 解決策（成功）：SMDリワークでNRF24LU1Pの新品（F32: 32KB版）を基板に載せ替える。適切な温度管理（例：Kaptonテープで周辺保護、リフローでチップを取り外し・実装）と手順を守れば成功率が高い。
- ペアリングとプロトコル：Valveは後に公式でソースを公開（Bluetooth対応の補助資料にドングル用ファームが含まれる）。ドングルとコントローラ間は独自USB Feature Reportベース（[type][length][payload]の単純構造）。Linuxでは/dev/hidraw*経由でやり取りでき、既製のライブラリ（例: kolrabi/steamcontroller 等）を活用すれば実用的にペアリングが可能。

## 実践ポイント
- 最初にやること：lsusb / dmesgで認識確認、外装だけか基板断線かを目視で判断する。マルチメータで電源ラインの連続性をチェック。
- 部品選定：NRF24LU1Pにはフラッシュサイズ違いがある（16KB vs 32KB）。置換用チップは32KB版を買うこと。Digikey等の信頼できる流通を推奨。
- フラッシュ前の注意：AliExpress安物NRF基板はInfoPageロックや読み取り不可のものが多い。SPI経由でのフラッシュは専用プログラマと正しいピンアサインが必要。
- SMD作業のコツ：Kaptonテープで周辺を保護、温度管理（リフロー温度帯と低風量）を守る。初心者は練習パーツで慣らしてから本番を。
- ソフト面：nrf-research-firmwareやOpenSteamControllerなどのOSSを参照。スクリプトのベンダーIDやPythonバージョン差に注意して自分で修正できると強い。
- セーフティ：静電気対策、適切な換気、基板を壊さないための温度管理を徹底する。

参考になるOSS：
- NRF24LU1prog（Arduinoベースの書き込みツール）
- BastilleResearch/nrf-research-firmware
- OpenSteamController / kolrabi/steamcontroller（プロトコル解析・制御例）

短く言うと：買い替えより面倒だが、正しいチップ特定→SMD交換→公式ファーム書き込みの流れを踏めば、廃盤ドングルを自力で復活できる—電子工作の良い修行になる話です。
