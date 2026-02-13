---
layout: post
title: "Implementing Auto Tiling with Just 5 Tiles - たった5枚のタイルで実現するオートタイル"
date: 2026-02-13T14:43:51.019Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.kyledunbar.dev/2026/02/05/Implementing-auto-tiling-with-just-5-tiles.html"
source_title: "Implementing Auto Tiling With Just 5 Tiles - Kyle Dunbar’s Blog"
source_id: 46930461
excerpt: "5枚の基本タイルを回転・反転で組合せ、Godotで自動境界処理とランタイム保存まで実装する手順を解説"
---

# Implementing Auto Tiling with Just 5 Tiles - たった5枚のタイルで実現するオートタイル
魅力的なタイトル: 5枚だけで描ける！シンプル＆高速なオートタイルの作り方（Godot対応）

## 要約
物理（当たり判定）タイルと表示タイルを分離し、表示タイルをタイルの角で塗ることで4ビット（16パターン）を表現。5種類の基本タイルを回転・反転で組み合わせてオートタイルを実現する手法の紹介。

## この記事を読むべき理由
- タイルセットを最小化しつつ見栄えの良いエッジを自動生成できるため、インディーやプロトタイプ作成で工数を大幅に削減できる。
- Godotユーザー向けに実運用（ランタイムでの保存→エディタ反映）までの流れが実装可能で、ワークフロー改善に直結する。

## 詳細解説
- 基本アイデア  
  - 2つのTileMapを用意：1つは物理（collider）用、もう1つは表示用。  
  - 表示TileMapを物理タイルから-0.5タイル分オフセットして描画し、表示タイルを「角（四分円的）」で塗ることで、隣接情報を4ビットのマスク（上右下左ではなくタイルの“角”）で表現する。  
  - 4ビットで16通り。これを5つのベースピース（コーナー／サイド／反対コーナー／内向きコーナー／全塗り）を回転・反転して組み合わせれば全パターンをカバーできる。  

- 実装上のポイント  
  - 各表示セルのどの四分割を埋めるかは、物理タイルの近隣（およびその近隣）を参照して決定。角の扱いは「物理で左下にあるなら、表示では右上の四分割を置く」等の逆転規則に注意。  
  - 16パターンを配列に順序（ビットマスク順）で格納し、マスク値をインデックスにして表示タイルの座標＋回転情報を引く設計が扱いやすい。例：  
```gdscript
# GDScript（例）: マスクをインデックスにしてタイル情報を参照
var visual_table = [
	# index 0..15 に対応するタイル情報（atlas座標＋回転）
	{atlas: Vector2(4,0), rot: 0}, # 0000
	{atlas: Vector2(0,3), rot: 0}, # 0001 ...
]
func place_visual_at(pos):
	var mask = compute_corner_mask(pos) # 0..15 を返す
	var info = visual_table[mask]
	visual_tilemap.set_cellv(pos, info.atlas, true, false, info.rot)
```

- ランタイム操作と保存  
  - マウス入力で物理タイルをON/OFFし、それに応じて周囲4セルの表示を再配置。全更新ボタン（update_all）を用意するとワークフローが楽。  
  - Godotではランタイム保存は user:// に行い、後でEditorPluginを使って user:// のデータを読み込み res://（シーン）を上書きしてエディタに反映する。Inspectorに「Import」ボタンを置くと自然。

## 実践ポイント
- 最初は小さなタイルセット（5枚）で試し、回転・反転でどのパターンが作れるかを確認する。  
- visual のオフセット（-0.5）と角のマスク計算を図で整理してから実装するとバグを減らせる。  
- 配列（16要素）はビットマスク順（0..15）に揃えること。順序がずれると表示が崩れる。  
- Godotではランタイムは user://、エディタ反映は EditorPlugin＋InspectorPlugin を組み合わせると自然なワークフローになる。  
- 参考にすると良い外部リソース：Nonsensical 2D の動画、元記事の作者のGitHubや実装コード。

---  
元記事: "Implementing Auto Tiling with Just 5 Tiles"（Kyle Dunbar） — 詳細実装やサンプルコードは元記事/作者のGitHubを参照してください。
