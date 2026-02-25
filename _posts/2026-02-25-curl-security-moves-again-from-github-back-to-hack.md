---
layout: post
title: "curl security moves again [from GitHub back to hackerone; still no bug-bounty] - curl セキュリティが再び動く（GitHubからHackerOneへ戻る／バグバウンティは継続して終了）"
date: 2026-02-25T17:39:30.980Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://daniel.haxx.se/blog/2026/02/25/curl-security-moves-again/"
source_title: "curl security moves again | daniel.haxx.se"
source_id: 396732193
excerpt: "curlがGitHubからHackerOneへ再移行、機密漏洩・CVE運用で報奨金は廃止"
image: "https://daniel.haxx.se/blog/wp-content/uploads/2020/04/steam-train-501638_1280-1200x676.jpg"
---

# curl security moves again [from GitHub back to hackerone; still no bug-bounty] - curl セキュリティが再び動く（GitHubからHackerOneへ戻る／バグバウンティは継続して終了）
なぜcurlは「報奨金なし」でGitHubをやめてHackerOneに戻したのか？――現場が直面した実務上の不都合と今後の教訓

## 要約
curlプロジェクトは2026年3月1日付でセキュリティ報告の受け口をGitHubからHackerOneへ戻した。バグ報奨金は廃止のままで、理由はGitHub側の運用上の制約や機密保護・ワークフローの問題による。

## この記事を読むべき理由
日本のOSS維持者やセキュリティ初学者にとって、報告受け口の選定がプロジェクト運用と脆弱性対応の質に直結する実例であり、CVE運用や透明性の確保に関する実務的な示唆が得られるため。

## 詳細解説
- 何が起きたか：curlは一度バグバウンティ終了と同時に報告受付をGitHubへ移行したが、運用上の問題でHackerOneへ戻す決定をした。報奨金は依然として無い。
- GitHubでの具体的な問題点：
  - 報告内容がメール通知で全文流れるため、機密（PoCやシークレット）が漏洩するリスク。
  - プロジェクト側で「無効報告」を公開・明示できない。OSSとしての透明性確保に不向き。
  - CVEフィールドを編集できず、CNAとして自前のCVE管理ができない。
  - チーム専用の非公開コメントや短い内部識別子、ラベル付け、ユーザーブロックなど運用に必須の機能が不足。
  - リポジトリごとの協力者管理やプライベートCIの制約など、実用の足かせになる点が複数存在。
- curl側が求める報告システム要件（抜粋）：
  - 初期は非公開で受け付け、後で必ず公開（確定・誤報ともに）する透明性。
  - チーム内のみのプライベート会話と、レポーターや招待者向けの公開会話を分離。
  - CVEの自前指定、アドバイザリ作成支援、無効/有効の明示、タグ付け（例：AIノイズ）、悪質行為者のブロック、レート制限など。
- 影響と論点：
  - バグバウンティ剥離後は報告数が大幅に減少。報奨金の有無はレポートの流入に直接影響するが、プラットフォーム選定は品質と安全性に関わる。
  - 他OSSプロジェクトにとって、ただ「多くが使うからGitHubで十分」という判断は再考の余地がある。

## 実践ポイント
- 脆弱性を見つけたら：curlの公式窓口はHackerOne（https://hackerone.com/curl）。アカウントを作り、機密情報は初期段階から慎重に扱う。
- OSS運営者へ（日本のプロジェクト向け短チェックリスト）：
  - 受け口選定で「機密漏洩リスク」「非公開コメント」「CVE運用」「タグ/識別子」「ユーザーブロック」を評価する。
  - 公開ポリシー（報告→公開のフロー）を明文化し、誤報の公開も含め透明性を担保する。
  - CNA運用やCVE発行が必要なら、プラットフォームのCVE編集可否を確認する。
- 研究／企業向け：報奨金を用意しない場合は報告フローとインセンティブ設計（レピュテーション、迅速なクレジット付与など）を整えると質を維持しやすい。

以上。
