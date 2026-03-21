---
layout: post
title: "Fujifilm X RAW STUDIO webapp clone - Fujifilm X RAW STUDIO の Webアプリ クローン"
date: 2026-03-21T07:20:12.836Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/eggricesoy/filmkit"
source_title: "GitHub - eggricesoy/filmkit: Create and manage Fujifilm camera profiles, with ease and speed. Connect your camera and you are good to go! · GitHub"
source_id: 47435081
excerpt: "ブラウザでカメラ直結、Xシリーズを高品質RAW現像・プリセット管理"
image: "https://opengraph.githubassets.com/718b02d346eabe7bc65668edd9df0c4c15a69414175c142afe3f4b844f35fb04/eggricesoy/filmkit"
---

# Fujifilm X RAW STUDIO webapp clone - Fujifilm X RAW STUDIO の Webアプリ クローン
魅せるプリセット管理とカメラ内RAW変換をブラウザで——FilmKitで“手元のXシリーズ”をもっと自由に

## 要約
FilmKit（eggricesoy/filmkit）は、Fujifilm Xシリーズのプリセット管理とカメラ内RAW→JPEG変換をブラウザ上で行えるクライアント専用アプリです。WebUSBでカメラと直接やり取りし、ローカル保存やモバイル対応も可能なゼロインストールツールです（現状はBETA、主にX100VIで動作確認）。

## この記事を読むべき理由
Fujifilmのフィルムシミュレーションやカメラ内現像は日本でも愛好者が多い分野です。公式アプリに依存せず、手元のブラウザだけでプリセットの読み書きや一括変換を高速に行えるFilmKitは、プロ・趣味問わず作業効率を大きく改善します。

## 詳細解説
- アーキテクチャ：FilmKitは静的なクライアントサイドWebアプリ（GitHub Pages公開想定）で、ブラウザのWebUSB経由でカメラとPTP（Picture Transfer Protocol）をやり取りします。RAFファイルと変換パラメータをカメラに渡し、カメラ側の画像エンジンで高品質JPEGを返す仕組みです。
- プリセット管理：カメラ内プリセットの読み取り・編集・書き込みが可能。変更差分のみを当てる「パッチ方式」を採用し、元プロファイルのバイト構造を保つことでEXIFやその他フィールドの破壊を避けます。プリセットはローカル保存・ドラッグ＆ドロップで移動可能。
- 互換性と制限：作者はX100VIで動作確認済み。他のXシリーズ（X-T5、X-H2等）でもプロトコル対応なら動く可能性あり。ただしプロパティのエンコードや書き込み条件（例：HighIsoNRの非線形エンコード、色温度はWBモード依存など）をリバースエンジニアしているため機種差に注意。
- リバースエンジニアリング：WiresharkでUSBキャプチャを取り、X RAW STUDIOとのやり取りからプロパティのエンコードや順序を解析しています。プロトコル詳細はリポジトリの QUICK_REFERENCE.md に記載。
- 実装技術：TypeScript＋Web技術で実装。ブラウザ側でUIは非ブロッキング、カメラ側のキュー管理を改良してX RAW STUDIOより高速な反復作業を目指しています。

## 実践ポイント
- 今すぐ試すには：Chromium系ブラウザ（Google Chromeなど）で開き、カメラを接続するだけ。LinuxでFlatpakを使う場合は適切なudevルール（例：SUBSYSTEM=="usb", ATTR{idVendor}=="04cb", MODE="0666"）が必要。
- 安全対策：プリセットを書き込む前に必ずカメラ内のバックアップを取ること（FilmKitはBETA）。特に未対応機種では注意。
- 機種追加に協力する方法：WiresharkでUSBキャプチャ（.pcapng）を取り、カメラモデル・ファームウェア・実行した操作（プロファイル読み取り／プリセット保存／RAW変換）とともにGitHubのIssueへ提出すると開発者が解析できます。
- 開発者向け：プロトコルやプロパティマッピングに興味があるなら QUICK_REFERENCE.md とリポジトリを参照。プロジェクトはPRは受けない方針ですが、バグ報告や互換性レポートは歓迎されています。

FilmKitリポジトリ：https://github.com/eggricesoy/filmkit

【注意】現状はベータ・限定検証。実運用前に必ずテストとバックアップを。
