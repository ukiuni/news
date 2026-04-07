---
layout: post
title: "Claude Code is locking people out for hours - Claude Code が何時間もログイン不能になる不具合"
date: 2026-04-07T15:21:08.768Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/anthropics/claude-code/issues/44257"
source_title: "[BUG] Claude Code login fails with OAuth timeout on Windows · Issue #44257 · anthropics/claude-code · GitHub"
source_id: 47676521
excerpt: "Windows版Claude CodeがOAuthタイムアウトで数時間ログイン不能になる重大不具合"
image: "https://opengraph.githubassets.com/23e18aa3ae6a8de1012a356b5b4f1aafe6ab69bcdb107e7bea8ce2b258ca6408/anthropics/claude-code/issues/44257"
---

# Claude Code is locking people out for hours - Claude Code が何時間もログイン不能になる不具合

Windowsユーザーを直撃する「OAuthタイムアウト」で、公式アプリにサインインできなくなる問題を分かりやすく解説します。

## 要約
Windows版Claude CodeでGoogleログインを完了してもアプリ側で「OAuth error: timeout of 15000ms exceeded」となりログイン不能になる報告（Issue #44257）。作業が完全に止まる深刻な障害です。

## この記事を読むべき理由
日本の開発現場でもWindows＋WSLや企業プロキシ環境での利用が多く、同様のOAuthフロー問題に遭遇する確率が高い。ツールが使えない時間が生産性に直結するため、原因と対策を知っておく価値があります。

## 詳細解説
- 再現手順（報告からの要約）
  1. WindowsでClaude Codeを起動
  2. Googleログインを開始し、ブラウザでサインインを完了
  3. ブラウザからアプリに戻るとアプリが「OAuth error: timeout of 15000ms exceeded」を表示して失敗

- 環境情報
  - Claude Code Version: 2.1.92（報告時）
  - OS: Windows（WSLを利用するターミナル/シェルを併用）
  - 発生状況: 毎回同じタイムアウトでログイン不可

- 技術的に考えられる原因
  - OAuthのリダイレクト（コールバック）がアプリに届かない：OS側のURLスキーム／プロトコルハンドラが登録されていない、またはブラウザからアプリへフォーカスが戻らない。
  - 組み込みブラウザ vs システムブラウザの差分：外部ブラウザでのコールバック処理が期待と異なる。
  - ネットワークやプロキシ、Windowsファイアウォールによるブロックでリクエストが遅延／失敗。
  - OAuthクライアントのタイムアウト設定（ここでは15,000ms）が短く、リダイレクト処理が間に合わない可能性。
  - WSLやターミナルの環境差異がネイティブアプリのハンドリングを阻害。

- 状況
  - 報告者は複数回試行しても再現し、現状ではアプリが使えない状態。Issueへの反応は得られていない（報告時点）。

## 実践ポイント
- まず試すこと
  - Web版（ブラウザ）でのログインを試し、当面はそちらで作業する。
  - デフォルトブラウザ設定を確認し、別のブラウザで試す（Chrome/Edge/Firefox）。
  - アプリを管理者権限で起動して試す。
  - WSLや特殊なターミナルを介さず、ネイティブWindows環境で再現するか確認する。

- トラブルシューティング（開発者向け）
  - アプリのログ（コンソール出力）とブラウザのネットワークログを保存する。
  - Windowsの既定のURLプロトコルハンドラ登録状況を確認する（deep linkが登録されているか）。
  - プロキシやファイアウォール設定で外部コールバックがブロックされていないか確認。
  - 再現手順、OSバージョン、アプリバージョン、使用ブラウザ、ログを添えてIssueに追記する。

- 回避策
  - 一時的にWebクライアントを利用する。
  - 似た機能の他ツールを使う（業務クリティカルなら代替手段を用意）。

問題の進展はGitHub Issue #44257をウォッチし、アップデートが出たら速やかにアプリを更新することを推奨します。
