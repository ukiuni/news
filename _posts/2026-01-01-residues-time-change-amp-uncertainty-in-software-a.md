---
  layout: post
  title: "Residues: Time, Change & Uncertainty in Software Architecture - 残留物：ソフトウェアアーキテクチャにおける時間・変化・不確実性"
  date: 2026-01-01T18:00:20.332Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://youtu.be/D8qQUHrksrE?list=PLEx5khR4g7PINwOsYrkwz3lTTJUYoXC53"
  source_title: "Residues: Time, Change &amp; Uncertainty in Software Architecture • Barry O&#39;Reilly • GOTO 2025 - YouTube"
  source_id: 474798175
  excerpt: "過去の設計が残す残留物を可視化し、安全に置換する実践法、モノリス近代化にも効く"
  image: "https://i.ytimg.com/vi/D8qQUHrksrE/maxresdefault.jpg"
---

# Residues: Time, Change & Uncertainty in Software Architecture - 残留物：ソフトウェアアーキテクチャにおける時間・変化・不確実性
技術負債だけでは語れない「残留物」を見抜き、未来に耐えるアーキテクチャを描く方法

## 要約
Barry O'Reillyが示す「Residues（残留物）」は、過去の設計決定が時間と変化、そして不確実性の下で残す痕跡のこと。これを可視化して管理することで、ソフトウェアの進化を安全かつ高速にする考え方を提案する。

## この記事を読むべき理由
日本の企業は長期運用されるシステムが多く、過去の決定が将来の開発速度とコストを左右します。残留物を正しく扱う視点は、モノリスの近代化や規制対応、現場の生産性向上に直結します。

## 詳細解説
- 残留物とは何か  
  コードやデータスキーマ、インフラ設定、組織的なプロセス、運用知見など、過去の決定が「痕跡」として残るもの。これらは単なる技術負債ではなく、時間経過で性質が変わる動的な存在だと捉える。

- 時間の影響  
  要件の変化、ライブラリの陳腐化、運用パターンの変化が残留物を肥大化させる。古いインターフェースや副作用を持つコンポーネントは、時間とともにシステム全体のリスクを増やす。

- 変化と不確実性への対処  
  未知の未来に対しては「安全に試す」アプローチが有効。小さな実験（feature flags、カナリア、A/B）と高速なフィードバックループで、誤った前提を早期に捨てる。アーキテクチャは置き換えやすさ（replaceability）と観測性を優先して設計する。

- 技術的手法（例）  
  - 残留物マッピング：コード、データ、インターフェース、組織の痕跡を可視化して影響範囲を評価する。  
  - ストラングラー・パターンで段階的移行。  
  - アーキテクチャ決定記録（ADR）で意思決定を残し、将来の残留物を意図的に作る。  
  - オブザーバビリティ（メトリクス、トレース、ログ）を設計の第一義にする。  
  - 自動化されたテストとデプロイ、フィーチャーフラグで安全な実験基盤を構築する。  

## 実践ポイント
- まず残留物を「見える化」する：影響度、保守コスト、変更頻度で分類する。  
- 優先度は「リスク×頻度」基準で決め、小さな駆動実験で検証する。  
- 置き換えは一度にやらない：Strangler、APIゲートウェイ、反腐敗層で段階的に。  
- ADRと運用プレイブックを整備して、将来の残留物を意図的に管理する。  
- 日本の現場では経営や規制の制約が強いので、短期ROIが示せる「小さな勝ち」を積み重ねる。

## 引用元
- タイトル: Residues: Time, Change & Uncertainty in Software Architecture • Barry O'Reilly  
- URL: https://youtu.be/D8qQUHrksrE?list=PLEx5khR4g7PINwOsYrkwz3lTTJUYoXC53
