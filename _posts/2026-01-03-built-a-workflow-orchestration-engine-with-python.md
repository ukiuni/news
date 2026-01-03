---
  layout: post
  title: "Built a workflow orchestration engine with Python - Pythonでワークフローオーケストレーションエンジンを作った話：タスクDAG実装で得た教訓"
  date: 2026-01-03T17:40:13.308Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/lordraw77/open-automator"
  source_title: "GitHub - lordraw77/open-automator: A python automator"
  source_id: 471970439
  excerpt: "Dockerで即導入、暗号化Wallet搭載のPython製DAG基盤"
  image: "https://opengraph.githubassets.com/6513fa21f881d6dc59664eafbe6bf3fcc810d7f6f4e00353e34e6a891a70fa1c/lordraw77/open-automator"
---

# Built a workflow orchestration engine with Python - Pythonでワークフローオーケストレーションエンジンを作った話：タスクDAG実装で得た教訓
手早く現場投入できる「使える」ワークフロー基盤 — Open Automatorが示すDAG設計と運用の実践知

## 要約
Python製のモジュール式ワークフローエンジン「Open Automator」は、YAML定義のタスクDAG、暗号化シークレット（Wallet）、FastAPI/Streamlit/CLIの複数インターフェースを備え、Dockerネイティブで現場導入しやすい設計を目指している。

## この記事を読むべき理由
日本のエンジニアにとって、オンプレ／クラウド混在環境やセキュアな資格情報管理が必須の現場で「すぐ使える」「拡張しやすい」ワークフロー基盤は価値が高い。Open Automatorは軽量コンポーネント構成と拡張ポイントが明確で、CI/CD／データパイプライン／運用自動化の導入候補として参考になる。

## 詳細解説
- アーキテクチャ（要点）
  - 4つの主要コンポーネント：Wallet（シークレット管理）、Streamlit（ダッシュボード）、FastAPI（REST/WebSocket API）、Shell（CLI）。各コンテナを独立で立てられるマイクロサービス構成。
  - 共有ボリュームでYAMLワークフロー定義・状態・ログを管理し、Docker Composeで簡単に起動できる設計。

- ワークフロー表現
  - YAMLでタスクを定義し、タスク間はon_success/on_failureで分岐する典型的DAGスタイル。変数にプレースホルダを使える：${ENV:VAR}, ${WALLET:key} 等で環境変数や暗号化ウォレットにアクセス。
  - タスクモジュールはプラグイン式（oahttp, oautils, oadatabaseなど）で、独自モジュール追加が容易。

- シークレット管理
  - WalletはPBKDF2でパスワード派生→Fernetで暗号化する実装例を備え、開発時は平文JSONも選べる。実運用では必ず暗号化＋安全なマスターPW管理を推奨。

- 実行と可観測性
  - 実行履歴（結果・実行時間・エラーログ）を保持。FastAPIはWebSocketでリアルタイム更新を提供し、Streamlit上でMermaidによる可視化表示も可能。
  - 並列実行の上限設定やタスク間での出力受け渡し機能をサポート。

- デプロイ／運用面
  - Docker第一設計でポータビリティが高い。環境変数でポート・パス・並列ジョブ数を設定でき、既存インフラに組み込みやすい。
  - テスト用のpytestやサンプルワークフローが同梱され、開発ループに馴染む。

## 実践ポイント
- まず試す（5分）
  1. リポジトリをクローンしてワークフロー／data／logsを作成
  2. docker-compose up -d で起動し、Streamlit（8501）やFastAPI（8000）を確認
- サンプルYAML（参考）
  ```yaml
  name: hello_world
  variables:
    MESSAGE: "Hello from Open Automator!"
  tasks:
    - name: print_message
      module: oautils
      function: print_text
      text: "${MESSAGE}"
      on_success: end
  ```
- セキュリティの鉄則
  - 本番では常に暗号化Walletを使い、OA_WALLET_PASSWORDを安全な方法で管理（VaultやKMS連携を検討）。
  - API公開時はCORS設定・認証（FastAPI側）を追加する。
- 拡張と運用
  - タスクは「冪等性」を担保する（失敗再試行で二重処理しない）。
  - ログと実行履歴を監視し、並列数はリソースに応じて制限する（MAX_CONCURRENT_JOBS）。
  - カスタムモジュールは既存 modules/ に合わせて実装し、CIでユニットテストを回す。
- 日本市場での活用提案
  - 社内バッチ／ETL、オンプレDBとクラウドAPIを橋渡しする統合層として採用しやすい。
  - セキュリティ要件が厳しい金融・製造系では、Walletの暗号化＋内部KMS連携で合格ラインを作りやすい。

興味があれば、ローカルでの起動手順や運用チェックリスト（監視項目／バックアップ方針）を短くまとめてお送りします。
