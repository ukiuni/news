---
layout: post
title: "I tried to make DevFest Ireland accessible - and ended up building a SaaS - DevFest IrelandをアクセシブルにしようとしたらSaaSが生まれた"
date: 2026-04-10T18:12:39.097Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/gdg/i-tried-to-make-devfest-ireland-accessible-and-ended-up-building-a-saas-1o87"
source_title: "I tried to make DevFest Ireland accessible - and ended up building a SaaS - DEV Community"
source_id: 3481980
excerpt: "DevFestの手話要望から誕生した高精度イベント向けライブ字幕SaaS"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fkngf7yjtjwp7o69yh3nw.jpg"
---

# I tried to make DevFest Ireland accessible - and ended up building a SaaS - DevFest IrelandをアクセシブルにしようとしたらSaaSが生まれた
「1件の問い合わせ」が生んだ、イベント向け高精度ライブ文字起こしサービス誕生の裏側

## 要約
デブフェストの運営中に出た「手話通訳はありますか？」という問い合わせをきっかけに、主催者が現場のニーズを満たすために自前で開発したライブ文字起こしサービス（VolenScribe）が生まれた話。技術カンファレンス特有の語彙や多言語対応を重視して精度を追求している。

## この記事を読むべき理由
イベント運営やコミュニティ主催をする日本のエンジニア／オーガナイザーにとって、単なる「補助機能」ではなく必須のアクセシビリティ技術（ライブ字幕・通訳手配）の現実的な課題と現場解決の実例が学べるから。

## 詳細解説
- 問題の発端：複数のろう者からの参加希望があり、「アイルランド手話（ISL）通訳」を確約できなかったことが出発点。手話通訳は人数・日数・早期予約の制約が大きい。  
- 可視化されたニーズ：手話だけでなく、難聴者、遠隔参加者、発表の速さやアクセントで聞き取りづらい参加者、神経発達特性のある参加者など、多様な参加者が「文字での補助」を必要としている。  
- 既存サービスの問題点：人手による字幕は高精度だが高コスト、既存AI字幕はコスト面は良くても専門用語や速い話し方で精度が落ちがちで技術系イベントには不十分。  
- 解決の方向性：現場で頼れる精度と現実的な価格の両立を目標に、自分たちでツールを作ることに。結果としてVolenScribeというSaaSが誕生。  
- 成果指標：多言語対応（25言語）や平均ワードエラー率（WER）約3.9%といった定量的な精度を追求し、「読めば話の内容が追える」レベルを目指している点が重要。

## 実践ポイント
- ライブ字幕はオプションではなく「イベント設計の中心」に据える。早期に見積もり・確保を。  
- 人手字幕＝高精度だが高コスト、AI字幕＝コストは下がったが事前に専門語彙で精度検証を必ず行う。  
- 技術トーク用の辞書（ライブラリ名・固有名詞・略語）を用意してモデルに学習・適用する。  
- 多言語・遠隔視聴を考慮すれば参加者の母語対応は競合優位にもなる。  
- 小規模イベントでも導入しやすい価格帯の代替手段を検討する（テスト導入・一部セッションのみなど）。

この記事は「アクセシビリティ対応はコストか理念か」という抽象論ではなく、実際に人が来られる・来られないに直結する実務課題として捉え直す契機を与えてくれます。
