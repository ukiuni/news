---
  layout: post
  title: "Uncloud, self hosted Cloud, seen by a developer for developers - Uncloud：開発者のためのセルフホスト型クラウド"
  date: 2026-01-05T20:41:18.268Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://blog.garambrogne.net/uncloud-en.html"
  source_title: "Uncloud, self hosted Cloud, seen by a developer for developers"
  source_id: 1477686898
  excerpt: "Kubernetesの負担を避け、単一コマンドでComposeデプロイする代替案Uncloud"
---

# Uncloud, self hosted Cloud, seen by a developer for developers - Uncloud：開発者のためのセルフホスト型クラウド
魅力的タイトル: 「Kubernetesに疲れたらこれを試せ——『Uncloud』が提示する“最小限で回る”セルフホスティングの世界」

## 要約
Uncloudは「自分でホストするHeroku風」を目指す軽量なセルフホスト型プラットフォーム。Docker/Composeを前提に、単一コマンドでデプロイを完結させ、WireGuardでノード間を暗号化したプライベートネットワークで繋ぐのが特徴だ。

## この記事を読むべき理由
日本のフリーランス、小規模チーム、あるいはオンプレ／ローカルGPUを活かしたAI実験を行う開発者にとって、Kubernetesのオーバーヘッドを避けつつ“デプロイの自動化”を実現する選択肢として興味深い。データ主権や帯域・レイテンシ要件が厳しい国内案件でも選択肢になり得るため、検討価値が高い。

## 詳細解説
- アーキテクチャ概観  
  - 各サーバーは同等の uncloudd を動かす分散構成。中央オーケストレータはなく、各ノードが役割を持ちすぎない分散設計。リソース消費は小さく抑えられる設計思想。  
- デプロイ体験（開発者寄り）  
  - クライアントは単一コマンド uc を使い、Compose ファイル拡張で設定。イメージは中央レジストリを経由せず、SSH経由でレイヤーごとに転送（いわゆる「pussh」）。Blue/Green 等のローリング戦略で無停止デプロイを目指す。  
- ネットワークと公開経路  
  - WireGuardで暗号化されたプライベートネットを構築し、iptablesでルーティング。各ノードに Caddy を置いてHTTP/HTTPS（Let’s Encrypt対応）やロードバランシングを担当させる。  
- 管理方針と可用性トレードオフ  
  - CAP観点では可用性を優先し、一貫性は犠牲にする設計。小規模クラスターで明示的なサービス配置を行い、自己回復（自動再スケール）は現状薄め。  
- 技術スタックのハイライト  
  - Docker / containerd、gRPC（grpc-gateway経由でREST）、unregistry（レジストリの代替）、Corrosion（サービス発見/状態共有）、Caddy、WireGuard。  
- 現状の限界と懸念点  
  - ドキュメントや運用機能が未成熟で、永続化（DBレプリケーション・バックアップ/リストア）はユーザーの責任。環境変数非対応など12-Factorアプリの要件と外れる点がある。DNS依存のフェイルオーバーや永続化戦略は設計段階での注意が必要。

## 実践ポイント
- 小さな実験環境でまず検証する：ローカルVMや少数のVPSでucを試し、デプロイ/ロールバック運用を体験する。  
- 永続データは外部設計で確保：Redis ClusterやMinIOなど自己復元性の高いサービスを併用し、DBは明示的なレプリケーション設計を行う。  
- バックアップ＋リストアを必須化：バックアップだけでなく復元テストを自動化しておく。  
- ネットワークと帯域を評価：国内向けなら配信ノードの分散と回線品質を検証。ローカルGPU混在（AI推論）を考える場合は帯域とトラフィック設計を慎重に。  
- 補助ツールで穴を埋める：IAC/CIはUncloudに任せず外部で実装し、監視・アラート・ログ集約は別途整備する。  
- セキュリティ運用を忘れずに：SSH鍵管理、WireGuardの鍵ローテーション、ファイアウォールポリシーを運用手順に含める。

小規模で“手を動かす”開発者には刺さるプロジェクト。完璧ではないが、Kubernetesの代替を探す国内の現場で試す価値は十分にある。興味があれば公式リポジトリやHacker Newsの議論を追って、実験的に動かしてみることを勧める。
