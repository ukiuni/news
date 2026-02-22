---
layout: post
title: "Fresh File Explorer – VS Code extension for navigating recent work - Fresh File Explorer — 最近の作業にフォーカスする VS Code 拡張"
date: 2026-02-22T18:35:09.390Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/FreHu/vscode-fresh-file-explorer"
source_title: "GitHub - FreHu/vscode-fresh-file-explorer: A vscode file explorer which shows only recently modified files based on a combination of Git history and your pending changes"
source_id: 47113325
excerpt: "巨大リポジトリでも今触るべきファイルを即表示、作業集中を取り戻すVS Code拡張"
image: "https://opengraph.githubassets.com/6a2c8e95ab69cfb81181b56c33c54031f034db7cfdd8e8700942c36b78675eef/FreHu/vscode-fresh-file-explorer"
---

# Fresh File Explorer – VS Code extension for navigating recent work - Fresh File Explorer — 最近の作業にフォーカスする VS Code 拡張
今触っているファイルだけを一覧化して開発の迷子を防ぐ、手放せない「作業フォーカス」パネル

## 要約
Fresh File Explorer は、Git履歴と未コミット変更を組み合わせて「最近編集されたファイル」だけをツリー表示する VS Code 拡張。大きなリポジトリや複数リポジトリ環境で、今やるべきファイルに素早く戻れるようにする。

## この記事を読むべき理由
巨大・レガシーなコードベースやリモートチームが増える日本の現場では、「どこを触ればいいか分からない」時間が生産性の大敵。Fresh File Explorer は、作業の文脈（未コミット変更や直近のコミット）に基づき視覚的にファイルを絞り込み、学習コストや手戻りを減らす実用的ツールである。

## 詳細解説
- 表示モード
  - Pending Changes（未コミット）と、任意の期間（例：過去7日、30日）で切替可能。コミット後も時間窓を広げれば作業履歴を保持できる。
- スマートなツリービュー
  - ディレクトリ構造でグループ化、フォルダごとのファイル数表示、指定深さで自動展開。
- 削除ファイル対応
  - 削除済みファイルは元の位置に「削除マーク」として表示。クリックで読み取り専用の一時ファイルを開く（Exhume）か、右クリックで元に戻す（Resurrect）ことが可能。
- ヒートマップ着色
  - 編集の新しさを色で可視化（より明るい色＝より最近の編集）。Fresh Filesビューだけでなく標準のファイルエクスプローラーにも適用可能。
- ピン（Pinned）機能
  - 特定ファイルやメモを常に先頭に固定。ワークスペース単位で保存され、削除ファイルや検索結果のファイルもピン可能。
- フィルタとグルーピング
  - 作者やコミットでフィルタリング、表示グループを「フォルダ／作者／コミット」などに変更して視点を切替。
- クイックオープンとコンテキスト操作
  - Fresh Files に限定したクイックオープン、差分表示で開くか通常オープンするか選択、変更破棄や復元などの右クリック操作をサポート。
- マルチリポジトリ対応
  - サブフォルダに複数リポジトリ、マルチルートワークスペース、ワークツリーに対応。サブモジュールは木に表示され内容は限定。
- 検索・履歴機能
  - 「Search in Fresh Files」：表示中のファイル群だけを対象に全文検索。「Search in Found Files」：チェイン検索で段階的に絞り込む。「File/Line/Function History」「Diff Search」など git の履歴探索機能も統合。

## 実践ポイント
- まずは拡張を入れて「Time Window」を7日〜30日に設定し、普段の作業でどれだけ有用か試す。
- よく参照するドキュメントや一時メモはピンしておくと作業効率が上がる。
- 削除ファイルの復元（Resurrect）はワンクリックで済むため、誤削除時の心理的負担が軽減される。
- チームで使う場合は作者フィルタで自分以外の変更を一時的に隠し、集中して作業するワークフローを試す。
- 大きなリポジトリではヒートマップとクイックオープンを併用すると、注力すべきファイルへ最短で辿り着ける。

以上を踏まえ、特に新メンバー受け入れや保守フェーズの効率化を目指す現場で導入検討する価値が高い拡張である。
