---
layout: post
title: "OpenSSL: Stack buffer overflow in CMS AuthEnvelopedData parsing - OpenSSL: CMS AuthEnvelopedData 解析でのスタックバッファオーバーフロー"
date: 2026-01-27T17:33:53.541Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://openssl-library.org/news/vulnerabilities/#CVE-2025-15467"
source_title: "Vulnerabilities | OpenSSL Library"
source_id: 46782662
excerpt: "CMSのAuthEnvelopedData解析でIVが原因の脆弱性、即更新して危険回避を"
---

# OpenSSL: Stack buffer overflow in CMS AuthEnvelopedData parsing - OpenSSL: CMS AuthEnvelopedData 解析でのスタックバッファオーバーフロー
AES-GCM系のCMS/S/MIME処理で即クラッシュ or 最悪はRCEも—今すぐバージョン確認と更新を

## 要約
OpenSSLがCVE-2025-15467を公表。CMSのAuthEnvelopedData（AEAD、例：AES-GCM）を解析する際、ASN.1で与えられたIVを固定長スタックバッファへ検証なしにコピーするため、悪意あるIVでスタックバッファオーバーフローを引き起こし得る。対象はOpenSSL 3.0～3.6系の一部（下記参照）。

## この記事を読むべき理由
OpenSSLはサーバやメールソフト、セキュリティ機器、組み込み機器まで幅広く使われるため、CMS／S/MIMEを扱うアプリが無防備にクラッシュしたり、プラットフォーム次第ではリモートでのコード実行につながる可能性がある。日本の企業でもメールゲートウェイや証明書管理ツール、組み込み機器で影響を受けやすい。

## 詳細解説
- 問題点：CMSのAuthEnvelopedDataでAEAD暗号（AES-GCM等）を使う場合、IV（Initialization Vector）長を検査せずに固定サイズのスタックバッファへコピーしている。攻撃者が過大なIVを仕込んだCMSメッセージを送ると、認証前にスタック上で書き越しが起きる。
- 重要な性質：オーバーフローは認証前に発生するため、有効な鍵や正しいタグが不要でトリガー可能。結果としてクラッシュ（DoS）や、環境によってはリモートコード実行（RCE）につながる危険性がある。
- 影響範囲（OpenSSL側の公表）：影響あり — 3.6.0～3.6.1未満、3.5.0～3.5.5未満、3.4.0～3.4.4未満、3.3.0～3.3.6未満、3.0.0～3.0.19未満。FIPSモジュール境界外の実装のため、FIPSモジュール自体は影響外とされている。
- 併記の脆弱性：同時にPKCS#12のPBMAC1未検証によるスタックオーバーフロー（CVE-2025-11187）や、コマンドラインツールの16MB切捨て（CVE-2025-15469）など複数の問題が報告されているため、総合的なアップデートが推奨される。

## 実践ポイント
- まずバージョン確認：  
```bash
openssl version -a
```
- 対応：OSベンダーのセキュリティ更新（パッケージ）を適用するのが最も安全。パッチ済みリリース（例：3.6.1、3.5.5、3.4.4、3.3.6、3.0.19以降）へ更新する。  
- 緊急回避（更新できない場合）：外部から受け取るCMS/PKCS#7/S/MIMEを解析しない、もしくは事前に検査（サイズ制限）を入れる。メールゲートウェイやサンドボックスでの検査を強化。  
- 依存調査：CI/CD、コンテナ、組み込みファームウェア、サードパーティ製ライブラリが古いOpenSSLをバンドルしていないかを確認。  
- ログと監視：クラッシュや異常なTLS/CMS関連の接続失敗が発生していないか監視を強化。

参考：OpenSSL公式アドバイザリ（CVE一覧）を確認して、利用中のバージョンに対応するパッチを適用すること。
