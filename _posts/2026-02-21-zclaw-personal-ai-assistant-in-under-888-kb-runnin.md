---
layout: post
title: "zclaw: personal AI assistant in under 888 KB, running on an ESP32 - ESP32で動く、888KB未満のパーソナルAIアシスタント"
date: 2026-02-21T22:37:57.676Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/tnm/zclaw"
source_title: "GitHub - tnm/zclaw: Your personal AI assistant in under 888 KB, running on an ESP32. GPIO, cron, memory, and more."
source_id: 47100232
excerpt: "ESP32で888KB未満の小型AIが会話・GPIO制御・スケジュール自動化を実現"
image: "https://opengraph.githubassets.com/10ec4109d00e41cf68ac8155d76ef7049abe38a6a8493e61148755999d26cec4/tnm/zclaw"
---

# zclaw: personal AI assistant in under 888 KB, running on an ESP32 - ESP32で動く、888KB未満のパーソナルAIアシスタント
驚きの小型AI：手のひらサイズのESP32が会話・GPIO制御・スケジュールをこなす！

## 要約
Cで書かれた軽量AIエージェント「zclaw」は、デフォルトビルドで888KB以下のファームウェアとしてESP32上で動作し、GPIO操作、タイムゾーン対応のスケジューラ、永続メモリ、外部LLMプロバイダ連携などを提供します。

## この記事を読むべき理由
超小型デバイスで「会話する」・「現場機器を制御する」AIを実現できる点は、日本のIoT／エッジAI導入に直結します。低コストなプロトタイプやプライバシー重視のローカル用途に最適です。

## 詳細解説
- 実装と言語: Cで実装。ESP-IDFベースでESP32-C3/S3/C6をサポート（他の派生も動作する可能性あり）。ライセンスはMIT。  
- 主要機能: Telegramやホスト型Webリレー経由のチャット、時刻／タイムゾーン対応のcron（daily／periodic／one-shot）、GPIOの読み書き（ガードレール付き）、永続ストレージ（NVS相当）、カスタムツールを自然言語で組み合わせる機能。  
- LLMプロバイダ: Anthropic、OpenAI、OpenRouterなどをサポートしており、クラウドLLMとデバイス制御を組み合わせられる。  
- サイズ目標: デフォルトビルドで888KB以下に収めることを目指して最適化。  
- 開発・運用ツール: build/flash/flash-secure/provision/monitor/emulate/web-relay/benchmark/test など多数のスクリプトで開発・検証フローを用意。QEMUエミュレーションも可能。  
- セキュリティ/運用: フラッシュ暗号化モード対応（credentialを暗号化してNVSへ配置）、プロビジョニングスクリプトでWi‑FiとLLMキーを投入。  
- 推奨ボード: Seeed XIAO ESP32-C3（実機テスト済み）。パフォーマンスや互換性はボードで差が出るため注意。

簡潔な導入例（macOS/Linux）:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/tnm/zclaw/main/scripts/bootstrap.sh)
```

## 実践ポイント
- まずはリポジトリをクローンしてbootstrap→install、provisionで資格情報を投入。テストは ./scripts/web-relay.sh で手早く確認。  
- セキュリティ重視なら ./scripts/flash-secure.sh で暗号化フラッシュを使う。  
- ローカルLLMやOpenRouter経由でレイテンシ／コストを調整可能。日本語プロンプトの扱いはプロバイダ側に依存するため事前検証を。  
- ハードウェア用途例：店舗のセンサー連携、自動化スケジューラ、オフィスのローカルアシスタント、教育用ハッカソン。  
- 開発時は QEMU エミュレーションとベンチマークスクリプトで反復検証→本機フラッシュの流れが効率的。

元リポジトリ／ドキュメントは GitHub: tnm/zclaw（MIT）。興味があればまずは推奨ボードで動かして、GPIO＋スケジュールの簡単な自動化から試してください。
