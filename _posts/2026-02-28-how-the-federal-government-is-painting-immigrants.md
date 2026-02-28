---
layout: post
title: "How the federal government is painting immigrants as criminals on social media - 連邦政府が移民をソーシャル上で「犯罪者」と描く手口"
date: 2026-02-28T19:04:47.456Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.npr.org/2026/02/27/nx-s1-5720167/trump-ice-immigration-social-media-deportation-dhs-immigrants-detained-disputes"
source_title: "Is the government really deporting the 'worst of the worst?'  : NPR"
source_id: 395566619
excerpt: "連邦機関がSNSで移民を凶悪犯扱い—誤情報や古い前科混在の実態"
image: "https://npr.brightspotcdn.com/dims3/default/strip/false/crop/4500x2531+0+0/resize/1400/quality/85/format/jpeg/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2F56%2Fb0%2F461812d5434598da11ab25f1e624%2F2026-02-dhs-tweets-final.jpg"
---

# How the federal government is painting immigrants as criminals on social media - 連邦政府が移民をソーシャル上で「犯罪者」と描く手口

政府のSNS投稿が「凶悪犯」を演出し、実際には過去の軽微な罪や無罪・記録不一致のケースが混在している—ソーシャルでつくられる「見せかけの危機」を読み解く。

## 要約
DHSやICEなど連邦機関がX（旧Twitter）で拘束者を「WORST OF THE WORST」などと断定的に紹介する投稿を大量に行い、NPRの調査では事実と異なる扱いや古い／確認できない前科が多数含まれていた。

## この記事を読むべき理由
プラットフォーム設計者、プロダクト関係者、広報、プライバシーに関心のある技術者は、政府の公式アカウントがもたらす情報の拡散力と誤情報リスク、信頼担保の仕組み（検証・訂正・監査）の重要性を理解する必要があるから。

## 詳細解説
- 手法：政府アカウントが容疑者の写真＋断定的文言で日次に近い頻度で投稿。感情喚起を狙うビジュアルと短い見出しで拡散力を高める。  
- 観察された問題点：
  - 投稿の対象は、NPRが抽出した範囲で2,000件超にのぼる。ミネソタ州130件の詳細調査では、19件が最後の有罪判決から20年以上経過（うち多くは重大犯罪）し、6件は有罪記録が確認できず、37件は公開記録と照合できなかった。  
  - DHSの「Worst of the Worst」サイトや関連投稿では、交通違反や軽微な所持で挙げられているケース、誤った州・写真の誤用、起訴が取り下げられたにもかかわらず投稿が残る例などが報告されている。  
  - 地方当局や州は反論・訂正を行っており、法廷での係争や公的記録との齟齬が明るみに出ている。  
- 技術的含意：プラットフォームは公式アカウントの発信に対する検証パイプライン（メタデータ、出所署名、編集履歴・訂正表示）や、画像と個人情報の取り扱いに関するガイドラインを持つべき。公開データと政府発表の突合が難しい点は、API設計やログ保全の必要性を示す。

## 実践ポイント
- プロダクト設計者／エンジニア：
  - 公式アカウント投稿に対する「証拠付きメタデータ」(発信根拠、日時、担当部署)を必須化する。  
  - 修正・撤回があった場合は目立つ形で履歴を残すUIを実装する。  
- コミュニケーション担当：
  - 断定表現を避け、法的ステータス（起訴中／有罪／不起訴）を明記する運用を作る。  
- 市民・記者：
  - SNSで見た「政府発表」は公開記録と突合し、複数ソースで確認する。誤りを見つけたら公式訂正を要求する。  
- 日本向け教訓：
  - 政府や自治体の公式SNS運用が増える日本でも同様のリスクは大きい。透明性、訂正の仕組み、個人情報保護を優先した運用ルール整備が求められる。
