---
layout: post
title: "Code-ing in a Tree: Adding Auto-Save to freeCodeCamp - 「木の下でコーディング：freeCodeCampに自動保存を追加する」"
date: 2026-01-19T03:33:58.535Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/sagi0312/code-ing-in-a-tree-adding-auto-save-to-freecodecamp-137b"
source_title: "Code-ing in a Tree: Adding Auto-Save to freeCodeCamp - DEV Community"
source_id: 3175520
excerpt: "localStorageと静かなUIでfreeCodeCampに自動保存を導入する手法"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F4w1ly567sdu3n032mks8.png"
---

# Code-ing in a Tree: Adding Auto-Save to freeCodeCamp - 「木の下でコーディング：freeCodeCampに自動保存を追加する」
魅せる学習体験を壊さない「そっと保存する」自動セーブの作り方

## 要約
freeCodeCampのエディタに自動保存を導入した実装記。localStorageへの保存、UIの小さな保存表示、そしてテスト周りの調整までを丁寧に扱い、ユーザー体験を壊さずにデータ消失を防ぐ方法を示す。

## この記事を読むべき理由
学習プラットフォームやオンラインエディタを作るとき、ユーザーの「書いたコードが消える」恐怖は致命的。日本でもProgateやドキュメンテーションを書きながら学ぶ層が増えており、簡潔で確実な自動保存の設計はすぐに役立つ実装知識です。

## 詳細解説
- 問題点
  - freeCodeCampのエディタは手動保存（Ctrl+S）に依存しており、多くのユーザーが保存を忘れてコードを失うケースが発生していた。
- 解決方針（設計）
  - silent autosave（目立たない自動保存）：自動保存はユーザーに大きな通知を出さず、画面上の小さなタイムスタンプやアイコンで安全を示す。
  - persistence 層：localStorageへ定期的に保存し、ページリロードや意図しないナビゲーション後も復元できるようにする。
  - イベントトリガー：onChange（デバウンス）、onBlur、beforeunload、コンポーネントのアンマウント時に保存を行う。
  - 最終保存時刻管理：'lastSavedTime'のような状態を持ち、5秒ごとなどで表示を更新して「Saved 10s ago」のような表示を出すが、遷移で古い表示が残らないようリセットする。
  - ユーザー操作と自動の区別：手動保存は明示的なフィードバック（トースト等）を出し、自動保存は静かに進めることでノイズを減らす。
- 実装上の選択肢
  - 状態管理：React Context / Zustand / Reduxのいずれでも可能。今回の実装では既存コードベースに合わせてReduxを採用し、lastSavedTimeをグローバルに管理。
  - 再利用性：保存ロジックはユーティリティ関数とカスタムフックに切り出してDRYに保つ。
- テストとCIへの影響
  - ユニットテストやe2eテストで自動保存が副作用を起こすと失敗するため、テストを更新する必要がある（自動保存時はフラッシュメッセージを抑制する等の対応）。
  - Playwright/Cypress系のE2Eでは自動保存の待ちや状態のリセットを明示的に扱うことが重要。

## 実践ポイント
- まずは小さく始める：localStorageにserializeしたスナップショットを定期保存する仕組みを作る。
- デバウンスは必須：onChangeの度に保存すると性能と書き心地を損なう。300–1000ms程度で調整する。
- 保存トリガーを増やす：onBlur、beforeunload、コンポーネントのunmountでフォールバック保存を行う。
- UIは控えめに：ツールバーの小さなアイコン＋「最後に保存した時刻」を表示し、自動保存は通知を鳴らさない（手動は通知する）。
- テストを忘れない：ユニット・E2E双方で自動保存の副作用をモック／抑制してテストを安定させる。
- 使い勝手を重視：ダウンロード（エクスポート）ボタンや、復元オプションを用意すると学習者に安心感を与える。

短いチェックリスト
- [ ] localStorageに保存するユーティリティを作る
- [ ] onChangeをデバウンスして保存
- [ ] beforeunloadで最後の保存を行う
- [ ] UIに「保存済み」タイムスタンプを追加
- [ ] 自動保存は通知を抑制、手動保存で明示通知
- [ ] ユニット/E2Eテストを更新して副作用を管理

参考（原著）
https://dev.to/sagi0312/code-ing-in-a-tree-adding-auto-save-to-freecodecamp-137b

この記事のアイデアは、日本の学習プラットフォームや社内ツールでもすぐに使えます。まずは「静かに、しかし確実に」保存する仕組みを導入して、ユーザーのストレスを減らしましょう。
