---
layout: post
title: "When Caching Made Things Worse - キャッシュが逆効果になったとき"
date: 2026-01-11T05:56:46.826Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://glama.ai/blog/2026-01-11-do-not-use-large-strings-as-cache-keys"
source_title: "When Caching Made Things Worse | Glama"
source_id: 465743497
excerpt: "巨大なMarkdownをキーにしてNode.jsが暴走した原因と即効のxxhash＋Redis対策"
---

# When Caching Made Things Worse - キャッシュが逆効果になったとき
50MB文字列をキーにしてサーバが悲鳴を上げた話 — 今すぐできる即効対策

## 要約
Markdown全文をそのままキャッシュキーに使ったため、Node.jsのメモリとGCコストが急増した事例。キーをハッシュ化してRedisに移行することで解決した。

## この記事を読むべき理由
日本でもNode.jsやサーバレスを使ったサービスで、大きなテキスト（ドキュメント、Markdown、JSON）を扱うケースは多い。知らずに「文字列そのままキー」を使うと、メモリ使用量とGC負荷でパフォーマンスが劇的に悪化する可能性があるため、対策を知っておくべき。

## 詳細解説
問題の本質
- 解析コストを下げるためにMarkdown→AST変換結果をキャッシュしようとしたが、キャッシュのキーにMarkdown全文（数MB〜数十MB）をそのまま使っていた。
- LRU実装自体の問題ではなく、キーが巨大文字列だとメモリ上に巨大なキー群が蓄積され、GCが頻発する。maxSizeが1000ならキーだけで数十GBになり得る。

V8の文字列比較挙動
- 同一参照（同じオブジェクト）なら参照比較で早く終わるが、現実的なリクエストでは毎回新しい文字列インスタンスが来るため、毎回数百万〜数千万文字の比較が発生する。
- ベンチマークでは「同一参照の大きな文字列」は速いが、「別参照の大きな文字列」は文字数分の比較コストが増幅され、遅延が桁違いになる。

元の悪い実装（概念）
```javascript
// javascript
const cache = new QuickLRU({ maxSize: 1000 });

function parseMarkdown(markdown) {
  const cached = cache.get(markdown); // markdown全文をキーにしている（NG）
  if (cached) return cached;
  const ast = parse(markdown);
  cache.set(markdown, ast);
  return ast;
}
```

対策
1. キーは必ず固定長のハッシュにする（高速ハッシュ推奨）。SHA系は安全だが遅いので、キャッシュ用途には xxhash 等の高速ハッシュが良い。
2. 大きなオブジェクト自体をメモリ内キーとして持たない。ASTなどは外部キャッシュ（Redis等）に移してプロセスのメモリ負荷を下げる。
3. キャッシュ設計は「キーの長さ・生成コスト」と「プロセス内メモリの影響」を常に評価する。

修正例（ハッシュ化＋Redis）
```javascript
// javascript
import xxhash from 'xxhashjs';
import Redis from 'ioredis';

const redis = new Redis();

function keyFor(markdown) {
  return `md:${xxhash.h32(markdown, 0x12345678).toString(16)}`;
}

async function parseMarkdown(markdown) {
  const key = keyFor(markdown);
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);
  const ast = parse(markdown);
  await redis.set(key, JSON.stringify(ast), 'EX', 60 * 60); // TTL例
  return ast;
}
```

なぜxxhash＋Redisが効くか
- xxhashはキャッシュ用キーとして十分速く、衝突確率は低い（暗号学的ハッシュが不要な場面では現実的）。
- Redisに移すことでプロセスのGC負荷を分散でき、インスタンス間でキャッシュ共有も可能になる。

## 実践ポイント
- まず自分のキャッシュキーをチェック：長い文字列や大きなオブジェクトをキーにしていないか確認する。
- 大きなコンテンツはキーではなくID/ハッシュに変換してからキャッシュする（xxhash等を検討）。
- Node.jsプロセスのGCログ／メモリプロファイラを見て、キャッシュ変更前後で改善を確認する。
- 単一プロセスのメモリだけに頼らず、Redis等の外部キャッシュを使うと運用性が上がる（スケール、永続化、共有）。
- キャッシュ設計にTTLを入れて、永続的に巨大データが残らないようにする。

短くまとめると：キーは軽く、値の保管は適切な場所へ。巨大文字列をそのままキーにするのは、思わぬGC地獄を招く。
