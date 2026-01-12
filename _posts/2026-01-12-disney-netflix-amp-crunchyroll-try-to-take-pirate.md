---
layout: post
title: "Disney, Netflix & Crunchyroll Try to Take Pirate Sites Down Globally Through Indian Court - ディズニー、Netflix、Crunchyrollがインド裁判所を通じて海賊版サイトを世界的に停止させようとする"
date: 2026-01-12T15:08:03.711Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://torrentfreak.com/disney-netflix-crunchyroll-try-to-take-pirate-sites-down-globally-through-indian-court/"
source_title: "Disney, Netflix &amp; Crunchyroll Try to Take Pirate Sites Down Globally Through Indian Court * TorrentFreak"
source_id: 428891125
excerpt: "ディズニー等がインド裁判所で海賊版の世界一斉停止を狙うが、海外レジストラの不協力で実効は限定的に終わる"
image: "https://torrentfreak.com/images/justice-court.jpg"
---

# Disney, Netflix & Crunchyroll Try to Take Pirate Sites Down Globally Through Indian Court - ディズニー、Netflix、Crunchyrollがインド裁判所を通じて海賊版サイトを世界的に停止させようとする

魅惑の見出し: インド裁判所が「グローバルキルスイッチ」宣言──でも域外レジストラは従わない？

## 要約
インド高等裁判所が米大手コンテンツ事業者（Disney、Netflix、Crunchyroll、Warner、Apple ら）の申立てを受け、約163ドメインを対象にした動的な差止め命令（Dynamic / Dynamic++）を出したが、多くの海外ドメインレジストラは応答せず、狙った「世界一斉停止」は限定的な効果にとどまっている。

## この記事を読むべき理由
グローバルに展開するドメイン運用と裁判管轄の交差点は、コンテンツ配信事業者、ISP、ドメイン事業者、日本の開発者や法務担当にとって運用・法務戦略を再考させる実例です。日本市場でも同様の手法が注目される可能性があり、対応の実務知識は役立ちます。

## 詳細解説
- 裁判所の手法：従来の域内ISPブロッキングから進化し、「Dynamic injunction」は新ドメインやミラーにも効くよう継続的な域内差止めを可能にしました。さらに「Dynamic++」やその上位版では、著作権未登録作品も保護対象に含め、ドメイン登録業者（registrars）自体を被告に加えることで、ドメインの凍結・ロックを求めます。
- 今回の事案（2025年12月18日、テジャス・カリア判事の命令）は163のドメインを列挙し、そのうち約125が具体的なレジストラに紐付けられていました。申立人はACE（MPAの反海賊版部門）と連携する大手スタジオ群で、ターゲットは「Stranger Things」「Squid Game」「Silo」など人気タイトル。
- グローバル効果の課題：命令はレジストラに72時間でドメイン凍結、4週間で登録者情報の提出を求めますが、多くの海外レジストラ（Namecheap、GoDaddy、NameSilo 等）は不応答または非協力で、実際に凍結されたのは一部（Porkbun、WHG、Hostingerなど）に留まりました。国家レベル（トンガ政府など）や国外法的強制力の限界が露呈しています。
- 海賊版側の回避手法：ドメイン切替、リダイレクト、ミラーサイト、別TLD移行などで短期間で復活するケースが多く、差止めだけで根絶は困難です。

## 実践ポイント
- コンテンツ権利者向け
  - ドメインレジストラのポリシー評価を事前に行い、協力的なレジストラを優先して監視と連携窓口を確保する。
  - 差止めに加え、ホスティング先や決済チャネル、広告ネットワークへの対処を同時進行で行うと効果が高い（刃を多方面に向ける）。
- レジストラ/ホスティング事業者向け
  - 海外裁判所からの差止め要請に対応する内部プロセス（法律審査、通知、ログ保存）を整備しておくと訴訟対応が迅速化する。
- ネットワーク運用者・エンジニア向け
  - DNS監視、Certificate Transparencyログ、クラウド/ CDN のログを利用して不正ドメインやリダイレクトの兆候を自動検知する仕組みを導入する。
- 日本の読者へ（実務的視点）
  - 日本からのアクセス遮断や国内ISPのブロッキングは既に実行可能だが、域外レジストラや法域越えの対応は複雑。コンテンツ事業者やプラットフォームは、国際的な法務戦略と技術対策を組み合わせる必要がある。

短く言えば、インド裁判所のDynamic++は有力なツールだが、「グローバルキルスイッチ」には法的・実務的な限界があり、現場では多層的な対策（法務＋技術＋インフラ）が不可欠です。
