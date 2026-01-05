---
  layout: post
  title: "There were BGP anomalies during the Venezuela blackout - ベネズエラ停電時にBGPの異常が発生していた"
  date: 2026-01-05T21:52:24.899Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://loworbitsecurity.com/radar/radar16/"
  source_title: "Radar #16: Week of 01/05/2026"
  source_id: 46504963
  excerpt: "ベネズエラ停電と同時期にBGPで異常なルートリークが発生し重要経路が迂回"
  image: "https://loworbitsecurity.com/content/images/2025/01/banner_bgDark_white.png"
---

# There were BGP anomalies during the Venezuela blackout - ベネズエラ停電時にBGPの異常が発生していた
暗闇の裏で進行した「ルーティングのいたずら」——ネットワーク観測者が見たBGPの痕跡

## 要約
Low Orbit Securityの調査は、ベネズエラでの大規模停電と時を同じくしてBGPの異常（ルートリークや奇妙なASパス）が観測されたことを示している。公開BGPデータを解析すると、特定のIPブロックが通常とは異なる経路を通ってアナウンスされていた。

## この記事を読むべき理由
国家レベルの事象や停電とリンクするインターネットのルーティング異常は、インフラ運用者やセキュリティ担当者にとって「他人事ではない」問題です。日本の事業者も国際トラフィックや海底ケーブル、トランジット事業者の選定で同じリスクにさらされています。

## 詳細解説
- BGPとASの基本  
  BGPは自律システム（ASN）間で経路情報を交換するプロトコル。経路はASパス（通過するASの列）で表現され、BGPは通常、経路長（ASホップ数）やポリシーでルートを選択する。だがBGP自体は認証・検証が不十分で、ルートハイジャックやルートリークが発生しやすい。

- 観測された異常の中身  
  Cloudflare RadarでAS8048（CANTV）に関するルートリークが1月2日に検出され、さらにRIPE RISのMRTデータをbgpdumpで解析すると、200.74.224.0/20（複数の/23、/24を含む）が通常経路と異なるASパスでアナウンスされていた。注目点はAS8048（CANTV）がASパスに繰り返し（約10回）挿入されていること。ASパスのプリペンド（同一ASを繰り返す）は通常その経路を「長くして」選ばれにくくするが、今回のような変則的なパスは明らかに通常運用ではない。

- 関係する事業者とセキュリティ状況  
  解析で出てきたASパスにはSparkle（イタリアのトランジット）やGlobeNet（コロンビア）などが含まれ、isbgpsafeyet.comではSparkleがRPKIフィルタリングなどの一部のセキュリティ対策を実装していない「unsafe」とされている。RPKI/ROA未整備やフィルタリング不足は、ルートの正当性検証を困難にする。

- インフラとタイミングの関連性  
  200.74.224.0/20はDayco Telecomに割り当てられており、逆引きやWHOISで銀行、ISP、メールサーバなど重要インフラが含まれることが確認できた。Cloudflareの検出（Jan 2 15:40 UTC）と停電・軍事的出来事の時系列（Jan 3の報道）とを照合すると、短時間のルート操作でトラフィックを経路上の任意ポイントに集めることで情報収集や通信妨害が理論的に可能であることが示唆される。ただし動機や主体は断定できない。

- データソースと再現可能性  
  公開MRTデータ（ris.ripe.net）、bgpdumpやbgpstreamなどのツールを用いることで、いつ、どのプレフィックスがどうアナウンスされたかを再現できる。Cloudflare Radarは検出を示すが、元のプレフィックス詳細はMRT解析が必要になるケースがある。

## 実践ポイント
- 自組織のプレフィックスを守る  
  - ROAを作成してRPKIでアナウンス正当性を担保する。  
  - トランジット事業者に対してRPKI検証／フィルタリングの実施を要求する。

- BGP運用の防御強化  
  - prefix-list、max-prefix、AS-pathフィルタ、IN/OUTの適切なフィルタリングを設定する。  
  - BGPセッションに対するMD5/TCP-AOやTTLセキュリティの検討。  
  - MANRS（Mutually Agreed Norms for Routing Security）準拠を目指す。

- 監視と早期検知  
  - Cloudflare Radar, RIPE RIS, BGPStream, isbgpsafeyetなどの公開資源を定期的に監視する。  
  - 自前でBGPDUMP/BGPStreamを動かし、重要プレフィックスのアラートを構築する（WHOIS/逆引き参照を自動化すると状況把握が速い）。

- 連携とインテリジェンス活用  
  - 海外トランジットやピアリング相手のセキュリティ姿勢を評価してリスクを把握する。  
  - 重大インシデント時にはBGPデータを保存・共有できる体制を整え、事後調査に備える。

短時間のBGP操作がネットワークの見通しやデータの経路を変える可能性は現実の脅威です。日本のネットワーク運用者も、公開データを活用した監視とRPKI導入を急ぐ価値があります。
