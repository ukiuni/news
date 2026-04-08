---
layout: post
title: "Full Text Search with IndexedDB - IndexedDBでの全文検索"
date: 2026-04-08T14:19:20.789Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.jmp.chat/b/2026-full-text-search-indexeddb"
source_title: "Full Text Search with IndexedDB — JMP Blog"
source_id: 1745945188
excerpt: "IndexedDB＋単語インデックスで100万件規模をブラウザ単体で高速全文検索する実装法"
---

# Full Text Search with IndexedDB - IndexedDBでの全文検索
ブラウザだけで1百万件も捌ける？IndexedDB×単語インデックスで作る“ローカル全文検索”

## 要約
IndexedDBの低レベルAPIだけで、テキストの全文検索を高速に実装する手法を解説。小規模はテーブルスキャン、大規模はmultiEntryインデックス＋最小語候補で絞り込むのが鍵。

## この記事を読むべき理由
ローカルにチャット履歴やメモを保持するWebアプリは増加中。日本のサービスでもプライバシー重視やオフライン対応が求められる中、IndexedDB上で実用的な全文検索を自前で実装できると差別化・速度向上につながります。

## 詳細解説
1) 基本方針（まずはテーブルスキャン）
- 小規模データ（例: <10k件）なら、全件を順に読み取ってトークン化・ステミングして照合するだけで簡単かつ十分速い。
- トークン化は正規表現で単語境界を取る、ストップワード除去、必要ならステマーを使う。

```javascript
// javascript
function tokenize(s){
  return s.toLowerCase()
    .split(/\s*\b/)
    .filter(w => w.length>1 && /\w/.test(w) && !stopwords.includes(w));
}
```

2) 大規模対応：multiEntryインデックスを使う
- IndexedDBのmultiEntryインデックスを使い、メッセージごとにトークン配列を保存すると各単語ごとに索引エントリが作られる。
- 検索時はクエリをトークン化した各語について index.count を取り、もっとも出現数が少ない語（最小ポスティングリスト）をプローブして、その候補集合だけを走査して完全一致(全語含有)を確認する。
- 最後に必要ならタイムスタンプでソートする（インデックス順と異なる順序は自前でソート）。

```javascript
// javascript (作成例)
tx.objectStore("messages").createIndex("terms","terms",{multiEntry:true});
// 保存時
store.put({ text, terms: [...new Set(tokenize(text).map(stemmer))], timestamp });
```

3) 効果
- 1Mメッセージのテストでも、典型的に最小語の候補集合は数千件以下になり、応答は実用的に高速化される。
- countを使った語選択は追加のメタデータに置き換え可能（挿入時に単語頻度を更新しておく）。

## 実践ポイント
- まずは単純なテーブルスキャンで動くプロトタイプを作る（挙動確認用）。
- トークナイザとストップワードは日本語対応を検討（形態素解析器の導入で精度向上）。
- multiEntryインデックスを導入し、検索時は最小出現単語で絞り込む実装に移行する。
- 更新コストが気になる場合は、単語頻度カウントをDB内で保持してcountの代替とする。
- ソートやランキングはクライアント側で行うため、必要ならスコアリングを追加する（TFや日時重みなど）。

以上を踏まえれば、ブラウザ単体で大規模データに耐える全文検索を比較的シンプルに実装できます。
