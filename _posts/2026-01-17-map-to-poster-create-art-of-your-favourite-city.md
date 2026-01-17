---
layout: post
title: "Map To Poster – Create Art of your favourite city - お気に入りの街をポスターにするツール"
date: 2026-01-17T10:43:58.635Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/originalankur/maptoposter"
source_title: "GitHub - originalankur/maptoposter: Transform your favorite cities into beautiful, minimalist designs. MapToPoster lets you create and export visually striking map posters with code."
source_id: 46656834
excerpt: "OpenStreetMapとPythonで、自分の街を美しいミニマルポスターに自動生成"
image: "https://opengraph.githubassets.com/0230c9c219f6bb27fb867a4430f4af0a7ba95a4a1aeb6ac7035f44d68e6f43e5/originalankur/maptoposter"
---

# Map To Poster – Create Art of your favourite city - お気に入りの街をポスターにするツール
あなたの街が一枚のミニマルなアートに変わる — コードで作る地図ポスターのススメ

## 要約
MapToPosterはOpenStreetMapデータを使い、Pythonで美しいミニマルな都市ポスターを自動生成するツール。テーマや半径を指定して、好きな街のビジュアルポスターを出力できる。

## この記事を読むべき理由
地図データをただ見るだけでなく、デザイナー的に再利用したい開発者や、地域ブランディングやオフィス装飾に使える都市アートを手早く作りたい日本のエンジニア／デザイナーに直結する実用ツールだから。

## 詳細解説
- 全体像  
  - CLI（argparse）で都市名・国名・テーマ・距離（半径）を指定すると、Nominatimで緯度経度を取得、OSMnxで道路・公園・水域などを取得し、matplotlibでレンダリングしてPNGを出力する流れ。
  - 出力先は posters/ に {city}_{theme}_{YYYYMMDD_HHMMSS}.png で保存。ライセンスはMIT。

- 主要コンポーネント  
  - ジオコーディング: Nominatim（地名→座標）  
  - データ取得: OSMnx（OSMの道路・ポリゴン・建物など）  
  - 描画: matplotlib（レイヤー順やテキスト配置を細かく制御）  
  - テーマ: themes/ にあるJSONで色や線幅を指定。fonts/ にフォント（例：Roboto）を置いて文字装飾。

- テーマとレンダリングの仕組み  
  - テーマJSONで背景色、道路カテゴリごとの色や水域、公園の色などを定義。17種類のプリセットが同梱（例：japanese_ink、noir、sunsetなど）。  
  - 道路はOSMのhighwayタグに応じて線幅と色を割り当て（motorway → 太く、residential → 細く）。  
  - レイヤーのZ順: 背景 → 水域 → 公園 → 道路 → グラデーション → テキスト。これにより視認性の高いミニマル表現が可能。

- 拡張ポイント（開発者向け）  
  - 新しい地物（鉄道など）を追加するには、OSMnxの features_from_point を使い、テーマJSONに色キー（"railway" など）を追加して描画すればOK。  
  - get_coordinates() を差し替えれば別のジオコーディングサービスにも対応可能。

- パフォーマンスと注意点  
  - 大きな半径（20km超）はダウンロード遅延とメモリ消費が増大。ネットワーク制限やNominatimのレート制限に注意。座標のローカルキャッシュを推奨。  
  - プレビュー用はdpiを300→150に落とすなどで高速化可能。network_type='drive' にすると道路のみ取得で速い。

## 実践ポイント
- 環境準備（Python仮想環境で実行推奨）
```bash
pip install -r requirements.txt
```
- まずは東京の中心で試す例（テーマ: japanese_ink、半径15km）
```bash
python create_map_poster.py -c "Tokyo" -C "Japan" -t japanese_ink -d 15000
```
- 小さな密集エリア（例：下町・歴史地区）は距離を4000–6000m、都心の全体像は10000–20000mを目安に。日本の狭く高密度な街路は短〜中距離が映える。
- カスタムテーマの最小例（themes/my_theme.json）
```json
{
  "name": "my_theme",
  "bg": "#0B0B0B",
  "text": "#FFFFFF",
  "water": "#1E90FF",
  "parks": "#2E8B57",
  "road_primary": "#FFD700",
  "road_residential": "#555555"
}
```
ファイルを themes/ に置けば --theme my_theme で使える。

- 拡張例：鉄道路線を描画したい場合（create_poster内に追記）
```python
try:
    railways = ox.features_from_point(point, tags={'railway': 'rail'}, dist=dist)
except:
    railways = None
if railways is not None and not railways.empty:
    railways.plot(ax=ax, color=THEME['railway'], linewidth=0.5, zorder=2.5)
```
- 配布や商用利用: MITライセンスなので再配布や改変がしやすいが、OSMのデータ利用規約は守ること。

最後に一言：東京、京都、金沢、函館のような「街の骨格」が個性的な日本の都市こそ、MapToPosterで驚くほど映える。デザイン・土産物・社内インテリアに使える一枚を、まずは手元で生成してみてほしい。リポジトリ: https://github.com/originalankur/maptoposter
