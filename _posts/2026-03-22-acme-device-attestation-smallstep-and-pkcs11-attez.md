---
layout: post
title: "ACME device attestation, smallstep and pkcs11: attezt - ACMEデバイス認証、smallstepとPKCS#11：attezt"
date: 2026-03-22T03:00:55.903Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://linderud.dev/blog/acme-device-attestation-smallstep-and-pkcs11-attezt/"
source_title: "ACME device attestation, smallstep and pkcs11: attezt"
source_id: 1242955561
excerpt: "TPMとPKCS#11で短期ハード結合証明書を実現するattezt実装を解説"
---

# ACME device attestation, smallstep and pkcs11: attezt - ACMEデバイス認証、smallstepとPKCS#11：attezt
TPMで「あなたのマシン」を証明する——ホームラボでも使える短期・ハードウェア結合型証明書ワークフロー

## 要約
TPMベースのデバイス認証（ACMEのdevice-attest-01）を、smallstep CAと連携して実現するオープン実装「attezt」とそのエージェントで、TPM鍵をPKCS#11経由で使い短期のデバイス証明書を発行できる仕組みを紹介する。

## この記事を読むべき理由
日本の企業・開発者にも当てはまるポイント：ほとんどのPC/サーバにTPMが載っており、ハードウェア結合の短期証明書は長期鍵運用のリスクを下げ、ホームラボや社内システムで認証を簡潔に・安全にする実用的な手法だから。

## 詳細解説
- device-attest-01（ACME拡張）  
  ACMEに新しいチャレンジ方式が加わり、TPM等のハードウェアで生成・保護された鍵の「生成元」を証明させることでデバイス単位の証明書を発行する。ACME自身は直接検証せず、外部の「attestation CA」が有効性を判断する。
- 主要コンポーネント（atteztプロジェクト）  
  - atteztd：小さなattestation CA。TPMのEndorsement Key（EK）ハッシュを登録して許可済みデバイスだけを受け付ける。  
  - attezt：クライアント／管理ツール。EKハッシュの登録やCAチェーン取得などを行う。  
  - attezt-agent：ローカルで動くデーモン。TPM鍵をPKCS#11インターフェース（p11-kit経由）として公開し、ACMEクライアント動作を仲介する（smallstepの商用エージェントを代替）。
- フロー（概略）  
  1. TPMのEK公開鍵を取り出しハッシュ化してattestation CAに登録（EKハッシュでデバイス識別）。  
  2. attestation CAはエンロール済みデバイスに対して、EKチャレンジを用いた検証を行い、デバイス上で作成したAttestation Keyに署名する。  
  3. その署名付きAttestation Keyを使ってACMEサーバ（smallstep）のdevice-attest-01チャレンジを満たし、短期のデバイス証明書を取得する。  
- 実際のコマンド例（要約）
  ```bash
  # EKのハッシュを取得（例）
  tpm2_nvread 0x01c00002 > ekpub
  openssl x509 -in ekpub -pubkey -noout | openssl pkey -pubin -outform der | sha256sum

  # atteztでCA作成・enroll
  attezt ca create
  atteztd &

  attezt ca enroll <ek-hash>

  # smallstepにプロビジョナー追加（attestation rootを渡す）
  curl -O https://attezt.home.arpa/root.pem
  step ca provisioner add acme-da \
    --type ACME \
    --challenge device-attest-01 \
    --attestation-format tpm \
    --attestation-roots ./root.pem

  # attezt-agentを起動してenroll→証明書取得
  sudo attezt-agent
  attezt enroll --acme "https://ca.home.arpa/acme/acme-da" --attestation "https://attezt.home.arpa"
  ```
- PKCS#11連携  
  attezt-agentはp11-kitソケットを提供し、一般的なツール（pkcs11-tool、ブラウザやSSH エージェント等）からTPM鍵を扱えるようにする。smallstep純正のagentが商用であるため、オープンに使える代替として有用。
- 注意点  
  実装は進行中でroot権限や手作業の設定が必要。現状は短期（例：24時間）証明書を想定したワークフロー。

## 実践ポイント
- まず自分のマシンにTPMがありtpm2-toolsが使えるか確認する。EKのハッシュ取得を試す。  
- home/社内CAとしてsmallstepを使っているなら、atteztでattestation CAを立て、smallstepにdevice-attest-01プロビジョナーを追加して試す。  
- attezt-agent経由でp11-kitを使えば既存アプリを大きく改修せずTPM鍵を利用可能。pkcs11-toolでオブジェクト確認を行うとデバッグが早い。  
- 運用面では短期証明書の自動更新とattestation CAのEKインベントリ管理（誰のデバイスか）を設計すること。  
- セキュリティ：atteztは開発中のため本番導入は慎重に。privilegedな実行やCAの信頼チェーン管理に注意する。
