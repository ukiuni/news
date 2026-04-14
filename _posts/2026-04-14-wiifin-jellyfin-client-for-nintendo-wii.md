---
layout: post
title: "WiiFin – Jellyfin Client for Nintendo Wii - Nintendo Wii向けJellyfinクライアント"
date: 2026-04-14T00:54:00.313Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/fabienmillet/WiiFin"
source_title: "GitHub - fabienmillet/WiiFin: Jellyfin Client for Wii · GitHub"
source_id: 47759341
excerpt: "WiiでNAS動画をテレビ再生、サーバー側トランスコード対応のJellyfinクライアント"
image: "https://opengraph.githubassets.com/a4d3c6f7ced8a237d63aebc6a0d5edb3578d63d5f21fe6005bccdff01dc95361/fabienmillet/WiiFin"
---

# WiiFin – Jellyfin Client for Nintendo Wii - Nintendo Wii向けJellyfinクライアント
往年のWiiが、あなたのテレビでNASの動画を再生する“最小限＆実用”ホームブリューに変身

## 要約
WiiFinはNintendo Wii向けの実験的なJellyfinクライアントで、Wii上でライブラリ閲覧・サーバー側トランスコード再生・再生位置同期などを実現します（C++/GRRLIB + MPlayer CE、HTTPS対応）。

## この記事を読むべき理由
Wiiは日本でも根強いユーザー層があり、レトロハードを活用した自宅メディア再生は実用的かつ話題性が高い。自前のJellyfinサーバーを持つ技術好きや個人運用者にとって、低リソース環境で動くクライアントは魅力的な選択肢です。

## 詳細解説
- アーキテクチャ：C++で実装。UIはGRRLIB、オーディオ/動画は統合されたMPlayer CE経由で再生。HTTPSは組み込みのmbedTLSを使用（自己署名証明書可）。
- 主要機能：ユーザ認証（パスワード／QuickConnect）、プロファイル保存（アクセストークンのみ）、ムービー/TV/音楽ライブラリ表示、シノプシス・キャスト表示、シークバーや音量などのプレイヤーHUD、視聴進捗のJellyfinへの報告。
- 再生方式：Direct-play非対応。すべてサーバー側トランスコードで配信されるため、サーバー側で対応コーデックや音声チャンネルに注意（5.1は不可、ステレオのみ）。
- ビルド／配布：devkitPro（devkitPPC, libogc）でコンパイル。MPlayer CEを静的ライブラリ化（libmplayer.a）すると動画再生が可能。成果物は.dol（実行ファイル）または.wadで配布。Dolphinエミュレータや実機（vWii含む）で動作確認可能。
- 制約：字幕はサーバーで埋め込みレンダリングに依存、実機での挙動に粗さあり。GPLv3ライセンス。

## 実践ポイント
- まずDolphinでWiiFin.dolを動かして動作確認する。実機へはSD:/apps/WiiFin/boot.dolにコピー、または.wadで導入。
- 動画再生を確実にするには、JellyfinサーバーにH.264/AACなどWiiが扱えるフォーマットでのトランスコード設定を用意する。
- MPlayer CEをビルドしてlibmplayer.aを用意しないと映像再生が無効なので要ビルド作業（MPLAYER_CE_BUILD.md参照）。
- HTTPSは自己署名可だが、QuickConnectやネットワーク設定でアクセス経路を事前確認すること。
- GPLv3なので再配布や改変時はライセンス遵守を忘れずに。興味があればGitHubでIssueやPRで貢献可能。

元リポジトリ: https://github.com/fabienmillet/WiiFin
