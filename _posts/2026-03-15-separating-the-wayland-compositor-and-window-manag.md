---
layout: post
title: "Separating the Wayland Compositor and Window Manager - Waylandコンポジタとウィンドウマネージャの分離"
date: 2026-03-15T14:37:12.166Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://isaacfreund.com/blog/river-window-management/"
source_title: "Separating the Wayland Compositor and Window Manager"
source_id: 988099033
excerpt: "riverの分離プロトコルで低遅延かつ手軽にWayland用WMを開発可能に"
---

# Separating the Wayland Compositor and Window Manager - Waylandコンポジタとウィンドウマネージャの分離
Waylandを“分離”して軽くする——window managerを切り出したriverの挑戦

## 要約
Waylandの従来の実装はコンポジタとウィンドウマネージャを一体化していたが、river 0.4.0でそれらを別プロセスに分離するプロトコル（river-window-management-v1）が登場し、ウィンドウ管理の実装を大幅に簡素化した。

## この記事を読むべき理由
日本のデスクトップ開発者や軽量環境好きにとって、Wayland上で多様なウィンドウマネージャを手軽に作れるようになることは、カスタムUXの実現や開発・デバッグコスト削減に直結するため必読です。

## 詳細解説
- 役割の整理  
  - Display Server：カーネルからの入力と表示バッファの仲介  
  - Compositor：各ウィンドウのバッファを合成して出力  
  - Window Manager：ウィンドウ配置やキーバインドなどポリシー決定  
  X11ではこれらが分離されすぎて往復が多く遅延を生み、従来のWaylandはDisplay ServerとCompositorを統合して遅延を解消してきた。

- riverのアプローチ  
  - river-window-management-v1は「コンポジタは描画と同期を担当」「ウィンドウマネージャはポリシーだけを担当」という明確な分離を実現。  
  - 描画遅延（input latency）を悪化させないため、毎フレームや毎イベントのラウンドトリップを強制しない設計。

- フレーム・パーフェクション（frame perfection）  
  - 新しいウィンドウを既存のタイルレイアウトに組み込む際など、ユーザーに破綻した中間フレームを見せないため、必要なバッファ更新を待って「原子的に」描画状態を切り替える仕組みを採用。遅延が過ぎる場合は短いタイムアウトで妥協する運用。

- 状態機械（manage/render sequences）  
  - ウィンドウ管理状態（サイズ、フォーカス、キーバインド等）とレンダリング状態（位置、重なり順、装飾等）を分離し、各種変更はそれぞれのシーケンス中にバッチで適用。これにより不要な起床や往復を減らし、フレーム完璧性を保つ。

- 利点と制約  
  - 利点：ウィンドウマネージャ作成の敷居が低下、言語選択の自由度（GC言語でも問題になりにくい）、クラッシュ時の耐性、既存のriver対応WMが増加中。  
  - 制約：VRや極端な3D/特殊効果のような非2Dパラダイムには非対応。複雑な描画制御には拡張が必要。

## 実践ポイント
- 今すぐ試す：river 0.4.0と既存のriver対応ウィンドウマネージャを組み合わせて試用してみる。  
- 開発ハンドル：まずはウィンドウ管理ロジックのみを実装し、描画はriverに委ねると開発コストが劇的に下がる。  
- 言語選定：高速なレスポンスが要るコンポジタは低レベル言語、ウィンドウマネージャは高レベル言語（例：Rust/Go/高級GC言語）で素早く実験可能。  
- コミュニティ参加：対応が足りないユースケースはissueを上げてプロトコル拡張を検討してもらうと良い。  

短く言えば、riverの分離アプローチは「Waylandで多様なウィンドウマネージャを簡単に作り、使い分けられる未来」を現実にしつつあり、日本のカスタムデスクトップ文化にも追い風となるはずです。
