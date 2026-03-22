---
layout: post
title: "Burrow - A gopher browser written in HTML - Burrow（HTMLで書かれたgopherブラウザ）"
date: 2026-03-22T05:03:29.073Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://burrow.din.gy/"
source_title: "Burrow"
source_id: 1396278190
excerpt: "HTMLだけで動くgopherブラウザでレトロWebを手軽に体験"
---

# Burrow - A gopher browser written in HTML - Burrow（HTMLで書かれたgopherブラウザ）
HTMLだけでゴーファーにアクセスできる！？Burrowで古き良きネットを覗く

## 要約
Burrowは「HTMLで書かれた」軽量なgopherブラウザで、シンプルなナビゲーション（Back / Forward / Home / Reload / Go）でレトロな情報プロトコルをブラウザ上で体験できます。

## この記事を読むべき理由
ゴーファーはHTTP以前の軽量プロトコルで、低帯域やシンプルな情報構造に強みがあります。Web開発者やレトロネット好き、日本の低帯域・IoT環境での応用を考える人に示唆を与えます。

## 詳細解説
- gopherとは：1990年代初頭に普及したテキスト中心のディレクトリ型プロトコル。メニューをたどるだけでコンテンツに到達する設計が特徴です。URLは通常 gopher:// で始まります。  
- Burrowの意義：タイトルどおり「HTMLで書かれた」ブラウザという点がポイント。ブラウザ上でgopherのUIを再現することで、既存のWeb技術でレトロプロトコルを簡単に体験・共有できます。ページにある「Back / Forward / Home / Reload / Go」は、gopherのメニュー型ナビゲーションを現代的なブラウザ操作にマッピングしたものです。  
- 実装の想像点：モダンブラウザは直接gopherスキームを扱わないことが多いため、Burrowはクライアント側でHTML/JavaScriptを使って表示を作り、必要に応じてサーバー側プロキシやフェッチ（HTTP経由でgopherを取りに行く仕組み）を使っている可能性が高いです。学習教材として、フロントエンドでのパースやナビゲーション管理の良い例になります。

## 実践ポイント
- まずBurrowのページを開き、表示ソースとDevToolsのネットワークタブを確認して仕組みを観察する。  
- 自分で簡単な「gopherビューア」をHTML+JavaScriptで作ってみる（メニューパース→リンク表示→簡易ナビ）。  
- 日本のレトロ好きコミュニティや低帯域環境向けサービスでの利用を検討する（テキスト配信や小規模ドキュメント配布に向く）。  
- gopherサーバーやgopherプロキシを立てて、ブラウザ側との連携を学ぶとネットワークプロトコル理解が深まる。
