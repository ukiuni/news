---
layout: post
title: "Vandalizing My Own Wikipedia Experience: A 90s Cyberpunk GeoCities Makeover - 自分のWikipediaを“改造”して90年代サイバーパンクGeoCities風にした話"
date: 2026-03-22T14:42:52.328Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/googleai/vandalizing-my-own-wikipedia-experience-a-90s-cyberpunk-geocities-makeover-13ie"
source_title: "Vandalizing My Own Wikipedia Experience: A 90s Cyberpunk GeoCities Makeover - DEV Community"
source_id: 3377401
excerpt: "LLMで自分のWikipediaを90年代GeoCities風に派手改造した実験記"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fqexbekq4ov3mu4amt5q0.jpg"
---

# Vandalizing My Own Wikipedia Experience: A 90s Cyberpunk GeoCities Makeover - 自分のWikipediaを“改造”して90年代サイバーパンクGeoCities風にした話
魅惑のネオンでWikipediaをぶっ壊す—懐かしのGeoCities aestheticをLLMで再現した実験リポート

## 要約
著者がLLM（Gemini 3.1 Pro Preview）を使って、Wikipediaのユーザースクリプト（Special:MyPage/common.js と common.css）を自動生成し、90年代GeoCities風のピンク／シアン網目背景、Comic Sans見出し、スクロールするタイトル、光るマウストレイル、歩くドット猫隊などを実装した実験記。

## この記事を読むべき理由
- MediaWikiのカスタムスクリプトを使ったブラウザ体験改造の実例がわかる。  
- LLMにドキュメントを「文脈として与える」ことで誤情報（API hallucination）を防ぐ手法を学べる。  
- 初心者でも手を動かして楽しく学べる実践ポイントがある（編集場所、性能配慮、CSSアニメーションの使いどころ）。

## 詳細解説
- 背景: WikipediaはUIが機能的すぎるため、好みで見た目を変える需要がある。ユーザースクリプト（Special:MyPage/common.js, common.css）を使うと自分だけのスタイルにできる。  
- LLMグラウンディング: 単に「Wikipediaをピンクにして」というと誤った提案を返すことが多い。著者は「URL Context」機能で公式ドキュメント（Wikipedia:User_scripts）をモデルに与え、MediaWiki特有のグローバル（mw.loader.using, mw.util.addCSS 等）に沿った安全なスニペットを得た。  
- 主な実装ポイント:
  - マーキー見出し: #firstHeading を差し替え、タイトルを <marquee> で横／往復スクロールさせる（レガシーTAGの互換性を利用）。  
  - マウストレイル: mousemove に反応して絶対配置のスパンを追加。ただし毎フレーム出すとGPUを圧殺するため「タイムスタンプによるスロットリング（例: 40ms毎に生成）」を入れて負荷を制御。生成要素はアニメーションでフェードアウトし、タイムアウトで削除。  
  - 歩く猫アニメ: setIntervalではなくCSSハードウェア加速アニメーションを多用。ヘッダ固定コンテナ（pointer-events: none でクリック妨害を回避）に猫を並べ、横移動は全体のスライドアニメ、縦揺れ（歩行感）は短周期の translateY を与え、nth-child で位相ずらしをして群れ感を出す。  
- 性能と安全: MediaWikiのユーティリティ関数でCSS注入することで互換性と「安全な適用」を担保。大量DOM生成はスロットリング＋短命ノードで回避。

## 実践ポイント
- 手順概要:
  1. ログイン → Special:MyPage/common.js と common.css を編集する。  
  2. 公式ドキュメント（Wikipedia:User_scripts）をまず読む／参照する。  
  3. 生成コードを使う場合はモデルにドキュメントを渡してAPI呼び出しの正当性を確かめる。  
- パフォーマンス注意:
  - mousemove 等の頻発イベントはタイムスタンプや requestAnimationFrame で制御する。  
  - アニメーションは可能な限り CSS（GPU加速）で実装する。  
- UX配慮:
  - pointer-events: none を適切に使い、検索やリンク操作が阻害されないようにする。  
  - 他ユーザーに見せるつもりならローカルのみで試す（Personal scriptsは個人限定）。

短くまとめると、LLMをドキュメントで「地固め」して使えば、MediaWiki特有の環境でも実用的で派手なユーザースクリプトが比較的安全に作れる—ただし性能と操作性には注意。日本の開発者やダッシュボード運用者にも、自分好みのUI改造やLLM利用法の参考になる実験例です。
