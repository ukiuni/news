---
layout: post
title: "Immigration agents have used Mobile Fortify to scan the faces of countless people in the US—including many citizens - 移民捜査官が使う顔認証アプリ「Mobile Fortify」が米国内で市民も含め数多くの顔をスキャンしていた"
date: 2026-01-29T07:11:01.909Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.wired.com/story/mobile-fortify-face-recognition-nec-ice-cbp/"
source_title: "Here’s the Company That Sold DHS ICE’s Notorious Face Recognition App | WIRED"
source_id: 414878956
excerpt: "移民捜査官の顔認証アプリが市民の顔まで大量スキャン、誤認や不透明さで深刻な影響"
image: "https://media.wired.com/photos/697a4e187173d3b04951493e/191:100/w_1280,c_limit/Company-That-Makes-ICE-Notorious-Face-Recognition-App-Security-2224533016.jpg"
---

# Immigration agents have used Mobile Fortify to scan the faces of countless people in the US—including many citizens - 移民捜査官が使う顔認証アプリ「Mobile Fortify」が米国内で市民も含め数多くの顔をスキャンしていた

魅力的な日本語タイトル：移民現場で稼働中の顔認証アプリ「Mobile Fortify」──誰の顔が、どう使われているのか？

## 要約
DHS（米国国土安全保障省）の移民関連機関が現場で使う顔認証アプリ「Mobile Fortify」は、ベンダーがNECであることや、顔・非接触指紋・身分証OCRを送って中央の生体照合システムで検索する仕組みが明らかになり、誤認識や透明性不足の懸念が浮上しています。

## この記事を読むべき理由
米国での実運用は、AI顔認証の社会実装が抱えるプライバシー・バイアス・ガバナンス上の課題を生々しく示します。日本でも顔認証や公的データ活用が進む中で、技術者・政策担当者・市民にとって示唆が大きい事例です。

## 詳細解説
- アプリ概要：Mobile Fortifyは現場（検問・停止など）で人物の顔写真、非接触指紋、身分証の写真を取得し、データをCBP（税関・国境警備局）へ送信して生体照合システムで照合します。  
- ベンダーと契約：公開された情報ではベンダーはNEC。NECの製品は一対多検索・一対一一致を謳っており、DHSと過去に約2,390万ドル規模の契約が存在しました（2020–2023）。  
- AIとデータ：アプリ自体はICE（移民関税捜査局）でも使用され、AIモデルの所有・運用は主にCBP側にあるとされています。CBPの「Trusted Traveler」関連データがモデルの訓練・評価・ファインチューニングに用いられた可能性が示唆されています（CBPは詳細非開示）。  
- 運用と規制上の問題：当局は「高影響」の運用と認めていますが、AI影響評価や監視・異議申し立てプロセスが未完成のまま配備・運用されている点が指摘されています。誤認での拘束事例や、渡航資格の剥奪につながった申告例も報告されています。

## 実践ポイント
- エンジニア向け：データセットの偏り検証（人種・年齢・性別別の誤認率）、外部監査可能なログや説明可能性（XAI）を組み込む。展開前にAI影響評価（AIA）を実施し、異議申立てのワークフローを実装する。  
- 組織・政策担当者向け：運用前の透明性（使用目的・データ保持期間・第三者アクセス）を公開し、独立監査と苦情対応チャネルを設置する。  
- 一般読者・市民向け：公的機関とのやり取りでは記録を残す（日時・場所・担当者名）、疑問点は書面で求める。信頼できる報道や市民団体の情報にも注目する。

短く言えば、Mobile Fortifyの事例は「顔認証を現場で使う」ことの利便性と重大リスクを同時に示しています。日本でも同様の技術が広がる前に、技術的・制度的な備えを進めることが求められます。
