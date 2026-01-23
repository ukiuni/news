---
layout: post
title: "Breaking Key-Value Size Limits: Linked List WALs for Atomic Large Writes - キー・バリューサイズ制限を破る：原子性を保つ連結リストWAL"
date: 2026-01-23T21:24:54.900Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://unisondb.io/blog/breaking-kv-size-limits-linked-list-wal/"
source_title: "Breaking Key-Value Size Limits: Linked List WALs for Atomic Large Writes | UnisonDB"
source_id: 419360494
excerpt: "WALを後方連結で分割して大容量KV書きを原子性で安全に実現する新設計"
image: "https://unisondb.io/images/wal_linked_list.png"
---

# Breaking Key-Value Size Limits: Linked List WALs for Atomic Large Writes - キー・バリューサイズ制限を破る：原子性を保つ連結リストWAL
巨大データでも「全部か無か」を守る—WALを後方リンクで繋いで安全に書く設計

## 要約
UnisonDBは、ネットワーク／メモリ制限を破らずに大きなKV／ワイドカラム／LOBを書けるよう、WALを「後方連結リスト」にしてトランザクションを分割しつつ原子性を保証する手法を紹介します。

## この記事を読むべき理由
日本でもエッジ展開やAIベクトル、大容量JSONなどで単一書き込みが大きくなる場面が増えています。既存のサイズ上限に悩むエンジニアが、安全に大きな更新を設計するための実践的な技術が学べます。

## 詳細解説
- 問題点（「Hard Wall」）  
  多くの分散KVは1件あたりのサイズ上限を設けており、これはメモリ保護やRaftのヘッドオブラインブロッキング防止のためです。エッジ複製（ISR）は多数ノードへの伝播が増え、遅延やOOMリスクが高まります。

- 手動チャンク分割が危険な理由  
  単に大きな値を複数リクエストに分けるだけだと、途中で失敗した際に「部分的な更新」が残り原子性が崩れます。

- UnisonDBの解決策：WALを「思い出す」ログにする  
  各WALレコードにPrevTxnWalIndex（前チャンクのディスクオフセット）を持たせ、同一トランザクションのチャンクが後方リンクでつながるようにします。BEGIN（アンカー）→PREPARE（チャンク連結）→COMMIT（最終章）というライフサイクルで、COMMITがディスクに確定されるまでユーザに可視化しません。途中で壊れたチェーンはリカバリ時に無視されます。

- コード概観（要点のみ）  
  - ログレコードは TxnID / TxnState / PrevTxnWalIndex / Data を持つ。  
  - Appendで書き込むときに前回のオフセットを PrevTxnWalIndex に埋める。  
  - Commitレコードが書かれて初めて memtable に反映する。  
  - リカバリは COMMIT から Prev ポインタをたどって BEGIN まで逆向きに歩き、完全なチェーンだけを再構成する。

```go
// go
type LogRecord struct {
  LSN uint64
  TxnID []byte
  TxnState TransactionState
  PrevTxnWalIndex []byte
  Data []byte
}
```

```go
// go
// Append: 新チャンクに前回オフセットを埋める
record.PrevTxnWalIndex = t.prevOffset.Encode()
offset, err := t.engine.walIO.Append(record.FBEncode(...), index)
t.prevOffset = offset
```

```go
// go
// Recovery: COMMITからPrevを辿る
records := w.GetTransactionRecords(commitOffset) // commitOffsetから逆走してBEGINまで集める
```

## 実践ポイント
- チャンクサイズはネットワーク／レプリケーションの上限内に抑える（例：etcd/Consulの既定値を参考に）。  
- 各チャンクに前チャンクのディスクオフセットを埋めて必ずリンクを作る。  
- BEGINアンカーと最終COMMITを必須にし、COMMITがfsync/flushされたら初めて可視化する。  
- リカバリ時はCOMMITに紐づくチェーンのみ再構成し、途中で途切れた断片は破棄する。  
- CRCやチェックサムを付けて不整合検知を強化する。  
- エッジ環境向けにメモリ負荷とネットワーク帯域を設計段階で評価する（小型インスタンスでのOOM対策）。  
- テストで「途中断絶」「ネットワーク遅延」「再起動」ケースを必ず検証する。

このアプローチは「大きな値を安全に扱いたい」日本のサービスやエッジ用途に直結する実務的な設計パターンです。興味があれば、WALの実装でのオフセット表現やチェックポイント戦略に踏み込んだ議論を続けましょう。
