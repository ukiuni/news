---
layout: post
title: "Making a Hardware Accelerated Live TV Player from Scratch in C: HLS Streaming, MPEG-TS Demuxing, H.264 Parsing, and Vulkan Video Decoding - Cで作るハードウェア加速ライブTVプレイヤー：HLS・MPEG‑TS・H.264解析・Vulkanデコード"
date: 2026-02-09T05:55:44.612Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.jaysmito.dev/blog/03-live-tv-inside-vulkan/"
source_title: "Building a Live TV Player from Scratch: HLS Streaming, MPEG-TS Demuxing, H.264 Parsing, and Vulkan Video Decoding"
source_id: 405591880
excerpt: "純CでHLS→MPEG-TS→H.264→Vulkanで実装する低遅延ライブTVプレイヤー構築の工程"
image: "https://blog.jaysmito.dev/_astro/thumb.HBNrXryW.png"
---

# Making a Hardware Accelerated Live TV Player from Scratch in C: HLS Streaming, MPEG-TS Demuxing, H.264 Parsing, and Vulkan Video Decoding - Cで作るハードウェア加速ライブTVプレイヤー：HLS・MPEG‑TS・H.264解析・Vulkanデコード

Vulkanで“ゼロから”作るライブTVプレイヤー — 既製メディアライブラリを使わない挑戦が見せるストリーミングの裏側

## 要約
作者はFFmpeg等を使わず、HLSのM3U8解析→MPEG‑TSデマックス→H.264ビットストリーム解析→Vulkan Videoによるハードウェアデコード、という一連のパイプラインをCで自作し、動くライブプレイヤーを構築した。

## この記事を読むべき理由
ストリーミングの各レイヤー（プレイリスト、コンテナ、コーデック、ハードウェアデコード）の役割と混乱しやすい落とし穴を「実装者視点」で学べるため、プレイヤー開発や低レイテンシ配信、組み込み機器向け最適化に直結する知見が得られる。

## 詳細解説
- 目標と制約：既存のメディアライブラリ（FFmpeg/GStreamer等）を使わず、純Cで自前パーサ／デマクサ／デコーダーパイプラインを作成。GUIやネットワークは外部を使っても良いがメディア処理は全部自作する挑戦。  
- 生まれたライブラリ群：stb風の単一ヘッダ設計で picoM3U8（M3U8解析、RFC8216準拠）、picoMpegTS（MPEG‑TSデマックス、ITU‑T H.222.0準拠）、picoH264（H.264ビットストリーム解析）、picoAudio（OSネイティブでの音声復号）を実装。  
- HLS概念：マスター／メディアプレイリストの違い、#EXTINF／#EXT-X-MEDIA-SEQUENCE等の意味、ライブではプレイリストをポーリングして新セグメントを取得する仕組み。メディアは通常.ts（MPEG‑TS）かfMP4で配信される。  
- MPEG‑TS→PES→ES：TSパケットは188バイト。PESにより音声/映像のエレメンタリーストリームが入るため、パケット再構築、NALユニット抜き出し、PTS/DTSによる同期管理が必要。AAC（ADTS）やH.264(NAL)の境界処理／タイミング管理が実装上の難所。  
- H.264解析：NALユニットの切り出し、SPS/PPSから解像度やタイムベースを得る処理、フレーム境界とデコード順（POC/順序）の扱い。  
- ハードウェアデコード（Vulkan Video）：Vulkan Video拡張を用いGPU側のデコーダでNALを渡してデコードする。ドライバ／GPU依存性や同期（レンダリング／プレゼン／オーディオ時間合わせ）の設計が鍵。  
- 同期とセグメント時間：TS/H.264だけで完全なタイミングが得られない場合があるため、M3U8のセグメント長情報を補助的に使う運用的知見。  
- 実装の工夫：stb風APIで導入障壁を下げる、ダウンロード→デマクサ→デコード→表示をワーカーで分離、グローバルなセグメントID（media sequence + index）で古いチャンクを安全に破棄。

## 実践ポイント
- まずRFC8216（HLS）とITU‑T H.222.0／H.264仕様の概観を読む。  
- テスト環境はffmpegでローカルHLSストリームを作る（開発用。プレイヤー実装でffmpegを使う必要はない）。  
- 開発順序：M3U8パーサ → TSデマクサ → H.264 NAL抽出 → ソフトデコードで動作確認 → Vulkan Videoへ移行。各段階でログと小さな再生確認を入れる。  
- 実運用では既存の成熟ライブラリを検討（保守性・互換性重視）。自作は学習・研究・特定要件向けに有効。  
- 日本では放送系コンテンツや低遅延ライブ（スポーツ、放送機器、組み込みSTB）でハードウェアデコーダと軽量依存の利点が活きるため、GPUドライバ対応状況やプラットフォーム（Windows/Mac/Linux/組み込み）を事前確認する。

興味があれば、作者のlibpico実装（picoM3U8/picoMpegTS/picoH264/picoAudio）を参考にして、まずはM3U8解析とTS→NALの観察から始めると理解が早い。
