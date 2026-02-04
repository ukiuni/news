---
layout: post
title: "RS-SDK: Drive RuneScape with Claude Code - RS‑SDK：ClaudeコードでRuneScapeを操作する"
date: 2026-02-04T19:08:37.499Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/MaxBittker/rs-sdk"
source_title: "GitHub - MaxBittker/rs-sdk: Runescape automation library, optimized for use by coding agents."
source_id: 46888142
excerpt: "RS-SDKでClaudeを使いRunescape風MMOを安全に自動化、エージェント研究を始める"
image: "https://opengraph.githubassets.com/544810becfc58c190986fdea74f265bf613f138d77d72ef51a8d846abd849f30/MaxBittker/rs-sdk"
---

# RS-SDK: Drive RuneScape with Claude Code - RS‑SDK：ClaudeコードでRuneScapeを操作する

AIにMMOを任せて遊ばせる――RS‑SDKで“Botだけ”の安全なRunescape風環境を自動化し、エージェント研究を始めよう

## 要約
RS‑SDKはTypeScript製のRunescape風ゲーム自動化ライブラリ兼研究用プラットフォームで、Claudeなどのコーディングエージェントと連携してボットを作り、経済・協調・競争の研究や目標指向プログラム合成の実験ができます。

## この記事を読むべき理由
エージェント駆動の自動化やRL/プログラム合成に興味がある日本のエンジニアや学生にとって、実動するMMO環境でスケールした実験が手早くできる数少ないオープンソース基盤です。商用ゲームに干渉せず安全にボット挙動を試せる点も重要です。

## 詳細解説
- コア構成
  - TypeScript SDK：エージェントから高レベル命令（例：walkTo(x,y)）を出すライブラリ。
  - botclient：強化されたウェブクライアントが実際のゲーム操作を代行し、SDKとは直接ではなくgateway経由で通信する設計。
  - gateway：botclientとSDK間の中継サーバー。ユーザー名でメッセージを振り分ける。
  - LostCityフォークのサーバーエミュレータ：公式サーバーと無関係な、ボット実験専用の環境。
- エージェント連携
  - Claudeなどのコーディングエージェント向けのドキュメントやバインディングが用意されており、自然言語で「このアカウントを育てる」指示を与えるだけで動かせる例がある。
- 運用上の特徴
  - デモサーバーで動作確認でき、リーダーボードも存在（アカウントの総レベル等でランク付け）。
  - テスト向けにゲーム挙動が調整されている（高速化された経験値曲線、無限の走力、ランダムイベント無効化）。
- 倫理・法的注意
  - 公式サービスや実アカウントへの利用禁止が明記されている。研究・教育目的の範囲で使うこと。
- ライセンス
  - MITライセンスで公開。改変・自己ホストが可能。

ローカルでの簡単な開始例（リポジトリをクローンしてデモへ接続）:

```bash
# リポジトリ取得
git clone https://github.com/MaxBittker/rs-sdk.git
cd rs-sdk

# 依存インストール（bun使用）
bun install

# デモサーバーに接続してボット作成（手動例）
bun scripts/create-bot.ts {username}
bun bots/{username}/script.ts
```

Claude経由で新しいボットを作る簡単なプロンプトもリポジトリに用意されています。チャットはデフォルト無効（scam対策）で、bot.envのSHOW_CHAT=trueで有効化可能。

## 実践ポイント
- まずはデモサーバーで試す：動作確認→挙動把握→自分のエージェント戦略を実験。
- Chat機能はデフォルトオフ：prompt injectionや詐欺を避けるため。必要ならbot.envで明示的にONにする。
- ローカルでgateway/botclient/engineを立ててデバッグ：実装変更やエージェント挙動の細かな検証が可能。
- 研究用途なら自己ホスト推奨：デモは永続性や稼働保証がないため、実験を継続するならサーバーを立てる。
- 法令順守：公式ゲームや実アカウントに対する自動化は禁止。研究・教育の枠組みで使うことを徹底する。

興味があるならまずリポジトリを覗ってREADMEとclaude.mdを確認し、簡単なボットを一体動かしてみてください。
