---
layout: post
title: "Why does SSH send 100 packets per keystroke? - なぜSSHは1キー押下で100パケットを送るのか？"
date: 2026-01-22T19:38:35.974Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://eieio.games/blog/ssh-sends-100-packets-per-keystroke/"
source_title: "Why does SSH send 100 packets per keystroke? · eieio.games"
source_id: 46723990
excerpt: "SSHの新機能が1キーで数百のダミーパケットを送信し、遅延と帯域を激増させ即効対処法も示す"
image: "https://eieio.games/images/ssh-sends-100-packets-per-keystroke/og_image.png"
---

# Why does SSH send 100 packets per keystroke? - なぜSSHは1キー押下で100パケットを送るのか？
ゲームの遅延を一掃する「SSHのキー入力難読化」を見抜いて性能を取り戻した話

## 要約
SSHクライアントが「keystroke timing obfuscation（キー入力タイミング難読化）」のために短い“chaff”パケット（36バイト）を約20ms間隔で大量送信しており、1キーで数百パケットに達する。これを無効化するとCPUと帯域が大幅に下がる。

## この記事を読むべき理由
- SSHを使ったリアルタイムアプリ（TUIゲーム、遠隔ターミナル、ブラウザベースの端末）で意外な遅延・帯域消費に悩んでいるなら即効性のある対処が得られる。  
- セキュリティ（入力タイミング情報漏洩）と性能のトレードオフを理解できる。

## 詳細解説
- 症状: 1キー押下でpcapを解析すると総パケットの約66%が36バイトの送信データ、残りに0バイトのACK。データパケット間隔は平均約20ms、1〜2秒で数十〜数百の「chaff」が出る。  
- 発見方法: tcpdump/tsharkでパケット分布を可視化、ssh -vvv でログを確認すると "obfuscate_keystroke_timing: starting: interval ~20ms" のデバッグ出力が出力される。  
- 原因: 2023年に追加されたSSHのキー入力タイミング難読化機能。タイプ速度の差からキーを推測されるリスクを下げるため、クライアントがSSH拡張（SSH2_MSG_PING/PONG をローカル拡張領域で実装）を使ってchaffパケットを送る。これをサーバがext-infoで対応を宣言するとクライアントはchaffを送信する。  
- 影響: セキュリティ上は有益だが、低遅延・大規模同時接続を目指すゲームや高頻度描画アプリでは大きなオーバーヘッドになる。  
- サーバ側対処の考察: クライアント側オプションで無効化できるが（後述）、ユーザにオプションを要求せず自動化したい場合はサーバがその拡張を広告しないようにする手がある。Goのcrypto/ssh等ライブラリではext-infoの導入コミットを差し替えることで解決できるが、ライブラリをフォークして維持するコストとセキュリティ影響を考慮する必要がある。

## 実践ポイント
- 確認コマンド例:
  - tcpdumpでフィルタ: sudo tcpdump -i eth0 'port 22' -w sample.pcap  
  - sshデバッグ: ssh -vvv user@host（"obfuscate_keystroke_timing" のログを探す）  
- 即効の回避（クライアント側）:
  - ssh起動時にオプションを付ける: 
```bash
# bash
ssh -o ObscureKeystrokeTiming=no user@host
```
- サーバ側で対処する場合の方針:
  - サーバが [email protected] 相当のext-infoを宣言しないようSSH実装を調整（例：Goのcrypto/sshをフォークして該当コミットを除去）。利点はクライアントに依存せず自動的にchaffを抑制できるが、ライブラリ維持とセキュリティレビューが必要。  
- 運用上の注意:
  - 難読化を無効化するとタイピング側チャネルからの情報漏洩リスクが戻るため、公開サーバや不特定多数が接続する環境では慎重に。社内・信頼できる環境や低レイテンシが最優先の用途で限定的に無効化するのが現実的。  
- テスト手順:
  1. ベースラインをtcpdumpで取得（帯域/CPUを記録）。  
  2. クライアント側で ObscureKeystrokeTiming=no を適用して差分を確認。  
  3. 長期運用するならサーバ側修正（ライブラリ差し替え）を検討し、セキュリティ影響をレビューする。

以上。必要なら短い手順書（サーバ側のGoライブラリ差し替え手順など）を補足する。
