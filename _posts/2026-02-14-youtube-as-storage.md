---
layout: post
title: "YouTube as Storage - YouTubeをストレージとして使う"
date: 2026-02-14T09:46:30.566Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/PulseBeat02/yt-media-storage"
source_title: "GitHub - PulseBeat02/yt-media-storage: https://www.youtube.com/watch?v=l03Os5uwWmk"
source_id: 47012964
excerpt: "FFV1/MKVと冗長化でYouTubeをファイル倉庫化するOSS（暗号化対応・復元可）"
image: "https://opengraph.githubassets.com/b36545ecb47fbebb1150f74616d91e410302fabb11f60a4cf6dc202ccac9a955/PulseBeat02/yt-media-storage"
---

# YouTube as Storage - YouTubeをストレージとして使う
動画で「ファイルを保存する」──YouTubeをファイル倉庫化する発想を試す

## 要約
任意のファイルをロスレス動画（FFV1/MKV）に変換して保存し、再び元に戻せるオープンソースツール。GUIとCLIを備え、フォウンテンコードによる冗長化やオプションの暗号化に対応します。

## この記事を読むべき理由
一風変わったバックアップ／アーカイブ手法として、低コストで長期保存を考える際の選択肢になります。日本の開発現場や個人でのメディア保存、災害対策や分散バックアップの発想を広げます。

## 詳細解説
- 基本概念：ファイルを小さなチャンクに分割→フォウンテンコード（Wirehair）で冗長化→各パケットを動画フレームに埋め込み→FFV1コーデック＋MKVコンテナでロスレス出力。復号ではフレームからパケットを抽出して再構築します。  
- 冗長化：フォウンテンコードにより一部のフレーム欠損や切り抜きがあっても復元可能性が高まります（ストリーミング媒体向けの耐障害性を意識）。  
- 暗号化：libsodiumのXChaCha20-Poly1305でパスワード保護が可能。パスワードを失うと復元不能になります。  
- 実装・依存：C++23で実装、FFmpeg（FFV1）、Qt6（GUI）、libsodium、OpenMPを利用。出力は4K（3840x2160）@30fpsがデフォルト。  
- 提供形態：CLI（media_storage）とGUI（media_storage_gui）。GPL-3.0ライセンスで公開。CI/CDのビルド成果物がリポジトリで配布されています。  
- 注意点：YouTube等への公開アップロードはサービス規約や著作権、運用ポリシーに抵触する可能性があるため、公開先の規約確認が必須。大容量動画になるためストレージや転送コスト、再生仕様にも注意。

ビルド／使用の基本例：
```bash
# ビルド（例）
cmake -B build
cmake --build build
```

```bash
# CLI 使用例
./media_storage encode --input example.bin --output example.mkv --encrypt --password secret
./media_storage decode --input example.mkv --output example.bin
```

## 実践ポイント
- まず小さなテストファイルでエンコード→デコードの一往復を確認する（整合性チェック）。  
- 暗号化を使う場合はパスワードを安全に管理する（忘れると復元不可）。  
- 大容量の出力動画を扱うためディスク容量とアップロード帯域を確保する。  
- 公開プラットフォームに置く前に利用規約・法律面を確認する。  
- 開発環境：Ubuntu/DebianやmacOSでのパッケージ例がREADMEに記載されているので依存を先に整える。

（出典：PulseBeat02 / yt-media-storage — GPL-3.0）
