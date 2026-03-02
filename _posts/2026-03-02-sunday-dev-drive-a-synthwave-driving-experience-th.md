---
layout: post
title: "Sunday DEV Drive: A Synthwave Driving Experience Through Your DEV Community Articles - Sunday DEV Drive：DEVコミュニティの記事がネオン看板になるシンセウェーブ・ドライブ体験"
date: 2026-03-02T19:54:48.288Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/georgekobaidze/sunday-dev-drive-a-synthwave-driving-experience-through-your-dev-community-articles-5032"
source_title: "Sunday DEV Drive: A Synthwave Driving Experience Through Your DEV Community Articles"
source_id: 3299096
excerpt: "DEV記事がネオン看板に変わる、Three.jsで作るシンセウェーブドライブ体験"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fyiwabw9dppqr1j1ehdx9.jpg"
---

# Sunday DEV Drive: A Synthwave Driving Experience Through Your DEV Community Articles - Sunday DEV Drive：DEVコミュニティの記事がネオン看板になるシンセウェーブ・ドライブ体験
週末に走らせたい、あなたの記事がネオンに輝く“デジタルドライブ”体験

## 要約
DEVの投稿をリアルタイムで取得して、記事タイトルや本文の抜粋をネオン看板として並べるブラウザ製のシンセウェーブ風ドライビング体験。技術的にはThree.js＋Canvas＋DEV APIで実現され、ビルボードはクリックで記事を開けます。

## この記事を読むべき理由
- 書いた記事を「景色」に変える発想は、技術発信の見せ方を再考させる。  
- Three.js＋CanvasでAPIデータを直に描画する実装は、初心者が学ぶべき実践的パターンが詰まっている。

## 詳細解説
- 全体スタック：Three.js（r170）、Vanilla JS（ESモジュール12個）、Canvas API、DEV API（認証不要）。ビルド不要で静的サーバーで動く。  
- 表示モード：自分の投稿を表示する「Your articles」、投稿が無ければ書くことを促す「Motivational」、アカウント無しで回せる「Test drive」。  
- 道の生成：手続き的（プロシージャル）道路。数セグメントごとにランダムな曲率（例：±0.042の範囲）と継続長（4–10セグメント）を選ぶことで、滑らかなカーブを生成。道路は200セグメント分のリボンメッシュとしてスライド再構築される。  
- ビルボード生成：Canvasで512×768や1024×512のテクスチャを描画。ヘッダー、カバー画像（非同期ロード）、抜粋、フッターを順に描く。画像が読み込まれたら tex.needsUpdate = true でGPUに再アップロード。カバー無しは遊び心ある代替表示に。  
- 抜粋抽出：DEV APIはMarkdownを返すため、コード・画像・リンク・見出しを削除し、60〜400文字の段落を選ぶパイプラインで読みやすい引用を生成。  
- API負荷対策：全投稿を深掘りするとリクエスト過多になるため、リストをシャッフルしてランダムに25件だけフルフェッチ。各リクエストに350msのウェイト、429はdescriptionでフォールバック。  
- 相互作用：Three.jsのレイキャストで看板クリックを検出し、userDataに格納したURLを開く。カメラ回転中の誤クリック防止あり。  
- 車と物理：車体はBox/Cylinderプリミティブを46個積み上げて構成。アクセルとブレーキ同時押しでは速度が8%に収束する「struggle」状態を導入し、滑らかな加速曲線は速度比に応じた減衰をかける実装。

## 実践ポイント
- まずデモを触る：sundaydevdrive.pilotronica.com で動作確認。  
- アイデアを応用：QiitaやZennなど日本のプラットフォーム向けに同様の「記事を景色にする」UIを作ればコミュニティ参加を促せる。  
- 再利用できる技術：
  - Three.js + Canvasで動的テクスチャを作る方法（tex.needsUpdateの扱い）。  
  - Markdown→抜粋のパイプライン（コード除去＋文字数フィルタ）。  
  - 手続き的道路生成の簡単実装（ランダム角度＋積分で滑らかに）。  
- 小さく始める：週末1日で「自分の投稿を表示するミニデモ」を作れば、API扱い・非同期画像処理・レイキャストなど実戦的なスキルが身につきます。
