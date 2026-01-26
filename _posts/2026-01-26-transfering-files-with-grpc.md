---
layout: post
title: "Transfering Files with gRPC - gRPCでのファイル転送"
date: 2026-01-26T14:17:02.102Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kreya.app/blog/transfering-files-with-grpc/"
source_title: "Transfering files with gRPC | Kreya"
source_id: 46765273
excerpt: "gRPCは大容量転送可能だが、チャンク設計とバッファ再利用が必須で多くはRESTが有利"
image: "https://kreya.app/thumbnails/default.png"
---

# Transfering Files with gRPC - gRPCでのファイル転送
gRPCで大容量ファイルを渡すべきか？RESTと実装・性能を比べてわかった最適解

## 要約
gRPCでも大容量ファイル転送は可能だが、メッセージ設計（チャンク分割）やバッファ管理に注意が必要。単純実装はメモリを浪費し、REST(特にHTTP/1.1)の方が簡潔かつ高速なケースが多い。

## この記事を読むべき理由
日本でもマイクロサービスやgRPC採用が増える中、ファイル配信をどう実装すべきかはよくある意思決定問題。特にクラウドストレージやモバイル向け配信でのコスト／性能に直結します。

## 詳細解説
- 問題点
  - 大きなファイルをそのままメモリにバッファするとOOMになる可能性が高い。
  - RESTでの正解はファイルシステム→レスポンスへストリームで流すこと（例：ASP.NET CoreのPhysicalFileResult）。
  - JSONにBase64で埋め込むのはサイズ増（約30%）かつ多くの言語で全体をメモリに乗せがちなのでNG。

- gRPCの制約と解法
  - gRPCは「1メッセージをストリームで部分送信する」という概念はなく、代わりに複数メッセージをストリーミングする（server-streaming）。
  - 解法はファイルを小さなチャンク（例 32KB）に分け、最初にメタデータ、続けてチャンクを送る設計。

protobuf例:
```protobuf
syntax = "proto3";
package filetransfer;
import "google/protobuf/empty.proto";

service FileService {
  rpc DownloadFile(google.protobuf.Empty) returns (stream FileDownloadResponse);
}

message FileDownloadResponse {
  oneof data {
    FileMetadata metadata = 1;
    bytes chunk = 2;
  }
}
message FileMetadata {
  string file_name = 1;
  string content_type = 2;
  int64 size = 3;
}
```

- C#での実装ポイント
  - naive実装は毎リクエストで新バッファを割り当て、ByteStringコピーで大量のアロケーションを招く。
  - 改善策：MemoryPool等でバッファを再利用し、Unsafe系APIでコピーを抑える（言語/実装依存の最適化）。
```csharp
// 要点のみ（最適化版のイメージ）
public override async Task DownloadFile(Empty req, IServerStreamWriter<FileDownloadResponse> resp, ServerCallContext ctx) {
  await using var fs = File.OpenRead("/files/test-file.pdf");
  await resp.WriteAsync(new FileDownloadResponse { Metadata = new FileMetadata { /*...*/ } });
  using var rented = MemoryPool<byte>.Shared.Rent(32 * 1024);
  var mem = rented.Memory;
  int read;
  while ((read = await fs.ReadAsync(mem)) > 0) {
    await resp.WriteAsync(new FileDownloadResponse { Chunk = UnsafeByteOperations.UnsafeWrap(mem.Slice(0, read)) });
  }
}
```

- クライアント側（例：Kreya）は受け取ったチャンクを結合してファイルに復元する必要がある。

- 転送オーバーヘッドと性能
  - gRPCはHTTP/2上でチャンクごとに小さなフレームオーバーヘッドが発生（例: チャンク当たり数十バイト）。
  - HTTP/1.1の単一ボディによるダウンロードはオーバーヘッドが小さい傾向。
  - 著者のローカル比較では、最適化したgRPCは良好だがHTTP/1.1 RESTが最速。HTTP/2はフレーム分割で遅くなる例があった。
  - naive gRPCは大量の総メモリアロケーションでGC負荷が激増。

## 実践ポイント
- 基本方針：ファイル配信は可能ならREST(HTTP/1.1)で提供するのがシンプルで高速。
- gRPCを使う必要がある場合：
  - server-streamingでチャンク化する（チャンクサイズ ≈ 16–32KB が定番）。
  - バッファを再利用し、不要なコピーを抑える（MemoryPoolやUnsafe API）。
  - 先にメタデータを送る設計にしてクライアントで再構築する。
- 大容量はS3等のプリサインURLで直接配信させるのが最も効率的。
- 再開機能が必要なら自前より標準プロトコル（例: tus.io）を検討。
- 日本市場向けの注意：モバイル／遅延回線への配慮、セキュリティ（TLS／認証）、そしてクラウド課金（転送料）も設計に組み込むこと。

以上。
