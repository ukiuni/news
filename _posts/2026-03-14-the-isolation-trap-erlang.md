---
layout: post
title: "The Isolation Trap: Erlang - アイソレーションの罠：Erlang"
date: 2026-03-14T10:57:55.280Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://causality.blog/essays/the-isolation-trap/"
source_title: "The Isolation Trap — Causality"
source_id: 47347920
excerpt: "Erlangの孤立設計は運用で共有状態やデッドロックを招き、性能逃げ道が並行バグを再導入する"
image: "https://causality.blog/og-essay-2.png"
---

# The Isolation Trap: Erlang - アイソレーションの罠：Erlang
Erlangの「孤立」が生む安心と、やむを得ず開ける“逃げ道”が招く落とし穴

## 要約
Erlangはプロセスごとの独立ヒープとメッセージコピーで高可用性を実現するが、実運用ではデッドロック、無限膨張するメールボックス、順序競合、型やプロトコル違反などの問題が残り、性能要請で導入される共有ストア（ETS、persistent_term、atomics 等）が元の問題を再導入する。

## この記事を読むべき理由
日本のプロダクト（通信系、決済、チャット、IoT等）で「高可用性＋高負荷」を目指す開発者は、Erlangの設計と現実的なトレードオフを理解すると、設計ミスや運用障害を未然に防げる。

## 詳細解説
- ActorモデルとErlangの強み  
  Erlangは各プロセスが独自ヒープを持ち、メッセージはコピーされることで「直接他のプロセスの状態を書き換えられない」安全性を提供。電話交換やWhatsAppの事例が示す通り、30年の実運用実績がある。

- 典型的な失敗モード（簡易例）
  同期的な相互呼び出しはメッセージで書かれていてもデッドロックになる例：
  ```erlang
  %% Server A
  handle_call(request, _From, State) ->
      Result = gen_server:call(server_b, sub_request),
      {reply, Result, State}.

  %% Server B
  handle_call(sub_request, _From, State) ->
      Result = gen_server:call(server_a, request),
      {reply, Result, State}.
  ```
  互いに返信を待つと永久待ち（mutex的デッドロック）になる。これ以外にも
  - 無界メールボックスによるメモリ膨張（バックプレッシャなし）  
  - 複数送信者のメッセージ間割り込みによる順序競合（non-determinism）  
  - 動的型のメッセージで起きるプロトコル違反（受信側の期待と不一致）  
  が現実的に発生する。

- 軽減策とその限界  
  タイムアウト、非同期cast、監視・モニタリング、OTP の設計規約や Dialyzer などの静的解析が有効だが、いずれも「運用と人の規律」に依存する。いわゆる「規律税（discipline tax）」が蓄積し、チームや時間で脆弱になる。

- 性能ボトルネックと逃げ道  
  「一プロセス＝一メールボックス」の直列化が読み取りホットスポットでスループットを殺すため、Erlangは意図的に ETS（共有ミュータブルテーブル）、persistent_term（読み多書少向け不変）や atomics/counters といった共有メモリの“逃げ道”を用意した。これらは性能的に有効だが、TOCTOUや並行更新レースなど、共有状態の古典的なバグを再導入する。

- 実証的な発見  
  研究者が OTP 自体を静的解析したところ、ETS周りのレース、プロセス名登録の競合、プロセス辞書による順序依存など、現場で使われるライブラリにも既知でない競合が見つかった。これは「モデルの設計意図」と「実運用で避けられない要求」のギャップを示している。

## 実践ポイント
- 同期的相互呼び出しは避け、可能なら非同期＋タイムアウトで設計する。  
- 読み取りホットスポットはシャーディング／キャッシュ／read-replicasで分散させる。  
- ETSやpersistent_termを使うときは、操作の原子性が保証されないことを前提に設計（チェック→更新の競合対策やバックオフを入れる）。  
- メールボックスサイズを監視し、バックプレッシャやレート制御を導入する（pobox 等のライブラリ検討）。  
- Dialyzer＋race検出ツール、負荷試験をCIに組み込み、運用でのレース検出と復旧手順を整備する。  

Erlangは強力だが万能ではない。安全性は設計だけでなく運用・ツール・トレードオフの理解で初めて保てる、という点を意識してほしい。
