---
layout: post
title: "Using the Browser’s <canvas> for Data Compression - ブラウザの<canvas>を使ったデータ圧縮"
date: 2026-02-19T18:13:55.367Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jstrieb.github.io/posts/canvas-compress/"
source_title: "Using the Browser’s &lt;canvas&gt; for Data Compression"
source_id: 807935792
excerpt: "ブラウザのcanvasで任意バイト列をPNG化し、サーバ不要でURLに載せられる圧縮トリック"
---

# Using the Browser’s <canvas> for Data Compression - ブラウザの<canvas>を使ったデータ圧縮
URLに詰め込む新トリック：canvasで任意バイト列をPNG圧縮してサイズを稼ぐ方法

## 要約
ブラウザが内部で行うPNG（deflate/zlib）圧縮を利用し、任意のバイト列をHTMLの<canvas>経由でPNGに変換して圧縮・復元するテクニックを紹介します。古いブラウザやCompression Streams API非対応時の実用的なフォールバックになります。

## この記事を読むべき理由
SPAの状態をURLハッシュや短い保存形式に入れたい、あるいはクライアント側で軽い圧縮を行いたい場面で、サーバー依存やWASM実装を増やさずにブラウザ実装を活用できるため。

## 詳細解説
- アイデア：任意のUint8ArrayをRGBピクセル（3バイト／ピクセル）に詰め、alphaチャンネルは常に255にしてからcanvasに書き出す。canvas.toDataURL("image/png")によって得られるPNGはブラウザ内の最適化された圧縮を利用しており、結果のbase64は元データより小さくなることが多い。
- 実装の要点：
  - 先頭バイトに「最後のピクセルで余るバイト数（0〜2）」を保存してデータ長を復元可能にする。
  - imageData.dataはRGBA順で4要素ごとにalphaがあるため、書き込み時／読み取り時にalphaをスキップする。
  - alphaは255（不透明）で統一しないとブラウザ間でエンコードの差が出ることがある。
  - 復元は画像を読み込んでcanvasに描画→getImageDataで取得→alphaを除去→先頭バイトで長さを復元、という非同期処理になる（img.onloadを待つ）。
- 注意点：
  - PNGフォーマットのヘッダ／チェックサム／base64のオーバーヘッドがあるため、すべての場合で有利とは限らない。ランレングスや冗長性の高いデータで効果的。
  - すでに圧縮済みデータ（JPEG/ZIP等）には効果が薄い。
  - URL長の制限やbase64のサイズ増（約4/3）を考慮する。
  - 近年はCompression Streams API（2023以降）でブラウザ内で直接圧縮が可能なので、新しい環境ではそちらが優先。

### 主要コード（概略）
```javascript
// javascript
function compress(data) {
  data = Array.from(data);
  data.unshift(data.length % 3); // 余りを先頭に
  const c = document.createElement("canvas");
  const numPixels = Math.ceil(data.length / 3);
  c.width = numPixels; c.height = 1;
  const ctx = c.getContext("2d");
  ctx.fillStyle = "white"; ctx.fillRect(0,0,c.width,c.height);
  const img = ctx.getImageData(0,0,c.width,c.height);
  let off = 0;
  for (const b of data) {
    if (off % 4 === 3) img.data[off++] = 255; // alpha
    img.data[off++] = b;
  }
  ctx.putImageData(img,0,0);
  const url = c.toDataURL("image/png");
  return url.split(",")[1]; // base64 部分
}

function decompress(base64) {
  return new Promise((resolve,reject)=>{
    const img = document.createElement("img");
    img.onerror = ()=>reject(new Error("img load failed"));
    img.onload = ()=>{
      try {
        const c = document.createElement("canvas");
        c.width = img.naturalWidth; c.height = img.naturalHeight;
        const ctx = c.getContext("2d");
        ctx.drawImage(img,0,0);
        const raw = ctx.getImageData(0,0,c.width,c.height).data;
        const bytes = Array.from(raw).filter((_,i)=>i%4!==3);
        const rem = bytes[0];
        const len = bytes.length - 1 - (3 - rem);
        resolve(new Uint8Array(bytes.slice(1,1+len)));
      } catch(e){ reject(e); }
    };
    img.src = `data:image/png;base64,${base64}`;
  });
}
```

## 実践ポイント
- まずCompression Streams APIが使えるか確認（モダンブラウザならそちらを優先）。使えない／フォールバックが必要ならこのcanvasトリックを導入する。
- 圧縮対象は冗長性の高いプレーンテキストやJSON（minify済み）などが有望。既にgzip等で圧縮済みのバイナリは非推奨。
- URLに埋める場合はbase64長＋ブラウザのURL長制限（数千文字目安）をチェック。
- セキュリティ：データURIに機密を入れる場合は露出リスクを考慮する（履歴やログに残る）。
- テスト：主要ブラウザ（Chrome/Firefox/Safari）でalpha・エンコードの差異を確認する。

以上を踏まえれば、サーバー側に頼らずブラウザの既存実装を活用して小さな圧縮タスクを巧くこなせます。
