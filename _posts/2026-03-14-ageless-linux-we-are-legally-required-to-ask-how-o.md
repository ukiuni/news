---
layout: post
title: "Ageless Linux. We are legally required to ask how old you are. We won't - Ageless Linux：年齢を尋ねる法的義務がありますが、私たちは聞きません"
date: 2026-03-14T23:18:56.575Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://agelesslinux.org/"
source_title: "Ageless Linux — Software for Humans of Indeterminate Age"
source_id: 47381791
excerpt: "Ageless Linuxが年齢確認義務に反抗し、OSS排除の仕組みを暴露する"
---

# Ageless Linux. We are legally required to ask how old you are. We won't - Ageless Linux：年齢を尋ねる法的義務がありますが、私たちは聞きません

魅力的な見出し：法で年齢確認が義務化される時代に反旗を翻す──「Ageless Linux」が示す、監視インフラか子どもの安全かの分岐点

## 要約
Ageless Linuxは、カリフォルニア州の年齢確認法（AB 1043）に意図的に「不服従」するDebianベースの配布物で、OS識別や年齢APIを改変して年齢データを収集しないことを明示します。目的は、巨大プラットフォームが容易に満たせる規制がボランティア系OSSを締め出す「コンプライアンスの柵（moat）」を露わにすることです。

## この記事を読むべき理由
日本のOSS開発者や教育現場にも示唆があるため。法律は州別でも、規制設計の姿勢（大手有利・小規模排除）は世界的な潮流になり得ます。プライバシー、配布インフラ、教育向け機材や学校導入を考える人は影響を理解しておくべきです。

## 詳細解説
- 法的定義（要点）
  - 「Operating system provider」：/etc/os-release を制御する者はOS提供者とみなされる（Cal. Civ. Code §1798.500(g)）。Agelessはこれを逆手に取り、自分がOS提供者であると宣言する。
  - 「Application」：Debianの各パッケージは法上アプリであり、起動時に年齢区分シグナルを要求される可能性がある。
  - 「Covered application store」：公開サイトやパッケージリポジトリも該当し得るため、ミラーやGitHubも影響対象になりうる。
- 技術的手法
  - 導入は「まずDebianを入れ、次に変換スクリプトを実行してAgeless化」するワークフロー。スクリプトは /etc/os-release を書き換え、年齢確認用のスタブAPIを配置してデータを返さないようにする。
  - 影響の本質は法執行（罰金）ではなく、潜在的な責任と訴訟コストが小規模プロジェクトを萎縮させる点（「存在するだけで効く」抑止力）。
- 教育・安全の観点
  - 著者らは、技術的な年齢ゲートは簡単に迂回され、子どもには教育的助言（人が言う一文）が効果的だと主張。監視基盤を整備することを「子どもの安全」だと誤認する危険を指摘する。
- 今後の計画
  - 数ドルのSBCを使った「Ageless Device」とストアを配り、意図的に法の枠を問い直す実験を予定。これは政策議論を促すための実践的なプロテストでもあります。

インストール（要点）：
```bash
# Debianを入れた後、変換スクリプトを実行（公式サイト提供）
curl -fsSL https://agelesslinux.org/become-ageless.sh | sudo bash
```

## 実践ポイント
- 試す：仮想マシンや検証環境でDebian→Ageless変換を試し、/etc/os-releaseや年齢APIの挙動を確認する。
- 自分のプロジェクトを棚卸し：自分が配るソフトやミラーが「covered application store」や「OS提供者」に該当し得るか検討する。
- 教育現場の選択肢を考える：年齢ゲートに頼らないデジタルリテラシー教育や、プライバシーを守る代替案の導入を検討する。
- 支援／発言：小規模OSSや教育向けデバイスを守る政策議論に参加する（寄付や提言、公的議論への参加など）。

短く：Ageless Linuxは技術と法の「実演」であり、監視的な年齢確認がもたらす副作用（排除・教育の欠如）を可視化するプロジェクトです。日本でも同様の規制設計が議論される前に、技術者として影響を理解しておきましょう。
