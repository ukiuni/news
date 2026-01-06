---
  layout: post
  title: "Zero heap allocation HTTP server using OxCaml - OxCamlで実現するゼロヒープ割当てHTTPサーバ"
  date: 2026-01-06T20:55:31.857Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/avsm/httpz"
  source_title: "GitHub - avsm/httpz: Zero heap allocation HTTP server using OxCaml. v experimental!"
  source_id: 837474848
  excerpt: "OxCamlでゼロ割当てのHTTPサーバが14.6M req/sを実現、GC無視で超高速"
  image: "https://opengraph.githubassets.com/86048768c5d0939b8df30a8cce6e49817c4e1c2e439a50b3fde0b500572ff17b/avsm/httpz"
---

# Zero heap allocation HTTP server using OxCaml - OxCamlで実現するゼロヒープ割当てHTTPサーバ
魅力タイトル: OxCamlで「GCを忘れる」超高速HTTPパーサ — 14.6M req/sを叩き出すゼロ割当てアプローチ

## 要約
OxCamlで書かれたHTTP/1.1パーサ／シリアライザ「httpz」は、スタックベースのデータ表現とゼロコピーI/Oでヒープ割当てをほぼ排除し、高スループット・低レイテンシを達成しています。

## この記事を読むべき理由
GCやヒープ割当てのオーバーヘッドがボトルネックになる日本の低レイテンシサービス（エッジサーバ、APIゲートウェイ、ネットワーク機器、IoTバックエンドなど）にとって、メモリ割当を抑えた実装は運用コスト削減と安定性向上に直結します。OCaml系の新興技術に興味があるエンジニアは必読です。

## 詳細解説
- 基本思想  
  httpzは「パーサ結果をヒープに置かない」ことを第一に設計。OxCamlの未ボックス化レコード（#{...}）とローカルリスト（@ local）を活用し、リクエスト表現やヘッダリストをスタック領域で扱います。文字列は入力バッファ（bigarray）に対するオフセット＋長さで参照する「スパン」ベースで、余分なコピーを避けます。

- 主な技術要素  
  - 未ボックス化レコード（#{...}）で構造体をスタック割当て  
  - ローカルリスト（@ local）でヘッダ等をローカルに蓄積（ヒープを増やさない）  
  - スパン（offset+length）で文字列参照、コピーを回避  
  - 32KBの事前確保読み取りバッファを再利用  
  - bigarray（bigstring）への直接I/Oでゼロコピーの入出力  
  - HTTP/1.1（メソッド、ヘッダ、チャンク転送、keep-alive）対応  
  - Asyncベースの静的ファイルサーバ（同時接続10k想定）。Linuxでio_uring対応を予定

- 性能指標（元リポジトリのベンチ結果）  
  - リクエスト処理レイテンシ（ns/op）：Small 69 vs 218（3.14x）、Medium 792 vs 1690（2.13x）、Large 1771 vs 4017（2.27x）  
  - スループット：14.6M req/s（httpz） vs 4.6M req/s（比較対象）  
  - ヒープ単語数削減：Small 94x、Medium 399x、Large 829x と大幅削減  
  - 細部タイミング：最小リクエストのパース 209ns（3 words割当）や、50ヘッダで 7.7μs（3 words）など、ほとんど割当てが発生しない

- 付属ツール・使い方（簡潔）  
  - OxCamlコンパイラが必要（https://oxcaml.org/）  
  - 同梱のAsync静的ファイルサーバで簡単に試用可能（dune execで起動）  
  - ベンチは dune exec bench/* で実行

## 実践ポイント
- まず試す：OxCaml環境を用意してリポジトリをクローンし、static serverを起動して挙動を確認する。  
  ```bash
  # Clone & run (例)
  git clone https://github.com/avsm/httpz.git
  cd httpz
  dune exec bin/httpz_server.exe -- -d . -p 8080
  ```
- プロダクションでの使いどころ：低遅延APIエンドポイント、エッジキャッシュ、静的コンテンツ配信、低リソースVMやコンテナでの高密度ホスティング。GCストールを極力避けたいサービスに向く。  
- 学ぶこと：未ボックス化型やローカルリスト、スパンベースのパースなど「ゼロ割当て」設計パターンは他言語でも応用可能（CやRustのゼロコピー設計に近い発想）。  
- 注意点：まだ実験的プロジェクトであり、IOの並列化（io_uring）や完全な機能網羅は進行中。運用前に十分なテストを行うこと。

短時間で実効性のある性能改善を狙いたいエンジニアには、有力な学びと実験素材を提供するリポジトリです。
