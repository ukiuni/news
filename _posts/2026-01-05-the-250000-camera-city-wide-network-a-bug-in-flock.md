---
  layout: post
  title: "The 250,000+ Camera \"City-Wide\" Network: A bug in Flock's system swept 257,806 cameras into an \"ICE detainer\" search. Flock claims no data was accessed—but California, Illinois, and Virginia prohibit such searches regardless. - 25万台超の“市域”カメラネットワーク：Flockのバグで257,806台が「ICE抑留」検索に巻き込まれた。Flockはデータ未閲覧と主張—だが各州ではそのような検索が禁止されている"
  date: 2026-01-05T01:01:08.868Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://haveibeenflocked.com/news/network-size"
  source_title: "The 250,000+ Camera &quot;City-Wide&quot; Network | Have I Been Flocked"
  source_id: 472207127
  excerpt: "Flockのバグで257,806台が「ICE抑留」検索に—データ未閲覧と主張も州法違反の恐れ"
  ---

# The 250,000+ Camera "City-Wide" Network: A bug in Flock's system swept 257,806 cameras into an "ICE detainer" search. Flock claims no data was accessed—but California, Illinois, and Virginia prohibit such searches regardless. - 25万台超の“市域”カメラネットワーク：Flockのバグで257,806台が「ICE抑留」検索に巻き込まれた。Flockはデータ未閲覧と主張—だが各州ではそのような検索が禁止されている

25万台規模の監視カメラ網が“誤って”一斉検索対象に――企業ログが示した現実と運用上の脆弱性。

## 要約
Flockの検索ログにより、257,806台・25,263ネットワークが「ICE detainer」検索の対象になった記録が残る。同社は「データは閲覧されていない」とするが、規模とアクセス可能性は明らかで、州法やアクセス制御の問題を浮き彫りにした。

## この記事を読むべき理由
国内でも監視カメラの民間委託やALPR（自動車ナンバー認識）導入が進む中、外資系ベンダーの運用実態やアクセス制御の甘さは、そのままプライバシーや法令順守リスクに直結する。技術者・調達担当・政策立案者が今すぐ知るべき教訓が詰まっている。

## 詳細解説
- 何が起きたか：ミズーリ州の捜査チームによる検索ログが二度記録され、"Networks Searched: 25,263"、"Devices Searched: 257,806" と表示。検索理由は「ICE detainer」。ログの「moderation」欄に手書き的メモでバグ原因と「No footage or data from these devices was accessed or viewed.」という同社の説明が記録されていた。
- 規模の意味：25万台は同社のカメラ（Falcon, Condor, Wing等）と推定され、月間数百億スキャンに相当する可能性が示唆される。5,000～6,000の公的機関利用数と比べ、25,263というネットワーク数は小売チェーン等の民間顧客を含むことを示唆している。
- 技術的な問題点：
  - アクセス制御が「ベンダー側のフラグやロール」に依存しており、暗号化や顧客保有の鍵で保護されていない可能性が高い。つまり「チェックボックスで共有」を前提とする設計で、ソフトウェアのバグで広範囲アクセスが可能になる。
  - 監査ログの可変性：ログを編集して事後説明を付与する手口が見られ、監査の信頼性が疑われる。改ざん検出や不変ログ（append-only, cryptographic signatures）が欠如している。
  - 法令順守のリスク：カリフォルニア、イリノイ、バージニアでは移民関連の検索を制限する法律があり、「検索対象に入った可能性」自体が問題。結果的に当該州の顧客が知らされていない可能性がある。
- 運用上の帰結：企業が「自分たちのデータだ」と誤認して外部捜査機関へ提供を許可してしまう設計は、データ主体の権利や地域法規制を無視するリスクをはらむ。

## 実践ポイント
- 調達・監査担当向け（すぐやること）
  - ベンダー契約で「顧客保有の暗号鍵」「エンドツーエンド暗号化」「キー管理の独立性」を必須条項にする。
  - 監査ログの不変性（tamper-evident logs）と第三者監査を要求する。
  - 共有ポリシー（誰がどの条件でアクセス可能か）を明文化し、例外は書面で通知させる。
- エンジニア向け（実装でやること）
  - 最小権限・ゼロトラスト原則でアクセス設計。ネットワーク分離とロールベースアクセスを強化する。
  - ログの署名・WORMストレージ・SIEM連携で改ざん検出を導入する。
  - 検索クエリのスコープ検証とレート制限、モニタリングによるアラートを実装する。
- 政策・コンプライアンス担当向け
  - 公共調達では法令順守（国内外の関連法）をチェックリスト化し、違反時の報告義務を契約に盛り込む。
  - 個人情報保護法（APPI）や自治体の指針に基づき、ALPRデータの用途・保持期間・第三者提供ルールを厳格化する。
- 市民・利用者向け
  - 小売店や自治体に設置情報と利用目的の公開を求める。透明性がない場合は問題提起を。

短く言えば：スケールだけでなく「誰がどのデータにいつアクセスできるか」が問題。技術的な鍵管理と不変ログがなければ、同様の事故は日本でも起こりうる。監視インフラを扱う組織は、今すぐ設計・契約・監査を見直すべきだ。
