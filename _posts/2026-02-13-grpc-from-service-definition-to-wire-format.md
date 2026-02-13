---
layout: post
title: "gRPC: From service definition to wire format - gRPC：サービス定義からワイヤフォーマットまで"
date: 2026-02-13T22:21:22.828Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kreya.app/blog/grpc-deep-dive/"
source_title: "gRPC deep dive: from service definition to wire format | Kreya"
source_id: 46944430
excerpt: "gRPCの.protoからHTTP/2上の5バイトワイヤフォーマットまで実践的に解説"
image: "https://kreya.app/thumbnails/default.png"
---

# gRPC: From service definition to wire format - gRPC：サービス定義からワイヤフォーマットまで
gRPCの“中身”を覗いて、.protoからバイト列まで理解する — 隠れた仕組みを短時間で掴む

## 要約
gRPCは単なるシリアライザではなく、.protoを起点にHTTP/2上でストリーミングやメタデータ、エラー表現、圧縮まで統一的に扱うRPCエコシステムである。本記事はサービス定義から実際のワイヤフォーマット（5バイトヘッダ＋ペイロード）までを平易に解説する。

## この記事を読むべき理由
日本のスタートアップや大手企業がマイクロサービス／モバイル最適化／IoTで低遅延・高効率通信を求める中、gRPCの内部挙動を理解しておくと設計・デバッグ・性能改善が格段に楽になるため。

## 詳細解説
- 契約ファースト（contract-first）  
  .protoファイルがAPIの唯一の真実（データ構造とRPCメソッド）になる。protocで各言語のスタブが生成され、クライアント・サーバが型で一致する。

  ```protobuf
  // protobuf
  package fruit.v1;
  service FruitService {
    rpc GetFruit (GetFruitRequest) returns (Fruit);
    rpc ListFruits (ListFruitsRequest) returns (stream Fruit);
    rpc Upload (stream Fruit) returns (UploadSummary);
    rpc Chat (stream ChatMessage) returns (stream ChatMessage);
  }
  ```

- ストリーミングモデル（4種類）  
  Unary（通常のREQ→RESP）、Server streaming（REQ→複数RESP）、Client streaming（複数REQ→1RESP）、Bidirectional streaming（双方独立送信）。これらはAPI設計の第一選択肢として扱うべき。

- メタデータ（headers/trailers）  
  キー値ペア（HTTP/2ヘッダ相当）。認証トークン、トレースID、インフラ情報などを運ぶ。バイナリ値はキー末尾に -bin を付けて扱う。

- HTTP/2上のマッピングとURL生成  
  各RPCはHTTP/2の1ストリームに対応。パスは /{Package}.{Service}/{Method}（ex: /fruit.v1.FruitService/GetFruit）。これにより単一TCP接続で多数のRPCを多重化可能。

- ワイヤフォーマット：5バイトの長さプレフィクス  
  DATAフレーム内の各メッセージは独立していて、先頭5バイトで示す。
  - 1バイト：圧縮フラグ（0=未圧縮, 1=圧縮）
  - 4バイト：ビッグエンディアンのメッセージ長
  例（ペイロード10バイト、未圧縮）:
  ```
  // text
  00 00 00 00 0A <protobuf-payload(10 bytes)>
  ```

- ステータスとトレーラ（trailers）  
  HTTPステータスは多くの場合200。実際のRPCステータスは trailers（grpc-status, grpc-message）で伝えられる。詳細エラーは grpc-status-details-bin に base64 された protobuf（google.rpc.Status）を載せられる。

- 圧縮とネゴシエーション  
  クライアントが grpc-accept-encoding を送り、サーバは grpc-encoding を返す。圧縮はメッセージ単位でフラグを立てて行う。モバイル回線では効果があるが、小さなメッセージでは逆に増えることがあるため計測が必須。

- 代替トランスポートとブラウザ対応  
  UnixドメインソケットやWindowsのNamed PipeでTCPを回避可能。ブラウザはHTTP/2の低レベル制御ができないため gRPC-Web が利用され、トレーラを本文内に埋め込む等の適応を行う。

## 実践ポイント
- .protoを単一の真実にしてCIで型生成を自動化する。  
- ストリーミングを使うか否かは遅延/メモリ/再試行モデルを基準に選ぶ。  
- デバッグには grpcurl / Kreya / wireshark（HTTP/2デコード）を併用し、ヘッダ・トレーラ・5バイトフレームを確認する。  
- エラーは grpc-status-details-bin を利用して構造化し、クライアントでデコードして処理する。  
- 圧縮は環境別にベンチする（モバイル⇄データセンタ）。小メッセージは非圧縮の方が良い場合が多い。  
- ブラウザ対応が必要なら gRPC-Web を検討し、プロキシ（Envoy等）で変換する。  
- ローカルテストはUnix Domain Socketで高速化すると便利。

短く言えば、gRPCは.protoで始まりHTTP/2＋5バイトフレームで終わる一貫したスタック。設計とデバッグの要所を押さえれば、性能と信頼性が大きく改善する。
