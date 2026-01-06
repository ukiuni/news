---
  layout: post
  title: "Show HN: Mantic.sh – Search 480k files in 0.46s without embeddings - Mantic.sh：48万ファイルを0.46秒で検索（埋め込み不要）"
  date: 2026-01-06T20:54:47.771Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/marcoaapfortes/Mantic.sh"
  source_title: "GitHub - marcoaapfortes/Mantic.sh: The reference implementation of cognitive code search. Zero-read, deterministic context retrieval for AI agents."
  source_id: 46512182
  excerpt: "埋め込み不要で48万ファイルを0.46秒検索、ローカルで高速かつ秘匿なコード検索エンジン"
  image: "https://opengraph.githubassets.com/b8a719089f83c49d1194007e4ed98b65ee6f8c4cf041e5712728ce550af21143/marcoaapfortes/Mantic.sh"
---

# Show HN: Mantic.sh – Search 480k files in 0.46s without embeddings - Mantic.sh：48万ファイルを0.46秒で検索（埋め込み不要）
480kファイルを瞬時に絞り込む“構造的”コード検索――埋め込みも外部DBも使わないAI向けコンテキスト取得エンジン

## 要約
Mantic.shは「ファイルの中身を読まずに」構造情報とメタデータだけで関連ファイルをスコアリングするローカル実装のコード検索エンジンで、Chromiumのような大規模リポジトリでも0.46秒で結果を返します。

## この記事を読むべき理由
- 大規模モノレポやプライベートコードを扱う日本の開発現場で、外部APIやベクトルDBを避けつつAIエージェントに安全で速いコンテキストを渡せる点は即戦力です。  
- トークンコスト削減（報告値で最大63%）やローカル完結のプライバシー重視ワークフローを検討しているなら、まず試す価値があります。

## 詳細解説
- 基本方針：ファイル内容全文を逐一埋め込むのではなく、パス・ファイル名・拡張子・gitトラッキング情報など「構造的手がかり」から意図を推定し、関連度を算出する「ゼロリード（zero‑read）」手法を取る。結果は決定的（deterministic）で再現可能。
- アーキテクチャ（主要コンポーネント）
  - Intent Analyzer：クエリからカテゴリ（例：auth, ui, test）を推定。
  - Brain Scorer：メタ情報に基づくスコア付け（パス重要度、ファイル名一致、ビジネスロジック優先、ボイラープレート減点）。
  - File Classifier：コード/設定/テスト等でフィルタリング。
  - Impact Analyzer：変更の潜在的影響範囲を推定。
- 技術的ポイント
  - ファイル列挙は git ls-files を使い、追跡対象のみを高速に扱う（ディスク全探索より速い）。
  - 埋め込みやベクトルDBを使わないため外部依存がなくローカル完結。MCP（Claude Desktop, Cursor 等）連携ルールも提供。
  - CLI出力はJSON/ファイルリスト/Markdownなど。オプションでコード／設定／テスト縛りやインパクト分析を選択可能。
- 性能例（M1 Proベンチマーク）
  - Cal.com: 9,621ファイル → 0.32s（従来ベクトル検索0.85s）  
  - Chromium: 480,000ファイル 59GB → 0.46s（従来ベクトル検索5–10s）  
  - トークン削減や検索応答速度は、AIアシストワークフローでの実用性に直結。
- ライセンス：AGPL‑3.0。個人/OSS/社内利用は無料だが、商用組み込みやホスティング提供には注意が必要（ライセンス確認を推奨）。

## 実践ポイント
- まず試す（インストール不要で一発実行）:
```bash
npx mantic.sh@latest "stripe payment integration"
```
- ローカルモノレポでの導入手順（参考）:
```bash
git clone https://github.com/marcoaapfortes/Mantic.sh.git
cd Mantic.sh
npm install
npm run build
npm link
```
- 即効で価値が出る設定
  - MANTIC_MAX_FILES=5000 や MANTIC_TIMEOUT=5000 でスキャン範囲・タイムアウトを調整。
  - git ls-files に追跡されているファイル中心に運用すると高速化しやすい。
  - AIツールのシステムプロンプト（Agent Rules）に組み込み、コード生成前に自動でコンテキスト取得させる。
- 注意点
  - AGPLの制約を確認してから商用組み込みやSaaS提供を検討する。  
  - 構造情報中心のため、ファイル内部の微細な意味解析は別途全文検索やランタイム解析と併用するのが実用的。

まずは自分のリポジトリでnpxコマンドを走らせ、どれだけノイズが減るか・応答が速くなるかを確かめると良いでしょう。
