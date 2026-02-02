---
layout: post
title: "MaliciousCorgi: AI Extensions send your code to China - MaliciousCorgi：AI拡張があなたのコードを中国に送信"
date: 2026-02-02T14:01:48.803Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers"
source_title: "Malicious VS Code AI Extensions Harvesting Code from 1.5M Devs"
source_id: 46855527
excerpt: "人気VSCodeAI拡張が開いたファイルを中国へ送信、社内コードと鍵が流出する危険"
---

# MaliciousCorgi: AI Extensions send your code to China - MaliciousCorgi：AI拡張があなたのコードを中国に送信
1.5M人がインストールした“可愛い”AI拡張が職場のソースコードを丸ごと外部へ送る危険性

## 要約
VS Code用とされるAI拡張（合計約1.5Mインストール、例: whensunset.chatgpt-china, zhukunpeng.chat-moss）が正常に動作する一方で、開いたファイルや編集内容を無断で中国のサーバへ送信することが確認された。

## この記事を読むべき理由
日本企業・開発者も標的になり得る。社内コード、APIキー、.envやSSH鍵などが流出すれば事業・顧客情報に直接影響するため、迅速な検査と対策が必要。

## 詳細解説
- 感染カバーストーリー：拡張はAI補助（補完・解説）を正常に提供し、評判やマーケットの信頼を得ている点が危険性を増幅。  
- 3つのデータ収集チャネル
  1. リアルタイム監視：ファイルを開いただけでファイル全体をBase64化してwebview経由で外部送信。編集ごとにも送信。  
  2. サーバ制御の大量収集：サーバから返すJSONのjumpUrlで「getFilesList」等を実行させ、ワークスペースから最大50ファイルを一括取得・送信。ユーザーには通知されない。  
  3. プロファイリング：目に見えないiframeで複数の中国系解析SDK（例: Zhuge.io、GrowingIO、TalkingData、Baidu Analytics）を読み込み、デバイス/ユーザ/企業の振る舞いを詳細にプロファイリング。価値の高いターゲットを特定後に狙い撃ちする流れ。  
- 影響範囲：ソースコード、未公開機能、認証情報（APIキー、DBパスワード）、クラウド認証ファイル、SSH鍵などが含まれる。  
- 技術的な巧妙さ：正しく機能するため、ユーザーは拡張を信頼しやすく、マーケットとレビューだけでは検出困難。

## 実践ポイント
- 即時確認（個人・チーム双方）
  - VS Code拡張一覧を確認し、whensunset.chatgpt-china / zhukunpeng.chat-moss 等があればアンインストール。  
  - ネットワークログで不審なドメイン（例: aihao123.cn 等）への通信を検出したら遮断・調査。  
  - 重要な秘密鍵・シークレットは念のためローテート。  
- 予防策（組織向け）
  - 開発端末のソフトウェアホワイトリスト化とマーケットプレイスの承認フロー導入。  
  - 拡張の権限・webview通信・外部ホストへのアクセスを監査するポリシーを適用。  
  - エンドポイント検出（ファイルI/O監視、未知のwebview/iframe挙動の検出）を導入。  
  - オフライン環境や機密プロジェクトは外部接続を制限した隔離環境で作業。  
- IOC（参考）
  - VS Code拡張：whensunset.chatgpt-china、zhukunpeng.chat-moss  
  - ドメイン例：aihao123.cn

短期的には「拡張の棚卸し→不審拡張除去→シークレット回収」を必ず行い、長期的には拡張の導入管理とエンドポイント可視化を整備すること。
