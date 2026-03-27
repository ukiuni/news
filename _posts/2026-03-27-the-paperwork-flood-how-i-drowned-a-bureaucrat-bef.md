---
layout: post
title: "The 'Paperwork Flood': How I Drowned a Bureaucrat Before Dinner - 『書類の洪水』：夕食前に役人を溺れさせた方法"
date: 2026-03-27T15:40:27.759Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sightlessscribbles.com/posts/the-paperwork-flood/"
source_title: "The &#39;Paperwork Flood&#39;: How I Drowned a Bureaucrat before dinner., Sightless Scribbles"
source_id: 47542057
excerpt: "盲目の著者が医療記録をPDF結合しインターネットFAXで役所の紙主義を暴いた痛快な反撃"
---

# The 'Paperwork Flood': How I Drowned a Bureaucrat Before Dinner - 『書類の洪水』：夕食前に役人を溺れさせた方法

フォーマットで仕返し──盲目の作家がデジタルツールで“紙主義”を可視化した痛快な一撃

## 要約
盲目の著者が役所の「紙で出せ」というルールに対して、膨大な過去の医療記録を一つのPDFにまとめてインターネットFAXで送信し、制度の非合理さとアクセシビリティの欠如を露呈させたエッセイ。

## この記事を読むべき理由
日本でも自治体や行政手続きの紙要求やレガシーシステムは日常的な悩みです。技術を使った抗議や、デジタル化・アクセシビリティの実務的示唆が得られます。

## 詳細解説
- 物語の核は「ルールは守るが、ルールが不合理ならテクで反撃する」という“悪意なき遵守（malicious compliance）”。著者は視覚障害者として、メール不可・郵送かFAXのみという運用に対し、デジタル手段で応答した。
- 技術面では「PDFの大量結合」「インターネットFAXサービスの利用」「自動再送設定（retry）」が登場。インターネットFAXはクラウドでPDFを受け取り、受信先のFAX番号へ紙として変換・送信する仕組みで、受け手側には物理な紙として届く。
- 行政側が「メールはセキュリティ上受け付けない」とする主張はよくあるが、TLSやS/MIME、受信側の保存ポリシーなどで安全に電子化できるケースが多い。むしろ紙ベースは物理保存コストや検索性、アクセシビリティの面で劣る。
- 物語は単なるユーモアではなく、アクセシビリティと行政サービス設計の欠陥（スクリーンリーダー利用者への配慮不足、電子受付の未整備）を鋭く指摘している。

## 実践ポイント
- 開発者/自治体向け：電子受付（API／ファイルアップロード）を整備し、受領確認の自動応答・アクセシブルなファイル形式（タグ付きPDF、テキスト代替）を必須にする。WCAGやバリアフリー要件を運用に組み込む。
- プロダクト設計：古い「FAX文化」を放置せず、受信側での変換フローやログを整備して紙主体の運用リスクを減らす。受給者のデジタル・インクルージョンを設計要件に。
- 個人ユーザー：重要書類はデジタルでバックアップし、正当な理由で電子提出が拒否された場合は記録を残して問い合わせる。障害者支援団体やデジタル窓口の相談を活用する。

--- 
原文：Robert Kingett, "The 'Paperwork Flood': How I Drowned a Bureaucrat Before Dinner" (Sightless Scribbles)
