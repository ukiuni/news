---
  layout: post
  title: "I built Ctrl: Execution control plane for high stakes agentic systems - Ctrlを作った：ハイステークスなエージェント実行の制御プレーン"
  date: 2026-01-06T11:25:17.302Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/MehulG/agent-ctrl"
  source_title: "GitHub - MehulG/agent-ctrl: Execution control plane for AI agents."
  source_id: 469823513
  excerpt: "実世界アクションを安全に制御するCtrlで、AIの実行を審査・承認・監査可能に"
  image: "https://opengraph.githubassets.com/4e4710c6e35e7eaf1831aa9d93c225986e202f3cfdb6dcb55092acf4df390d41/MehulG/agent-ctrl"
---

# I built Ctrl: Execution control plane for high stakes agentic systems - Ctrlを作った：ハイステークスなエージェント実行の制御プレーン
魅惑の見出し：AIエージェントが「実行」する世界で必須になるガバナンス層 — Ctrlで止め、審査し、監査する

## 要約
CtrlはLangChain向けのラッパーとして、エージェントの「実行行為」を傍受・リスク評価・ポリシー適用・承認済みのみ実行する実行制御プレーン（action gateway）を提供するプロジェクトです。実行の監査ログをSQLiteに残し、承認APIとダッシュボードで人間の介入を組み込めます。

## この記事を読むべき理由
エージェントが単に「生成」するだけでなく、メール送信、払い戻し、記事公開、インフラ変更など実世界アクションを起こす流れは日本のプロダクトや金融・カスタマーサポート領域でも急速に進んでいます。実行権限・安全性・監査性の欠如は重大なリスクになるため、実装レベルでのガバナンス層は今すぐ検討すべき必須要素です。

## 詳細解説
- アーキテクチャ（概念）
  - LangChainエージェント → CtrlMCPラッパー（傍受）→ 意図を記録 → リスクスコア算出 → ポリシー適用（allow/deny/pending）→ 実行（許可された場合のみ）
  - 記録はSQLiteの「intent（requests）」「decisions」「events」に残り、再現や監査に利用可能。

- 主要コンポーネント
  - CtrlMCP: LangChainのMCPクライアントをラップしてツール呼び出しを制御。
  - ポリシーエンジン: YAMLでマッチ条件と効果（allow/deny/require approval）を定義。
  - リスクスコアリング: ルールベースでモード（safe/review/danger）を割当て、閾値で承認要否を判断。
  - 承認API + ダッシュボード: pendingのアクションは明示的承認を待つ。承認後に安全に再実行。
  - CLI: 設定検証、ポリシーチェック、DB初期化などのユーティリティを提供。

- 実行とデプロイ
  - 要件: Python 3.11+, Poetry, SQLite
  - デモはリポジトリ内にあり、ローカル実行やDocker Composeで動かせる。pending時は何も実行されない設計で安全性を優先。

- 技術的要点（実装上の注意）
  - 「意図」のハッシュ化や不変なイベントログで再生可能性を担保している点が重要。
  - ポリシーはサーバ／ツール／環境単位で粒度を調整でき、低リスクは自動承認、高リスクは人間が介入するフローを作れる。
  - 将来的目標は「委譲された権限」「予算・制約管理」「自動承認ルール」「エスカレーションのみ対応する運用」など。

- 短いコマンド例（セットアップ）
```bash
# リポジトリ取得、依存解決、設定検証
git clone https://github.com/MehulG/agent-ctrl
cd agent-ctrl/ctrl
poetry install
poetry run ctrl validate-config --servers demos/e2e_publish_market_report/configs/servers.yaml --policy demos/e2e_publish_market_report/configs/policy.yaml --db ctrl.db
```

- 簡単なポリシー例（概念）
```yaml
# language: yaml
policies:
  - id: context7-approval
    match: { server: "context7", tool: "*", env: "*" }
    effect: allow
    require_approval_if: "risk.mode in ['review','danger']"
```

## 実践ポイント
- まずは「読み取り専用ツール」やステージング環境でCtrlを導入して挙動を把握する。real-money操作は最終段階にする。
- 既存のLangChainツール群をCtrlMCPでラップし、先に意図ログ＋リスク判定を得るワークフローを作る。
- 日本の規制や企業ポリシー（個人情報保護、金融規制、内部統制）に合わせたポリシーを作り、承認フローで法務/コンプライアンスを組み込む。
- 低リスク操作には自動承認を設定して業務効率化、一方で払い戻しや機密データ変更は必ず「pending」→人承認のルールにする。
- 監査・事故対応のためにSQLiteの履歴をSIEMやログ管理に取り込み、再生可能性（replay-safe）を確保する。

このプロジェクトは「実行」を安全にするための実践的な基盤です。まずはデモを動かして、ポリシー設計の要点を掴んでみることを勧めます。
