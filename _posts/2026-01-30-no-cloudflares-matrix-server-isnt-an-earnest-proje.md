---
layout: post
title: "No, Cloudflare's Matrix server isn't an earnest project - CloudflareのMatrixサーバーは本気のプロジェクトではない"
date: 2026-01-30T06:11:52.298Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nexy.blog/2026/01/28/cf-matrix-workers/"
source_title: "No, Cloudflare's Matrix server isn't an earnest project - Nex's Blog"
source_id: 1173085427
excerpt: "CloudflareのWorkers版Matrixは誤記・誇張でコストや安全性に重大な疑問"
---

# No, Cloudflare's Matrix server isn't an earnest project - CloudflareのMatrixサーバーは本気のプロジェクトではない
Cloudflareが宣伝する「Workersで動くMatrix」は本当に実用的？技術的な食い違いと日本での意味を分かりやすく解説

## 要約
CloudflareがWorkers上で動くMatrixホームサーバーを発表したが、元記事は実装／運用・暗号・コストに関して誤記や誇張が多く、実務的には懐疑的に評価されている。

## この記事を読むべき理由
Cloudflareは日本でも広く使われるインフラ事業者で、同社の「サーバレスで簡単」「ポスト量子で安全」といった主張は自分ごととして影響します。誤情報を見抜き、自己ホスティングや運用判断に活かすために必読です。

## 詳細解説
- 発端：Cloudflareが「WorkersでフルMatrixホームサーバーを動かせる」と発表。初動では期待が湧いたが、コミュニティから技術的な指摘が相次いだ。  
- AI生成疑惑：元記事の文面にLLMっぽい表現や、既存LLMの断片知識の痕跡があり、内容の正確性に疑問符。  
- ストレージ実装の誤表記：CloudflareはTuwunel（conduwuit系の実装）をPostgreSQL/Redis前提と記載したが、実際はTuwunelはRocksDB（ローカルKVS）を用いる。これはアーキテクチャ前提を根本から取り違えている。  
- コストと「ゼロ時の料金」主張への反論：Matrixはサーバ間フェデレーションで非常にトラフィックが多く、リクエスト課金のWorkersでは想定外にコストが増える可能性が高い。小規模コミュニティでも常時稼働のVPSで十分な場合がある。  
- TLS／ポスト量子の主張の限界：CloudflareがエッジでTLSをポスト量子にしても、E2EE（Megolm）自体が破られれば「伝送は安全でも保存データに関するリスク」は消えない（store-now-decrypt-later問題）。加えてWorkersがTLSを終端する点は、運用者が鍵管理やデータ可視性をどう扱うかを変える。  
- セキュリティの“標準搭載”主張は営業文句：CloudflareがDDoS/フィルタを提供する利点はあるが、小規模運用のハードニングはそこまで複雑ではない（例：Caddyでの自動TLS等）。  
- コミュニティ反応と透明性問題：Element CEOやMatrixコミュニティで疑念が噴出。Cloudflare側のブログ修正やリポジトリでの編集履歴が注目されている。Tuwunel維持者へ事前連絡がなかった点も問題視された。

## 実践ポイント
- 主張を鵜呑みにしない：ベンダーブログはマーケティング色が強いので、実装は必ずソースコード／アーカイブで確認する（例：Cloudflareブログのアーカイブを参照）。  
- ストレージ前提を確認：TuwunelはRocksDBベース。Postgres/Redis前提の説明と実装は一致するかをチェック。  
- 運用コストを試算する：フェデレーション量やリクエスト率を元にWorkers課金モデルでの見積もりを出す。小規模ならRaspberry Pi＋軽量ホームサーバーで十分な場合がある。  
- TLS終端の信頼境界を理解する：エッジでTLS終端するなら、誰が復号可能か（Cloudflare含む）を運用方針として明確に。E2EEの既存限界（store-now-decrypt-later）を把握。  
- 実務的な即効策：個人で試すならCaddyで自動TLS、Raspberry Piや低コストVPSでSynapse/Conduit系を動かし、実トラフィックで性能とコストを比較する。  
- 情報ソースを分散：公式MatrixフォーラムやプロジェクトのGit履歴、コミュニティの議論を追い、単一ベンダー発信だけに依存しない。

短く言えば、Cloudflareの提案は面白いが「そのまま信頼して移行すべき」ではない。日本の個人・企業もコスト・プライバシー・可視性の観点で冷静に評価し、自社／自分の要件で検証することを推奨します。
