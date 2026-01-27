---
layout: post
title: "Parametric CAD in Rust - RustでのパラメトリックCAD"
date: 2026-01-27T21:41:35.365Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://campedersen.com/vcad"
source_title: "Parametric CAD in Rust - Cam Pedersen"
source_id: 46786196
excerpt: "Rust製vcadで設計をコード化し、STL出力・CI・AI連携で自動化"
image: "https://campedersen.com/og/vcad"
---

# Parametric CAD in Rust - RustでのパラメトリックCAD
もうGUIで延々クリックしない：Rustで「コードとしてのCAD」を始める — vcadで設計を型とテストで管理する

## 要約
Rust製の小さく堅牢なパラメトリックCADライブラリ「vcad」は、プリミティブ＋ブール演算で部品をコード化し、STL/GLB出力、CIテスト、AIエージェント連携までを視野に入れたワークフローを提供します。

## この記事を読むべき理由
クリック中心のGUIワークフローに疲れたプロトタイパーやロボット開発者、また設計の再現性・テスト・CIを重視するチームにとって、vcadはすぐに試せる代替案になり得ます。日本のものづくり現場でも「パラメータ一つで図面が更新される」価値は高いです。

## 詳細解説
- 基本思想：部品は名前付きジオメトリ。プリミティブ（立方体・円柱等）を作り、+（和）、-（差）、&（共通）でCSG（Constructive Solid Geometry）を組み立てます。演算子オーバーロードにより式が算術に近い直感を実現。
- コード例（要点）:
```rust
use vcad::{centered_cube, centered_cylinder, bolt_pattern};

let plate = centered_cube("plate", 120.0, 80.0, 5.0);
let bore = centered_cylinder("bore", 15.0, 10.0, 64);
let bolts = bolt_pattern(6, 50.0, 4.5, 10.0, 32);
let part = plate - bore - bolts;
part.write_stl("plate.stl").unwrap();
```
- エンジンの強み：マニフォールド（watertight）なメッシュ生成を担保する幾何コアを持ち、Rust側はゼロコスト抽象でラップ。GCやスクリプト層に伴う不確実性が少ない。
- ツールチェーン：cargo testで体積・表面積・ボックス等を自動検証、cargo clippyで静的チェック。設計をコードにすることでレビュー・CI・差分管理が可能。
- 出力と可視化：3D印刷向けSTL、PBR設定を含むglTF/GLB（TOMLでマテリアル定義）をサポート。
- エージェント連携：ドキュメントとレシピが揃っており、AIエージェント→vcadでジオメトリ生成→Blender MCPで自動レンダリング、という完全自動化ループを想定して設計されている点が特徴。

## 実践ポイント
- まずは導入：cargo add vcad、公式Docs（docs.rs/vcad）とGitHub（github.com/ecto/vcad）を確認。
- 小さく始める：中心の立方体/円柱を作って差し引きする例で、パラメータを変えてSTLを再生成する練習をする。
- CI化：単体テストで寸法・体積確認を自動化し、clippyをCIに入れておくと事故が減る。
- Blender連携：レンダリング確認を自動化すれば設計レビューが迅速化。日本のチームでは試作前の確認コスト削減に有効。
- 注意点：現状はフィレットやねじ山など高度な仕上げ機能は未実装（ロードマップに記載）。必要に応じて既存CADと組み合わせる運用を検討。

出典・導入先：vcad（MITライセンス）、Rustで設計をコード化して「クリック」から「編集→再生成」へ移行したい開発者におすすめ。
