---
layout: post
title: "Built a real-time vessel tracker using H3 hexagonal spatial indexing for proximity detection - H3 六角形空間インデックスで作るリアルタイム船舶トラッカー"
date: 2026-01-11T00:28:28.533Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev-jeb.com/deliberate/portal/showcase/ocean-terminal-vessel-tracker"
source_title: "Showcase - Projects Built with Deliberate API | Deliberate API"
source_id: 465956195
excerpt: "H3で港周辺の船舶を100m単位でリアルタイム検出し、入出港管理や災害対応に活かす方法を解説"
image: "https://dev-jeb.com/deliberate/portal/favicon.png"
---

# Built a real-time vessel tracker using H3 hexagonal spatial indexing for proximity detection - H3 六角形空間インデックスで作るリアルタイム船舶トラッカー
魅力的なタイトル: 港に近づく船を100m単位で追う──H3で軽快に実装するリアルタイム船舶モニタ

## 要約
米国の海上ターミナル付近をAISストリームで監視し、H3（六角形）空間インデックスを用いたwithin_radiusフィルタで「端末から100m以内」の船舶をリアルタイム検出するシステムの紹介。Deliberate APIとWebSocketで更新を受け、端末→親ポートの関係情報でマッピングして表示する。

## この記事を読むべき理由
港湾や海上輸送は日本経済に直結する分野であり、リアルタイム追跡は入出港管理、埠頭混雑予測、災害対応、物流可視化に役立つ。H3のような効率的な空間インデックスを使えば、大量のAISデータを低レイテンシで処理できるため、実運用に近い実装例として学ぶ価値が高い。

## 詳細解説
- 全体の流れ
  - サーバは Deliberate API を使って「海上ターミナル（ocean_terminal）」タグのついた全米の端末境界または位置データを取得。
  - AISデータはWebSocketのストリームで受信（各船舶の緯度経度を含む更新が流れる）。
  - 各船舶更新ごとに Deliberate API に対して within_radius（半径100m）クエリを投げ、近接する端末を検出。
  - 検出された端末を、その親である「ポート」に紐付けて地図表示やアラート生成を行う。

- 技術の肝：H3（六角形空間インデックス）
  - H3は地球表面を階層的な六角形セルに分割するライブラリ。点近傍検索やセル間集合演算が速いのが特徴で、円形近傍を近似する用途に適している。
  - within_radiusフィルタは H3 を内部で使い、指定距離内のオブジェクト候補を効率的に絞り込む。これにより、毎秒大量のAIS更新を受けても応答性を維持できる。
  - 実務上は境界線上の誤差やAISのノイズ（位置のスパイク）への対策が必要。ヒステリシス（入／退出閾値を少し広げる）、移動平均や速度ベースのフィルタを併用すると良い。

- データ設計とAPI例
  - 検索クエリ例（船舶緯度経度を入れて端末を検索）:

  ```json
  {
    "where": {
      "tags": { "contains": "ocean_terminal" },
      "spatial": {
        "within_radius": {
          "lat": ship.latitude,
          "lng": ship.longitude,
          "radius_meters": 100
        }
      }
    },
    "limit": 10
  }
  ```

  - "limit"で候補数を抑え、応答時間とコストを制御する。結果に含まれる関係データを使って端末→親ポートを復元する。

- 運用上の注意
  - AISは受信環境や端末の送信頻度で更新間隔がまちまち。短時間で過剰にAPIを叩かない工夫（バッチ化、位置変化量閾値の導入）が必要。
  - 100mという閾値は端末の物理的境界と用途に依存。計測単位の感覚として $1^\circ \approx 111\,\mathrm{km}$ を覚えておくと、緯度経度でのスケール感が掴みやすい。
  - 高頻度処理時のスケーリング：WebSocketのパーティショニング、ワーカーによる並列処理、H3セルキャッシュの活用など。

## 実践ポイント
- 小さく始める
  - まずは特定の港1つを対象にWebSocket経由でAIS更新を受け、within_radiusクエリを叩くPoCを作る。
- ノイズ対策
  - 位置が短時間で振れる場合は、速度（knots）と進行方向を使ったフィルタで誤検出を削減する。
- 可視化
  - 地図（LeafletやMapbox）で端末ポリゴンとH3セルを重ねると、検出ロジックの挙動が理解しやすい。
- 日本向け応用案
  - 港湾管理（入出港スケジュールの精緻化）、漁業管理（保護海域の侵入検出）、災害時の緊急対応（避難・迂回情報）のリアルタイム提供。
- 性能チューニング
  - API呼び出し回数を減らすために、船舶が移動した距離が閾値を超えたときだけクエリを発行する、または複数更新をバッチ処理する。

以上を踏まえれば、H3を中核にした近接検出は、日本の港湾・物流分野でも低レイテンシかつスケーラブルに実装可能。まずは小さな港でPoCを回し、AIS特性に合わせた閾値調整とノイズ対策を進めると良い。
