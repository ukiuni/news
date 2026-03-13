---
layout: post
title: "Launch HN: Captain (YC W26) – Automated RAG for Files - Captain（YC W26）—ファイル向け自動RAG"
date: 2026-03-13T17:00:19.204Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.runcaptain.com/"
source_title: "Captain - Accurate knowledge search that scales"
source_id: 47366011
excerpt: "ファイルを放り込むだけで数分導入、社内文書を高精度検索化する自動RAGプラットフォーム"
image: "https://hn.runcaptain.com/opengraph.jpg"
---

# Launch HN: Captain (YC W26) – Automated RAG for Files - Captain（YC W26）—ファイル向け自動RAG
ファイルを放り込むだけで「検索が答える」世界へ──数分で運用できる高精度RAGプラットフォーム

## 要約
Captainはファイル中心の自動RAGパイプラインを提供し、OCR/VLM・チャンクング・埋め込み・再ランキングまで一気通貫で管理。導入数分・運用ゼロメンテを目指し、精度は約78%から再ランキングで最大95%をうたいます。

## この記事を読むべき理由
日本の企業はMicrosoft 365やS3/Azureを中心にファイル資産が散在しがち。CaptainはSharePointやGoogle Driveなど既存のストレージと連携して、社内ドキュメントを即座に検索可能資産に変えられるため、データ活用の速度を劇的に上げられます。

## 詳細解説
- コア機能：自動OCR・画像理解（VLM）・ファイル変換→チャンク分割→埋め込み生成→ベクトル検索→再ランキング、というRAGワークフローをマネージドで提供。外部のベクタDBは不要（Managed vector storage）。
- 検索方式：キーワード重み付けと意味検索（類似度）を組み合わせたハイブリッド検索＋再ランキングで精度改善を図る。プロンプト工夫やリランクが精度向上のポイント。
- API例（要約）：RESTでコレクションにクエリを投げ、inference/stream/rerank/top_kなどを指定して検索結果を取得可能。短時間でのデプロイを重視。
- データ連携：Azure Blob/GCS/S3、SharePoint、Google Drive、Dropbox、Confluence、Slack、Gmail、Notionなど幅広く対応。これにより既存インフラを活かした導入が可能。
- セキュリティ・ガバナンス：ロールベースアクセス制御やメタデータフィルタリングに対応、SOC2準拠の運用をアピール。
- 製品状況：Captain v2 APIやプラットフォーム更新を進行中（記事抜粋では2026年1月の記載）。

javascript
```javascript
const res = await fetch(`${BASE_URL}/v2/collections/my_documents/query`, {
  method: "POST",
  headers: { "Authorization": `Bearer ${API_KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "重要な契約条件は？",
    inference: true,
    stream: true,
    rerank: true,
    top_k: 10
  })
});
```

## 実践ポイント
- 小さなコレクションでPoC：まずSharePointやS3の代表的フォルダをインデックスして検索精度を確認する。
- 再ランキングとtop_k調整：初期はtop_k=10、rerank=trueで結果の信頼度向上を試す。
- メタデータ活用：ファイル作成者や部門タグを付与してロールベースフィルタを設計する（日本の情報ガバナンスで重要）。
- セキュリティ確認：SOC2報告やデータ所在（リージョン）要件を社内コンプライアンスと照合する。
- 既存投資の活用：M365/SharePoint中心の企業は接続コストが低く、導入効果が出やすい。

簡潔に言えば、Captainは「ファイルを放り込んで高精度な検索結果をすぐに得る」ことを目標にしたマネージドRAGサービス。まずは小規模で試し、アクセス制御と再ランキングをチューニングして本番導入を進めるのが現実的な道筋です。
