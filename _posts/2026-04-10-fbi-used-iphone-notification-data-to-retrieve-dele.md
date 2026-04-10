---
layout: post
title: "FBI used iPhone notification data to retrieve deleted Signal messages - FBIがiPhoneの通知データから削除済みSignalメッセージを復元"
date: 2026-04-10T12:37:56.496Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://9to5mac.com/2026/04/09/fbi-used-iphone-notification-data-to-retrieve-deleted-signal-messages/"
source_title: "FBI used iPhone notification data to retrieve deleted Signal messages - 9to5Mac"
source_id: 47716490
excerpt: "FBIがiPhoneの通知履歴から削除済みSignalメッセージを復元。"
image: "https://i0.wp.com/9to5mac.com/wp-content/uploads/sites/6/2025/12/Reddit-comment-led-police-to-identify-Brown-University-shooter.jpg?resize=1200%2C628&quality=82&strip=all&ssl=1"
---

# FBI used iPhone notification data to retrieve deleted Signal messages - FBIがiPhoneの通知データから削除済みSignalメッセージを復元
削除したはずのSignalメッセージがiPhoneの通知履歴に残る――あなたの端末、本当に安全ですか？

## 要約
米国の裁判証言によれば、FBIは被告のiPhoneから「通知の内部保存領域」に残っていた受信Signalメッセージの内容を復元した可能性がある。Signal本体は削除されていたが、通知プレビューが内部に残っていたという報告。

## この記事を読むべき理由
通知は「軽いUI情報」に見えるが、実務上は端末内やバックアップに残り得る。日本でもプライバシー対策や法執行機関によるデータ取得の現実に直面する可能性があり、対策を知る価値がある。

## 詳細解説
- 何が起きたか：裁判の証拠資料（Exhibit 158）では、削除済みのSignalアプリからの「着信メッセージ（送信側は含まれない）」がiPhoneの内部通知ストレージから取得されたと説明される。  
- 技術的要因：
  - iOSは通知のプレビュー（本文テキスト）を内部データベースやキャッシュに保持することがある。アプリ削除だけではそのデータや通知トークンが即座に無効化されない場合がある。  
  - 端末のセキュリティ状態（BFU/AFU／ロック解除状態）によってアクセス可能なデータ範囲が変わる。端末がアンロックされているとより多くの保護データにアクセス可能になる。  
  - 証拠抽出はデバイス本体のイメージやバックアップ、あるいは市販の法執行向け解析ツールを介して行われた可能性がある。  
  - AppleはiOS 26.4でプッシュ通知トークンの検証を変更しており、タイミング的に関連が示唆されているが直接の因果は不明。  
- Signal側の設定：Signalには通知で本文を隠すオプションがあるが、今回の端末では有効化されていなかった模様。

## 実践ポイント
- 通知プレビューをオフにする（Signalの「通知プレビューを表示しない」設定、iOSの「通知のプレビュー」を「ロックされているときは非表示」または「しない」に）。  
- 端末を使わないときはロックを厳格に（強力なパスコード、Biometricsと組み合わせ）。  
- 不要な通知は届かないようにアプリ側・サーバ側設定を見直す。重要情報は通知で全文表示しない運用を徹底。  
- 端末を手放す・譲渡する際はバックアップと通知キャッシュを含め完全消去（出荷時リセット）する。  
- 常にiOSを最新に更新する（通知トークン管理などの改善が行われることがある）。  

短いまとめ：アプリを消しても通知の痕跡は残る可能性がある。設定と運用で露出を減らすことが現実的な対策です。
