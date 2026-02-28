---
layout: post
title: "OpenAI – How to delete your account - OpenAI – アカウント削除方法"
date: 2026-02-28T12:26:42.447Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://help.openai.com/en/articles/6378407-how-to-delete-your-account"
source_title: "OpenAI – How to delete your account"
source_id: 47193478
excerpt: "ChatGPTアカウントの完全削除手順と課金・再利用の落とし穴を図解"
---

# OpenAI – How to delete your account - OpenAI – アカウント削除方法
今すぐわかる：ChatGPT（OpenAI）アカウントの完全削除ガイド — 失敗しない手順と注意点

## 要約
OpenAIアカウントは「プライバシーポータル経由」と「ChatGPT内の自己操作」の2通りで削除でき、削除するとChatGPT Plusは自動キャンセルされ、復活はできません。メール再利用は30日後、電話番号は利用回数制限があります。

## この記事を読むべき理由
個人情報保護や請求停止、アカウント運用の制約（メール再利用や電話番号の上限）など、日本の開発者・利用者に直接影響するため、正確な手順と落とし穴を把握する価値があります。

## 詳細解説
- 削除方法（2オプション）  
  - オプションA：Privacy Portal（https://privacy.openai.com/）  
    1. 「Make a Privacy Request」を選択  
    2. 「I have a consumer ChatGPT account」→「Delete my ChatGPT account」を選ぶ  
    3. 画面の案内に従う（ログイン不可時はパスワードリセット手順へ）  
  - オプションB：ChatGPT内の自己操作（Web）  
    1. chat.openai.com にサインイン → プロフィール → Settings → Account  
    2. 「Delete account」→ 削除条件：直近10分以内にログイン済みであること（超過なら再ログイン）  
    3. 確認画面で自分のメールアドレスと "DELETE" を入力し、「Permanently delete my account」を実行  
  - モバイル：iOS/Android 各アプリのヘルプ記事に従う  
- 重要な挙動と制約  
  - ChatGPT Plusはアカウント削除で自動キャンセル（課金停止）  
  - 削除済みアカウントは再活性化不可。メールは30日後に同一アドレスで再作成可（完全削除が前提）  
  - 電話番号は検証で3アカウントまで利用可能。削除してもその枠は消えず、完全削除後30日で電話番号が削除され再利用可能になる場合あり  
  - 認証方式の変更は削除で解決しない（例：削除でメール→Google/Appleに自動変わるわけではない）  
- データ取り扱い  
  - 削除したチャット：通常30日以内に完全削除（復元不可。法的/安全理由で保持される例外あり）  
  - アーカイブ：履歴から非表示にするだけで保存され続ける  
  - メモリ：個別削除または「Delete all」で一括削除可能  
  - ユーザー提供コンテンツ：個人向けサービスではモデル改善に使われる場合がある（オプトアウト設定を確認）。Enterprise契約は別扱い（企業データは通常学習に使わない）  
  - SoraデータはSora設定から削除可能  
- よくあるエラー表示  
  - 「You do not have an account because it has been deleted or deactivated」は対象メールのアカウントが削除/無効化済みである合図

## 実践ポイント
- アクション前：重要な会話やデータはローカルにバックアップする（削除後は基本復元不可）。  
- ChatGPT Plusだけやめたい場合は、まずサブスクリプションのキャンセル手順を行う（アカウント削除は最後の手段）。  
- Webで削除する場合は直前にログインしておき、10分ルールに注意。  
- 同一メールで再作成したいなら「30日待つ」。電話番号の利用回数制限（3回）も計画に入れる。  
- 個人情報やモデル学習への利用を避けたいなら、オプトアウト設定やEnterprise向けの扱いを確認する。
