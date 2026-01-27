---
layout: post
title: "How I built a collaborative editing model that's entirely P2P - 完全P2Pで作った協調編集モデルのつくり方"
date: 2026-01-27T01:50:32.502Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.kevinmake.com/writings/p2p-realtime-collaboration"
source_title: "You might not need a sync server for real-time collaboration"
source_id: 416634705
excerpt: "軽量シグナリング＋P2Pで即時感と整合性を両立する協調編集の実践ガイド"
image: "https://www.kevinmake.com/multiplayer-games-preview.jpg"
---

# How I built a collaborative editing model that's entirely P2P - 完全P2Pで作った協調編集モデルのつくり方
サーバ不要で遊べる！ブラウザ同士だけで同期する“軽量リアルタイム協調”の実例と作り方

## 要約
WebRTCで軽いシグナリングだけ使い、同期サーバを排してブラウザ同士（P2P）で状態（state）と瞬時イベント（event）を組み合わせることで、カジュアルなリアルタイム協調体験を低コストで実現した事例。

## この記事を読むべき理由
日本でもリモート会議・ペアプログラミング・オンライン授業で“ちょっとインタラクティブ”な機能を手早く作りたいなら、重いコラボ基盤を導入せずに済む実践的なアーキテクチャとトレードオフが学べます。

## 詳細解説
- 基本アーキテクチャ  
  - 軽量シグナリングサーバでピア同士を接続（WebRTCのperfect negotiation）。接続後はブラウザ同士が直接通信（RTCDataChannel）。  
  - “ホスト＝権威（authoritative）”モデル：一方のピアをホスト（記事ではWebRTCのimpolite側を利用）にして状態の単一ソースにする。分散合意やサーバ同期を省ける。  

- 状態（state）とイベント（event）の二層モデル  
  - State：ゲームやキャンバスの確定した事実（例：体力、完成したストローク）。ホストが受け取ったアクションを検証して更新を全員に配布。  
  - Event：瞬時性のある一時的な情報（例：手の角度、ポインタ移動、音符の押下）。順序性はRTCDataChannelが保証するため、リアルタイム表現に最適。  
  - 両者を組み合わせることで「見た目は即時、整合性は後で確定」の体験を作れる。  

- 実例（記事のプロダクト）  
  - Sword Duel：体力や状態はstateで合意、スイング角やヒット演出はeventでストリーム。短い遅延とレスポンスを優先する設計。  
  - Draw Together：描画中はstrokeUpdateをeventで流し、筆を離したときにaddStrokeアクションでstateに確定。カーソル存在もeventで同期。  
  - WebRTCのRTCDataChannelは既定で順序配信されるため、イベントの順序管理が楽。  

- 限界とトレードオフ  
  - チート耐性なし：クライアントが送る有効なアクションは受理されるため、信頼できる相手向け（友人や授業）に適する。  
  - レイテンシーの矛盾：状態伝播の遅延で見た目と判定がズレる場面がある（防ぐには被打者を権威にする等の改良が必要だが往復遅延が増える）。  
  - ビデオを使うなら帯域の都合で2人向けに現実的（ビデオがなければ小グループでも応用可）。  

## 実践ポイント
- 必要なもの：WebRTC（シグナリング＋RTCDataChannel）、軽量シグナリングサーバ、クライアント側のstate管理ロジック、イベントストリーム処理。  
- ホスト決定：perfect negotiationでのimpolite/polite役割をホスト割当に流用すると実装が簡単。  
- 設計指針：  
  1. 共有すべき“事実”はstateで、瞬間表現はeventで分離する。  
  2. 小・低スループットの用途なら「ホストが勝つ」単純ルールで充分。  
  3. 再接続時はフルstate交換＋ID（更新番号）で優位側を採用すると復旧が簡単。  
  4. 即時性を優先するならローカル検証を許容、厳密性を優先するなら被検証側を権威にして往復確認を入れる。  
- 推奨ライブラリ／技術：MediaPipe（クライアント側の姿勢検出）、WebRTC（P2P通信）、Web Audio API（音の即時再生）。  

小規模でインタラクティブな協調体験なら、サーバを全部担保する前に「まずP2Pで試す」価値があります。導入コストが低く、プロトタイプや社内ツール、教育用途に向いています。
