---
layout: post
title: "Firefox & Gtk Emoji picker - Firefox と Gtk 絵文字ピッカー"
date: 2026-03-27T18:00:15.993Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mastransky.wordpress.com/2026/03/20/firefox-gtk-emoji-picker/"
source_title: "Firefox &amp; Gtk Emoji picker &#8211; Martin Stransky&#039;s Blog"
source_id: 1124469892
excerpt: "Firefox 150でGTKネイティブ絵文字ピッカーが導入され、Ctrl+.でLinuxの入力欄にその場で絵文字を挿入可能に"
image: "https://mastransky.wordpress.com/wp-content/uploads/2026/03/image-1.png"
---

# Firefox & Gtk Emoji picker - Firefox と Gtk 絵文字ピッカー
FirefoxがLinuxネイティブの絵文字ピッカーに対応！GTKの慣れたUIでサクッと絵文字挿入

## 要約
Firefox 150（Beta）で、GTKネイティブの絵文字ピッカーをウェブ入力欄内から直接呼び出せるようになりました。Ctrl+. または Ctrl+; でGTKの絵文字選択ポップオーバーを表示し、テキストに絵文字を挿入できます。

## この記事を読むべき理由
Linuxデスクトップ（特にGNOME/GTK環境やWayland上）でブラウザ操作をする日本のユーザー／開発者にとって、デスクトップとブラウザの操作感が統一される重要アップデートです。社内チャットやSNS投稿、Webアプリの入力体験が改善され、カスタムキー割り当てや日本語入力との相性確認も必要になります。

## 詳細解説
- 実装概要  
  FirefoxはGTK3の組み込みウィジェットである GtkEmojiChooser を利用。従来、GtkEmojiChooserはGtkEntry/GtkTextView のキーイベントでしか起動できず、かつウィジェットが「表示されている」必要がありました。一方Firefoxは独自描画（GTKウィジェットを直接使わない）アーキテクチャのため、そのままでは呼び出せませんでした。

- 解決法の肝  
  Firefoxにはオフスクリーン（目に見えない）GtkEntryがあり、これを通じてGTKのキーイベント（例：Ctrl+.）を受け取れます。今回の実装では、受け取った 'emoji-insert' シグナルを、実際にフォーカスされている GtkWindow の子として「見せる」新しい GtkEntry にリダイレクトし、その位置を調整して GtkEmojiChooser を正しい場所に出すようにしています。GtkEntry は見える状態にする必要がありますが、Firefox側が上から描画するためユーザーには隠れたまま動作します。選択された絵文字は 'insert_text' シグナル等で取得して入力欄へ挿入されます。

- 動作範囲と設定  
  メインウィンドウやポップアップウィンドウの入力欄で動作。キーは Ctrl+. または Ctrl+;。不要な場合は about:config の widget.gtk.native-emoji-dialog を false にして無効化できます。

- 開発上の注意  
  GtkEmojiChooser の性質上、ウィジェットの可視性や位置取り、キー割り当ての競合（カスタムショートカットやIME）といった微調整が必要。実装にはテキスト処理や座標計算のノウハウが絡みます（貢献者: Emilio Cobos Álvarez, Masayuki Nakano 等）。

## 実践ポイント
- 使い方（すぐ試せる）
  1. Firefox 150 Beta を入手して起動  
  2. Webページの任意のテキスト入力欄をクリック  
  3. Ctrl+. または Ctrl+; を押して絵文字ピッカーを表示、選択すると挿入される

- 無効化したい場合  
  about:config を開き、widget.gtk.native-emoji-dialog を false に設定する

- チェックリスト（日本の環境向け）
  - Wayland（GNOME/Fedora/Ubuntu）で挙動を確認する  
  - Mozc等の日本語IMEとのショートカット衝突を確認する（必要ならIME側かFirefox側で調整）  
  - Webアプリの入力テスト（ポップアップやカスタム入力コンポーネント）を実施し、表示位置や挿入タイミングを確認する

元記事の実装ノートは開発者Martin Stranskyによる報告。Linux上でよりネイティブな絵文字体験を期待できるアップデート。
