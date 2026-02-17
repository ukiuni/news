---
layout: post
title: "Show HN: Cycast – High-performance radio streaming server written in Python - Cycast — 高性能なPython製インターネットラジオサーバ"
date: 2026-02-17T16:54:18.781Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/LukeB42/Cycast"
source_title: "GitHub - LukeB42/Cycast: A high-performance internet radio streaming server written in Python with Cython optimizations."
source_id: 47048790
excerpt: "Python+Cythonで手軽に低遅延な自宅/コミュニティ向けネットラジオを構築"
image: "https://opengraph.githubassets.com/60e06019a1a87ad3c2f109e6b406eb885d4f479e17b3f4a1adc2f539a8e28dd3/LukeB42/Cycast"
---

# Show HN: Cycast – High-performance radio streaming server written in Python - Cycast — 高性能なPython製インターネットラジオサーバ
Python×Cythonで「自宅／コミュニティ用」低遅延ネットラジオを手早く立ち上げる方法

## 要約
CycastはPythonで書かれ、Cythonでボトルネックをネイティブ化した高性能インターネットラジオサーバ。ライブ入力（Mixxx/VLC等）を受けつつ、DJ不在時はプレイリストにフォールバックする設計。

## この記事を読むべき理由
個人・コミュニティラジオや社内配信を低コストで立ち上げたい日本の開発者／音響担当者にとって、Pythonエコシステム内で比較的簡単に高負荷配信を試せる実装例は貴重。Cythonを使った実運用寄りの最適化手法や設定の実践知が学べる。

## 詳細解説
- アーキテクチャ
  - audio_buffer.pyx：ゼロコピーの円形バッファ（memcpyベース）で書き込み／読み出しを高速化。
  - stream_broadcaster.pyx：複数リスナーへの効率的ブロードキャスト（動的バッファ調整）。
  - cycast_server.py：ソース管理と切替ロジック（ライブ⇄プレイリスト）。
  - flask_app.py + Tornado：UI/APIはFlaskで実装し、Tornadoで高並列のHTTP配信を実現。
  - 設定はHCL（config.hcl）で人間に読みやすく管理。

- 動作フロー
  1. Mixxx/VLC等が source_port（デフォルト8000）に接続して音声を送信。
  2. 音声はCython円形バッファへ書き込まれ、別スレッドのブロードキャスタが読み出してリスナーへ配信（listen_port 8001）。
  3. ソース切断時はプレイリストフィーダが同じバッファへ書き込みフォールバック。

- パフォーマンス設計
  - Cythonでクリティカルパスをネイティブ化→3–5xの改善を報告。
  - 動的バッファ制御（buffer fillに応じてsleep値を変える）で安定性を確保。
  - chunk_sizeやbuffer sizeでトレードオフ（帯域／遅延／CPU）を調整。

- インストール／ビルドの流れ（要コンパイラ）
  - pip install -r requirements.txt
  - python setup.py build_ext --inplace

- 制限と用途
  - 趣味〜中規模の配信に最適。数百同時接続以上はIcecast/CDN＋負荷分散推奨。

## 実践ポイント
- クイック起動
  - 依存インストール、Cythonビルド後に: python cycast_server.py
- 主要設定（config.hcl）
  - server: host, source_port(8000), listen_port(8001), source_password
  - buffer.size_mb, playlist.directory, broadcaster.chunk_size, broadcaster.sleep_*、advanced.max_listeners
- チューニングTips
  - バッファ増（size_mb↑）でスタッタ回避、より大きなchunk_sizeでオーバーヘッド低減（ただし遅延↑）。
  - 本番はマルチコア・SSD・nginxリバースプロキシ＋/api/statsで監視。
  - Cythonビルド失敗時はCコンパイラ（gcc/xcode/MSVC）を確認。
- 日本での活用例
  - 地域コミュニティ放送、大学ラジオ、イベント会場のローカル配信、社内BGM配信のプロトタイプに最適。

シンプルに試して、パフォーマンス調整の手法を学びたい人に有用なリポジトリ。興味があればconfig.hclを用意して実際に音を流してみるのが早い。
