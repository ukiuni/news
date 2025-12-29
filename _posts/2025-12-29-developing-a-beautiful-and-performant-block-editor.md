---
layout: post
title: "Developing a Beautiful and Performant Block Editor in Qt C++ and QML"
date: 2025-12-29T08:51:03.828Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rubymamistvalove.com/block-editor"
source_title: "Ruby Mamistvalove"
source_id: 46396824
excerpt: "Qt(C++)×QMLで作る、Markdown基盤の高速軽量WYSIWYGブロックエディタ"
---

# Notionっぽくても軽い──Qt(C++)×QMLで作る「見たまま」高速ブロックエディタの舞台裏

## 要約
QtのC++ロジック＋QMLビューで、Markdownを下地にした「WYSIWYGかつブロック式」エディタをゼロから作り、ネイティブに近い見た目・挙動・高速性を両立させた話。

## この記事を読むべき理由
ブラウザ依存の重いツールに疲れた日本の開発者やプロダクト担当へ。バッテリやメモリを節約しつつ、ユーザーに優しいブロック編集体験をローカル・オフラインで提供する実装方針と技術的肝を具体的に学べます。

## 詳細解説
- 技術選定の理由  
  - Qt(C++)はネイティブの見た目/性能に近づけやすく、QMLは宣言的UI・バインディング・アニメーションを簡潔に書ける。UIはQML、重いロジックはC++で実装するのが基本パターン。

- アーキテクチャ（簡潔）  
  - Data: ノート本体はプレーンテキスト（Markdown）で保管（例: SQLite）。  
  - Model: Qtの QAbstractListModel を継承した BlockModel。各ブロックは QObject ベースの Block オブジェクト（blockType, text, indent 等）として管理。  
  - View: QML の ListView。各デリゲートは共通の Block レンダラーで、blockTypeに応じてテキスト・Todo・Kanban・画像などのコンポーネントを差し替え。

- ブロック内外の選択と連続選択  
  - ListViewの「デリゲートが分かれている」状況でも、レンダリング上の連続したテキスト選択を実現するため、可視デリゲートそれぞれに「自分のインデックスが selectionStartIndex..selectionEndIndex の範囲内か」を問い合わせ、selectionChangedシグナルで同期的に選択状態を更新する手法を採用。これによりブロックをまたいだ選択やドラッグでの範囲取得が可能になる。

- カーソル操作や編集操作（地味だが重要）  
  - 上下移動でのx位置維持、単語選択、範囲選択、クリップボード連携など、エディタで当然と思っている挙動は自前で揃える必要がある。特に「レンダリング済み（リッチテキスト）上の位置 ↔ 元のMarkdown上の位置」マッピングは最難関。

- Undo/Redoの設計と操作のマージ  
  - シンプルな実装路線を採用：SingleAction構造体に「操作前のプレーンテキスト」と「操作後のプレーンテキスト」を丸ごと保持。  
  - ユーザー期待に合わせるため、連続入力や複数ブロックのインデントなど複数の小操作をCompoundActionとしてマージして扱う。  
  - 高度ブロック（例：Kanban、画像）の独自操作履歴は最初は個別保持していたが、オブジェクト削除で履歴が消える問題を回避するため、BlockModel側で集中管理する設計に統一。

- MarkdownとWYSIWYGの共存（表示/編集切替）  
  - 普段はMarkdownを解析してリッチに表示（アスタリスク等は隠す）しつつ、カーソルがその書式内にある場合は生のMarkdownを一時表示する挙動を実現。  
  - 実装の要点は「レンダリング済みテキスト（QMLのRichText/HTML）からカーソル位置に対応するMarkdown部分を復元する」こと。手法の一例としては TextArea の HTML を取り出して Markdown に戻し、位置に対応する部分を抽出するフローを使う（レンダリング→HTML→Markdown→位置対応）。

- パフォーマンスの優位性  
  - 多層抽象のブラウザ系アプリに比べ、C++実装＋QML描画はCPU／メモリ効率で優位になる。実体験では同様の編集操作でWebベースより大幅に軽いという定性的・定量的な差が確認されている。

## 実践ポイント
- 基本はMVC：UIはQML、データとロジックはC++（QAbstractListModel）で切り分ける。  
- Blockは軽いQObjectにして、KanbanやImageのような重い構造はポインタで遅延生成する（メモリ節約）。  
- 選択はデリゲート側で「自分が選択範囲内か」を判定させるイベント駆動型にすると扱いやすい。  
- Undo/Redoはまずは全体スナップショットで実装し、ユーザー体験向上のために操作マージを実装していく（過度な最適化は後回しでも可）。  
- MarkdownとWYSIWYGの同期は「表示HTMLをMarkdownに戻す」ワークフローで実現可能だが、境界条件（複数書式ネスト、部分選択）を丁寧にテストすること。  
- 低消費電力デバイスや企業のオフライン要件を考えるなら、ネイティブ／ネイティブ風（Qt）実装は有力な選択肢。

この設計方針は、軽快でシンプルなUXを求める日本のアプリ開発にマッチします。まずは小さなBlockModel＋QML ListViewのプロトタイプを作って、選択・コピー・Undoの一連挙動を固めることを推奨します。
