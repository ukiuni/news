---
layout: post
title: "CadQuery is an open-source Python library for building 3D CAD models - CadQueryは3D CADモデルを作るオープンソースのPythonライブラリ"
date: 2026-04-17T01:28:24.447Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cadquery.github.io/"
source_title: "CadQuery | Create parametric CAD models with Python"
source_id: 47772725
excerpt: "Pythonでパラメトリック設計を自動化し、3DモデルのCI出力や共有を実現するCadQuery。"
---

# CadQuery is an open-source Python library for building 3D CAD models - CadQueryは3D CADモデルを作るオープンソースのPythonライブラリ
魅力的タイトル: コードで設計する時代へ —— Pythonで描くパラメトリックCAD「CadQuery」のすゝめ

## 要約
CadQueryはPythonでパラメトリックな3D CADモデルを記述できるオープンソースライブラリで、GUIに頼らずコードで設計を自動化・共有・バージョン管理できます。

## この記事を読むべき理由
日本のものづくり現場やプロトタイプ開発、個人のメイカーズや教育現場では、設計の再現性・自動化・CI連携が重要です。CadQueryはそのニーズにマッチし、低コストで設計ワークフローをプログラム化できます。

## 詳細解説
- コードとしての設計: CadQueryは「設計をコードで記述」するアプローチを採ります。寸法や拘束を変数として扱えるため、パラメータを変えるだけで部品のバリエーションを自動生成できます。
- GUI不要で自動化向け: スクリプト実行でモデル生成が完結するため、CI/CDパイプラインやバッチ処理、生成系テストに組み込みやすいのが特徴です。設計履歴はGitで管理できます。
- 互換性と出力: 一般にCADカーネル（OpenCASCADEベース）を利用し、STEPやSTLなど汎用フォーマットへのエクスポートが可能なので、CAMや3Dプリント、他のCADソフトとの連携が容易です。
- エコシステム: ドキュメントやGitHubでのプロジェクト管理、エディタやサンプルが整備されており、学習リソースも豊富です。

## 実践ポイント
- まず公式ドキュメントのサンプルを動かす（ローカルでサンプル実行→出力ファイル確認）。
- 設計パラメータを変数化してテンプレート化し、複数バリエーションを自動生成する習慣をつける。
- Gitでスクリプトを管理し、CIで自動ビルド（STEP/STL出力）を導入する。
- 3DプリントやCAMに渡す際は必ずエクスポート形式（STL/STEP）と寸法精度を確認する。
- 日本の試作・中小製造業では、定型部品のカスタマイズ自動化や社内ライブラリ化で即効性のある効果が期待できます。

元記事・公式ドキュメントで最新の導入手順やAPI例を確認してから試してみてください。
