---
layout: post
title: "France is moving government PCs to Linux: The end of the 'Microsoft Monopoly' in public sectors or just another failed attempt? - フランス政府、官公庁PCをWindowsからLinuxへ移行：公共部門の「Microsoft独占」の終わりか、それとも別の失敗か？"
date: 2026-04-10T21:27:03.344Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.tomshardware.com/software/windows/french-government-say-its-ditching-windows-for-linux-country-accelerates-plans-to-ditch-us-based-software-in-digital-sovereignty-push"
source_title: "French government says it's ditching Windows for Linux &mdash; country accelerates plans to ditch US-based software in digital sovereignty push | Tom's Hardware"
source_id: 364986525
excerpt: "フランスが官公庁PCをWindowsからLinuxへ移行、デジタル主権と互換性の闘いを始動"
image: "https://cdn.mos.cms.futurecdn.net/8rh5kLKHAvNzqnaeftVA6a-2000-80.jpg"
---

# France is moving government PCs to Linux: The end of the 'Microsoft Monopoly' in public sectors or just another failed attempt? - フランス政府、官公庁PCをWindowsからLinuxへ移行：公共部門の「Microsoft独占」の終わりか、それとも別の失敗か？

フランスが「Windowsを捨ててLinuxへ」本格移行を宣言──日本にも波及しそうなデジタル主権の実験。

## 要約
フランスのDINUM（デジタル政策局）を中心に、政府ワークステーションをWindowsからLinuxへ移行する方針が発表された。目的は米国系ソフト依存の低減と「デジタル主権」の確立で、年内に具体案を固め、健康保険関係などで既に大規模なオープンソース移行を進めている。

## この記事を読むべき理由
EU内で最大級の先例となれば、調達ポリシーや公共ITのベストプラクティスに影響を与える。日本の自治体・官公庁や企業も対抗戦略やリスク管理の観点から注目すべき動きです。

## 詳細解説
- 主導組織と範囲：DINUMに加え、企業局（DGE）、国家サイバー局（ANSSI）、調達局（DAE）らが関与。対象は「ワークステーション／協業ツール／アンチウイルス／AI／DB／仮想化／ネットワーク機器」まで広範。
- 既往の取り組み：国民健康保険の約8万人を、Microsoft TeamsやZoom等から国内オープンソース系のTchap/Visio/FranceTransfert（La Suite）へ移行済。健康データ基盤の「信頼できるソリューション」移行は2026年末目標。
- 背景と狙い：「データ・インフラ・戦略的決定を外部に依存させない」という政治的狙い。米国系ベンダーへの価格・進化・リスク管理上の依存を断つ意図。
- 技術面の論点：
  - アプリ互換性：Office文書、業務専用ソフト、e-Gov連携の整合性（文字化けや書式崩れ）検証が必須。
  - 認証・管理：Active Directory置換（Samba4/FreeIPA等）、端末管理、パッチ供給体制の確立。
  - セキュリティ：ANSSI関与で脆弱性管理・サプライチェーン監査が強化される可能性。
  - 運用負荷：教育・サポート、人員のスキルチェンジ、ドライバや専用ハード対応の確認。
- 成否に影響する要素：段階的移行、現行システムの仮想化／コンテナ化、ベンダーの協力、コミュニケーションツールの成熟度、文書フォーマット互換性。

## 実践ポイント
- まずは現状把握：業務アプリ一覧、OS依存／ライブラリ依存を棚卸し。
- 非重要業務でのパイロット導入：教育・サポート負荷を低リスクで検証。
- 文書互換テスト：日本語フォント・レイアウト・e-文書提出の互換性を実地確認。
- 認証と管理設計：AD代替、SSO、MDMの評価（Samba4・FreeIPA・Linux向け管理ツール）。
- 協業ツールの選定：Matrix/Element、Nextcloud、LibreOffice/OnlyOfficeなどの組合せを検討。
- 調達・契約の見直し：サプライチェーンと更新ポリシーを契約条件に明記。
- セキュリティ監査を早期導入：脆弱性対応ルールとベント対応フローを整備。
- 人材育成：現場向けマニュアルとオンサイト支援を計画。

フランスの動きは「理想」と「現実運用」のせめぎ合いです。日本でも同様の議論と実証が進む可能性が高く、早めの準備と小規模検証が有効です。
