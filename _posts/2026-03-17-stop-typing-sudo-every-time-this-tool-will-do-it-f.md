---
layout: post
title: "Stop typing sudo every time - もう毎回sudoを入力する必要はありません"
date: 2026-03-17T14:41:09.291Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ashxj/sudotoggle"
source_title: "GitHub - ashxj/sudotoggle: ⚒️ Don&#39;t want to enter your sudo user password every time? This tool is for you! · GitHub"
source_id: 381617033
excerpt: "期限付きでsudoをパスワード不要に一瞬切替、開発効率激増ツール"
image: "https://opengraph.githubassets.com/ca35081ecb8bc33169762f4c0107ab7aa89d145a637d58955d3f67eb39500e5e/ashxj/sudotoggle"
---

# Stop typing sudo every time - もう毎回sudoを入力する必要はありません
一瞬でON/OFF、期限付きで使える「sudotoggle」で開発フローをスムーズに

## 要約
sudotoggleは、/etc/sudoers.d に一時的・恒久的な NOPASSWD ルールを作成して、パスワード無しで sudo を使えるように切り替える軽量な Bash ユーティリティです。自動期限設定、デバッグ表示、構文検証で安全性にも配慮しています。

## この記事を読むべき理由
開発中やスクリプト実行で頻繁に sudo を使うと生産性が落ちます。日本の開発現場（ローカル Linux、WSL、サーバ保守、自動化スクリプト）でも、必要なときだけ安全にパスワードフリーにする運用は有用です。

## 詳細解説
- 仕組み
  - コマンドで NOPASSWD ルールファイル（/etc/sudoers.d/nopasswd_<user>）を作成・削除。
  - 有効化時にまず sudo -v で認証を取り、visudo -cf で構文チェックしてから反映するため壊れにくい。
  - 有効期限は秒単位（-time）か時刻指定（-timef HH:MM）で設定。期限は ~/.config/sudotoggle/config に保存される。
  - Bash/Zsh 用のフック（preexec/DEBUG trap）で、sudo 実行前に状態確認や自動無効化をトリガーできる。
- 主なコマンド
  - sudotoggle -on（無期限有効）
  - sudotoggle -on -time 3600（3600秒＝1時間）
  - sudotoggle -on -timef 18:30（当日18:30まで）
  - sudotoggle -off（即時無効）
  - sudotoggle -status（状態確認）
  - sudotoggle -debug on/off（デバッグ表示切替）
- 安全対策
  - visudo での構文検証、ファイル名分離による管理、自動期限で長期にわたる権限放置を防止。
  - とはいえ NOPASSWD は強力なので、信頼できる環境で・必要最小限の時間だけ使うこと。

## 実践ポイント
- すぐ使う（インストール）
```bash
# Clone と実行権限付与
git clone https://github.com/ashxj/sudotoggle.git
cd sudotoggle
chmod +x sudotoggle.sh
# 任意で PATH に置く
sudo mv sudotoggle.sh /usr/local/bin/sudotoggle
```
- 日常運用
  - 一時的に使うなら: sudotoggle -on -time 3600
  - 終わったら: sudotoggle -off
  - 他端末で sudo キャッシュが残る場合: sudo -k（キャッシュをクリア）
  - シェル起動時にフックを有効化するには、~/.bashrc や ~/.zshrc をソースする
- 推奨ルール
  - 本番サーバでは原則使わない／使うなら監査ログやアクセス制限と併用する
  - 自動化ジョブは鍵や適切な権限分離を優先し、NOPASSWD は開発用途に限定する

以上を踏まえ、まずはローカル環境で短時間のタイマー設定から試してみてください。
