---
layout: post
title: "BrowserStack local leaking private key - BrowserStack Local が秘密鍵を漏洩？"
date: 2026-04-07T11:24:55.404Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://infosec.exchange/@badkeys/116359377342260172"
source_title: "badkeys: &quot;There&#39;s a software called &quot;BrowserStack local&quot;, w…&quot; - Infosec Exchange"
source_id: 1289131572
excerpt: "BrowserStack Localに秘密鍵混入の指摘、CIでの流出リスクを今すぐ確認"
---

# BrowserStack local leaking private key - BrowserStack Local が秘密鍵を漏洩？
あなたのCI/CDが丸裸に？BrowserStack Localで指摘された「秘密鍵流出」の可能性

## 要約
Infosec研究者の報告によると、BrowserStackのローカルトンネルクライアント（BrowserStack Local）に「秘密鍵が含まれている／漏洩している可能性」が指摘されました。CIや共有環境で使うとリスクになり得ます。

## この記事を読むべき理由
多くの開発チームがローカル環境を外部サービスでテストするためにBrowserStack LocalをCIに組み込んでいます。もしバイナリや動作が秘密情報を露出するなら、社内システムや認証情報が危険に晒されるため、特に日本の企業やクラウドCI利用者は知っておくべき問題です。

## 詳細解説
- 問題の概要（報告ベース）  
  - Mastodon上の投稿（badkeys）では、BrowserStack Localに関連して「プライベートキーがバイナリ内／実行時ファイルに存在する／漏れている」可能性が示されています。投稿自体は調査結果のアラートであり、具体的な鍵の中身公開ではなく「秘匿情報が含まれる恐れがある」という指摘です。  
- 影響範囲（想定）  
  - CIランナーや共有ビルド環境で使われると、同一環境の他プロジェクトや攻撃者により鍵が抽出されうる。抽出された鍵はトンネリングの認証や中間者攻撃（MITM）、内部サービスへの不正アクセスに利用される可能性があります。  
- 技術的なポイント（検証手法の例）  
  - バイナリや実行ディレクトリをstringsで調べ、「BEGIN PRIVATE KEY」などの文字列が含まれていないか確認する。実行中のプロセスが一時ファイルを作る場合は /tmp やカレントディレクトリを監査する。ネットワーク接続を監視して不審な接続がないか確認する。  
  - 例（簡易チェック）：
```bash
# バイナリに秘密鍵の痕跡がないか調べる
bash
strings ./BrowserStackLocal | grep -i "BEGIN .*PRIVATE KEY"

# 実行中に作られる一時ファイルを監視（簡易）
bash
lsof -p <pid_of_BrowserStackLocal> | awk '{print $9}' | xargs -I{} sh -c 'file {} 2>/dev/null'
```
- 注意点  
  - 上記はあくまで調査手順の例です。実際の漏洩の有無や影響はBrowserStackや独立したセキュリティ調査で確定する必要があります。

## 実践ポイント
- まずは影響範囲確認：CI/CDでBrowserStack Localを使っているジョブを洗い出す。  
- バージョン確認と更新：BrowserStackからの公式アナウンスや最新バージョンを確認し、パッチが出ていれば速やかに更新。  
- 環境隔離：共有ランナーではなく専用ランナーやエポックごとのクリーン環境で実行する。  
- 鍵のローテーション：疑いがある場合、該当するトンネルやサービスの鍵・トークンを即時ローテーション。  
- 監査とログ：ビルドログ、/tmp、プロセスのファイルオープン、ネットワーク接続を監査し、不審な痕跡がないか確認する。  
- 代替策検討：必要なら別の安全なトンネル手段（VPNや社内プロキシ、信頼できるZero Trustソリューション）を検討する。

元ツイート／投稿は「警告」に当たるため、確定情報はBrowserStackの公式発表や追試による検証を待ち、リスク軽減策を優先してください。
