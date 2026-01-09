---
layout: post
title: "Show HN: EuConform – Offline-first EU AI Act compliance tool (open source) - Show HN: EuConform — オフライン優先のEU AI法コンプライアンスツール（オープンソース）"
date: 2026-01-09T20:02:43.722Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Hiepler/EuConform"
source_title: "GitHub - Hiepler/EuConform: EU AI Act Compliance Tool - Risk classification and bias testing"
source_id: 46557823
excerpt: "ブラウザで完全オフラインにEU AI法対応のリスク診断とバイアステストを一括で試せるツール"
image: "https://opengraph.githubassets.com/aaddbebd170cc2c7d51b49ae2443e85746936507a9a2cd0cd25fd41902ec2256/Hiepler/EuConform"
---

# Show HN: EuConform – Offline-first EU AI Act compliance tool (open source) - Show HN: EuConform — オフライン優先のEU AI法コンプライアンスツール（オープンソース）
魅力タイトル: EU対応を“まず試せる”ツール — ブラウザ完結でAI法リスク診断・バイアステストができるEuConform

## 要約
EuConformはブラウザ内で完全オフラインに動作するEU AI Act向けのオープンソース診断ツールです。リスク分類、バイアス検出、Annex IV準拠の技術文書（PDF）作成までを手早く試せます（ただし法的助言ではありません）。

## この記事を読むべき理由
- 2027年から本格化する「高リスク」義務に備える必要がある組織（EU向けサービスを持つ日本企業や多国籍チーム）にとって、実務に即した技術的な準備ができるため。  
- データやモデルをクラウドに送らずに評価できるため、GDPRや社内情報管理ポリシーを重視する現場で導入しやすい点が魅力です。

## 詳細解説
- コア機能
  - リスク分類：EU AI Act（Art.5の禁止、Art.6＋Annex IIIの高リスク該当検査）をベースにしたインタラクティブな診断フローを提供。事業・利用ケースを入力すると赤/高/その他のリスク判定の目安を示します。
  - バイアス検出：CrowS-Pairs（Nangia et al., 2020）を使った言語モデルのステレオタイプ検出。log-probabilityベースのスコアを算出し、閾値でLight/Strongバイアスを判定します。ドイツ語向けに一部ローカライズされたペアも含まれます。
  - 技術ドキュメント生成：Annex IV（技術文書）の形式でPDFをブラウザ側で生成。監査や社内レビューのひな形として使えます。
- オフライン＆プライバシー設計
  - すべての処理はクライアント（ブラウザ）で実行され、外部トラッキングやサーバー送信はありません。transformers.jsとWebGPUでモデル推論を行えます。
  - ローカルのOllamaサーバーを接続すると、ログ確率（log-probs）を返すモデルでより精度の高いバイアス検出が可能（Llama 3.2+, Mistral 7B+ 推奨）。
- 技術スタック
  - Next.js 16（App Router + RSC）、TypeScript 5.9、Turborepo（モノレポ）、transformers.js（ブラウザ推論）、Tailwind v4、Radix UI、Vitest / Playwrightなど。アクセシビリティはWCAG 2.2 AA対応を目指しています。
- ライセンスと注意点
  - デュアルライセンス（MIT と EUPL-1.2）。ツールは技術的ガイダンスを提供するもので、法的な適合判定・正式審査の代替にはなりません。

## 実践ポイント
- まず試す（サンドボックス）
  - Vercelデプロイのデモを開けばインストール不要ですぐ触れます。ローカルで動かす場合は以下コマンドで起動できます。
```bash
# 必要: Node.js >= 18, pnpm >= 10
git clone https://github.com/Hiepler/EuConform.git
cd EuConform
pnpm install
pnpm dev   # http://localhost:3001
```
- 精度向上のためのローカル設定
  - Ollamaをローカルに立て、log-probs対応モデル（Llama 3.2+, Mistral 7B+ 等）を使うとバイアス測定の精度が上がります。Ollama接続はUIから選択できます。
- 日本企業への応用案
  - EU市場向けプロダクトのコンプライアンス事前チェックツールとしてCIに組み込む（定期的なリスク再評価）。  
  - Annex IV出力をベースに社内の技術文書テンプレートを作り、法務・監査チームと連携する。  
  - CrowS-Pairsは文化差があるため、日本語・日本文化向けのペアを追加して精緻化することで国内チームの実務性を高められます。
- 限界と注意
  - あくまで技術的評価の補助ツール。最終的な法的判断や通知機関による適合評価は専門家に依頼してください。  
  - モデルによってはlog-probsが出ない場合があり、その場合は近似手法での評価となります。

興味があれば、翻訳や日本語データセットのローカライズ提案、社内PoC導入のチェックリスト作成などの次ステップ案も提供できます。
