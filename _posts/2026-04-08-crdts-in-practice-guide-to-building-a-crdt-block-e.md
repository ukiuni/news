---
layout: post
title: "CRDTs in Practice: Guide to building a CRDT Block Editor Engine from Scratch - CRDTを実践する：ブロックエディタ用CRDTエンジンをゼロから作るガイド"
date: 2026-04-08T18:15:40.366Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ashwinhprasad.substack.com/p/crdts-in-practice-building-a-block"
source_title: "CRDTs in Practice: Building a Block Editor Engine from Scratch"
source_id: 366806598
excerpt: "RGAベースのCRDTでNotion級のブロック共同編集をゼロから実装する実践ガイド"
image: "https://substackcdn.com/image/fetch/$s_!ZTBq!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18998a97-6a18-41cf-ab96-67eb6891bed5_3544x4394.png"
---

# CRDTs in Practice: Guide to building a CRDT Block Editor Engine from Scratch - CRDTを実践する：ブロックエディタ用CRDTエンジンをゼロから作るガイド

NotionやGoogle Docs級の共同編集を自前で作る：CRDTで競合を“コードで解決”する実践ガイド

## 要約
Notion風のブロックエディタを対象に、実装に必要なCRDT（RGAベース）の設計と実装上の注意点を実務寄りに解説する。キーは「一意ID」「afterポインタ」「トゥームストーン」「決定論的ソート」「遅延到着対策」の組合せ。

## この記事を読むべき理由
分散・オフライン対応の共同編集は日本のSaaS／社内ツールでも需要が高い。既存ライブラリ任せでなく、自分で動作原理を押さえれば、軽量で堅牢な独自エディタや同期層を設計できる。

## 詳細解説
- 全体像：CRDTDocumentがエントリーポイント。すべての編集はCRDTOpとして出力でき、任意順に適用しても最終的に収束する。
- 識別（CRDTId）：各要素は [replicaId, counter]（または特別なHEAD）で唯一に識別。replicaIdはピア固有、counterはそのピアのローカルLamportクロック。
- データ構造（RGA = Replicated Growable Array）：平坦なリストではなくツリー表現。各要素は挿入先をafter（親）として保持し、同じ親の子要素はidでソートして決定論的順序を作る。
- 要素構成（RGAElement）：主要フィールドは id, value, after, deleted（トゥームストーン）、children。削除は物理削除せず deleted=true にして残すことで参照整合性を守る。
- 同時挿入の解決：同一の after を参照する複数挿入は id（counter→replicaId）で全ピアが同じ順序にソートするため衝突しない。
- 遅延到着対策：ある操作の parent が未到着なら pending キューで待ち、親が来た時点で適用することで順序依存を解消。
- 汎用性：RGAは文字列／段落／リスト項目など汎用で、上位のブロック構造はRGAのラッパーとして設計する。

TypeScriptでの要素イメージ（簡略版）:

```typescript
export class RGAElement<T = string> {
  public children: RGAElement<T>[] = [];
  constructor(
    public id: [number, number] | "HEAD",
    public value: T | null,
    public after: [number, number] | "HEAD",
    public deleted: boolean = false
  ) {}
  insertChild(child: RGAElement<T>) {
    this.children.push(child);
    this.children.sort((a, b) => compareIds(a.id, b.id));
  }
}
```

## 実践ポイント
- replicaId を一意に割り振り、ローカルの counter（Lamport時計）を各操作で増やす。
- 削除は必ず tombstone（deleted=true）にしてから物理削除はGC的に別処理で行う。
- children を id 比較で常にソートして決定論的順序を保証する実装を用意する。
- parent が未着の ops は pending に溜め、親到着で自動適用するロジックを実装する。
- まずは小さなRGA<string>で文字列編集を実装し、段階的にブロック（段落・リスト・表）をラップして拡張する。
- テスト：fork→同時編集→相互適用で各レプリカの内容が一致することを自動化して検証する。

以上を押さえれば、CRDTの理論を実際のブロックエディタ実装に落とし込む土台ができます。
