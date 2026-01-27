---
layout: post
title: "Lennart Poettering, Christian Brauner founded a new company - Lennart Poettering と Christian Brauner が新会社を設立"
date: 2026-01-27T20:44:33.596Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://amutable.com/about"
source_title: "About Us - Amutable"
source_id: 46784572
excerpt: "systemdとVFSの主要開発者が改ざん不可のLinux基盤を実装する新会社を設立"
image: "https://amutable.com/og-image.png"
---

# Lennart Poettering, Christian Brauner founded a new company - Lennart Poettering と Christian Brauner が新会社を設立
クリックせずにはいられないタイトル: Linuxの“信頼の土台”を作る――systemdとVFSの主要開発者が掲げる「改ざんできないOS」の挑戦

## 要約
有名なLinux開発者たちが設立したAmutableは、「Linuxワークロードに対する暗号的に検証可能な整合性」を目指し、起動時からランタイムまでシステムを常に検証済みの状態に保つことを狙います。

## この記事を読むべき理由
日本企業は製造業、金融、政府機関、組込み/IoTまで幅広くLinuxに依存しており、サプライチェーン攻撃やファームウェア改ざん対策が急務です。Amutableのアプローチは、国内のインフラ／デバイス運用者にとって即効性のある設計思想を示します。

## 詳細解説
- ミッションと焦点  
  - Amutableは「Build integrity」「Boot integrity」「Runtime integrity」の三本柱で、システムが初回起動時から信頼でき、稼働中に改変されていないことを暗号的に担保することを目標にしています。具体的には署名・測定・遠隔検証（attestation）を組み合わせる設計が想定されます。

- なぜ重要か（技術的背景）  
  - 近年はブートローダーやカーネル、ユーザ空間の改ざんを狙う攻撃が増加。TPMやSecure Boot、カーネルの測定機構（IMA）やdm-verityのような技術を組み合わせ、起動チェーンとランタイムの状態を証明して信頼境界を守る必要があります。Amutableはこれらをエンドツーエンドで整備しようとしていると見られます。

- チームが示す信頼性  
  - 創業メンバーに systemd の Lennart Poettering、Linux VFS の Christian Brauner、前Kinvolkの Chris Kühl などが名を連ねており、OS／ランタイム周りの深い技術知見をプロダクトに注ぎ込める点が大きな強みです。

- 期待される機能要素（推測と合理的期待）  
  - ハードウェアルート（TPM）を用いた測定とリモートアテステーション、署名済みイメージの配布・検証、ランタイム整合性チェック、既存システム（systemdやVFS）との密な連携、クラウド／オンプレ双方での運用サポート。

## 実践ポイント
- 今すぐできること（優先順）
  1. ハードウェア（TPM）とSecure Bootの有効化を検証環境で試す。  
  2. 既存のディストロ／カーネルでIMA/dm-verityや署名機能が使えるか確認する。  
  3. ビルドパイプラインにSBOMや再現可能ビルド、イメージ署名を組み込む。  
  4. Amutableの公式情報（ブログ/ニュースレター）をフォローし、設計方針と互換性をチェックする。  
  5. ステージング環境で起動時とランタイムの検証フローを実際に回し、運用手順を整備する。

短めのまとめ: 有力なLinuxコア開発者たちが「改ざん検出と証明」を製品化しようとしています。日本の現場では早めにTPM/署名/測定の基礎を整え、Amutableの動向を追うことが実務的な先手になります。
