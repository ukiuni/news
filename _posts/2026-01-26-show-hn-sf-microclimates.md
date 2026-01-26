---
layout: post
title: "Show HN: SF Microclimates - SFのマイクロクライメイト（超局所天気）"
date: 2026-01-26T06:48:59.966Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/solo-founders/sf-microclimates"
source_title: "GitHub - solo-founders/sf-microclimates: Free hyperlocal weather API for 50 San Francisco neighborhoods. No API key required. Claude Code and Clawdbot Skills"
source_id: 46760927
excerpt: "3マイルで20°F差も、SFの50近隣を実測集約した無料APIで超局所天気を即確認"
image: "https://opengraph.githubassets.com/4d0160f4d94a1a525b1c3e2beae37bd25613fa058fd3178b67d8db91f8b8ad6c/solo-founders/sf-microclimates"
---

# Show HN: SF Microclimates - SFのマイクロクライメイト（超局所天気）
3マイルで20°F差？サンフランシスコの「本当に当たる」天気を返す無料API

## 要約
サンフランシスコ内の50の近隣区域ごとに、PurpleAirの実測センサーを集約してリアルタイムの局所天気を返す無料API。公開版はAPIキー不要で、Cloudflare Workers＋KVで高速応答・キャッシュされる。

## この記事を読むべき理由
都市の「マイクロクライメイト」は表示される街全体の気温では伝わらない。日本でも地域差の大きい都市（東京の湾岸と内陸、横浜・川崎など）で同様の課題があり、ローカルな天気データはUX改善や自動化に直結するから。

## 詳細解説
- データソース：PurpleAirの屋外センサー（location_type=0）を利用。150以上のセンサーを近隣ごとにグルーピングして平均を算出する。  
- アーキテクチャ：Cloudflare WorkersでAPIを公開。Cloudflare KVに結果をキャッシュ（デフォルト1時間）し、レート制限も導入。  
- エンドポイント：  
  - GET /sf-weather — 全50区のデータ  
  - GET /sf-weather/:neighborhood — 単一近隣区域  
  - GET /neighborhoods — 利用可能な近隣名一覧  
- レスポンス例（単一近隣）:
```bash
# bash
curl https://microclimates.solofounders.com/sf-weather/mission
# => {
#   "neighborhood":"mission",
#   "name":"Mission District",
#   "temp_f":58,
#   "humidity":52,
#   "sensor_count":8,
#   "updated":"2026-01-25T23:00:00.000Z"
# }
```
- 自前ホスティング：リポジトリをクローン → npm install → PurpleAir APIキー（開発者登録が必要）を設定 → wranglerでCloudflare KVネームスペース作成・シークレット登録 → wrangler deploy。主要設定は CACHE_TTL_SECONDS（キャッシュ秒）、RATE_LIMIT_PER_MINUTE。近隣の境界ボックスは src/index.ts 内の SF_NEIGHBORHOODS を編集して変更する。  
- ライセンス：MIT（商用利用や改変OK）

## 実践ポイント
- すぐ試す：curlで上記エンドポイントを叩くだけで局所天気が得られる。  
- ボット/エージェント連携：チャットボットやAIエージェントに「今ここは霧？」を判断させるコンテキストとして利用。  
- スマートホーム：ローカル温度で暖房や窓の自動制御をトリガー。  
- 他都市への展開：src/index.ts の近隣定義とPurpleAirの緯度経度フィルタを差し替えれば、東京／大阪などに簡単に移植可能。  
- 自ホスティング時はPurpleAir利用規約とAPIキー発行条件を確認すること。

この記事を読んで、まずは公開APIを叩いてみて、自分の地域版を作るアイデアを試してみてください。
