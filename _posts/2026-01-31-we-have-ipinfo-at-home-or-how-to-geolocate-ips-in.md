---
layout: post
title: "We have ipinfo at home or how to geolocate IPs in your CLI using latency - 自宅でできるipinfo風：レイテンシでCLIからIPの位置を割り出す方法"
date: 2026-01-31T12:39:28.387Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.globalping.io/we-have-ipinfo-at-home-or-how-to-geolocate-ips-in-your-cli-using-latency/"
source_title: "We have ipinfo at home or how to geolocate IPs in your CLI using latency"
source_id: 46834953
excerpt: "Globalpingと遅延測定でVPN偽装を見破り国・州・都市を特定する実践ツール解説"
image: "https://blog.globalping.io/content/images/2025/12/latency-based-ip-geo-location.png"
---

# We have ipinfo at home or how to geolocate IPs in your CLI using latency - 自宅でできるipinfo風：レイテンシでCLIからIPの位置を割り出す方法
CLIで“嘘のロケーション”を見破る！レイテンシだけで国・州・都市まで突き止める実験レポート

## 要約
Globalping の分散プローブ群を使い、ping/traceroute の遅延からIPの国・州・都市を推定するCLIツールを作った話。ipinfoが行う「大量プローブによる検証」を小規模に再現し、高い精度を出せることを示す。

## この記事を読むべき理由
VPNやプロキシが偽の登録情報（geofeeds）でロケーションを欺く時代、実際のレイテンシに基づく検証は信頼できる代替手段。日本のエンジニアや運用担当者にとって、CDNやトラフィックルーティング、セキュリティ・不正検知で実用的な手法だから。

## 詳細解説
- 背景：ipinfo は大量のプローブを世界に配置してレイテンシ/ホップ情報から実際の物理位置を推定している。多くのVPNは管理する国数を水増しせず、登録情報を偽ることで「その国のIP」に見せかけている。レイテンシ測定はこれを検出する有力な手段。
- Globalping：オープンソースでコンテナ運用できるコミュニティプローブ群（3000+）を使い、誰でもネットワーク測定（ping/traceroute）を実行可能。APIで任意のロケーション指定やランダムなプローブ選択ができる。
- アプローチ（ツールの流れ）：
  1. 単一IPを入力
  2. 大陸ごとに少数のプローブでping（大陸判定）
  3. 勝った大陸からさらに多数プローブで測定（国判定）
  4. 必要なら米国内は州レベル、最後に最短レイテンシのプローブの都市を採る（都市判定）
- 実装上の工夫：
  - ICMP pingはブロックされやすい → traceroute の最終ホップ遅延を利用（多くの経路で最終近傍は同国にあることが期待できる）。
  - TCP ping はポート依存で不安定。複数手法（ICMP/TCP/UDP）や最終数ホップを組み合わせると精度向上。
  - デフォルト設定は大陸判定に5プローブ、国判定に50プローブ（API制限に配慮）。より多くのプローブで精度は向上するがAPI制限やクレジット消費が増える。
- 精度と制約：
  - 中央ヨーロッパの自宅IPは容易に国判定（例：Poland 7.29 ms）。
  - 米国内は州レベルまで高精度（例：Florida 0.45 ms → Miami 推定）。
  - 都市レベルは近隣ハブを指す程度の精度。プローブ分布が薄い地域や島嶼部、カバレッジ不良地域では精度が落ちる。
  - 「magic field」による自動プローブ割当は国の網羅を保証しないため、国や州ごとの明示的なプローブ指定が必要な場合あり。
- API制限と運用：
  - 無認証：250テスト/時・1測定につき50プローブ制限（時期により変動）。認証トークンで500テスト/時まで拡張可能。プローブをホストするとクレジットが得られる。

## 実践ポイント
- 試す：geolocate $IP（まずは小さく試す）。--limit でプローブ数を調整（全フェーズに適用されるので注意）。
- 精度上げる：国ごと／州ごとにプローブを明示指定して各地から複数プローブを回す。特に米国は州ごとにプローブ数を変える（例：US 200、Canada 20、Mexico 10）。
- ブロック対策：ICMPがブロックされる環境では traceroute（最終ホップ）や複数プロトコルの組合せを試す。
- 実務活用例（日本向け）：
  - CDN 配置やエッジ選定の検証：接続先が偽装されていないかチェック。
  - 不正検知：VPNを使った地理的な詐称を識別してフィルタリング強化。
  - 障害切り分け：遅延経路からどの国・地域で遅延/断線が発生しているか推定。
- リソース：ツールはOSS（GitHub 上の geolocation-tool）。Globalping のプローブを自ホストしてクレジットを稼ぎ、より多くのテストを実行可能。

以上を踏まえ、まずは手元で数IPを試してみてください。特に日本発着のトラフィックやVPNの挙動を観察すると、思わぬ発見があるはずです。
