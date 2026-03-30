---
layout: post
title: "Build123d: A Python CAD programming library - Build123d：Python製CADプログラミングライブラリ"
date: 2026-03-30T15:33:00.295Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/gumyr/build123d"
source_title: "GitHub - gumyr/build123d: A python CAD programming library · GitHub"
source_id: 47567242
excerpt: "PythonでCAD設計を自動化、STEP/STL出力で即実用化できるbuild123d"
image: "https://opengraph.githubassets.com/e8d905af8bdecc1e5635285c881a3b127e2038606a865c6462b544d575934da8/gumyr/build123d"
---

# Build123d: A Python CAD programming library - Build123d：Python製CADプログラミングライブラリ
Pythonで設計を「コード化」する——設計の自動化と3D出力を手軽に始めるためのビルドツール

## 要約
build123dはOpen Cascade上に構築されたPython向けのB-Rep CADライブラリで、アルジェブラ的な記法と状態管理モードを備え、3DプリントやCNC向けの精密モデル作成をコードで行える。

## この記事を読むべき理由
日本のメーカー、ものづくりコミュニティ、プロトタイピング現場で「設計の自動化」と「CADデータ互換性」は重要課題。build123dはPythonで学習コストが低く、STEP/STLなどへ出力できるため実務やホビーで即戦力になる可能性が高い。

## 詳細解説
- 基盤と設計思想  
  - Open Cascade（高精度幾何カーネル）を下に持つB-Rep（境界表現）ライブラリ。  
  - 「CAD-as-code」を標榜し、PEP8等に準拠したPythonicなAPIで可読性を重視。  

- モードと操作スタイル  
  - Algebraモード：状態を極力持たない代数的な操作（演算子で形状を合成/変換）。例：obj += sub_obj。  
  - Builderモード：設計履歴風に状態を管理し、スケッチ→押し出し→加工を文脈的に記述できる。  

- 主要機能  
  - 1D/2D/3Dの明確なジオメトリクラス（Edge, Face, Solid 等）とShapeListによるセレクタ操作（面積・長さ・軸方向などでフィルタ）。  
  - 演算子駆動の直感的API（位置・回転・スケールの合成が簡潔）。  
  - 拡張性：Baseクラスを継承して再利用可能なパラメトリックオブジェクトを作成可能。  
  - 入出力：SVG/STEP/STL等のインポート・エクスポート対応でFreeCADやSolidWorks、スライサとの連携が容易。  

- 開発体験とツール連携  
  - VS Code向けのビューア（ocp_vscode）があり、コード→可視化→出力のワークフローが実用的。  
  - pipでインストール可能。活発に開発されておりコミュニティ貢献も歓迎。

## 実践ポイント
- まずはインストール（推奨）:
```python
# python
pip install build123d
pip install ocp_vscode
```
- 最短で試すサンプル:
```python
# python
from build123d import *
with BuildSketch():
    Rectangle(10, 5)
part = extrude(amount=2)
export_stl(part, "plate.stl")
```
- 日本市場での活用例: 3Dプリント用の治具自動生成、量産前のパラメトリック試作、CNC用STEP出力による製造連携。  
- 次の一手: ドキュメントとexamplesフォルダを読み、ocp_vscodeで視覚確認→STL/STEP出力→実機で検証。興味があればGitHubでIssueやPRで参加。
