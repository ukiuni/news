---
layout: post
title: "Firefox & Linux in 2025 - Firefox と Linux（2025年）の状況"
date: 2026-01-23T19:12:36.485Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mastransky.wordpress.com/2026/01/23/firefox-linux-in-2025/"
source_title: "Firefox &amp; Linux in 2025 &#8211; Martin Stransky&#039;s Blog"
source_id: 784918635
excerpt: "Wayland上のFirefoxがHDR・分数スケール・非同期描画で動画品質と省電力を大幅改善"
image: "https://mastransky.wordpress.com/wp-content/uploads/2026/01/screenshot-from-2026-01-23-13-23-54.png"
---

# Firefox & Linux in 2025 - Firefox と Linux（2025年）の状況
魅力的タイトル: 「LinuxでFirefoxが変わる：HDR・高DPI・高速描画で動画もバッテリーも賢くなる」

## 要約
Firefox が Wayland 環境で大幅に進化し、HDR動画再生、分数スケール対応、非同期描画などが実用段階に入ってきた。これらは表示品質と電力効率、安定性を同時に向上させる変更群です。

## この記事を読むべき理由
日本でもGNOME（Mutter）やKDE（KWin）を使う開発者・クリエイター、HiDPIノートPCやHDR対応ディスプレイを持つユーザーにとって、ブラウザでの動画体験やバッテリー挙動が直に改善されるからです。特にストリーミング品質や省電力は実用面での恩恵が大きいです。

## 詳細解説
- HDR再生
  - Wayland側のHDRサポート（Bug 1642854）を利用し、Firefoxは「composited/native rendering」でアプリの一部レイヤー（動画フレーム）を直接コンポジタに渡す方式を実装。これにより動画はGPUでデコード→wl_bufferやdmabufで直接出力（ゼロコピー）され、フルスクリーン時はmpvに近い低消費電力再生が可能になります。
  - 色空間はBT.2020＋PQ、10bitベクトルを用い、ハードウェアデコードはVP9 v2が必要。ソフトデコードからdmabufへ直接アップロードするフォールバックも用意。
  - 有効化は最新のWaylandコンポジタで about:config の gfx.wayland.hdr（または強制なら gfx.wayland.hdr.force-enabled）。

- 分数スケール（Fractional scale）
  - Firefox 147で、125%などの小数スケールに対するレンダリングとウィジェットサイズ処理を改善。ウィンドウ/サーフェスのサイズは「拡大は行うが縮小は避ける」方針で丸め誤差を抑制。
  - Waylandで明確な丸め規定がないため、Mutter/Sway向けにはStable roundingを採用、KWin向けは別実装。将来的には fractional-scale-v2 へ移行予定。

- 非同期描画（Asynchronous rendering）
  - これまでスケール変更やウィンドウの表示/非表示で描画パイプラインを再構築していたため同期コストやクラッシュ要因があったが、最近の改修（Firefox 149のNightly相当）で wp_viewport を使いサイズ不一致でのプロトコルエラーを回避。
  - ウィンドウ作成後にオフスクリーン用の wl_surface / wl_buffer / EGLWindow を準備しておき、表示時に subsurface として接続する手法で描画を途切れさせず高速化。Windows/macOSに近い挙動に近づいた。

- そのほか
  - 音声再生中は画面を暗くするがスリープを防ぐ（スクリーンロック更新）、Waylandオブジェクト管理の非同期化で安定性向上など。

## 実践ポイント
- 試したい人は最新のFirefox（Nightlyや最近のリリース）と、HDR対応のWaylandコンポジタ（最新の Mutter/KWin など）を用意。about:config で gfx.wayland.hdr を有効化してテスト。
- HDR再生はハードウェア（VP9 v2 対応）とドライバのサポートが必要。対応しない場合はソフトデコードのフォールバックを確認。
- HiDPI表示で文字やUIがぼやける場合は Firefox 147+ の分数スケール改善が有効。デスクトップ環境ごとの丸め差異があるので挙動を確認する（GNOME/KDE）。
- 問題が見つかったらバグ報告に協力すると開発が早まる（特にサブサーフェスのマッピング/アンマップ周りやバッテリー挙動の報告が有用）。

（参考：元記事は Martin Stransky による Wayland と Firefox の進捗報告）
