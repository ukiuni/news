---
layout: post
title: "We Synchronized Editing for Rec Room's Multiplayer Scripting System - Rec Roomのマルチプレイヤースクリプティングで編集を同期させた方法"
date: 2026-03-22T12:23:48.972Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.tyleo.com/blog/how-we-synchronized-editing-for-rec-rooms-multiplayer-scripting-system"
source_title: "How We Synchronized Editing for Rec Room&#x27;s Multiplayer Scripting System - tyleo.com"
source_id: 47476707
excerpt: "Redux風の単一状態＋アクションファネルで競合を排し、RPCとスナップショットで共同編集を高速同期"
image: "https://www.tyleo.com/img/how-we-synchronized-editing-for-rec-rooms-multiplayer-scripting-system-hero-de935adb.webp"
---

# We Synchronized Editing for Rec Room's Multiplayer Scripting System - Rec Roomのマルチプレイヤースクリプティングで編集を同期させた方法
リアルタイム共同制作を壊さない同期術：Circuits V2の「アクションファネル」で学ぶ

## 要約
Rec RoomのCircuits V2は、数千の個別オブジェクト同期で起きる複雑さを避け、アプリ全体を一つの状態（Reduxライク）として扱い、全ての操作を「アクション」として一箇所で処理することで、競合と不整合をほぼ排除した。

## この記事を読むべき理由
日本でも増えるリアルタイム共同編集、ユーザー生成コンテンツやマルチプレイ開発で「状態同期の破綻」を避けたい開発者・プロダクト責任者は、この単純で実務的な設計パターン（単一状態＋アクションファネル）が即戦力になる。

## 詳細解説
- 問題点（Circuits V1）
  - 各要素を個別のゲームオブジェクトで同期するとメモリ/CPUが爆発し、競合処理が散らばるため不整合検出・修正が困難に。
- 基本アイデア（Circuits V2）
  - アプリ全体を一つのインメモリ状態として持ち、状態変更は全て「Action」を通す。Reducerで純粋に状態遷移を決める（Redux風）。
- ネットワーク実装
  - ActionはProtocol Buffersなどでシリアライズして送信。
  - 全ての操作を単一RPC経路で流すことで処理経路を一元化。
  - 要点：ローカル即時反映 → 所有者（owner）に送信 → 所有者が全員へ転送 → 受信でローカル状態を上書き（シリアライズ可能隔離水準を実現）。
- 衝突回避と整合性
  - アクションが順序化されるため、並行性があっても結果は直列実行と同じになる（シリアライズ可能）。
- ジョイン時の追いつき（Join-in-Progress）
  - 定期的にInitialize（スナップショット）アクションを保存し、参加者はそれを基点に以降アクションを再生して同期。
- 大きなペイロード対策
  - 単一パスを活かし、送信前に圧縮（CompressIfOversized）→ 分割（SplitIfOversized）して再構成する仕組みを挟むことで帯域上限を回避。
- ロギング／自動化／観測性
  - 全アクションの送受信をログ化し、クラッシュ時やバグ時に再生してユニットテスト化可能。
  - 定期的に全クライアントが状態ハッシュを送り合う仕組みで分岐検出と解析が容易に。
- 「社会的解決」の設計判断
  - マスター切断でアクションが失われた場合はハイリスクな自動復元を作らず、ユーザーの再作成や協議で解決する方針を選択。複雑化を避けるコスト判断。

短いコード例（概念）：
protobuf
message ActionData {
  oneof payload { AddNode add_node = 1; RemoveNode remove_node = 2; }
}

csharp
public static Reducers CreateReducers() =>
  Reducers.Begin()
    .SyncReducer(ActionData.PayloadOneofCase.AddNode, AddNodePayload.Deserialize, AddNodePayload.Reduce)
    .End();

csharp
public static bool Reduce(CircuitsRoot root, AddNodePayload p) {
  if (!root.TryGetState(out var s)) return false;
  return s.Graph.AddNode(p.DefId, p.Position);
}

## 実践ポイント
- 単一の整合経路を作る：全操作を一つのRPC/ハンドラで通すとバグ修正と観測が激的に楽になる。
- グローバル状態＋Reducerパターンを採用して、状態遷移を純粋関数で表現する。
- 参加者追いつきは「スナップショット（Initialize） + アクション再生」で実装。
- 大きな操作は圧縮・分割・再構成で対処する（送受信の共通パスで実装）。
- ログを必ず残し、再生可能な形でテスト化することで再発防止を図る。
- 全自動で直さない判断も重要：運用上許容できる範囲は「社会的解決」を選び、システムの複雑さを抑える。

日本の開発現場では、モバイル回線や低帯域の環境、コミュニティ運営の文化が絡むため、この「単純で観測しやすい」パターンは特に有効。導入コストが低く、チームのスキル差があっても貢献しやすい設計と言える。
