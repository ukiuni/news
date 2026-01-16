---
layout: post
title: "🌈 Looking for help if possible: I’m Stuck on My TrackMyHRT App (Medication + Symptom Tracker) - お手伝い募集中：TrackMyHRT（投薬＋症状トラッカー）で行き詰まり中"
date: 2026-01-16T09:11:29.362Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/codebunny20/looking-for-help-if-possible-im-stuck-on-my-trackmyhrt-app-medication-symptom-tracker-38fa"
source_title: "🌈 Looking for help if possible: I’m Stuck on My TrackMyHRT App (Medication + Symptom Tracker) - DEV Community"
source_id: 3165171
excerpt: "ローカル志向HRT記録アプリのデータ設計・UI・エクスポート課題を実務視点で具体提案"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fgjuho0crnkhdpn80di47.png"
---

# 🌈 Looking for help if possible: I’m Stuck on My TrackMyHRT App (Medication + Symptom Tracker) - お手伝い募集中：TrackMyHRT（投薬＋症状トラッカー）で行き詰まり中

プライバシー重視のローカルHRT記録アプリを次の段階に進めたいが、データ設計・UI・エクスポートまわりで迷っている――という投稿を、実務寄りに分かりやすく整理した記事。

## 要約
TrackMyHRTはオフライン・ローカル保存でHRT（ホルモン療法）経過を記録するデスクトップツール。作者はデータモデル、入力フロー、エクスポート・移行方針で迷っており、設計上の意思決定を求めている。

## この記事を読むべき理由
- 個人データをクラウドに預けないローカルファースト設計は日本でも注目度が高く、医療情報やプライバシー配慮アプリの参考になる。  
- 小型ツールの拡張性（データ設計、移行戦略、エクスポート）をどう決めるかは、多くのプロダクトで必須の課題だから。

## 詳細解説
1. 背景と目的  
   - TrackMyHRTは「記録を取りやすく、外部に出さない」ことを最優先に作られている。ユーザーは投薬量、症状、気分、エネルギー、性欲、メモを日々入力する想定。これらを後で可視化・エクスポートできることが目的。

2. データモデルの選択肢と考え方  
   - 現状：JSON/JSONL中心の単純構造。利点は可読性と手軽さ。欠点は検索性やスキーマ進化の扱い。  
   - 選択肢：
     - 維持：シンプルなJSONLを貫く（追記型ログに適する）。移行が最小だが、複雑化に弱い。  
     - 分割：エントリを meds / symptoms / metadata 等に分ける（参照IDで結合）。拡張と部分更新が楽。  
     - 組み込みDB（推奨候補）：SQLiteを採用すると検索・集計・トランザクション・マイグレーションが扱いやすい。エクスポートはいつでもJSON/CSV生成可能。  
   - 実務的な妥協点：内部はSQLiteで管理し、外部インポート/エクスポートはJSON(スキーマ付き)またはCSVで対応。内部と外部フォーマットを分離すると将来が楽。

3. UIフロー／UXの設計ポイント  
   - 目標：「低プレッシャー」「気軽に続けられる」こと。  
   - 手法：
     - プログレッシブディスクロージャ（最小入力→詳細は展開）でフォームの重さを減らす。  
     - デフォルト値、テンプレート、頻繁に使う項目のワンクリック追加。  
     - 自動保存とアンドゥ。入力の途中で中断しても安心。  
     - アクセシビリティ：大きめのタップ領域、明瞭なラベル、キーボード操作対応。  
   - PySide6での実装ヒント：Model/View（QAbstractListModel等）を使い、UIとデータ層を分離。重い処理はQThreadへ移す。

4. エクスポート形式と長期戦略  
   - 現状の候補：.jsonl、.json、.txt、.md。多すぎると維持コストが上がる。  
   - 推奨方針：
     - 公式エクスポート1つを定義（例：JSON + JSON Schema）。可搬性と検証を担保。  
     - 追加でCSV（表計算向け）と要約Markdown（人が読むレポート）を用意。  
     - Open/文書化されたスキーマを同梱し、バージョンを明示（schema_version）。

5. マイグレーションと互換性戦略  
   - 小さな移行ロジックを用意し、アプリ起動時に「自動バックアップ→移行→完了」を行う。  
   - レガシー形式のサポートは短期的に保持し、移行ツールを提供してから段階的に切るのが現実的。  
   - 内部的にスキーマバージョンを持ち、各バージョンへ対応する移行ステップを順番に実行する。

6. プライバシーと信頼性  
   - ローカル保存とエクスポート明示は最大の差別化要素。ユーザーがデータを自分でコントロールできるUI（エクスポート／削除ボタン）を用意する。  
   - 安全のためにオプショナルで暗号化、バックアップのエクスポート機能を検討。

## 実践ポイント
- データ層：まずSQLiteを検討（ファイル1つで可搬、クエリや集計が容易）。JSONはエクスポート向けに残す。  
- スキーマ：各レコードに timestamp, id, schema_version を必ず入れる。これで将来の移行が楽。  
- UI：最小入力フォーム＋「詳細を編集」ボタンで気軽さを担保。自動保存とテンプレートを実装する。  
- エクスポート：公式は JSON + JSON Schema。追加で CSV と Markdown 要約を提供。  
- マイグレーション：起動時に自動バックアップ→段階的変換。古いフォーマットは移行ツールで吸収してから非推奨に。  
- PySide6実装ヒント：QAbstractListModelでデータを管理、シリアライズはQJsonDocumentや標準のjsonモジュール、重い処理はバックグラウンドで。

以上を踏まえれば、過度な過設計を避けつつ将来の拡張に耐えうる基盤が作れる。必要なら、具体的なスキーマ例や簡単なマイグレーション手順を提示する。どの部分のサンプルが欲しいか教えてほしい。
