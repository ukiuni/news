---
  layout: post
  title: "Show HN: Offline tiles and routing and geocoding in one Docker Compose stack - Docker Composeでオフラインのタイル・ルーティング・ジオコーディングを一つのスタックに"
  date: 2026-01-03T16:28:18.871Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.corviont.com/"
  source_title: "Corviont - Offline maps &amp; routing in Docker"
  source_id: 46478061
  excerpt: "Docker Composeで完全オフライン地図・経路・ジオコーディングを現場で即導入"
  image: "https://unicorn-images.b-cdn.net/ac60ebeb-ae8b-40a6-987a-22530d3da0c1?optimizer=gif"
---

# Show HN: Offline tiles and routing and geocoding in one Docker Compose stack - Docker Composeでオフラインのタイル・ルーティング・ジオコーディングを一つのスタックに
Docker Composeで「完全オフライン地図スタック」を一発構築 — Corviontが現場のマップとルーティングを変える

## 要約
CorviontはMapLibre UI、PMTilesベクトルタイル、Valhallaルーティング、SQLiteベースのジオコーディングをDocker Composeで一つにまとめ、ネットワークが不安定な現場でも完全にローカルで地図・経路検索・住所検索を提供するスタックを提供する。

## この記事を読むべき理由
日本は離島や山間部、災害時の通信途絶、工場・プライベートネットワークなど「常時オンラインでない」ユースケースが多い。オンプレ／エッジで動く地図とルーティングを手早く試せるCorviontは、モビリティ、物流、現場運用、プライバシー重視のシステム設計に即戦力となる。

## 詳細解説
- アーキテクチャ
  - MapLibre UI：ブラウザ側フロントエンド例を同梱。自前のフロントエンドからHTTPエンドポイントへ直接アクセス可能。
  - ベクトルタイル（PMTiles）：MonacoデモはPMTiles一ファイルで配信。外部タイルサーバを不要にする軽量配信形式。
  - ルーティング（Valhalla）：コンテナ化されたValhallaがHTTP APIを提供。オフラインで任意点間の経路計算が可能。
  - ジオコーディング（SQLite + Nominatimデータ）：Nominatim由来データをSQLiteに落とし、前方／逆ジオコーディングを軽量APIで提供。
- デプロイ形態
  - Docker Composeでローカルやエッジ機器に導入。将来的にはK3s/Kubernetes、Portainer、Menderなどのエッジ運用向け統合も想定。
- 運用・更新
  - ローカルマップアップデータ（今後）：差分や新バンドルの取得・検証・切替をダウンタイムなしで行うサービスを計画。
- 法務・ライセンス
  - コアはオープンソース（Valhalla、MapLibre）、地図データはOpenStreetMap（ODbL 1.0）。UI上に適切な帰属表示を行う設計。
- 料金モデル（予定）
  - リージョン単位でビルドを優先しつつ、最終的にはデバイス単位のライセンスモデルを想定（リクエストや経路ごとの課金はなしの方針）。
- 現状の利用方法
  - Monacoデモで動作確認可能。必要な地域が無ければサイトからリクエストして優先的にビルドを依頼できる。

## 実践ポイント
- まず触る：Monacoのデモをローカルで起動して、MapLibre→Valhalla→ジオコーディングの流れを確認する。既存のフロントエンドはそのまま接続可能。
- 日本での導入候補
  - 離島・山間部での物流ルーティング、災害時の指揮通信、工場や港湾など閉域ネットワークでの位置情報処理、車載ユニットや一時拠点でのオフライン地図。
- 運用設計
  - 地図更新ポリシー（どの頻度でバンドルを配るか）、ディスク容量（PMTilesとSQLiteのサイズ）、バックアップと検証プロセスを事前に決める。
- 法務チェック
  - OSMのODbL準拠とUIへの帰属表示を確認。社内で地図データを加工する場合の再配布条件にも注意する。
- 導入相談
  - 特定地域や大規模フリートでの導入は、Corviontに地域リクエストを提出して優先対応を依頼するとスムーズ（メール送付での依頼も可）。

短時間で「ローカルで完結する地図＋経路＋検索」を検証したいエンジニアやプロダクト担当にとって、CorviontのDocker Composeスタックは実運用レベルの出発点になる。日本の現場要件（通信不安定、閉域運用、プライバシー重視）と親和性が高く、PoCから本番導入までのロードマップが見えやすい。
