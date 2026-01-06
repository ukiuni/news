---
  layout: post
  title: "Stop Doom Scrolling, Start Doom Coding: Build via the terminal from your phone - ドゥーム・スクロールをやめてドゥーム・コーディングを始めよう：スマホのターミナルでどこでも開発"
  date: 2026-01-06T19:57:27.736Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/rberg27/doom-coding"
  source_title: "GitHub - rberg27/doom-coding: A guide for how to use your smartphone to code anywhere at anytime."
  source_id: 46517458
  excerpt: "スマホで自分の常時稼働PCにSSH接続し、移動時間を即開発時間に変える5分セットアップガイド"
  image: "https://opengraph.githubassets.com/470b8cd50ebad65be000440efac300e24954f1b663482dd32a4196355998c42e/rberg27/doom-coding"
---

# Stop Doom Scrolling, Start Doom Coding: Build via the terminal from your phone - ドゥーム・スクロールをやめてドゥーム・コーディングを始めよう：スマホのターミナルでどこでも開発

スマホで“ながら”コーディングを本気化する—通勤・出張・カフェ時間を開発時間に変える5分セットアップ。

## 要約
スマホ＋常時稼働PC＋Tailscale＋モバイルSSHクライアントで、どこからでも自分の開発マシンにターミナル接続し、コード編集・ローカルプレビュー・データベース確認まで行う方法を紹介するガイド。

## この記事を読むべき理由
日本の開発者はリモートや出張が多く、短時間でも生産的に動きたいケースが増えている。社内PCや自分の開発環境に安全にアクセスできれば、移動時間や待ち時間が有効な「実働時間」に変わる。

## 詳細解説
この手法の肝は「自分のマシンを24/7で稼働させ、スマホから安全にSSH接続する」こと。主要コンポーネントは以下。

- 常時稼働PC（自宅やクラウドのマシン）: スリープ無効化、リモートログイン（SSH）有効化が必要。
- Tailscale: Zero‑configなWireGuardベースのVPN。MagicDNSで自分のマシンを固有のホスト名で参照できる（例: my-computer.tailnet-name.ts.net）。
- Termius（または他のモバイルSSHクライアント）: スマホからSSH接続するためのアプリ。
- Claude Code（任意）: ローカルで動かす補助ツールやAIコーディングセットアップを組み合わせる場合に利用。

基本フロー:
1. PC側：スリープを無効化、SSH（Remote Login）を有効化、Tailscaleをインストールして同アカウントでサインイン、必要ならClaude Codeをインストール。
2. スマホ側：Tailscaleアプリで同アカウントにログイン、Termiusをインストール。TermiusにMagicDNSのホスト名（my-computer.tailnet-name.ts.net）を登録してSSH接続。
3. 接続後は通常のターミナル作業が可能。ローカルサーバーはMagicDNSのホスト名＋ポートでスマホからプレビューできる。

実用的なコマンド例:
```bash
# シンプルな静的ファイルのプレビュー
python -m http.server 3005
# その後スマホで:
# http://your-machine.tailnet-name.ts.net:3005/your-html-file.html
```

接続トラブルの典型例:
- Tailscaleの接続が切れている（アプリで緑色のオンライン表示を確認）
- PCがスリープ中またはロックされている（リモートで起動する場合はWake-on-LANや常時電源を検討）
- SSH認証の設定ミス（パスワードではなく公開鍵＋パスフレーズ推奨）

セキュリティ上の注意:
- 公衆Wi‑Fiやキャリア回線でもTailscale経由なら安全性は高いが、端末紛失時を考えスマホ自体の生体認証・画面ロックを必須にする。
- 会社のポリシーによっては社内PCの常時接続が許可されない場合があるため事前確認を推奨。
- SSHは公開鍵方式を利用し、必要なポートだけ開ける（Tailscaleを使えば直接ポート解放は不要）。

## 実践ポイント
- 初期チェックリスト
  - PC: スリープ無効、SSH有効、Tailscaleインストール・ログイン済み
  - スマホ: Tailscaleログイン、TermiusにMagicDNSホストを登録
- Termius設定のコツ
  - Hostname: your-machine.tailnet-name.ts.net
  - Port: 22（必要なら変更）
  - 認証: SSHキー（推奨）またはユーザ/パスワード
- すぐ使えるワークフロー
  - 小さなタスクはスマホでコード編集→テスト→コミット（git CLI）
  - ブラウザでプレビューが必要なら python -m http.server などを使って確認
  - データベース確認にはモバイル向けPostgresクライアントを利用
- 生産性ハック
  - セッション終わりにAIアシスタント（Claude等）で作業ログ更新（READMEやCLAUDE.md）
  - よく使う開発サイトをPC側でブックマークしておき、スマホから即アクセス
- 日本向けの実務配慮
  - 社内規程に従い、機密情報は端末に残さない／ログを暗号化する
  - モバイルデータ通信量が気になる場合はWi‑Fiでの使用や差分同期を工夫する

このセットアップを使えば、通勤電車や出張中の空き時間が「ちょっとした開発サイクル」になり得る。まずは5分で接続確認をして、短いタスクから試してみることを推奨する。
