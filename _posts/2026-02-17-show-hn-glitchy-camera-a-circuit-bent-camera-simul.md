---
layout: post
title: "Show HN: Glitchy camera – a circuit-bent camera simulator in the browser - ブラウザで動く「回路改造カメラ」シミュレータ"
date: 2026-02-17T12:27:56.577Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://glitchycam.com"
source_title: "Glitchy | Circuit bent camera"
source_id: 47033954
excerpt: "ブラウザだけで即グリッチ映像を生成し、写真は端末内で完結する回路改造カメラ体験"
image: "https://glitchycam.com/images/favicon.png"
---

# Show HN: Glitchy camera – a circuit-bent camera simulator in the browser - ブラウザで動く「回路改造カメラ」シミュレータ
ブラウザだけで“回路を改造した”ようなグリッチ（破損風）映像を即生成する、ローカル処理重視のプライバシーに配慮したカメラ体験

## 要約
Glitchy cameraは、Webブラウザ上でリアルタイムに「回路改造（circuit-bent）」風のグリッチエフェクトをカメラ映像に適用するツール。写真・動画は端末内で処理され、外部に送信されない点が明示されている。

## この記事を読むべき理由
日本でもプライバシー重視で手早くヴィジュアル表現を試したいクリエイターやフロントエンド開発者が増えています。本ツールは追加ソフト不要で試せ、エフェクトの技術的要素やローカル処理の実装アイデアが学べます。

## 詳細解説
- 基本挙動：ブラウザのカメラを起動して映像フレームを取得し、ピクセル操作や色チャネルのずらし、ノイズ注入、フレームフィードバックなどの処理を施して表示・保存する仕組み。サイト文言に「Your photos and video never leave your device. Everything is processed locally in the browser」とあるため、getUserMediaで取得した映像をサーバに送らずクライアント側で完結させている設計。
- 想定される技術要素：実装には通常 getUserMedia → <canvas>／WebGL（フラグメントシェーダ）でのピクセル処理、MediaRecorderでのローカル録画が使われることが多い。高負荷処理はWebGL（GPU）やWebAssemblyで最適化されることがある。UI上の「RG+TG Capture」などは色チャネル混合・シフトのプリセットを示すラベルと推測される。
- なぜ「回路改造」か：ハードウェアの回路改造(circuit-bending)で得られるランダムで破綻したノイズ／色ずれ／タイミング崩壊をソフト的に再現し、意図的なアーティファクトを作るアプローチ。リアルタイム性と操作性がポイント。

## 実践ポイント
- まずサイトを開いてカメラ権限を許可して試す（映像は端末内で完結）。  
- ブラウザ実装の学習：getUserMedia, canvas/WebGL, requestAnimationFrame, MediaRecorder を順に調べると理解が深まる。  
- パフォーマンス改善：解像度を下げる／WebGLシェーダを使う／WebWorkerで重い処理を分離する。  
- プロジェクト応用例：SNS用の短尺グリッチ動画作成、Webアート作品、UIのアクセント演出。  
- セキュリティ：ローカル処理とはいえカメラ権限は慎重に扱い、ソースを確認して不審な挙動がないか確認する。

興味があればサイト（https://glitchycam.com）を開いて実際に操作してみてください。
