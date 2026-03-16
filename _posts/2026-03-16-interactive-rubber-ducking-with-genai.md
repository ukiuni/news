---
layout: post
title: "Interactive Rubber Ducking with GenAI - 生成AIで行うインタラクティブ・ラバーダッキング"
date: 2026-03-16T13:40:31.380Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://event-driven.io/en/interactive_rubber_ducking_with_gen_ai/"
source_title: "Interactive Rubber Ducking with GenAI - Event-Driven.io"
source_id: 382460803
excerpt: "生成AIと対話で設計の盲点を炙り出し、即使えるspecとQAログを自動生成する実践法"
image: "https://event-driven.io/static/a08c97f5281d31661ba3946fbc3b1ec0/2a4de/2026-03-16-cover.png"
---

# Interactive Rubber Ducking with GenAI - 生成AIで行うインタラクティブ・ラバーダッキング
魅力的なタイトル: 生成AIを「相棒」にして設計の盲点を引き出す — インタラクティブ・ラバーダッキング入門

## 要約
生成AIを「質問役」として反復的に問い返すことで、自分の設計の盲点を炙り出す手法（Interactive Rubber-Ducking）。会話ログ（qa.md）と要約仕様（spec.md）を残す運用で再現性を高める。

## この記事を読むべき理由
日本のOSS保守者やアーキテクトはレビューが得にくく孤独になりやすい。短時間で設計の弱点を洗い出し、開発者に渡せる形に整える実践テクニックは、業務効率と品質向上に直結する。

## 詳細解説
- 概念：自分（盲目の人）がアイデアを持ち、生成AIが「一度に一問ずつ」質問して設計を深掘りする。目的はAIに実装させることではなく、設計者自身の思考を引き出すこと。
- 典型プロンプト（要点）：「一度に一つだけ質問して、私の回答に基づいて次を作り、最終的に開発者に渡せる詳細なspec.mdを作ってください。対話ログはqa.mdに保存してください。」（実例は記事参照）
- ツール選定：コードベースを読み込めるモデル（例：Claude Code、Opusなどの大きめモデル）が有利。軽量モデルでは思考力・質問の質が落ちる。
- 生成物：qa.md（逐次のQ&Aログ）、spec.md（要点をまとめた仕様）。後続レビューや別モデルへの入力に便利。
- 実例（記事からの技術話題：Second-level cache導入）
  - 解くべき問題：大量イベントからのプロジェクション再構築でN+1が発生 → バッチ処理＋2nd-level cacheでI/O削減。
  - 設計決定（抜粋）：
    - キャッシュは薄いインターフェース（get/set/delete/clear）でプラガブルに。デフォルトはメモリLRUアダプタ。
    - カスケード設定（クライアント／DB／コレクション単位）を許容し、継承ルールは一般パラメータは継承、タイプ固有パラメータはリセット。
    - インターフェースはPromiseLike<T>対応で同期/非同期両対応。getMany/setManyなどバッチ操作はデベロッパー体験向上のため用意。
    - キー衝突対策は名前空間管理（{db}:{collection}:{id}）をPongo側で行う。
    - 一貫性：書き込み成功時に更新/削除、競合時に該当エントリをevict。デフォルトはキャッシュ有効、必要に応じて skipCache オプションを用意。
    - handle API は id | id[] を許容し内部でバッチ化。キャッシュ内の _version を比較して短絡できる場面あり。
    - デフォルト設定案：max ≈ 1000、TTLは運用上のトレードオフ（TTLを短めにするかL R Uのみで運用するかはサービス要件次第）。
- 運用上の注意：AIは「イエスマン」になりがち。あくまで質問を引き出す道具として使い、仕様の抜け・誤りは人が検証する。

## 実践ポイント
1. 最初の一歩：リポジトリを読み込めるモデルを選び、上記プロンプトをそのまま投げて「一問ずつ」の対話を開始する。  
2. 出力を保存：毎問QAを qa.md に追記、最終仕様を spec.md として保存する運用を徹底する。  
3. まずは小さく：メモリLRU（max 1000）をデフォルトで導入し、後から外部キャッシュ用アダプタを追加する。  
4. API設計：get/set/delete/clear（PromiseLike対応）、getMany/setMany を用意し、キーは Pongo 側でプレフィックス付与する。  
5. 一貫性戦略：書き込みで更新/evict、競合でevict→リトライ。高競合ケースは skipCache フラグで回避可能にする。  

まずは数回試してログを見返すこと。設計の見落としが出たら、その部分だけを再度ラバーダッキングして磨くと効果が早い。
