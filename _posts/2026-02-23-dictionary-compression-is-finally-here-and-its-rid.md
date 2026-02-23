---
layout: post
title: "Dictionary Compression is finally here, and it's ridiculously good - 辞書圧縮がついに実用化、効果が圧倒的"
date: 2026-02-23T12:52:55.827Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://httptoolkit.com/blog/dictionary-compression-performance-zstd-brotli/?utm_source=newsletter&amp;utm_medium=email&amp;utm_campaign=blog-post-dictionary-compression-is-finally-here-and-its-ridiculously-good"
source_title: "Dictionary Compression is finally here, and it&#x27;s ridiculously good"
source_id: 398659474
excerpt: "たった数十バイトの辞書でYouTube JSが最大90%削減、配信劇的高速化"
image: "https://httptoolkit.com/images/header-images/dictionary.jpg"
---

# Dictionary Compression is finally here, and it's ridiculously good - 辞書圧縮がついに実用化、効果が圧倒的

魅力的なタイトル: たった数十バイトで大幅削減！辞書圧縮でWeb配信が劇的に速くなる理由

## 要約
辞書圧縮（Zstandard/Brotliのカスタム辞書）が広く実装され始め、既存圧縮比を大きく上回る帯域削減（例：YouTube JSで最大90%、Google検索HTMLで約50%）を現実にしています。

## この記事を読むべき理由
日本のサービス運営者やフロントエンド開発者は、ユーザー体験改善と転送コスト削減の両方を一度に得られるこの技術を、今すぐ検討・試験導入できる段階にあるからです。

## 詳細解説
- 仕組み：事前に共通の「辞書」を圧縮器／伸張器に読み込ませ、送るデータは辞書への参照（例："辞書のオフセットから33バイトコピー"）で表現するため、差分だけを送るような効率になる。  
- アルゴリズム：Zstandard（高速、辞書サポートは標準化済み）とBrotli（静的圧縮で高効率、2023年にカスタム辞書対応）の2択が実用的。用途により速度と比率で使い分ける。  
- 歴史背景：SDCHの失敗やDEFLATEの制約を経て、近年のブラウザ/ライブラリ対応（Zstd/Brotli）で再び現実的になった。  
- 運用面：HTTP側の新しいやり取り仕様（Compression Dictionary Transport）で辞書の通知・交渉が定義されている。クライアントは Available-Dictionary ヘッダで辞書ID（SHA-256のbase64表現をコロンで囲む）を提示し、Accept-Encoding に dcb（辞書付きBrotli）や dcz（辞書付きZstd）を含める。サーバは Content-Encoding: dcb|dcz と応答する。キャッシュには Vary: Accept-Encoding, Available-Dictionary を付ける必要がある。  
- 実装状況：Node.js（zstd辞書が組み込み: v24.6+/v22.19+）、Python（3.14でcompression.zstd）、主要なRust/JVMライブラリや各言語のネイティブバインディングあり。ブラウザは現状 Chrome 130+ が対応、Safari/Firefox も対応予定。

簡単なデモ（Node.js）
```javascript
const zlib = require('zlib');

// 以前のレスポンスを辞書にする例
const dictionary = Buffer.from('{"type":"event","source":"server-2","status":"active"}');
const dataToCompress = Buffer.from('{"type":"event","source":"server-1","status":"inactive"}');

console.log("without dictionary:", zlib.zstdCompressSync(dataToCompress).length);
console.log("with dictionary:", zlib.zstdCompressSync(dataToCompress, { dictionary }).length);
```

HTTP交渉の例
```http
# クライアント→サーバ
GET /app.js HTTP/1.1
Accept-Encoding: br, zstd, dcb, dcz
Available-Dictionary: :<base64-sha256>:

# サーバ→クライアント（辞書圧縮を使用）
HTTP/1.1 200 OK
Content-Encoding: dcz
Vary: Accept-Encoding, Available-Dictionary
```

## 実践ポイント
- まずは影響が大きい「更新頻度が低く差分が小さいアセット」（JSバンドル、WASM、定型APIレスポンス）で試す。  
- 辞書を作る：過去の配信データ群を学習させるか、APIキー/フィールド名など既知の文字列をまとめたカスタム辞書を生成する。  
- 配信方法：辞書ファイルに Link rel="compression-dictionary" を付けるか、既存レスポンスに Use-As-Dictionary ヘッダを添えてクライアントに取得させる。  
- ヘッダ管理：Vary を正しく設定してキャッシュ破壊を防ぐ。  
- 対応ブラウザとフォールバック：現状は Chrome が主戦場。未対応クライアント向けに従来の gzip/Brotli を残す。  
- 測定：帯域・CPU・レイテンシ・キャッシュヒット率を比較して導入効果を評価する。

以上を踏まえ、まずは内部環境やステージングで辞書を作ってNode/Pythonのライブラリで圧縮・伸張を試し、段階的に本番での配信テストを行うことを推奨します。
