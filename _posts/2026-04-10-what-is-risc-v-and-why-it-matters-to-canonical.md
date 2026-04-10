---
layout: post
title: "What is RISC-V and why it matters to Canonical - RISC-Vとは何か、そしてCanonicalにとってなぜ重要か"
date: 2026-04-10T21:27:47.656Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ubuntu.com/blog/risc-v-101-what-is-it-and-what-does-it-mean-for-canonical"
source_title: "RISC-V 101 &#8211; what is it and what does it mean for Canonical?     | Ubuntu"
source_id: 47691538
excerpt: "RISC-Vの開放性とUbuntuのLTS支援で日本のIoT/エッジ開発が加速"
image: "https://ubuntu.com/wp-content/uploads/c26a/Isometric-One-logo.png"
---

# What is RISC-V and why it matters to Canonical - RISC-Vとは何か、そしてCanonicalにとってなぜ重要か
オープンCPUが拓く未来：RISC-Vで日本のIoT・エッジ開発が加速する理由

## 要約
RISC-Vは誰でも実装可能なオープンな命令セット（ISA）で、拡張性と柔軟なビジネスモデルで半導体の地図を塗り替えている。Canonical（Ubuntu）はRISC-Vを正式サポートし、Linuxエコシステム上での実用化を後押ししている。

## この記事を読むべき理由
日本のIoT、組込み、エッジAI、データセンター分野で自前のハードウェアやサプライチェーンの選択肢を増やす上で、RISC-Vは重要な要素。Ubuntuの長期サポートやベンダーツールが揃えば導入コストと運用リスクが下がるため、今後の製品企画や研究に直結する情報だから。

## 詳細解説
- RISC-Vの基本：ISA（命令セットアーキテクチャ）として2010年に登場し、標準化はRISC-V Internationalが主導。Armやx86と違い「開かれた仕様」で、誰でもコアを作れる。
- 拡張性の特長：標準命令群に加え、用途別に選べる拡張（浮動小数点、カスタム命令、AI向け型など）を組み合わせられるため、AIアクセラレータやセキュリティ回路などを密に結合した独自SoCが作りやすい。
- ビジネス面：実装はオープンソース化、商用IP販売、社内専用など柔軟。GoogleのOpenTitanの例に見るように、セキュリティルートやデータセンター用途での採用も進む。
- ソフトウェア成熟度：LinuxカーネルやGCC/LLVM、主要RTOSでサポートされており、Ubuntuは2021年から対応。プロファイル（例：RVA20、RVA23）により互換性を担保し、RVA23準拠ハードならLinux互換性が期待できる。
- Canonicalの立場：コミュニティと顧客の要望に応じてRISC-Vを「ファーストクラス」でサポート。Ubuntu 24.04 LTSはRVA20対応、25.10以降（26.04 LTS含む）でRVA23対応予定。Ubuntu Proで最長15年のLTSサポートを提供。

## 実践ポイント
- まず触る：RVA23対応の開発ボードやベンダー提供のUbuntu RISC-Vイメージで動かしてみる。
- 互換性確認：ターゲットSoCがどのプロファイルに準拠しているか（RVA20 vs RVA23）を最初にチェックする。
- 開発基盤：GCC/LLVMや既存のツールチェーンが対応しているか、カスタム命令がある場合はUbuntuのLaunchpadやベンダー提供パッケージで検証する。
- 運用計画：長期運用が必要ならUbuntu ProのLTSサポートを検討する。
- 参考資源：CanonicalのRISC-V公式ビルド、パートナービルド、RISC-V向けクックブックやLaunchpadリポジトリを活用してイメージ生成やパッケージ管理を進める。
