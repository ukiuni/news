---
layout: post
title: "FIM – Linux framebuffer image viewer - FIM（fbi improved）：Linuxフレームバッファ向け画像ビューア"
date: 2026-04-17T08:42:24.021Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.nongnu.org/fbi-improved/"
source_title: "FIM: fbi improved (lightweight customizable image viewer) home page"
source_id: 47803323
excerpt: "Vim風操作でコンソールやSSH上に画像を高速プレビューできるFIM入門"
---

# FIM – Linux framebuffer image viewer - FIM（fbi improved）：Linuxフレームバッファ向け画像ビューア
キーボードだけで高速プレビュー！Vim感覚で使える軽量画像ビューア「FIM」入門

## 要約
FIM（fbi improved）はVimライクな操作感を持つ軽量で高拡張な画像ビューア。フレームバッファ／SDL／GTK3／ASCII出力など多彩な出力モードを持ち、スクリプトやメタデータ連携で大規模写真コレクションの管理も可能です。

## この記事を読むべき理由
日本の開発者や組込み・サーバ運用者はGUIが使えない環境（コンソール、SSH、組込みデバイス）で画像確認が必要な場面が多いです。FIMはそうした環境に最適で、Vim慣れした人なら生産性をすぐに高められます。

## 詳細解説
- 基本設計
  - 軽量かつモジュール化。依存ライブラリは最小限かつ多くがオプション。
  - キーボード中心の操作体系（Vim風のj/k/h/lや繰り返しコマンド、コマンドモード(:)など）。
- 出力モード
  - Linuxフレームバッファ（直接コンソール表示）
  - SDL（ウィンドウ表示）
  - GTK3（メニュー付きウィンドウ）※新版で追加
  - ASCIIアート（libcaca／AAlib経由）— SSH接続時のプレビューに便利
- フォーマットと環境
  - 多数の画像形式をサポート。変換ラッパー fimgs を用いた透明な変換が可能。
  - Unix系メインだが、emscripten経由でWebAssembly、TermuxでAndroid、Windowsへも移植例あり。
- メタデータとコレクション機能
  - EXIFタグを自動で読み込み、ステータス行に表示可能（例：露出／絞り／ISO）。
  - files.dsc 形式でファイル毎にテキスト説明や任意変数（#!fim:var=val）を付与でき、表示や絞り（limitコマンド）に利用可。
  - マーク機能で選別→終了時に選択リストを出力。
- コマンドライン/連携
  - 基本：fim <file_or_dir>, 再帰：fim -R ~/Pictures
  - パイプ入力対応：cat image.jpg | fim -i
  - 起動時にコマンド実行：fim -c 'command'
  - Mutt等のメールクライアントや mailcap との組み合わせで添付画像をシームレスに表示可能。
- 最近の改善（抜粋）
  - GTK3出力追加、Wayland環境を考慮した自動選択、スライドショーの小数秒指定対応、各種ビルド/ランタイムのバグ修正。

例（よく使うコマンド）
```bash
# ディレクトリを再帰的にブラウズ
fim -R ~/Pictures

# files.dsc を読み込んで説明付きで開く
fim --load-image-descriptions-file files.dsc sample.jpg

# stdinから読み込み（変換パイプと併用）
convert image.pic ppm:- | fim -i
```

## 実践ポイント
- SSHでサーバ上の画像確認をしたいなら、ASCII出力（-o aa）を試す。
- 大量写真のアーカイブ管理は files.dsc と limit／mark を組み合わせると効率的。
- GUI環境があるデスクトップでは -o gtk によりメニュー付きで使える（Vim操作も維持）。
- パッケージが無ければソースからビルド可能。emscriptenやtermuxでの活用でクロス環境対応が可能。URLや配布は公式ページ（元記事）を参照してください。
