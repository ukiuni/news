---
layout: post
title: "Secure Boot, TPM and Anti-Cheat Engines - セキュアブート、TPM、アンチチートの関係"
date: 2026-01-22T11:46:13.747Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://andrewmoore.ca/blog/post/anticheat-secure-boot-tpm/"
source_title: "Secure Boot, TPM and Anti-Cheat Engines – Andrew Moore"
source_id: 1477244227
excerpt: "Secure BootとfTPMでチート抑止とハードウェアBANが現実化、プライバシー懸念も"
image: "https://andrewmoore.ca/blog/post/anticheat-secure-boot-tpm/opengraph-share.jpg"
---

# Secure Boot, TPM and Anti-Cheat Engines - セキュアブート、TPM、アンチチートの関係
ゲームの不正と戦う“ハードウェア縛り”は有効か？Secure BootとfTPMがオンライン対戦の安全性をどう変えるか

## 要約
アンチチートがSecure Bootと（f）TPMを要求する動きは、不正コードのカーネル侵入とアカウント乗り換えを技術的に困難にし、検出と永久追放の実効性を高める狙いがある。一方で導入やプライバシーへの懸念も生じている。

## この記事を読むべき理由
日本でもオンライン対戦やeスポーツの利用者は多く、PC環境の多様性やWindows 11移行状況を考えると、Secure Boot/TPM要件が自分のゲーム環境や今後の対戦ルールに与える影響を知ることは重要です。

## 詳細解説
- Secure Boot: UEFIファームウェアが起動イメージの署名を検証し、改ざんされたブートローダや未承認のカーネルドライバの読み込みを防ぐ仕組み。鍵階層（Platform Key → Key Exchange Key → DB/DBX）で誰が署名を追加・無効化できるかを管理する。
- TPM（Trusted Platform Module）: ハードウェアに紐づく変更不可能な鍵（Endorsement Key：EK）と、起動時の状態を記録するPCR（Platform Configuration Registers）を持つ。EKでハードウェア固有の識別が可能、PCRにはSecure Boot等の状態が測定・記録される（Measured Boot）。
- アンチチートの狙い: 
  - カーネルレベルのチート用ドライバをSecure Bootで容易に阻止。
  - TPMのEKで「そのマシン自体」を識別してハードウェアバン（アカウント作り直しでは回避できない罰則）を可能にする。
  - PCRログの検証により、起動プロセスが改ざんされていないことを遠隔で担保できる。
- 注意点: ソフトウェア報告だけではSecure Bootの有無を偽装できるため、TPMの測定・署名と組み合わせて検証する必要がある。dTPM（別体モジュール）はfTPM（CPU内蔵）に比べて識別に弱点があり、アンチチート側は利用制限を設ける可能性がある。
- プライバシー懸念: EK自体は個人情報を含まないが、ハードウェア識別と永続的なバン措置は議論を呼ぶ。実装次第で透明性やユーザー同意が重要になる。

## 実践ポイント
- 自分のPCでSecure Boot/TPM状態を確認する（管理者権限が必要）。
  
  ```powershell
  # PowerShell (Windows)
  Get-TpmEndorsementKeyInfo -HashAlgorithm SHA256
  ```
  ```bash
  # Linux (tpm2-tools が必要)
  sudo tpm2_readpublic -c 0x81010001 --format=pem -o EKpub_pem.pub
  sudo tpm2_getekcertificate -u EKpub_pem.pub -o EKcert_DER.cer
  ```
- BIOS/UEFIでSecure Bootを有効にし、fTPM（AMD/Intel）を有効化する。メーカーの手順に従いSetup Mode等に注意。
- 競技シーンやコミュニティのルールを確認し、導入方針とプライバシーポリシーを確認する（ハードウェアBANやデータ利用の範囲）。
- 自作PCや古いハードは互換性問題が出る可能性があるため、購入前に要件を確認する。

（参考）Windows 11導入の流れとCPU世代でfTPM普及が進んでいる点は、日本のゲーマー環境にも影響します。
