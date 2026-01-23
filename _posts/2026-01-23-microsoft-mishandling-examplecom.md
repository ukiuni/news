---
layout: post
title: "Microsoft Mishandling Example.com - Microsoftがexample.comを誤処理していた件"
date: 2026-01-23T13:49:50.580Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tinyapps.org/blog/microsoft-mishandling-example-com.html"
source_title: "Microsoft mishandling example.com"
source_id: 46731996
excerpt: "Outlook自動設定がexample.comをsei.co.jpに向け、認証情報が外部へ流出の恐れ"
---

# Microsoft Mishandling Example.com - Microsoftがexample.comを誤処理していた件
Outlookの自動設定が「example.com」を住友電工のメールサーバへ向ける重大ミス — あなたの“テスト用”パスワードが第三者に届く可能性

## 要約
MicrosoftのAutodiscover（Outlook向け自動設定）に、IANA予約済みのドメイン example.com が少なくとも2020年2月から誤って住友電気工業（sei.co.jp）のメールサーバへ割り当てられており、テスト用アカウントの認証情報が第三者サーバへ送られるリスクがあると報告されています。

## この記事を読むべき理由
日本の企業・開発者がテスト用やダミーアカウントで安全だと思って使っているドメインが、実際には外部サーバへ自動接続される可能性がある点は、ログ流出やコンプライアンス違反、情報漏洩につながるため即時確認と対策が必要です。

## 詳細解説
- 問題点：OutlookのAutodiscover（Microsoftのautodetectサービス）が example.com を解決し、imapgms.jnet.sei.co.jp（IMAP）と smtpgms.jnet.sei.co.jp（SMTP）を返す挙動を示した。example.com は RFC 2606 等でドキュメント用に予約されたドメインで、本来外部サービスに向くべきではない。  
- 確認方法（例）:
  - DNS確認:
```bash
dig MX example.com +short
dig CNAME autodiscover.example.com +short
dig SRV _autodiscover._tcp.example.com +short
```
  - Microsoft Autodiscover API 呼び出し（検証用）:
```bash
curl -v -u "email@example.com:password" "https://prod.autodetect.outlook.cloud.microsoft/autodetect/detect?app=outlookdesktopBasic"
```
  - 返却JSONは protocols 配列に imap/smtp のホスト名（sei.co.jp 系）とポートが含まれ、validated:false のまま表示された。  
- 発生範囲：Windows/macOS の Outlook、複数ネットワーク、DNSリゾルバ、Windows 365 Cloud PC 等で再現。  
- 原因の示唆：x-debug-support ヘッダ（Base64デコード）からこのエントリは2020-02-03に作成され、crowdsourced ではなく手動でデータベースに追加された可能性が高い。つまり Microsoft 側の内部データ誤登録が長期間放置されたと推定される。  
- リスク：テストで仮のメールアドレスとパスワードを使うと、クライアントが自動的に外部SMTP/IMAPに接続し認証情報を送る可能性がある（認証失敗でも認証トラフィックが発生する）。ログ・監査上の問題、第三者による解析・悪用のリスクがある。

## 実践ポイント
- すぐやること：
  - テストで example.com や他の予約済みドメインを使わない（例：example.test や自社管理のテストドメイン、ローカルホストで代替）。
  - 既にテストで使ったアカウントのパスワードは即時変更／無効化する。
  - 社内のテスト手順書を見直し、実運用と混同しないダミー運用ルールを作る。  
- 検査・防御：
  - 自社環境で Autodiscover の応答を curl 等で確認し、未知ホストが返る場合は記録する。  
  - メールクライアントの自動設定を無効化し、手動で安全な設定を使う運用に切り替える。  
  - 外向き通信ログで imapgms.jnet.sei.co.jp 等への認証試行がないか監視・調査する。  
- 報告：
  - Microsoft に対し事象を報告（MSRC など）し、該当データベースエントリの修正を促す。日本の情報セキュリティ責任者は関係当局やベンダーへ迅速に連絡を。  

短くまとめると、「見慣れたダミーアドレスが必ず安全とは限らない」— テスト運用の基本ルール（専用ドメイン・秘密鍵の分離・ログ監視）を見直す好機です。
