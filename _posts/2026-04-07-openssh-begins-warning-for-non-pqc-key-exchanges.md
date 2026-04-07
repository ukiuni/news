---
layout: post
title: "OpenSSH begins warning for non-PQC key exchanges - OpenSSH、非PQC鍵交換に対する警告を開始"
date: 2026-04-07T14:25:12.865Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.openssh.com/pq.html"
source_title: "OpenSSH: Post-Quantum Cryptography"
source_id: 1307776723
excerpt: "OpenSSHが非PQC鍵交換を警告、今盗まれ後で解読される恐れに備え早急にバージョンと設定を確認"
---

# OpenSSH begins warning for non-PQC key exchanges - OpenSSH、非PQC鍵交換に対する警告を開始
今すぐ確認を：あなたのSSH接続は「今盗って後で解読される」リスクにさらされているかもしれません

## 要約
OpenSSHはポスト量子暗号（PQC）による鍵交換を既にサポートしており、OpenSSH 10.1からPQCでない鍵交換を使う接続に対して警告を出すようになりました。これは「今盗って後で解読する（store now, decrypt later）」攻撃への対策です。

## この記事を読むべき理由
日本の企業・クラウド利用者は長期間保存される機密データが多く、量子耐性のないSSH接続は将来の量子機による解読リスクに曝されます。今から対策を始めることで重要データを守れます。

## 詳細解説
- OpenSSHのPQC対応状況（簡潔）
  - OpenSSH 9.0（2022年4月）で最初に sntrup761x25519-sha512 を導入。
  - OpenSSH 9.9 で mlkem768x25519-sha256 を追加。
  - OpenSSH 10.0（2025年4月）で mlkem768x25519-sha256 が新しいデフォルトに。
  - OpenSSH 10.1 から、PQCでない鍵交換を選んだ場合に以下の警告を表示：
    WARNING: connection is not using a post-quantum key exchange algorithm. This session may be vulnerable to "store now, decrypt later" attacks.
- なぜ今重要か
  - 量子コンピュータが将来、鍵交換や署名を破る可能性があり、暗号化通信を「今」盗んで「後で」解読されるリスクがあるため。推定タイムラインは5〜20年（多くは2030年代半ばを指摘）。
- ハイブリッド設計
  - OpenSSHのPQC鍵交換は従来アルゴリズム（例：x25519）と組み合わせたハイブリッドで、万が一PQC部分が弱くても従来の安全性を下回らない設計。
- 署名アルゴリズムについて
  - RSA/ECDSA等も量子に脆弱だが、署名については「過去トラフィックの即時危険」はない（ただし将来に向けて鍵更新が必要）。OpenSSHは今後PQC署名を追加予定。
- 警告の制御
  - デフォルトで警告は表示されるが、ssh_configのWarnWeakCryptoオプションで無効化可能（ただし推奨はしない）。

## 実践ポイント
- 自分の環境でバージョン確認：
```bash
ssh -V
```
- 接続時の鍵交換を確認（デバッグ出力）：
```bash
ssh -vvv user@host
```
- サーバーの対応状況確認／対応方法
  - サーバーをOpenSSH 9.0以上（sntrup対応）、9.9以上（mlkem対応）へアップデートするのが理想。可能なら10.0以上へ。
  - sshd_config / ssh_config の KexAlgorithms 設定でPQアルゴリズムが無効化されていないか確認する。
- 警告を一時的に抑える（非推奨、例としてFAQの記述を参照）：
```bash
# ~/.ssh/config または /etc/ssh/ssh_config の例
Match host unsafe.example.com
    WarnWeakCrypto no-pq-kex
```
- 日本向けの実務判断
  - 長期保存する機密データを扱うシステム（法務、人事、医療、金融、IoTログなど）は優先的にサーバーのOpenSSH更新と設定確認を行う。

まずは自分のクライアント／サーバーのOpenSSHバージョンを確認し、運用ポリシーに沿って順次アップデートと設定見直しを行ってください。
