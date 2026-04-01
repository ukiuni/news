---
layout: post
title: "Is BGP Safe Yet? No. Test Your ISP - BGPはもう安全か？いいえ。あなたのISPをテストしよう"
date: 2026-04-01T14:05:18.475Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://isbgpsafeyet.com/"
source_title: "Is BGP safe yet? · Cloudflare"
source_id: 47600382
excerpt: "BGPは未だハイジャック危機、ISPがRPKI/ROV対応か今すぐ確認を"
image: "https://isbgpsafeyet.com/resources/open-graph.png"
---

# Is BGP Safe Yet? No. Test Your ISP - BGPはもう安全か？いいえ。あなたのISPをテストしよう

今すぐ確認！あなたの回線はBGPハイジャックに無防備か？

## 要約
インターネットの経路選択を担うBGPは本質的に暗号化されておらず、経路の不正広告（ハイジャック）で大規模障害が起きる。RPKIとROVで「発信元の正当性検証」を行えば防げるが、ISPごとに対応状況が分かれるため自分の回線を確認する必要がある。

## この記事を読むべき理由
日本のサービスやユーザーもBGP経路汚染の影響を受けうる。NTTやIIJなど日本主要事業者の対応状況が異なる今、自社サービスや開発環境の可用性とセキュリティを守るために知っておくべき基礎知識と実務アクションを短時間で得られる。

## 詳細解説
- BGPの役割：AS間で最適経路を共有するプロトコル。設計上「誰でも経路を広告できる」ため、誤設定や悪意ある広告でトラフィックが別経路へ流れる（経路ハイジャック）。
- 問題点：経路の「正当な発信元」を検証する仕組みが標準ではないため、金融サービスやクラウド、CDNなどが被害に遭うリスクが常態化していた。
- 対策（RPKI + ROV）：
  - RPKI（Resource Public Key Infrastructure）：IPプレフィックスと正当なASを証明する署名インフラ。
  - ROV（Route Origin Validation）：受信したBGPルートのRPKI署名を検証し、無効なプレフィックスをフィルタまたは拒否する運用。
- 現状の展開（概要）：
  - 大手クラウド/キャリア（Google、Microsoft、Amazon、Cloudflare、Comcast、Verizon、NTTなど）はRPKI署名とROV導入が進んでいるため「安全」と表示されている事例が多い。
  - 一方で一部キャリアやピアで「部分導入」や未導入が残り、依然として経路汚染の窓口が存在する。
  - サイト「Is BGP Safe Yet?」は主要事業者のRPKI/ROV導入状況を可視化している（出典: isbgpsafeyet.com）。

## 実践ポイント
- 自分の回線（ASN）を調べる（例）：
```bash
curl -s https://ipinfo.io/org
```
- まず isbgpsafeyet.com で「Test your ISP」を実行して自分のISPの状態を確認する。
- 結果が「signed + filtering（safe）」ならROVで無効ルートを捨てている可能性が高い。部分導入や未導入ならISPにRPKI/ROV対応を問い合わせる。
- 自社ネットワーク運用者は：プレフィックス署名、RPKIバリデータ（例：Routinator 等）の導入、ルータでのROVフィルタの設定を検討する。
- 開発者/運用者は：重要サービスのマルチホーミングや監視（BGP経路変化アラート）を整備してリスクを低減する。

（参考：isbgpsafeyet.com の最新採用状況には大手キャリアやクラウド事業者の導入情報が逐次掲載されています。まずは自分のASNを確認してみてください。）
