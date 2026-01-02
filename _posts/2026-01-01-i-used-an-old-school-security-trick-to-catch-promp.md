---
  layout: post
  title: "I used an old-school security trick to catch prompt injection on AI agents - 古典的トリックでAIエージェントのプロンプトインジェクションを捕まえた"
  date: 2026-01-01T19:07:45.792Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/mariocandela/beelzebub"
  source_title: "GitHub - mariocandela/beelzebub: A secure low code honeypot framework, leveraging AI for System Virtualization."
  source_id: 473578584
  excerpt: "LLMを騙すハニーポットでリアルなプロンプト注入を検出し攻撃手口を収集する実践ガイド"
  image: "https://repository-images.githubusercontent.com/490028114/6bb2bae0-6869-4731-960d-3d7880c1066a"
---

# I used an old-school security trick to catch prompt injection on AI agents - 古典的トリックでAIエージェントのプロンプトインジェクションを捕まえた
AIエージェントを「だます」ための古典的ハニーポット手法をモダンに再構築した──Beelzebubが示すプロンプトインジェクション検出の現実解

## 要約
Beelzebubは、LLMを使って高相互作用に見せかける低リスクなハニーポットフレームワーク。特に「MCP（エージェントが呼ぶべきでないツール）」を罠として仕掛け、プロンプトインジェクションによるガードレール突破をリアルタイムで検出・記録する点が特徴。

## この記事を読むべき理由
日本でも業務自動化（RPA）、社内アシスタント、外部ツール連携などでAIエージェントの導入が進む中、エージェント経由での権限逸脱や機密リークリスクが現実化している。Beelzebubの手法は、実運用で発生する“悪意あるプロンプト”を自動収集して防御を強化する実践的な一手となる。

## 詳細解説
- アーキテクチャ
  - YAMLベースの低コード設定で、HTTP/SSH/TCP/MCPなど複数プロトコルのハニーポットを定義可能。
  - LLMをバックエンドに使い「実際は低相互作用だが振る舞いは高相互作用」という擬似環境を実現。これにより攻撃者の操作を引き出しやすく、安全性も確保する設計。
- MCP（Model Control Protocol）ハニーポットの狙い
  - 「決して呼ばれるべきでないツール」をデコイとして配置。正常系では呼ばれないはずのAPI呼び出しが観測されたら、プロンプトインジェクション／ガードレール回避を示す即時のアラートとなる。
  - 実際に呼ばれたプロンプトをログ化し、フィルタやルールの微調整に使える「生の攻撃データ」を収集可能。
- LLM統合
  - OpenAIやローカルのOllama/Codellamaなどをプラグインで利用。SSHインタラクティブやカスタムプロンプトでの振る舞いをエミュレートできる。
  - サンプル設定では、ターミナル応答や認証ダイアログ、ツールの「実行結果」を返すハンドラを用意できる。
- 運用・観測
  - Prometheusメトリクス、ELK統合、Docker/Kubernetesデプロイ対応により監視・分析が容易。
  - テスト、CI、静的解析（CodeQL等）を重視した開発プロセスが公開されている。
- セキュリティ注意点
  - ハニーポットであっても実APIキーや機密を置かない、ネットワーク分離を徹底する、ログに含まれる個人情報の扱いに注意する必要あり。

## 実践ポイント
- まず試す
  - ローカルで: docker compose build && docker compose up -d で動かしてみる。
- MCPハニーポットを作る
  - エージェントが絶対に呼ばないはずの「管理ツール」をツール一覧として定義し、呼び出しを検知したら即ログ／アラート。
- 攻撃データを防御に活かす
  - 捕まえたプロンプトを分類してフィルタルール／正規表現やスコアリングへ反映し、False Negativeを減らす。
- LLMプロバイダは慎重に
  - 本番で外部APIキーを直置きしない。可能ならローカルモデルで検証→段階的に本番へ導入。
- 可観測性を整える
  - PrometheusやELKに接続し、HAR/TPR/MTPなど指標でトレンド監視を行う。
- 運用ガイド
  - 隔離された環境で実行し、テストスイート（make test.unit / make test.integration）で挙動を検証してから本番に持ち込む。

