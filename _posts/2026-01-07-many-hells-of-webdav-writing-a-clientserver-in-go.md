---
  layout: post
  title: "Many Hells of WebDAV: Writing a Client/Server in Go - WebDAV地獄：Goでクライアント／サーバを書く話"
  date: 2026-01-07T16:20:54.453Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://candid.dev/blog/many-hells-of-webdav"
  source_title: "Many Hells of WebDAV | Candid Development"
  source_id: 46527775
  excerpt: "WebDAVの実装差を暴き、Goで短期間に動くCalDAVクライアント/サーバを作る実践ノウハウ"
  image: "https://candid.dev/candiddev-wide.png"
---

# Many Hells of WebDAV: Writing a Client/Server in Go - WebDAV地獄：Goでクライアント／サーバを書く話
WebDAVの「規格はあるけど現実は別物」な罠を突破して、Goで実用的なCalDAVクライアント／サーバを作るためのリアルな教訓

## 要約
RFCどおりに実装しても動かないことが多い——著者は既存ライブラリに頼らず、RFC読み込み＋実運用のリバースエンジニアリングで最小限の機能（特にカレンダーのCRUDと同期）を短期間で実装した経験を共有している。

## この記事を読むべき理由
- Web連携やカレンダー同期を扱う日本のサービス開発者にとって、Apple/Googleの挙動差や実装の“癖”は直接の障害になる。  
- RFC依存だけだと泥沼にハマる実例と、実務で使える回避策（リバースエンジニアリング、柔軟なXML処理、テスト戦略）が学べる。

## 詳細解説
- 背景と問題点  
  WebDAV/CalDAVは古くからある標準（RFC 2518 → RFC 4918 ほか拡張群）だが、現実のサービスはRFCを部分的にしか実装しなかったり、独自の振る舞いをしている。結果として「仕様どおり作れば互換する」は期待通りにならない。著者はHomechart向けにGoでクライアント／サーバを作ろうとしてこの問題に直面した。

- 既存実装の限界  
  go-webdav など既存のGoライブラリを確認したが、サーバ側の collection synchronization（サーバサイドのコレクション同期）など必要な機能が足りず、データモデルともインターフェースが合わなかったため自前実装を選択している。製品機能として重要なら実装に対する所有権を持つ方が現実的、という判断だ。

- RFCよりも「実装の観察」へ  
  RFCを最初から全て実装するのは時間がかかり、不要な“レガシーの層”に捕まる。そこで著者は主要クライアント（Apple Calendar, DavX, Thunderbird）とサーバ（Apple iCloud, Google Calendar, Radicale）の通信をプロキシやWiresharkでキャプチャし、実際に交換されるリクエスト/レスポンスとヘッダを洗い出すことで短期間に必要なAPIをマッピングした。

- XML処理の現実  
  WebDAVはXMLベースで、リクエストやレスポンスのスキーマが緩く「自由度が高い」場合が多い。Go標準のencoding/xmlは扱いにくかったため、JavaScriptのDOMライクにノードを操作できるラッパーを作り、柔軟にマシュ／アンマシュできる仕組みを用意した。これにより「最良ケースのみを想定したstruct」を大量に書くことを避けられた。

- 標準と現実の乖離（スタンダードは提案に過ぎない）  
  大手（Apple, Google）はRFCの半分程度しか実装しないことが多く、Capabilityを広告するHTTPレスポンスも必ずしも正確でない。クライアント側も実装がバラバラで、効率的なsync-collectionを使うクライアントが多い一方、Apple Calendarはctag/etagベースの方式を使うなど差がある。つまり「相手に合わせる」柔軟性が必要になる。

## 実践ポイント
- まずは最小実装を定義する  
  カレンダーでは「イベントのCRUD」と「同期（sync-collection または ctag/etag）」あたりを最優先にする。RFC全文を一度に実装しようとしない。

- 実際のトラフィックを観察する  
  自サービスが対応したいクライアント・サーバの通信をプロキシ（mitmproxy 等）やWiresharkでキャプチャして、どのヘッダ／XML要素が実際に飛んでいるかを確認する。

- 柔軟なXMLパーサを用意する  
  厳密なstructバインディングに頼らず、ノード操作が容易なラッパーを作るか既存のライブラリを活用して異常系にも耐える設計にする。

- ヘッダとボディ両方をしっかり見る  
  WebDAVの挙動はHTTPヘッダ（ETag, If-Match, Content-Type, 特殊なCapabilityヘッダ等）に依存することが多い。ヘッダごとに処理を分けるテストを書こう。

- プロバイダごとのフォールバックを用意する  
  AppleやGoogleの「癖」に対応するため、sync-collectionが無ければctag/etagの経路にフォールバックするなど多経路対応を組み込む。

- 実機対策の自動テストを用意する  
  主要プロバイダ（iCloud, Google）や代表的クライアントを対象とした統合テスト／シナリオテストを用意し、挙動差を検出できるようにする。

- 日本市場への示唆  
  日本でもカレンダー同期は業務アプリ、医療予約、社内グループウェア連携などで需要が高い。Apple/iCloudやGoogle Calendarを相手にするケースが多く、それらの“非準拠”ぶりを前提に設計することが、開発工数と運用コストを抑える近道になる。

短く言えば：仕様書を鵜呑みにせず、観察→最小実装→柔軟パーサ→プロバイダ別フォールバック、のサイクルで進めるとWebDAV地獄を生き抜ける。
