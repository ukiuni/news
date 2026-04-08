---
layout: post
title: "Converting old home movie DVDs into a private streaming site - 古いホームムービーDVDをプライベートなストリーミングサイトに変換する"
date: 2026-04-08T21:22:13.858Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/peter/converting-old-home-movie-dvds-into-a-private-streaming-site-5bmb"
source_title: "Converting old home movie DVDs into a private streaming site - DEV Community"
source_id: 3472952
excerpt: "古いDVDをISO→MP4化しR2で家族限定ストリーミング、スマホ再生可"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fyia9i5a1wa8hlkdhoiwy.png"
---

# Converting old home movie DVDs into a private streaming site - 古いホームムービーDVDをプライベートなストリーミングサイトに変換する
思い出をスマホで見返せる「家族専用ストリーミング」を手軽に作る方法

## 要約
古いホームムービーDVDをISOでバックアップ→ffmpegでMP4に変換→Cloudflare R2＋Pagesで家族専用の軽量ストリーミングサイトにする手順を、CLIツール中心に解説します。

## この記事を読むべき理由
実家や押し入れに眠るDVDは再生機がなくても劣化します。低コストかつ技術的ハードルが低い手順で「安全に保管」かつ「スマホで簡単に再生できる」形にできるため、家族の思い出を守りたい日本の読者に有用です。

## 詳細解説
- 必要なツール（無料）
  - ddrescue（ビット単位で安全に吸い出す。ddはエラーで止まるがddrescueはリトライ可能）  
    - brew install ddrescue
  - ffmpeg（VOB→H.264 MP4に変換）
  - wrangler（Cloudflare R2へのアップロード用CLI）
  - Cloudflare Pages + R2（ホスティングとオブジェクトストレージ）
  - Cloudflare Access（アクセス制限：家族メールだけ許可）
- ワークフロー概要
  1. ISOで「ビットパーフェクト」バックアップ（ddrescue）
     - macOSはドライブ検出に drutil status を使い、ブロック数×2048でディスクサイズを算出する必要あり。
     - ddrescueは最初に読みやすい領域を取り、後でエラー領域を再試行する2パスが有効。
  2. VIDEO_TS内の.VOBをffmpegで変換
     - 例: VOB → H.264 MP4（ブラウザ向けの最適化フラグを付ける）
     - 主要フラグの意味：-c:v libx264（映像）、-crf 22（画質と圧縮のバランス）、-c:a aac -b:a 128k（音声）、-movflags +faststart（メタデータを先頭に置きブラウザでのストリーミング開始を高速化）
  3. Cloudflare R2へアップロード、Pagesでシンプルなギャラリーを公開
     - R2は小規模利用なら10GBまでほぼ無料。帯域も実質無料で家族利用には低コスト。
     - Pages側でR2バケットをBindingしてPages Functionから配信。アクセス制限はCloudflare Accessでメール制御。
  4. UX改善（軽量化）
     - サムネイルは小さいJPEG（例：~5KB）を表示。再生時に初めて動画をロード。
     - ホバーでプレビューはスプライトシート（各クリップごとに20コマ程度を横並びの画像、~40KB）を使い、動画本体を読み込まずにスクラブ表示。
     - 動画一覧は単一HTML（ビルド不要）＋小さなJSでmanifest（ディスク名→クリップ数）を管理。リップして1行足して再デプロイで済む。

## 実践ポイント
- まずは1枚で試す：安いUSB DVDドライブ（約$25相当）を買い、1枚をISO化→変換→アップロードして動作確認。
- ddrescueは2パス：最初は -n で早く取り、次に -r 3 などで問題箇所を再試行。
- ffmpegの基本変換コマンド（参考）:

```bash
ffmpeg -i VTS_01_1.VOB -c:v libx264 -crf 22 -c:a aac -b:a 128k -movflags +faststart clip-01.mp4
```

- macOS向けの自動化スクリプト例（rip.sh）:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <disc-label>"
  exit 1
fi

LABEL="$1"
RAW_DIR="$(dirname "$0")/raw"
LOG_DIR="$(dirname "$0")/logs"

DISC=$(drutil status 2>/dev/null | grep "Name:" | awk '{print $NF}')
if [[ -z "$DISC" ]]; then
  echo "No disc detected. Insert a disc and try again."
  exit 1
fi

BLOCKS=$(drutil status 2>/dev/null | grep "Space Used:" | sed 's/.*blocks:[[:space:]]*//' | awk '{print $1}')
DISC_SIZE=$(( BLOCKS * 2048 ))

diskutil unmountDisk "$DISC" 2>/dev/null || true

ddrescue -b 2048 -s "$DISC_SIZE" -n "$DISC" "$RAW_DIR/${LABEL}.iso" "$LOG_DIR/${LABEL}.log"
ddrescue -b 2048 -s "$DISC_SIZE" -r 3 "$DISC" "$RAW_DIR/${LABEL}.iso" "$LOG_DIR/${LABEL}.log"

echo "Done! $(ls -lh "$RAW_DIR/${LABEL}.iso" | awk '{print $5}')"
```

- アップロードは wrangler の r2 object put をループで実行。Pages側のR2バインディングは現状ダッシュボードで設定が必要。
- 目安：1枚あたり約10分でリップ（ISO）、ディスク毎に13〜21クリップがよくある。全体の費用は数ドル〜月$1未満に収まる想定。

家族の思い出を「見られる形」に残すのは技術的にも現実的です。まず1枚、試してみてください。
