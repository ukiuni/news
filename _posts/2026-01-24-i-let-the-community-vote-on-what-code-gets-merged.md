---
layout: post
title: "I let the community vote on what code gets merged. Someone snuck in self-boosting code. 218 voted for it. When I tried to reject it, they said I couldn't. - コミュニティ投票でマージを任せたら「自分優遇コード」が紛れ込んだ：218票、拒否は通らず"
date: 2026-01-24T01:56:46.822Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.openchaos.dev/posts/week-3-the-trojan-horse"
source_title: "Week 3: The Trojan Horse | OpenChaos Blog"
source_id: 420396051
excerpt: "コミュニティ投票で自分優遇コードが潜入、218票で承認寸前、ルール整備を強制された顛末"
image: "https://blog.openchaos.dev/og?title=Week%203%3A%20The%20Trojan%20Horse&amp;description=A%20PR%20hid%20vote%20manipulation%20in%20plain%20sight.%20Democracy%20overruled%20the%20maintainer.%20So%20the%20maintainer%20wrote%20a%20constitution."
---

# I let the community vote on what code gets merged. Someone snuck in self-boosting code. 218 voted for it. When I tried to reject it, they said I couldn't. - コミュニティ投票でマージを任せたら「自分優遇コード」が紛れ込んだ：218票、拒否は通らず

魅力的なタイトル：民主主義にトロイの木馬？GitHub投票で明かされた「運営ルール」の穴と即実践すべき対策

## 要約
コミュニティ投票で自動マージする実験リポジトリに、作者自身を優遇する隠しロジック（Base64で隠匿）が紛れ込み218票で通過寸前に。運営が拒否すると「ルールに書いてないから合法」と反論され、結局ルールを明文化してCIで保護する流れになった。

## この記事を読むべき理由
コミュニティ主導のOSS運営や社内での民主的ワークフローを考える日本の開発者／プロダクト担当者にとって、ルール設計の抜けや自動化の落とし穴を実例で学べるから。

## 詳細解説
- 何が起きたか：PRにあった一行（例: btoa(b.author) === 'RmVsaXhMdHRrcw=='）はBase64で作者名を隠し、当該作者のPRを優先表示して目立たせる仕掛けだった（虹の点滅境界も追加）。表向きの票数だけでなく「見える化」で優位を取るトロイの木馬的改変。
- ガバナンスの対立：運営者は「マルウェアはNG」として拒否したが、コミュニティからは「ルールに明示されていないならOK」の反論。最終的に運営はルールに従い一旦マージを承認し、その後明文化で対処。
- 技術的副産物：その後のデプロイでは認証ヘッダ不足で「健康指標」機能が全て壊れて表示されるなど、誰も動作確認しておらず「動くか確認しないまま投票」で問題が拡大。
- 波及効果：プロジェクト外で$CHAOSトークンが作られるなどブランディングの拡散も発生。速度（毎日マージ）と分散意思決定のトレードオフが露呈した。

## 実践ポイント
- ルールを明文化し、不可侵なファイル（例：RULES.md）をCI／ブランチ保護で守る。  
- マージ前に自動テスト・統合テストを必須化し、API認証や外部呼び出しはモック検証を行う。  
- レビュー遅延（quorum）や「最低レビュー数／オーナー承認」を設定して、速すぎるマージを抑制する。  
- 変更に自己利益が絡む可能性がある場合は明示的な開示を義務化する（UIで目立たせる等の変更は特に要注意）。  
- リントや静的解析で「ベース64で自己識別」「動的ソートで作者優先」などの疑わしいパターンを検出するルールを追加する。  
- ブランディングやトークンの発生は外部リスク。公式発表ルールを明確にして法務/コンプライアンス窓口を用意する。

短いまとめ：民主的プロセスは強いが「書かれていないことは認められる」性質もある。期待する振る舞いがあるなら、それをコード化してCIで守るのが最短の防御だ。
