---
layout: post
title: "France is replacing 2.5 million Windows desktops with Linux - フランスが250万台のWindowsデスクトップをLinuxに移行"
date: 2026-04-13T20:39:58.660Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.zdnet.com/article/france-leaves-windows-for-linux-desktop/"
source_title: "France is replacing 2.5 million Windows desktops with Linux - and I mapped out its new stack | ZDNET"
source_id: 362673062
excerpt: "フランスが250万台の官公庁PCをLinux化、主権確保と巨額コスト削減を狙う理由とは？"
image: "https://www.zdnet.com/a/img/resize/0c459c506fb3a54eeb5d7f043ee8bb797ff4459b/2026/04/13/23b3fd94-63bc-4625-981e-ed952278c141/gettyimages-2256863568.jpg?auto=webp&amp;fit=crop&amp;height=675&amp;width=1200"
---

# France is replacing 2.5 million Windows desktops with Linux - フランスが250万台のWindowsデスクトップをLinuxに移行
魅力的タイトル: フランスが“Windows離れ”を決断：250万台の官公庁PCをLinuxで再設計する理由と日本企業が学ぶべきこと

## 要約
フランス政府が2.5百万台の行政用デスクトップをWindowsからLinux（既存のGendBuntuベース）へ全面移行する計画を正式発表。主目的はコスト削減と「デジタル主権」の確立で、2026–2027年にかけて段階的に実行される見込みです。

## この記事を読むべき理由
国内の自治体や企業でも「海外クラウド／ソフト依存」の見直しやコスト圧縮が課題となる中、世界規模で進む官民のオープンソース移行は対岸の火事ではありません。日本のIT担当者が実務的な教訓を得られる好事例です。

## 詳細解説
- 背景と狙い
  - DINUM（仏政府のデジタル統括部門）がWindows廃止を命令。理由は「デジタル主権（extra‑European依存の排除）」「安全性」「コスト削減」。
  - フランスは警察向けに長年運用してきたGendBuntuの実績（約100,000台）を全国展開のブループリントとして利用。
- デスクトップ基盤（想定）
  - ベースはUbuntu LTS系（次期はUbuntu 26.04ベース想定）→ Linuxカーネル7.0相当、GNOME 50採用見込み。
  - グラフィックは従来のX11からWaylandへ本格移行（CanonicalがWaylandをデフォルト化）。
- 標準アプリケーション（予定バージョン）
  - LibreOffice 26.2.2（オフィス文書処理）
  - Firefox ESR 140（ブラウザ）、Thunderbird ESR 140（メール）
  - GIMP 3.0.6（画像編集）
- 主体となるクラウド/コラボレーション群：La Suite Numérique（The Digital Suite）
  - Tchap：MatrixベースのセキュアIM（エンドツーエンド暗号、 federation）
  - Visio：LiveKit/WebRTCベースのビデオ会議（大規模参加対応、録画・文字起こし）
  - Docs：BlockNoteベースの共同編集
  - Grist：スプレッドシート兼ローコード（Relationalなデータ操作）
  - Fichiers：Nextcloudベースのファイル共有（EU内ホスティング、SecNumCloud等準拠）
  - Messagerie：Open Xchangeによるメール・カレンダ
  - 統合SSOとEUホスティングでデータ主権を担保
- コストと運用面
  - GendBuntu導入で数百万ユーロの年次削減を報告。全国移行で数千万ユーロの削減見込み。
  - 技術的チャレンジ：業務アプリの互換性、エンドユーザートレーニング、周辺機器ドライバ、レガシーシステムの接続（認証・ファイル形式等）。

## 実践ポイント
- 小さく始める：まずは部門単位でパイロット（例：非クリティカル部門で3ヶ月）を実施。
- 互換性評価：主要Excel/Word文書、電子署名、専用業務ソフトの動作検証を優先。
- SSOとアイデンティティ戦略を先行：移行失敗の多くは認証・アクセス管理で発生。
- ユーザー教育計画：操作差分、キーボード入力/IME、印刷環境の周知を確実に。
- インフラ設計：EU型の「主権クラウド」モデルを参考に、データ所在地とバックアップ方針を明確化。
- コスト試算を現実的に：削減額だけでなく、移行工数・保守コスト・ユーザー生産性の変化を織り込む。

以上を踏まえ、日本の自治体・企業でも「部分的なLinux導入」「オープンソースによる主権確保」は現実的な選択肢になり得ます。興味があれば、まずは社内で小規模パイロットを立てることをおすすめします。
