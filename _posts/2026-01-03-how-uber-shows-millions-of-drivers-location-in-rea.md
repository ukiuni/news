---
  layout: post
  title: "How Uber Shows Millions of Drivers Location In Realtime - Uberが数百万ドライバーに位置情報をリアルタイム表示する方法"
  date: 2026-01-03T07:45:56.680Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://sushantdhiman.substack.com/p/how-uber-shows-millions-of-drivers"
  source_title: "How Uber Built a Real-Time Push System for Millions of Location Updates | EP: 4 Behind The Screen"
  source_id: 472335259
  excerpt: "RAMENとFireballでポーリング廃止、gRPCで秒単位の高信頼位置配信を実現"
  image: "https://substackcdn.com/image/fetch/$s_!FZvf!,w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54f94c33-4083-4460-8580-0532363c0182_2500x1455.png"
---

# How Uber Shows Millions of Drivers Location In Realtime - Uberが数百万ドライバーに位置情報をリアルタイム表示する方法
ポーリング地獄を脱した「RAMEN」──秒単位の位置配信を可能にした設計と、日本のサービスで使える実践ノウハウ

## 要約
Uberは大量のモバイルクライアントに対する位置更新を、ポーリングからプッシュへ移行し、RAMEN（Realtime Asynchronous Messaging Network）とFireballによる判定ロジックで効率化。初期はSSEを使い、その後gRPC+Protocol Buffersへ移行して遅延と信頼性を大幅に改善した。

## この記事を読むべき理由
日本でも配車、フードデリバリー、物流、モバイルIoTなどリアルタイム位置情報が重要な分野が増加中。スケールとバッテリ効率、モバイルネットワークの不安定さを両立する設計は即戦力になる。

## 詳細解説
- 問題点（ポーリングの限界）  
  - クライアントが数秒ごとにサーバへ位置要求する方式は応答性確保のために頻繁なリクエストを必要とし、サーバ負荷増大、バッテリ消費、コールドスタート時の多数API呼び出しを招いた。Uberではある時点でリクエストの約80%が位置プーリングだった。

- RAMEN + Fireball のアーキテクチャ  
  - Fireball：各種イベント（ユーザがリクエスト、ドライバーの受諾、位置変化など）を監視し「本当に送るべきか」を決定するマイクロサービス。不要な微小変化は送らないことでノイズを削減。  
  - API Gateway：Fireballが示した“いつ”に必要な最小データを受け取り、端末属性（Locale、OS、アプリ版など）を付与してRAMENへ渡す。  
  - RAMEN：端末へ実際にプッシュする基盤。初期はServer-Sent Events（SSE）を採用。

- SSE時の実装ポイント（信頼性の担保）  
  - シーケンス番号でメッセージ整列（例：/ramen/receive?seq=0で接続開始）。TCPの性質と接続再確立で未配信シーケンスを再送。  
  - ハートビート（1バイト）を4秒ごと送信、7秒受信が途絶したら切断と判断。  
  - クライアントは30秒ごとに /ramen/ack?seq=N を送り、古いメッセージのフラッシュやバックログ制御を補助。  
  - この構成はSSEの単方向性の制約をACKで補うことで「少なくとも一度の配信」を狙う工夫。

- なぜgRPCへ移行したか  
  - SSEだと配信状態の確定に遅延（最大30秒）や、イベント用接続とシーケンス管理用接続の二重管理、JSONによるバイナリ非対応などの問題が残った。  
  - gRPCにすると双方向ストリーミングが可能になり、同一接続でACKや再送制御が行え、Protocol Buffersによりバイナリ/効率性も改善。結果、p95の接続レイテンシが約45%改善、プッシュ成功率も1–2%向上したと報告されている。

## 実践ポイント
- プッシュを第一選択にする：頻繁なポーリングはサーバコストと端末バッテリを圧迫する。可能ならプッシュ設計へ移行する。  
- イベント判定層（Fireball相当）を入れる：全変更を送らず、意味あるイベントのみをトリガーして帯域と端末負荷を下げる。  
- シーケンス＋ACK＋ハートビートは必須：モバイルネットワークは断続的なので、再接続・再送のためのシーケンス管理と定期ACK、短めのハートビート閾値を設ける。  
- プロトコル選定はユースケース次第：片方向で軽量な互換性重視ならSSE、双方向やバイナリ・低遅延重視ならgRPC+protobufを検討。  
- モバイル考慮（SDK・バイナリサイズ・セキュリティ）：古いOSや帯域制限のある環境向けにフォールバック（HTTP Long PollingやWebSocket）を用意する。  
- 測定とSLA設計：p95接続時間、プッシュ成功率、再接続頻度などをKPI化して改善効果を数値で把握する。  
- 日本向けユースケース：配車、即時配送、荷物追跡、現場作業員の安全監視など、ネットワーク品質が変動する環境での応答性改善に直結する。

参考：Uber Engineeringの技術ブログには実装や移行の詳細がある（RAMENのSSE版→gRPC版の比較を掲載）。上記の設計パターンは、日本のモバイルサービスでも即応用可能で、スケールとユーザ体験の両立に有効。
