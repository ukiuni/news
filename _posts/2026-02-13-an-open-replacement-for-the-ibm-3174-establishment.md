---
layout: post
title: "An open replacement for the IBM 3174 Establishment Controller - IBM 3174 エスタブリッシュメントコントローラのオープン代替"
date: 2026-02-13T16:54:21.247Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/lowobservable/oec"
source_title: "GitHub - lowobservable/oec: IBM 3270 terminal controller - IBM 3174 replacement"
source_id: 46926299
excerpt: "物理3270端末をHerculesへ実機検証できるオープンな3174代替oec"
image: "https://opengraph.githubassets.com/bd8ad813da10191cdaf17c2e363de1715d916aead63f3040ef2610abae50e356/lowobservable/oec"
---

# An open replacement for the IBM 3174 Establishment Controller - IBM 3174 エスタブリッシュメントコントローラのオープン代替
レガシー3270端末を現代につなぐ：オープン実装「oec」で物理端末をHerculesへ接続する

## 要約
oecはIBM 3174コントローラのオープン代替を目指すプロジェクトで、TN3270/TN3270EやVT100エミュレーションを提供し、実機3270端末をHerculesメインフレームエミュレータへ接続できるようにするツールです。

## この記事を読むべき理由
日本でも金融・製造・官公庁などで残るメインフレーム資産やレトロ端末を扱う現場・趣味層にとって、物理端末を現代環境に接続・検証する手段は貴重です。oecはオープンで手が入れやすく、保存・検証・開発に実用的な選択肢を提示します。

## 詳細解説
- 主な機能
  - TN3270/TN3270E（Extended Data Stream）対応、LU名交渉、基本的な3270端末ハンドリング
  - VT100エミュレーション（Windows上のサポートは限定的）
  - MLT（Multiple Logical Terminals）とIBM 3299マルチプレクサを用いた最大8端末の接続サポート（特定のインターフェースとファームウェアを要する）
- 対応端末
  - CUT（Control Unit Terminal）タイプに限定。テスト済み例：IBM 3179, 3278-2, 3472, 3483-V, Memorex 2078
  - キーマップ等、端末固有の調整が必要な場合あり
- 技術的要件
  - Python 3.8+
  - 物理インターフェース（例：interface2相当のデバイス）と対応ファームウェア
  - Hercules等のメインフレームエミュレータとの連携想定
- 開発状況
  - オープンソース（ISCライセンス）で進行中。完全な3174相当の機能は未実装だが、基本的な接続・エミュレーションは動作する
- 参考プロジェクト
  - coax（実機接続ツール）、pytn3270（Python TN3270ライブラリ）、5250向けの別プロジェクトなどと組み合わせ可能

## 実践ポイント
- 環境構築（例）
```bash
# Python 仮想環境作成（bash）
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- 実行例（デバイスが /dev/ttyACM0、ホスト名が mainframe の場合）
```bash
python -m oec /dev/ttyACM0 tn3270 mainframe
# VT100を使う例（/bin/sh をホストプロセスとして）
python -m oec /dev/ttyACM0 vt100 /bin/sh -l
```
- 注意点
  - 物理インターフェースの入手・ファームウェア確認が最重要（interface2互換等）
  - キーマップ調整や端末固有の挙動テストは必須
  - Windows上でのVT100は非推奨。Linux/macOSやCygwinでの動作検証を推奨
- 活用案
  - レガシー端末の保存・展示、Herculesでの現物検証、教育・デモ環境の構築、レガシー資産の段階的モダナイズ検証

元リポジトリ：https://github.com/lowobservable/oec  を参照し、READMEとコードを確認のうえ検証を進めてください。
