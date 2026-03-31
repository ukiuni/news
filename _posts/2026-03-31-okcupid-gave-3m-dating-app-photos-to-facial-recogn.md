---
layout: post
title: "OkCupid gave 3M dating-app photos to facial recognition firm, FTC says - OkCupidが300万枚の出会い系写真を顔認識企業に提供したとFTCが主張"
date: 2026-03-31T19:30:50.798Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/tech-policy/2026/03/okcupid-match-pay-no-fine-for-sharing-user-photos-with-facial-recognition-firm/"
source_title: "OkCupid gave 3 million dating-app photos to facial recognition firm, FTC says - Ars Technica"
source_id: 47591104
excerpt: "OkCupidが約300万件のユーザ写真を無通知で顔認識企業に提供、FTCが虚偽表示を問題視"
image: "https://cdn.arstechnica.net/wp-content/uploads/2026/03/okcupid-1152x648-1774975675.jpg"
---

# OkCupid gave 3M dating-app photos to facial recognition firm, FTC says - OkCupidが300万枚の出会い系写真を顔認識企業に提供したとFTCが主張
驚愕：出会い系アプリの写真がAIの学習データに──あなたの顔は誰に売られたのか？

## 要約
2014年にOkCupidが約300万枚のユーザ写真（位置情報や属性データを含む）を顔認識企業Clarifaiに提供していたとFTCが指摘。両社は和解し、金銭罰は科されなかったが、利用目的や共有の虚偽表示を永久に禁じられた。

## この記事を読むべき理由
個人の顔写真や位置情報は極めて敏感な個人情報で、日本でも顔認証・データ利活用の議論が進む中、サービス利用者と開発者双方にとって重要な前例になるため。

## 詳細解説
- 何が起きたか：OkCupid（Match傘下）がClarifaiに対し約300万枚のユーザ写真と位置・属性データへのアクセスを許可。正式な契約や利用制限は設定されず、利用者に共有の機会や通知はされなかったとFTCは主張。  
- Clarifaiの利用用途：同社は提供画像を用いて年齢・性別・人種などを推定する顔認識モデルを構築し、軍や政府機関などにも販売する可能性があると報じられている。  
- 法的対応：FTCは虚偽表示や調査妨害の疑いを指摘。和解では金銭罰はなく、個人情報利用の表示やユーザー選択肢の虚偽表示を禁止する恒久的命令が含まれる。  
- 技術的観点：学習データに個人特定可能な画像が混入すると、バイアスやプライバシー侵害、非承認利用（再配布・顔識別サービス化）といったリスクが生じる。契約での利用目的限定、データ最小化、匿名化の不備が問題の核心。

## 実践ポイント
- ユーザー向け：アプリのプライバシーポリシーと権限（写真・位置情報）を定期的に確認し、不要なら権限を取り消す。顔写真を公開プロフィールに載せるか慎重に判断する。  
- 開発者／事業者向け：第三者にデータを提供する際は書面契約で用途制限・保存期間・再利用禁止を明確化し、DPIA（データ保護影響評価）と監査ログを実装する。モデル訓練用データは可能な限り匿名化・合成化を検討する。  
- 法務／プロダクト：利用規約やUIでの明示的な同意フローを設計し、透明性を担保する。日本の個人情報保護法や今後の顔認証規制を見据えた準備を。

この事例は「便利なAIサービスの裏にあるデータ供給チェーン」を問い直す契機です。ユーザーも事業者も、顔データの扱いに一層の注意が必要です。
