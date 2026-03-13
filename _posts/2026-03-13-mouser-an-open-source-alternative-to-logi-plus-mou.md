---
layout: post
title: "Mouser: An open source alternative to Logi-Plus mouse software - Mouser：Logi‑Plus代替のオープンソースマウス設定ツール"
date: 2026-03-13T21:34:48.335Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/TomBadash/MouseControl"
source_title: "GitHub - TomBadash/MouseControl: A lightweight, open-source alternative to Logitech Options+ for remapping buttons on the Logitech MX Master 3S mouse · GitHub"
source_id: 47368033
excerpt: "人気のMX Masterをログイン不要で全ボタン再割当できるMouser"
image: "https://opengraph.githubassets.com/90011b0dfd183ba7030100d8b95f4143f624ad7f76b2b54b3028ff0be22233c4/TomBadash/MouseControl"
---

# Mouser: An open source alternative to Logi-Plus mouse software - Mouser：Logi‑Plus代替のオープンソースマウス設定ツール
魅力タイトル：MX Masterユーザー必見 — ログイン不要で使える「Mouser」でボタンを完全リマップしよう

## 要約
MouserはLogitech Options+に代わる軽量なオープンソースアプリで、MX Master 3Sの全プログラム可能ボタンをローカルで再割り当てできます。クラウドやテレメトリはなく、WindowsとmacOSに対応しています。

## この記事を読むべき理由
MX Masterシリーズは日本でも人気の作業用マウス。企業ポリシーやプライバシー懸念で公式ソフトを使えない・使いたくない人に、手軽で安全な代替手段を知っておく価値があります。

## 詳細解説
- 対応機種と環境：主にLogitech MX Master 3S（PID 0xB034）。Windows 10/11とmacOS Monterey以降をサポート。USBレシーバーでも一部動作しますが、Bluetooth＋HID++が最も安定。  
- 主要機能：6つのプログラム可能ボタン（中ボタン・ジェスチャーボタン・戻る・進む・左右水平スクロール）をアクションにマッピング、アプリごとのプロファイル自動切替、DPIスライダー（200–8000）、垂直/水平スクロール反転、22種類のビルトインアクションなど。UIはQt Quickでモダンなダークテーマ。  
- ジェスチャーボタン検出：Bluetooth上でHID++ 2.0の「divert」を使う一次検出が主体。未検出時はRaw Inputのフォールバック、さらに中クリックフォールバックで挙動を補います。  
- フックと注入：低レベルのWindowsマウスフック（WH_MOUSE_LL）でイベントを横取りし、必要に応じてSendInput相当でキーや操作を注入。アプリ切替時はフックスレッドを再作成せず軽量にプロファイル切替を行います。  
- 再接続と状態表示：マウスの電源オフ/オンや切断を検出して自動再接続。UIに接続状態がリアルタイム表示されます。  
- 設定保存：Windowsは%APPDATA%\Mouser\config.json、macOSは~/Library/Application Support/Mouser/config.jsonにローカル保存。クラウド送信は行いません。  
- 制限事項：現状はMX Master 3S専用（将来的に拡張予定）、Linux未対応、Logitech Options+と同時起動不可（HID++競合）。

## 実践ポイント
- まず試す方法：公式リポジトリのZipをダウンロード→解凍→Mouser.exeを実行。初回はWindows SmartScreenの警告が出る場合は「詳細→実行」。  
- ソースから実行：Python 3.10+で仮想環境を作り、requirements.txtをインストールして main_qml.py を実行。macOSではアクセシビリティ許可が必要。  
- 常時使うには：付属のPyInstaller specで自己完結型の実行ファイルをビルド（build.bat / pyinstaller Mouser.spec）。  
- 注意点：Logitech Options+ は必ず終了させる（競合で動作しない）。Bluetooth接続が推奨。ゲームなど管理者権限が絡むアプリではキー注入が効かない場合あり。  
- 日本の現場での利点：社内ポリシーでサードパーティクラウドを避ける必要がある開発チームや、プライバシー重視の個人ユーザーに最適。MX Masterユーザーならまず導入候補に入れてよいツールです。
