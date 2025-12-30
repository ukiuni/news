---
layout: post
title: "Streaming compression beats framed compression - ストリーミング圧縮はフレーム圧縮に勝つ"
date: 2025-12-30T05:18:02.185Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bou.ke/blog/compressed/"
source_title: "Streaming compression beats framed compression"
source_id: 46392382
excerpt: "WebSocket/HTTPで接続ごとに圧縮状態を共有し帯域を約80%削減"
---

# Streaming compression beats framed compression - ストリーミング圧縮はフレーム圧縮に勝つ
WebSocketやHTTPの「毎フレーム圧縮」を捨て、エンコーダ／デコーダのコンテキストを接続で共有してフラッシュするだけで帯域が劇的に下がる — 工事現場のロボットで80%削減した実例。

## 要約
フレームごとに独立して圧縮する既存手法より、同じ圧縮コンテキストを接続ごとに共有し、各メッセージ後に「flush」するストリーミング圧縮の方が圧縮効率が高く、実運用で大幅な帯域削減を確認した。

## この記事を読むべき理由
日本でも屋外Wi‑Fiや5G／L2ネットワークで帯域と安定性が課題のリアルタイム制御や観測データ送信が増えています。既存プロトコルのまま短時間・中サイズメッセージを大量に送る用途（ロボット制御、OpenTelemetryのエクスポート、gRPC‑web/SSE）で即効性のある帯域削減手法になるため、エンジニアは知っておくべきです。

## 詳細解説
- フレーム圧縮（per-frame compression）:
  - WebSocket標準などで一般的。各メッセージを独立に圧縮するため、コンテキスト（辞書）がメッセージ内に限定される。
  - 大きな単一メッセージなら有利だが、同種の中サイズメッセージを連続で送る場面では効率が落ちる。

- ストリーミング圧縮（shared encoder/decoder context）:
  - 接続ごとに1つの圧縮コンテキスト（エンコーダ/デコーダ）を作り、各メッセージを送るたびにデータを圧縮して「flush」する。
  - zstdの用語では「フレームを開始して終端しない（ZSTD_e_continue）」を繰り返し、必要に応じてブロック単位でflush（ZSTD_e_flush）するイメージ。
  - 圧縮器はストリームを通じて学習的に辞書（内部状態）を作るため、同種データの反復に非常に強い。H.264のインフレーム vs MJPEGの例えと同様。

- 実測効果:
  - 著者のケース（約100KBのserde flexbufferメッセージを毎秒10件）では、フレーム圧縮済みのzstdに対してさらに約80%の帯域削減を達成。
  - 辞書を事前配布する手間が不要で、接続開始後に自動で「辞書相当」の効果が得られる点が運用上の利点。

- 制約と注意点:
  - gRPC標準ではストリーミングRPCでもメッセージ単位の圧縮しかサポートしておらず、そのままでは適用困難（カスタムプロトコルが必要）。
  - ストリーミング圧縮は遅延とCPU負荷のトレードオフを伴う。flushの頻度や圧縮レベルを調整すること。
  - tower-httpの既存レスポンス圧縮はストリーミングに対応していないため、自作ミドルウェアや別ライブラリが必要になる場合がある。

## 実践ポイント
- 接続（WebSocketやHTTP/2の長寿命接続）ごとに CCtx/DCtx を一個作って再利用する。
- 各メッセージを圧縮後に ZSTD_e_flush でブロックを終端して送ることで、受信側は同一デコーダで連続復号できる。
- flush頻度はネットワークMTU・リアルタイム要件・CPU負荷を見て調整する。小さすぎると効率低下、大きすぎると遅延増。
- gRPC環境ではプロトコル制約を確認。gRPC-web／SSEやカスタムWebSocketなら導入しやすい。
- まずはサーバ／クライアント間でログ（バイト数、CPU時間、パケット化）を取り、per-message圧縮との比較を行う。
- オープンソース実装を活用する（著者はRust crateを公開）。既存ライブラリがストリーミングに未対応な場合は置き換え検討を。

## 最短サンプル（概念的なRustの骨子）
```rust
use std::io::Write;
use zstd_safe::{CCtx, DCtx, InBuffer, OutBuffer, zstd_sys::ZSTD_EndDirective};

struct Encoder { cctx: CCtx<'static> }
impl Encoder {
  fn new() -> Self { Encoder { cctx: CCtx::create() } }
  fn encode(&mut self, data: &[u8], dst: &mut impl Write) -> std::io::Result<()> {
    let mut in_buf = InBuffer::around(data);
    // 継続で圧縮して出力し、最後に flush を呼ぶ
    while in_buf.pos() < data.len() {
      let mut out = [0u8; 16_384];
      let mut out_buf = OutBuffer::around(&mut out);
      self.cctx.compress_stream2(&mut out_buf, &mut in_buf, ZSTD_EndDirective::ZSTD_e_continue)?;
      dst.write_all(&out[..out_buf.pos()])?;
    }
    // メッセージ末尾で flush（受側にブロックを確定させる）
    loop {
      let mut out = [0u8; 16_384];
      let mut out_buf = OutBuffer::around(&mut out);
      let remaining = self.cctx.compress_stream2(&mut out_buf, &mut in_buf, ZSTD_EndDirective::ZSTD_e_flush)?;
      dst.write_all(&out[..out_buf.pos()])?;
      if remaining == 0 { break; }
    }
    Ok(())
  }
}

struct Decoder { dctx: DCtx<'static> }
impl Decoder {
  fn new() -> Self { Decoder { dctx: DCtx::create() } }
  fn decode(&mut self, data: &[u8], dst: &mut impl Write) -> std::io::Result<()> {
    let mut in_buf = InBuffer::around(data);
    let mut buf = [0u8; 16_384];
    loop {
      let mut out_buf = OutBuffer::around(&mut buf);
      self.dctx.decompress_stream(&mut out_buf, &mut in_buf)?;
      let pos = out_buf.pos();
      if in_buf.pos() >= data.len() && pos == 0 { break; }
      dst.write_all(&buf[..pos])?;
    }
    Ok(())
  }
}
```

## 引用元
- タイトル: Streaming compression beats framed compression
- URL: https://bou.ke/blog/compressed/
