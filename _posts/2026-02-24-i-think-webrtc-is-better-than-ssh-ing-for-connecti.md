---
layout: post
title: "I think WebRTC is better than SSH-ing for connecting to Mac terminal from iPhone - iPhoneからMacのターミナルに接続するならSSHよりWebRTCの方が良いと思う"
date: 2026-02-24T20:36:12.395Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://macky.dev"
source_title: "Macky - Connect to Mac Terminal from iPhone"
source_id: 47140612
excerpt: "iPhoneからMacターミナルへ、ポート開放不要でWebRTCのE2E暗号化接続が可能に"
image: "https://macky.dev/app_icon.png"
---

# I think WebRTC is better than SSH-ing for connecting to Mac terminal from iPhone - iPhoneからMacのターミナルに接続するならSSHよりWebRTCの方が良いと思う

魅力的なタイトル: iPhoneでMacのターミナルを「安全かんたん」に使う方法 — SSHじゃなくてWebRTCを選ぶ理由

## 要約
WebRTCを使ったMackyは、iPhoneからMacのネイティブシェル（zsh/bash）へE2E暗号化で手軽に接続できるサービス。ポート開放や複雑なSSH設定を不要にし、認証・デバイス制御・プライバシー保護も組み込まれている。

## この記事を読むべき理由
Mac＋iPhoneの組み合わせが一般的な日本の開発者／愛好者にとって、外出先から安全にターミナルアクセスするニーズは高い。社内ポリシーや家庭環境でSSHのポート開放が難しい場合、代替として実用的な選択肢を知っておく価値がある。

## 詳細解説
- トランスポート: MackyはWebRTCのDTLS＋SRTP経路を使い、ネットワーク上での盗聴を防ぐE2E暗号化トンネルを構築する。これによりNAT越えやファイアウォール透過が容易になる。  
- 検証と認証: サインリング段階でのトークン検証（Dual Layer Identity）に加え、端末側に設定するマスターパスワードで実際の端末アクセスを二重に保護する設計。アカウントが侵害されても端末は守られることを意図している。  
- 認可（許可管理）: ホスト側で各デバイスIDを明示的に承認するデバイス・アロウリスト方式を採用。見知らぬ端末の接続を防げる。  
- プライバシー: シグナリング（ハンドシェイク）のみをコーディネートする「ブラインド」サーバー構成。実際の端末データはクラウドを経由しないと説明されている。  
- 付帯機能: Claude（Anthropic）やCodex（OpenAI）連携といった開発支援の組み込みが見られる（記事抜粋に基づく）。  
- 対応環境・料金: ホストはmacOS 15+、リモートはiOS 18+。無料プラン（短時間・1ホスト・1リモート）と、無制限セッションやバックグラウンド接続・ログ保持などを含む有料（買切り）プランがある。

## 実践ポイント
- まずは無料プランで動作確認：macOS/iOSのバージョン要件を満たしているか確認して試す。  
- セキュリティ設定：マスターパスワードを必ず設定し、ホストでデバイス許可リストを有効化する。  
- 企業利用の注意：社内セキュリティ／MDMポリシーに照らして可否を確認する。  
- Proを検討するケース：複数デバイス運用や常時接続・接続ログが必要なら買切りプランが実用的。  
- 比較視点：従来のSSHは自己管理の透明性が高いが、NAT/ポート開放や鍵管理の手間がある。利便性／セキュリティのトレードオフを評価して選ぶ。

原典: "I think WebRTC is better than SSH-ing for connecting to Mac terminal from iPhone"（macky.dev）
