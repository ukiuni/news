---
layout: post
title: "Show HN: TUI for managing XDG default applications - XDG デフォルトアプリ管理用 TUI"
date: 2026-01-25T12:31:09.660Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mitjafelicijan/xdgctl"
source_title: "GitHub - mitjafelicijan/xdgctl: TUI for managing XDG default applications"
source_id: 46753078
excerpt: "ターミナルで既定アプリを直感切替、軽量TUI xdgctlで作業効率化"
image: "https://opengraph.githubassets.com/b03c900d8c4822ae51700c8406602eba095d47d1465e886877f99e88dc5d5d3a/mitjafelicijan/xdgctl"
---

# Show HN: TUI for managing XDG default applications - XDG デフォルトアプリ管理用 TUI
GUI を開かずにキー操作で既定アプリを切り替えられる「xdgctl」――ターミナル好きのワークフロー革命

## 要約
xdgctl は C + GLib/GIO + termbox2 で作られたターミナルUI（TUI）で、XDG の既定アプリ（MIME ハンドラやスキームハンドラ）をカテゴリ別に閲覧・切替できる軽量ツールです。xdg-mime を直接叩かなくても直感的に操作できます。

## この記事を読むべき理由
Linux デスクトップで「既定のブラウザ／エディタ／ファイルマネージャ」を頻繁に切り替える開発者や、軽量環境（WM/Tiling 環境、WSL など）で GUI 設定に頼りたくない日本のユーザーにとって、手早く安全に設定変更できる実用的なツールだからです。

## 詳細解説
- 何をするツールか  
  - XDG（mimeapps.list を介した既定アプリ設定）の閲覧・変更を TUI で行う。カテゴリ（Browsers, Text Editors など）別にアプリ一覧を表示し、現在の既定は * でマークされる。  
- 技術スタック  
  - 言語: C  
  - ライブラリ: GLib/GIO（XDG/GIO API 経由で既定アプリを操作）、termbox2（ターミナル描画）  
- 操作感（キー操作）  
  - ↑/↓: カテゴリやアプリを移動  
  - →/Tab: カテゴリ一覧 → アプリ一覧  
  - ←: アプリ一覧 → カテゴリ一覧  
  - Enter: 選択アプリをそのカテゴリの既定に設定  
  - Esc / q: 終了  
- ビルドとインストール（要点）  
  - 必要ライブラリ: glib-2.0, gio-2.0, gio-unix-2.0、コンパイラ（clang/gcc）  
  - 一般的な手順:
    - git clone https://github.com/mitjafelicijan/xdgctl.git
    - cd xdgctl
    - make
    - sudo make install  （または PREFIX=/usr/local や PREFIX=~/.local でローカルインストール）
  - もし ~/.local/share/applications に手動で .desktop を追加した場合は update-desktop-database を実行する必要あり。  
- 参考となる組み込みコマンド（xdg-mime）  
  - 既定確認:
    - xdg-mime query default text/plain
    - xdg-mime query default x-scheme-handler/http
  - 手動で設定:
    - xdg-mime default brave.desktop x-scheme-handler/http
  - 参照ファイル:
    - ~/.config/mimeapps.list
    - /usr/share/applications/mimeapps.list
- サンプル Desktop Entry
  ```ini
  [Desktop Entry]
  Name=Brave Browser
  Exec=/home/m/Applications/brave
  Type=Application
  Categories=Applications
  MimeType=text/html;text/xml;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;
  ```

## 実践ポイント
- 導入前に現在の設定をバックアップ: cp ~/.config/mimeapps.list ~/.config/mimeapps.list.bak  
- システム全体とユーザー個別の違いを理解（/usr/share/... vs ~/.local/...）してから変更する。  
- ローカルインストール: make PREFIX=~/.local install でユーザー権限のみで運用可能。  
- 新しい .desktop を追加したら update-desktop-database を忘れずに。  
- 自動化: スクリプトで xdg-mime と組み合わせれば環境ごとの既定アプリ切替が容易（例: work vs personal）。  
- TUI は設定ミスの可視化に有効：GUI で見つけにくい MIME カテゴリも一覧で確認できる。
