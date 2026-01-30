---
layout: post
title: "Why France just dumped Microsoft Teams and Zoom for homegrown videoconferencing - なぜフランスはTeamsやZoomを捨て、自国製のビデオ会議へ移行したのか"
date: 2026-01-30T04:07:10.896Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.zdnet.com/article/france-dumps-teams-zoom-homegrown-videoconferencing-eu-digital-sovereignty/"
source_title: "Why France just dumped Microsoft Teams and Zoom for homegrown videoconferencing | ZDNET"
source_id: 414142106
excerpt: "データ主権重視でフランスがTeams/Zoomをやめ国産Visioへ移行"
image: "https://www.zdnet.com/a/img/resize/75524a59797d1038d50b8eb40f0afec9b82eda4d/2026/01/29/e23c26b7-49d9-4842-bead-99f6261ae1bf/franceflaggettyimages-521854066.jpg?auto=webp&amp;fit=crop&amp;height=675&amp;width=1200"
---

# Why France just dumped Microsoft Teams and Zoom for homegrown videoconferencing - なぜフランスはTeamsやZoomを捨て、自国製のビデオ会議へ移行したのか
フランスが「Teams／Zoom」を捨てて自国開発のオープンソース会議ツール「Visio」へ移行した理由とは？

## 要約
フランス政府はデータ主権と安全保障の観点から、Microsoft TeamsやZoomなど米国製サービスの契約更新を打ち切り、MITライセンスのオープンソース「Visio」を政府標準のビデオ会議に採用。2027年までに全面移行を目指す。

## この記事を読むべき理由
欧州の「デジタル主権」戦略は、クラウド・コラボレーションの主流を変えつつあります。日本の企業・自治体でもデータ管理や法的リスク（例：米国Cloud Act）を再評価する潮流が広がる可能性があり、技術選択と調達方針に直接関係します。

## 詳細解説
- 背景：フランスは国家機密や研究データが外国法でアクセスされるリスクを懸念。欧州全体で自国内（EU内）技術への依存を高める「デジタル主権」政策の一環。
- Visioの概要：MITライセンスのオープンソース。Django（Python）、React（UI）、LiveKit（スケーラブルなビデオ基盤）で構築。既存機能はHDビデオ、画面共有、チャット、AI字幕・話者識別（フランスのPyannote技術）など。
- セキュリティと準拠：ANSSI（仏独立サイバー機関）が暗号化・セキュリティ強化を支援。MatrixベースのTchapなど既存の安全なメッセージと統合可能。
- 展開スケジュールと規模：約1年のテストで4万人の定期ユーザー、短期に20万人規模へ拡大目標。非欧州プラットフォームのライセンス更新は順次停止、完全移行を2027年目標とする。
- 経済的側面：政府側はライセンス費削減や地場産業の活性化を強調（政府試算で100,000ユーザーごとに年間約100万ユーロの削減見込み）。
- 論点：可用性・ユーザビリティを米国大手と同等に保てるか、コストとスケールのトレードオフ、産業競争力への影響（エリクソンCEOの懸念など）。

## 日本市場との関連
- 日本でも「データ国内管理」「特定国法のアクセス懸念」は重要課題。官公庁や大企業の調達ポリシー見直し、国内クラウド・OSS採用の検討が増える可能性あり。
- ローカル事業者（NTT、富士通、NEC等）や日本発OSSとの連携で、同様の「主権」モデルを検討する余地がある。
- 調達面では「運用体制」「セキュリティ監査」「長期保守」をどう担保するかが鍵。国際相互運用性も意識する必要あり。

## 実践ポイント
- 自社で扱うデータの「機微度」を分類し、どの通信・コラボツールで扱うかポリシー化する。
- LiveKitやMatrixなどのOSSスタックをPoCで試し、可用性・遅延・運用コストを評価する。
- 契約更新時に法的リスク（Cloud Actなど）とデータ移転条項をチェックする。
- セキュリティ基準（暗号化、ログ管理、監査）を明確化し、外部監査や第三者評価を導入する。
- 行政・業界での「国内代替」動向を注視し、共同開発や地場企業との連携を検討する。

（出典：ZDNET「Why France just dumped Microsoft Teams and Zoom for homegrown videoconferencing」要約）
