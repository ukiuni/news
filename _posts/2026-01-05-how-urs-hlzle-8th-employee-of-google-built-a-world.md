---
  layout: post
  title: "How Urs Hölzle 8th employee of Google built a world-class infra using LEGO and saved millions of dollars of Infra cost for Google. Not only he built Infra which was cheap for Google but Infra that was super reliable for Google users. - グーグル8人目の社員、ウルス・ヘルツレが“安価なハードで作った頭脳”でインフラを変えた話"
  date: 2026-01-05T10:23:28.251Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://deepsystemstuff.com/urs-holzle-the-professor-who-built-googles-brain-using-cheap-hardware-strategy/"
  source_title: "Urs Hölzle: The Professor Who Built Google&#8217;s Brain using Cheap Hardware Strategy &#8211; deepsystemstuff.com"
  source_id: 474444558
  excerpt: "LEGO発想で安価サーバを連結、Googleが数百万ドルを節約し超高可用性達成"
---

# How Urs Hölzle 8th employee of Google built a world-class infra using LEGO and saved millions of dollars of Infra cost for Google. Not only he built Infra which was cheap for Google but Infra that was super reliable for Google users. - グーグル8人目の社員、ウルス・ヘルツレが“安価なハードで作った頭脳”でインフラを変えた話

クリックせずにはいられない一言タイトル案:
「安物サーバで世界一の信頼性をつくる──Google初期の“インフラの魔術師”ウルス・ヘルツレの設計思想」

## 要約
Google初期のインフラ設計を主導したウルス・ヘルツレは、安価な汎用ハードウェア＋ソフトウェア側の耐障害設計で電力と設備コストを大幅に削減し、高い可用性を実現した。

## この記事を読むべき理由
日本でもクラウド／データセンター運用コストと省電力は喫緊の課題。早期にスケール問題に向き合ったGoogleの設計原則は、コスト最適化や信頼性向上を目指すエンジニア、SRE、インフラ投資の意思決定者にとって具体的な示唆を与える。

## 詳細解説
- 背景：検索サービスの急成長に伴い、単純な高価な専用機器ではコストと拡張性の問題が顕在化。Larry／Sergeyは「既存のインフラではスケールしない」と判断し、専門家を必要としていた。
- 人物と役割：ウルス・ヘルツレはスタンフォード博士で、大学教授や企業経験を持つ初期メンバー（社員番号8）。データセンター設計とソフトウェア両面の改善を主導した。
- 基本戦略（技術の核）
  - 汎用（commodity）ハードウェアの採用：高価な専用機ではなく、安価で大量調達できるx86系サーバ群を標準化し、均一な設計で運用を単純化。
  - フェイルファスト前提の設計：個々のサーバ故障を前提にし、ソフトウェア層で冗長性と再配置（リトライ／リスケジューリング）を担わせることでハード故障のコストを下げる。
  - ソフトウェア重視の可用性：独自の高スケーラブルWebサーバ（GWSなど）や、Linuxカーネル周りのチューニング・拡張で大規模クラスタの性能と信頼性を引き出した。
  - 電力効率の追求：データセンター設計でPUE（電力利用効率）改善を狙い、従来比で大幅な電力削減を達成したとされる（結果として数百万ドル単位のコスト削減に寄与）。
- 成果と派生：こうした設計思想はクラスタ管理システムやコンテナ運用など後続の大規模オーケストレーション技術（Borg → Kubernetes 等）にも影響を与え、クラウド時代の基盤概念の礎になった。

## 日本市場との関連性
- 電気料金・省エネ規制が厳しい日本では、電力効率を高める設計は直接的なコスト競争力に直結する。大手企業やクラウド事業者だけでなく、オンプレ運用企業やエッジ事業者にも適用可能。
- ハード調達のサプライチェーンや国内データセンター事情を踏まえ、汎用機＋ソフト耐障害化はコスト最適化の現実的な選択肢となる。
- 技術人材の育成面でも、「ソフトで信頼性を作る」文化はSREやDevOpsの導入を進める日本企業にとって模範となる。

## 実践ポイント
- 小さく均一なサーバ設計を採用し、故障は前提にした運用フローを整備する（自動復旧・リトライ・フェイルオーバーを標準化）。
- PUEやサーバ当たりの電力消費を測定し、データセンター設計（冷却、レイアウト、電源設計）を見直す。
- Linuxやミドルウェアのチューニングに投資し、ソフトウェアでスケール・信頼性を確保する。必要ならカーネルやネットワークスタック周りの設定を検証する。
- 小規模なPoCで「安価なハード＋冗長ソフト」の設計を試し、運用手順を整える（障害挙動の自動化テストを必ず実施）。
- 学ぶための参考：Googleが実践したクラスタ運用の考え方（Borgなどの系譜）や公開された論文・事例を読み、設計原則を自社に落とし込む。

短くまとめると：高価な専用機に頼らず、「安価なハードを大量に、ソフトで守る」設計はコストと信頼性の両立を可能にする。日本の現場でも即応用できる実践的な指針だ。
