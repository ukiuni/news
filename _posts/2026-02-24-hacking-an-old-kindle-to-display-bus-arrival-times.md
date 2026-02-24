---
layout: post
title: "Hacking an old Kindle to display bus arrival times - 古いKindleをバス到着時刻表示端末に改造する"
date: 2026-02-24T20:36:58.518Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.mariannefeng.com/portfolio/kindle/"
source_title: "Repurpose your old Kindle"
source_id: 47141797
excerpt: "古いKindleを脱獄して路線APIを画像化し、e-inkで省電力なバス時刻表示端末に改造する手順"
---

# Hacking an old Kindle to display bus arrival times - 古いKindleをバス到着時刻表示端末に改造する
魅力的タイトル: 使い古したKindleが「置き型時刻表」に早変わり — e-inkで省電力なバス時刻ダッシュボードを自作しよう

## 要約
古いKindleを脱獄してKUAL/MRPIとSSHを導入し、路線APIから取得した情報をサーバ側で画像化してKindleに表示する手順を解説する。結果は1分ごとに更新され、メニューボタンでダッシュボードを終了できる。

## この記事を読むべき理由
– 古いデバイスを再利用して実用的なIoT端末を低コストで作れる。  
– e-inkの低消費電力・視認性を活かした実践的プロジェクトで、初心者でも学べるポイントが多い。

## 詳細解説
1. 全体像  
   高レベルの流れは：Kindleを脱獄 → KUAL/MRPI導入 → SSH接続（USB経由可）→ サーバで端末解像度に合わせたPNGを生成 → KUAL拡張としてダッシュボード起動スクリプトを作成、という流れ。端末は画像を受け取り eips コマンドで表示する仕組み。

2. 脱獄（Jailbreak）  
   機種・ファームウェアごとに手順が異なるので、対応のtarファイルと手順書を参照して実行。成功後にKUAL等を入れる準備が整う。

3. KUAL と MRPI の導入  
   KUALはKindle上のカスタムアプリランチャー、MRPIは拡張のインストールを助けるツール（機種によって不要）。導入前にホットフィックス系の手順を踏む必要があることが多い。導入後はOTA更新を無効化するのが定石。

4. SSH（USBNetwork）セットアップ  
   KUAL拡張のUSBNetworkを入れれば、USB接続時にPCからKindleへSSHでログインできる。Linux/Macのネットワーク接続に「Connected」と表示されれば成功。これで eips 等のコマンドが使える。

5. サーバ側：データ取得と画像生成  
   - データ取得：元記事はNJTransitのGraphQLを直接叩いてバス到着データを取得。国内なら公共交通のAPIやGTFS-RT/GQLなどを利用可能。例（NJTransitのcurl）:

```bash
# bash
curl 'https://www.njtransit.com/api/graphql/graphql' \
  -H 'content-type: application/json' \
  --data-raw '{"operationName":"BusArrivalsByStopID","variables":{"stopID":"YOUR_STOP_NUMBER"},"query":"query BusArrivalsByStopID($stopID: ID!) { getBusArrivalsByStopID(stopID: $stopID) { departingIn destination route time capacity } }"}'
```

   - 画像化：HTMLをレンダリングしてPNG化する方法としてはPuppeteerやwkhtmltoimageがある。小規模サーバ（安価なDroplet等）ではPuppeteerが重く、wkhtmltoimageを使いHTMLエンドポイントを定期的にキャプチャしてPNGを生成する手法が安定する。Docker内でcron→wkhtmltoimageでpngを作り、Kindleはその画像を取得するだけ。

6. 画像の向きと解像度の調整（重要）  
   Kindleの解像度は eips -i で確認。機種によって回転が必要。HTML側で回転（CSSの transform: rotate(90deg) translateX(...) translateY(...) ）してから画像化し、切れや位置ずれが出ないよう調整する。表示用PNGは端末解像度に厳密に合わせる。

7. KUAL拡張（ダッシュボード起動アプリ）の作成  
   /mnt/us/extensions/ に拡張フォルダを置くとKUALから起動できる。拡張は menu.json や bin/start.sh などを含み、start.shは長時間動作するスクリプト。KUALがGUIに絡むため、スクリプト内で SIGTERM/SIGHUP を無視する trap を設定してプロセスが途中終了しないようにする。

8. ユーザー操作と終了検出  
   evtest を使い /dev/input/eventX を監視してメニューボタン（例: code 102 (Home), value 1）を検出し、押下で stop.sh を呼び出してダッシュボードを終了・UIを復帰させる。

9. 電源と耐久性の考慮  
   - 画面の色残り（color bleeding）は長時間表示で出る。画面を黒→白でフラッシュして改善を試す。  
   - バッテリー：1分毎更新だと数日持つ。更新間隔を伸ばしたり就寝時間に電源を落とすなどで延命可能。

## 実践ポイント
- 端末機種・FWの確認は最初に必須。脱獄手順を間違うと文鎮化のリスクあり。  
- まずはローカルで動作確認：サーバをローカルで立ててKindleから画像が取得できるか試す。  
- 画面表示は eips -i で解像度確認、HTMLはその寸法で作る。回転やtranslateの微調整を忘れずに。  
- 小さいVPSで動かすなら wkhtmltoimage + cron の方が軽量で安定する。Puppeteerはメモリ重め。  
- KUAL拡張は /mnt/us/extensions/<your-ext> 配下に置き、menu.jsonで「Start dashboard」を実行するスクリプトを指定。  
- メニューで終了させる実装（evtestでボタン検出）は必須のUX。ボタンが使えないと端末が使いづらくなる。  
- 日本の公共交通API（地方自治体や民間のオープンデータ）を活用すれば同様の仕組みで駅・バス・運行情報を表示可能。

このプロジェクトは古いハードの再活用、低コストな情報端末作りに最適です。興味があれば、実際のKUALスクリプトやHTMLテンプレート、wkhtmltoimageのcron設定例も用意しますか？
