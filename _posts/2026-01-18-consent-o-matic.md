---
layout: post
title: "Consent-O-Matic - クッキー同意自動応答ツール"
date: 2026-01-18T10:22:16.527Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/cavi-au/Consent-O-Matic"
source_title: "GitHub - cavi-au/Consent-O-Matic: Browser extension that automatically fills out cookie popups based on your preferences"
source_id: 46666283
excerpt: "ワンクリックでクッキー同意を自動処理、200種以上のCMPに対応するオープンソース拡張"
image: "https://opengraph.githubassets.com/f163c751338e162b0445dfd54a31155b1e7e85ccb2957db8114519a8df138a36/cavi-au/Consent-O-Matic"
---

# Consent-O-Matic - クッキー同意自動応答ツール
魅力的なタイトル: 「もうポップアップに悩まされない──ワンクリックでクッキー同意を自動化する無料拡張」

## 要約
Consent-O-Maticは、Webサイトのクッキー同意ポップアップ（CMP）を利用者の設定に従って自動で操作するオープンソースのブラウザ拡張です。多数の主要CMPに対応し、ルールを追加・共有して継続的に改善できます。

## この記事を読むべき理由
- 毎回の「同意」「設定を保存」クリックにうんざりしている人に役立つ実用ツールだから。  
- 日本でもOneTrustやCookieBotなど国際的なCMPが使われており、業務でのブラウジング効率化やプライバシー管理に直結するから。

## 詳細解説
- 概要: デンマーク・Aarhus大学のCAVIが開発。拡張インストール時に好みを設定すると、ページ上の既知のCMPを検出して自動で操作し、アイコンにチェックマークで完了を示します。オープンソースなのでルール追加や改良に誰でも参加可能。
- 対応範囲: 200以上のCMP（UserCentrics、CookieBot、OneTrust など）。不具合は報告・修正でき、ルールリストは更新され続ける。
- 仕組み（技術的ポイント）:
  - ルールはJSONで定義。各CMPごとに detectors（検出）と methods（操作）が記述される。
  - detectors は presentMatcher（DOMに存在するか）と showingMatcher（実際に表示されているか）で判定。
  - methods は HIDE_CMP / OPEN_OPTIONS / DO_CONSENT / SAVE_CONSENT の順で実行される（存在すれば）。
  - DOM選択は parent と target の二段構造で柔軟に指定可能。textFilter、styleFilter、displayFilter、iframeFilter、childFilter など細かな条件で要素を絞れるため、shadow DOMやiframe内のボタンも処理可能。
  - 主なアクション例: click（クリックをシミュレート）、list（複数処理）など。
- プライバシーと権限: ページの読み取り、タブURL情報、ストレージ利用のみ。外部と通信するのはルールの取得/更新と、ユーザーが「動作しない」と報告したときのみ（報告はURIエンコードされたURLを送信）。
- インストール・開発: 公式ストアからのインストール推奨。ソースからビルドする場合は GitHub リポジトリをクローンして npm でビルド可能。
  
  ```bash
  # 例（開発用）
  git clone https://github.com/cavi-au/Consent-O-Matic.git
  cd Consent-O-Matic
  npm install
  npm run build-chromium
  ```

## 実践ポイント
- まずは公式ストアからインストールして、初回設定で自分の同意ポリシーを選ぶ（例えば「広告拒否」「必要最小限のみ許可」など）。
- 日本でよく使われるサービス（楽天、ヤフー、LINEなど）で動作確認する。動かなければ拡張の「Let us know!」で報告。
- ルールを自分で追加したい場合は、拡張の「Rule lists」にカスタムJSONのURLを登録するか、GitHubでPull Requestを送る。
- 開発者向けには、問題のあるポップアップを特定して rules.json を編集・テストするワークフロー（Load Unpacked）がおすすめ。社内でブラウザ自動化を行う場合は、このルール定義が自動化スクリプトと相性が良い。
- 注意点: 自動操作は誤操作や誤検出を招くことがあるため、金融やログイン必須のサイトでは一時的に無効化して挙動を確認すること。

短くまとめると、Consent-O-Maticは「毎回の同意ダイアログを自分ルールで自動化してブラウジングを快適にする」ための実用的なオープンソース拡張で、日本のユーザーや開発者もルール追加で恩恵を受けられます。興味があればリポジトリを覗いて、よく使う日本のサイト向けルール作りに貢献してみてください。
