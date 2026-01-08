---
  layout: post
  title: "Loongarch Improvements with Box64 - Loongarch向けBox64の改善"
  date: 2026-01-06T18:49:13.258Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://box86.org/2026/01/new-box64-v0-4-0-released/"
  source_title: "Loongarch Improvements with Box64"
  source_id: 46514807
  excerpt: "Box64 v0.4.0でLoongArch上にSteam/Wine/Protonが実用域へ急接近"
---

# Loongarch Improvements with Box64 - Loongarch向けBox64の改善
LoongArchでSteamが動く？Box64 v0.4.0が切り拓く非x86ゲーミングの実用化

## 要約
Box64 v0.4.0でLoongArch（とRISC‑V／ARM64）のサポートと性能改善が大きく進み、Linux版SteamやWine/Protonが実用域に近づいた。メモリ削減やダイナレック改良、同期方式（ESync/FSync/NTSync）周りの対応が目玉。

## この記事を読むべき理由
- 日本でもエッジな非x86（LoongArch / RISC‑V / ARM64）マシンを使う動きが出ており、ゲームや互換レイヤの実用性が急速に高まっている。
- Box64 v0.4.0の実装と設定知識は、ローカルでSteamやProtonを動かす際の成功確率を大きく左右するため、導入前に押さえておきたい技術ポイントがまとまっている。

## 詳細解説
- コア改善
  - プレフィクス opcode デコーダをインタープリタと3つのダイナレック（dynarec）バックエンドに実装。特殊なプレフィクスを汎用的に扱えるようになり、ハックや冗長コードを削減。結果として多くのソースファイルが不要になり保守性が向上。
  - ダイナレック側では希少なオペコードも自動的にサポートされるケースが増え、追加実装なしで恩恵が出る箇所が増大。

- メモリ管理
  - libcef等を使うアプリ（例：Steam）は起動後に大量メモリを使うことがあるため、「生成済みのネイティブ変換ブロックの未使用検出＋削除」でメモリの再利用を試みる仕組みを導入中。まだ作業は継続中だが今後のリリースで改善が期待される。

- ループ最適化
  - ループ開始前に必要なXMM/YMMレジスタを事前ロードするなど、ループ検出と最適化を強化。特定ケースで大きな速度向上が見込める。

- プラットフォーム別状況
  - ARM64: GB10用ビルドプロファイル追加、ダイナレックのリファクタで性能向上の下地を整備。
  - RISC‑V: PLCT Labsらの貢献でダイナレックがかなり成熟。Steam/Proton/Wineが動作するが、ハードウェアのアドレス空間制限（39bit）やSV48非対応だとDRMやWindows syscall系は制約あり。
  - LoongArch: 今回最も進展。Steam（Linux版）とWine/Protonが動作。重要な注意点は「カーネルで4Kページサイズを使うこと」—多くのLoongArch環境はデフォルトで16Kだが、4Kオプションが必要。

- 同期機構（ESync / FSync / NTSync）
  - ESync/FSyncは高速化を狙う反面、一部のゲームランチャ（Rockstar、Xboxサービス等）で同期不具合を起こすことがある。問題が出る場合は環境変数で無効化するのが実用的。
  - NTSyncは非常に有望だが、カーネル側の対応（NTSync有効ビルド）と新しいWine/Proton-GEが必要。x86向けディストリや一部のビルド（Armbian、AOSCの一部）はNTSync有効だが、Debian/UbuntuのARM64系は未対応の場合が多い。

## 実践ポイント
- ソース取得とビルド（概要）
```bash
# bash
git clone https://github.com/ptitSeb/box64.git
cd box64
mkdir build && cd build
cmake ..   # 必要な依存を事前にインストール
make -j$(nproc)
sudo make install
```
- LoongArchでSteamを試す前に
  - カーネルが4Kページサイズで起動していることを確認／切り替える（ディストリ固有オプションあり）。
  - GPUドライバ（e.g. AMD系）とハードウェアエンコードがあると録画や負荷時の体感が改善する。
- Proton実行時のトラブル対処
  - 起動しない／ランチャが動かない場合はまずESync/FSyncを無効化:
    - Steamの起動オプションに: PROTON_NO_ESYNC=1 PROTON_NO_FSYNC=1 %command%
  - NTSyncを使うなら、カーネルとProton/Wine（Proton‑GE推奨）両方を最新化する。
- 期待値管理
  - Box32はまだ実験的で不安定。ダウンロード／大きな処理でクラッシュする可能性あり。
  - DRMやWindows syscall依存のタイトルは、RISC‑VやLoongArchで動かないケースが残る（SV48や特殊パッチが必要）。

Box64 v0.4.0は「非x86でのゲーム環境」を一段階実用に近づける重要なリリースです。LoongArch環境を持っている／検討している日本の技術者や趣味家は、まずソースを落としてビルドし、上の実践ポイントを試してみてください。
