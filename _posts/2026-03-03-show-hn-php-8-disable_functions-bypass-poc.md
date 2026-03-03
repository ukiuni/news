---
layout: post
title: "Show HN: PHP 8 disable_functions bypass PoC - PHP 8 の disable_functions 回避 PoC"
date: 2026-03-03T02:23:57.679Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/m0x41nos/TimeAfterFree"
source_title: "GitHub - m0x41nos/TimeAfterFree: PHP 8 Sandbox Escape"
source_id: 47226605
excerpt: "PHP8 DateIntervalで無効化関数を突破、サンドボックス脱出PoC"
image: "https://opengraph.githubassets.com/4fa56a496938b7a2744322d0f6c79e5ee3972aa49fb94324a53e23efe58ca7d6/m0x41nos/TimeAfterFree"
---

# Show HN: PHP 8 disable_functions bypass PoC - PHP 8 の disable_functions 回避 PoC
魅せる見出し: PHP 8で「無効化」したはずの関数が復活する？DateIntervalを悪用するサンドボックス脱出PoCの衝撃

## 要約
PHP 8 系で報告されたPoCは、use-after-free 型のヒープ破損を使って disable_functions 制限を回避し、システムコマンド実行に到るサンドボックス脱出を示しています（影響: PHP 8.2.x〜8.5.x、CLI/PHP-FPM/Apacheモジュールで再現）。

## この記事を読むべき理由
日本の多くのウェブサービスはPHP上で動作しており、共有ホスティングや古いPHPバージョンを使う環境が残っています。disable_functions に依存した安全策が必ずしも有効でない可能性を理解し、防御の優先順位を見直す必要があります。

## 詳細解説
- 問題の本質はメモリの安全性の欠如：PHPコアに残るメモリ破損（use-after-free）を悪用すると、本来制限された関数呼び出しの制約を回避できる、というクラスの脆弱性です。  
- PoCは、DateInterval オブジェクトを利用したヒープ情報のリークと読み書きプリミティブの獲得手法を組み合わせ、disable_functions による制限を突破していると報告されています。  
- 重要なのは、攻撃成功のために「特権的な設定」や「特殊なモジュール」は不要で、標準的なPHP配布や一般的なSAPI（CLI、FPM、Apache）で再現可能だとされる点です。  
- こうした脆弱性は単に「バグ」ではなく、サンドボックス設計の前提（例えば disable_functions による隔離）が破られるリスクを示しています。

## 実践ポイント
- まず自環境のPHPバージョンを確認し、ベンダー/メンテナの修正が出ている場合は速やかに適用する（8.2〜8.5 系に注意）。  
- disable_functions だけに依存しない防御策を採る：最新のPHPを適用する、最小権限実行、コンテナ分離、OSレベルのサンドボックス（AppArmor/SELinux、seccomp）を併用する。  
- 共有ホスティングや外部プラグインを利用している場合は、プロバイダやベンダーの対応状況を確認し、脆弱なバージョンを使わない運用に切り替える。  
- 開発・運用チームはメモリ安全性やヒープ破損に関するモニタリングを強化し、外部のPoC公開を追跡して影響範囲を早期に評価する。  
- PoCや攻撃コードそのものに触れる際は研究/教育目的に限定し、責任ある開示と法令遵守を徹底する。

（出典: GitHub リポジトリ "m0x41nos/TimeAfterFree" の公開情報に基づく要約。PoCは教育目的とされており、実害を防ぐためパッチと防御策の導入を推奨します。）
