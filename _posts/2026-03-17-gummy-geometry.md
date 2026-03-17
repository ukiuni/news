---
layout: post
title: "Gummy Geometry - グミのように変形するジオメトリ"
date: 2026-03-17T12:11:00.235Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://newkrok.github.io/nape-js/examples.html?open=soft-body&mode=3d&outline=0"
source_title: "nape-js — Examples"
source_id: 47368660
excerpt: "ブラウザで触れるグミ状ソフトボディをリアルタイムで操作・共有できるデモ"
image: "https://newkrok.github.io/nape-js/logo.svg"
---

# Gummy Geometry - グミのように変形するジオメトリ
触って遊べる！ブラウザで動く「グミ状」ソフトボディ物理シミュレーション

## 要約
ブラウザ上で動くソフトボディ（変形する物体）のデモ「Gummy Geometry」を紹介。nape-jsを使ったリアルタイム物理挙動とマルチプレイヤー／サーバー主導シミュレーションの考え方が体験できる。

## この記事を読むべき理由
インタラクティブなウェブ体験やブラウザゲーム、教育コンテンツを作るなら、軽量で触って楽しいソフトボディ物理は強力な表現手段。日本のWeb／モバイル向けプロトタイプ作成やUX実験に即役立ちます。

## 詳細解説
- 元はHaxeで書かれたエンジン（Luca Deltodesco）をJSにコンパイル（Andrew Bradley）、さらにTypeScriptラッパー（Istvan Krisztian Somoracz）で扱いやすくしたのがnape-jsの系譜。MITライセンスで商用利用もしやすい点が魅力。
- 「Gummy Geometry」デモはソフトボディ（soft-body）を粒子＋ばね（particles & springs）や拘束（constraints）で表現し、衝突判定と数値積分で安定して動作させている。ユーザーはキャンバスをタップ／ドラッグして変形や力を与えられるため、入力→物理→レンダリングの一連がブラウザ内で完結する。
- マルチプレイヤー面では「サーバー主導（server-authoritative）」の考えが示されており、クライアントの不正を防ぎつつ、位置や力の同期で複数プレイヤーが同一世界を共有する実装パターンが使われる。通信は通常WebSocket等で状態や入力を送受信する設計になる。
- 実装上のポイント：ソフトボディは粒子数と拘束数でコストが増えるため、解像度調整や固定タイムステップ、衝突解決の反復回数をチューニングすることが重要。重い計算はWeb Workerやサーバーにオフロードするとレスポンスが良くなる。

## 実践ポイント
- デモを触って挙動を観察する（キャンバスをタップ／ドラッグ）。挙動から必要な精度・負荷感を確認する。  
- nape-js（TypeScriptラッパー）はMITなので、プロトタイプや商用プロジェクトの導入ハードルが低い。  
- パフォーマンス対策：粒子数削減、固定タイムステップ、衝突反復回数の制御、重い処理はWorker/WASMへ移行。  
- マルチプレイヤーを狙うならサーバー主導の同期を検討（ラグや不正対策に有効）。  
- 日本のWeb制作やゲーム開発で試作→ユーザーテスト→製品化の流れに組み込みやすい技術スタック。

元デモ（試せるページ）：https://newkrok.github.io/nape-js/examples.html?open=soft-body&mode=3d&outline=0
