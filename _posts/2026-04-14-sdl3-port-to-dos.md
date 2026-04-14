---
layout: post
title: "SDL3 port to DOS - SDL3 の DOS 移植"
date: 2026-04-14T16:01:56.233Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bsky.app/profile/dosnostalgic.bsky.social/post/3mjfdos7iok2o"
source_title: "@dosnostalgic.bsky.social on Bluesky"
source_id: 361865387
excerpt: "SDL3がほぼ完全にDOSへ移植、古いPCやDOSBoxで最新ゲームが動く可能性を開く"
image: "https://cdn.bsky.app/img/avatar_thumbnail/plain/did:plc:ucwjleevh3u7yq4safl6dnsa/bafkreidh3frqhqffe7k2koawkrtnd5byxwe5d3qddtxakok72x4h76w5ku"
---

# SDL3 port to DOS - SDL3 の DOS 移植
レトロPCで最新のマルチプラットフォームAPIが動く――SDL3がほぼ完全にDOSへ移植されました！

## 要約
SDL（Simple DirectMedia Layer）v3 のほぼフル機能なDOS移植が複数人の協力で実現され、GitHub PR #15377 にまとめられています。古いPCやDOSBoxでモダンなSDL3ベースのソフトが動かせる道が開かれました。

## この記事を読むべき理由
レトロ系開発者、ゲーム再現・保存、教育用途にとって、SDL3がDOSで動くことは「古い環境でも現代的なAPIで開発できる」大きな追い風になります。日本のレトロPC愛好家やインディー開発者にも直接メリットがあります。

## 詳細解説
- 元情報は Anatoly Shashkin 氏による報告と、libsdl-org の GitHub PR（https://github.com/libsdl-org/SDL/pull/15377）。「pretty much fully featured」とあるとおり、グラフィック、入力、サウンドなど主要機能の移植が進んでいます。
- DOSはMS-DOS系の制約（メモリモデル、古いBIOS/ハードウェアAPI、ドライバ差分など）があり、SDLの移植ではグラフィックバックエンド（VGA/VESA等）、入力デバイス対応、サウンドドライバ、タイマー処理、ファイルI/Oまわりの対応が鍵になります。今回のPRはそうした課題を実装・調整した成果と考えられます。
- 実行環境としては実機のDOS、DOSエクステンダ、あるいはDOSBox/PCemのようなエミュレータでの利用が想定されます。ビルドや互換性の詳細はPRの差分とディスカッションを参照してください。

## 実践ポイント
- まずPRを確認： https://github.com/libsdl-org/SDL/pull/15377
- 試す方法：PRブランチをcloneしてビルドし、DOSBoxなどで動かしてみる（ビルド手順・依存はPRの説明を参照）。
- 活用例：レトロゲームの移植、教育用デモ、ハードウェア制約下でのプロトタイピング。日本のレトロコミュニティやゲームイベントでのデモに最適。
- 貢献：バグ報告や互換性テスト、ローカライズ（日本語ドキュメントやチュートリアルの提供）でプロジェクトを支援できます。

元の報告は2026-04-13付の記事です。興味があればPRの差分と議論を追い、日本語での導入ガイドや検証報告を共有してみてください。
