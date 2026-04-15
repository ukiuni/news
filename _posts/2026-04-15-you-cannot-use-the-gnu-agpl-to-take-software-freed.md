---
layout: post
title: "You cannot use the GNU (A)GPL to take software freedom away - GNU（A）GPLを使ってソフトウェアの自由を奪うことはできない"
date: 2026-04-15T21:04:43.398Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.fsf.org/blogs/licensing/agpl-is-not-a-tool-for-taking-freedom-away"
source_title: "You cannot use the GNU (A)GPL to take software freedom away &mdash; Free Software Foundation &mdash; Working together for free software"
source_id: 1045595414
excerpt: "OnlyOffice騒動が示すAGPL誤用：ロゴ等の追加条件で利用者の自由を奪えない理由"
---

# You cannot use the GNU (A)GPL to take software freedom away - GNU（A）GPLを使ってソフトウェアの自由を奪うことはできない
AGPLを“自由を奪う道具”にしてはいけない――OnlyOffice騒動が教えるライセンス遵守の鉄則

## 要約
FSFは、(A)GPLは利用者の自由を守るためのものであり、追加条件で利用者の権利を制限することは許されないと明確に指摘している。OnlyOfficeの例では「元ロゴを保持せよ」という追加条件がAGPL互換性を損なう可能性が問題になった。

## この記事を読むべき理由
日本でもSaaSやクラウド経由でオープンソースを使うケースが増え、ライセンス誤用は企業リスクや開発者の権利混乱を招く。法律的・実務的観点での注意点を短く押さえておく価値がある。

## 詳細解説
- FSFの立場：FSFはGNU系ライセンスの管理者として、(A)GPLの目的は利用者の「実行・複製・調査・改変・再配布」の自由保護にあると再確認している。  
- 追加条件の扱い：(A)GPLv3は「追加条件」を許容するが、それがライセンスの与える自由を実質的に狭める“さらに制限する条項（further restriction）”なら、受領者はその条項を削除できる。  
- OnlyOffice事例：READMEではAGPLv3と表記しつつ、LICENSEやソースコメントで「配布時に元の製品ロゴを保持せよ」といった条項を追加。FSFはこれがAGPLの許容範囲外の追加制限であり、混乱を招くと批判している。  
- 法的・運用上の帰結：ライセンス表記と実際のLICENSEファイルが矛盾すると、受領者・再配布者の権利が不明確になり、コンプライアンス問題やENforcement（権利行使）で争いが生じやすい。

## 実践ポイント
- ライセンス表記は一貫させる：READMEとLICENSE、ソース内のヘッダを整合させる。  
- 追加条項は慎重に：AGPLの許容範囲を超える制限（例：必須ロゴ保持）を入れない。どうしても必要ならFSFのガイダンスを参照し、別ライセンス表記にする。  
- 受領者としての権利を理解：配布物に「further restriction」があれば、それを削除できる可能性があることを認識する。  
- 企業はコンプライアンス体制を整備：特にクラウド/SaaSでの利用はライセンス確認を調達プロセスに組み込む。  
- 不明点は相談を：FSFやライセンス専門家に問い合わせることで事前対応が可能。

以上。
