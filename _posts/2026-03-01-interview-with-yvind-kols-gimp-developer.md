---
layout: post
title: "Interview with Øyvind Kolås, GIMP developer - Øyvind Kolås（GIMP開発者）へのインタビュー"
date: 2026-03-01T14:11:57.408Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.gimp.org/news/2026/02/22/%C3%B8yvind-kol%C3%A5s-interview-ww2017/"
source_title: "Interview with Øyvind Kolås, GIMP developer - GIMP"
source_id: 47168405
excerpt: "Pippinが語るGEGLの仕組みと非破壊編集でGIMPがどう変わるか"
image: "https://www.gimp.org/news/2026/02/22/øyvind-kolås-interview-ww2017//Øyvind_Kolås.jpg"
---

# Interview with Øyvind Kolås, GIMP developer - Øyvind Kolås（GIMP開発者）へのインタビュー
GIMPを劇的に変えた“Pippin”の仕事術：GEGLと非破壊編集をやさしく解説

## 要約
GEGL（画像処理のグラフエンジン）とbabl（色変換エンジン）のメンテナであるØyvind “Pippin” Kolåsが、GIMPへの関わり方、GEGLの設計思想、非破壊編集や今後の展望について語ったインタビューをわかりやすくまとめます。

## この記事を読むべき理由
GIMPは日本でも広く使われるフリーの画像編集ソフト。GEGLの仕組みを知ると、非破壊編集やプラグイン連携、将来の高速化・他アプリ連携の可能性が見えてきます。開発者の視点から実践的に学べます。

## 詳細解説
- GEGLとは：ノード（操作）をつなげる“データフロー型”の画像処理ライブラリ。色調整→フィルタ→合成といった処理をグラフで表現し、再利用や非破壊処理を実現する。
- bablとは：色変換や色空間処理を担うライブラリ。GEGLと組んで正確な色処理を行う。
- Øyvindの来歴：最初はGIMPの変形ツールの品質改善パッチ（スーパーサンプリングによるモアレ軽減）で関わり始め、以後GEGL/bablの主要開発者に。
- 非破壊編集：GEGLのグラフ構造でレイヤー処理やフィルタを“結果を書き換えずに”保持できるため、設定の変更やアニメーション（動画編集へ応用）に向く。UI設計と安定性の確保が課題。
- 性能と課題：対話的なプレビュー（ドラッグや色調整で10fps程度を目指す）やミップマップ問題、起動時のプラグイン/ファイルシステム負荷がボトルネック。将来的にはCPU/GPU実装の入れ替えや最適化で改善予定。
- 他技術との比較：GStreamerはストリーミング（動画再生）中心、GEGLは生成・合成（静止画／フレーム単位）向け。libvipsなどとのベンチ比較は条件次第で評価が変わる。
- ドキュメント/API：GObject introspection を使ったドキュメント表示や、コマンドラインツール・XML/JSONでのグラフ記述が利用可能。

## 実践ポイント
- まず触る：GEGLのコマンドラインツールで簡単なノードチェーンを試し、XML/JSONでのグラフ構築を学ぶ。
- 既存を読む：まず既存のGEGLフィルタやbablの実装を読み、そこから改変してみる（差分学習が最短）。
- 開発言語：公式はC/GObject中心。言語バインディングはあるが、最初はCかコマンドラインでの試行を推奨。
- パフォーマンス観察：対話的な操作での遅延を重視し、プロファイル→ミップマップ等の最適化を意識する。
- 応用例：GIMPだけでなく動画編集や他GUIアプリへの組込みを検討すると、機能の再利用性が広がる。

この記事を読んで、まずはGEGLのコマンドラインと既存フィルタを触ってみてください。GIMPの「中身」を知ると、ツール選びやプラグイン作成がぐっと楽になります。
