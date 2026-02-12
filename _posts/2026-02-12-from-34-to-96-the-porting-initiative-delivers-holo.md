---
layout: post
title: "From 34% to 96%: The Porting Initiative Delivers – Hologram v0.7.0 - 34%から96%へ：Porting Initiativeが実現したこと — Hologram v0.7.0"
date: 2026-02-12T04:53:16.619Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hologram.page/blog/porting-initiative-delivers-hologram-v0-7-0"
source_title: "From 34% to 96%: The Porting Initiative Delivers - Hologram v0.7.0 - Hologram"
source_id: 46982943
excerpt: "Hologram v0.7.0でErlang移植が96%到達、ブラウザでElixirが実用域に拡大"
image: "https://hologram.page/images/og/blog/porting-initiative-delivers-hologram-v0-7-0-47ed5fc67d8d5349b19eb04272961f6c.jpg"
---

# From 34% to 96%: The Porting Initiative Delivers – Hologram v0.7.0 - 34%から96%へ：Porting Initiativeが実現したこと — Hologram v0.7.0
ついにブラウザでここまで動く！Hologram v0.7.0でElixir/Erlangの標準機能が大幅拡張

## 要約
Hologram v0.7.0で150のErlang関数がJavaScriptへ移植され、Erlangランタイムのフェーズ1カバレッジが34%→96%に到達。Elixir標準ライブラリのブラウザ実行準備率も74%→87%に向上しました。

## この記事を読むべき理由
ブラウザ上でElixirを使ったフルスタック開発やローカルファーストアプリを検討している日本の開発者にとって、クライアント側で利用できる標準機能の幅が劇的に広がった重要なマイルストーンです。実務で使える関数群が一気に増え、移植の進捗や互換性、開発体験の改善点が分かります。

## 詳細解説
- 進捗の要点  
  - 追加で150関数を移植し、Phase 1に必要なErlang関数は228/238（96%）に。Elixir stdlib準備度は74%→87%。  
  - 対象は文字列、集合、コレクション、ビット列、Unicode正規化、時間、ファイルパス操作など。プロセス関連はPhase 2へ保留。

- 主要に動くようになった機能例  
  - 文字列：String.split/3, String.replace/4, String.length/1, Jaro距離、titlecase 等  
  - コレクション：Enum/List系（ソート、フィルタ、fold 等）  
  - Set：MapSetの作成・交差・和集合・メンバー判定  
  - ビット列/バイナリ操作、Unicode正規化（NFC/NFD/NFKC/NFKD）、グラフェム分割  
  - 数学（ceil/floor/べき/対数等）、モノトニック時間・変換、クライアント側パス操作（Path.join等）

- リリースでの改善点（抜粋）  
  - コンパイル高速化（非同期のコンパイラ変異）  
  - cross-platformなmixセットアップ、NixOSでのBiomeフォールバック対応  
  - Parserのraw HTMLブロック出力、:erlang.float_to_binary/2の追加オプション等  
  - バグ修正：OPFSを使ったハイブリッドストレージでのQuota回避、Mapの不変性保持、テンプレート補間のString.Chars準拠、URLパラメータの正確なエンコード/デコードなど

- インフラ面の下地  
  - クライアント側ERTSの基礎（ノードテーブル、シーケンス、UTF-8デコーダ等）やETSサポートの土台、ページスナップショットの三層保存（メモリ／OPFS／session）など、今後の機能拡張に向けた整備が進行。

## 実践ポイント
- すぐ試す（mix）  
  - mix.exsで依存を更新: {:hologram, "~> 0.7.0"} を追加／更新し、mix deps.update hologram を実行。  
- ブラウザで試せる範囲を確認  
  - String、Enum、MapSet、Path、Unicode、Float系などクライアントで期待通り動くか小さなサンプルを作って検証。  
- NixOS/特殊環境の注意点  
  - Biomeバイナリの互換性問題がある場合は今回のフォールバック改善を確認。  
- 既存コードのチェックポイント  
  - プロセス依存の機能はまだPhase 2なので、プロセスや並行処理に依存するロジックは動作対象外と考慮する。  
- 情報収集／貢献  
  - Client Runtime Referenceやリリースノート、GitHubの移植一覧を確認して未移植関数やエッジケースを把握。プロジェクトへの貢献やスポンサー支援も検討。

短く言えば、v0.7.0で「ブラウザ上で使えるElixirの実用域」が大幅に拡張されました。実プロジェクトでの検証を始める良いタイミングです。
