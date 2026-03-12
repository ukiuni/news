---
layout: post
title: "Iranian Hacktivists Strike Medical Device Maker Stryker and Wiped Systems - イランのハクティビストが医療機器メーカーStrykerを攻撃、システムをワイプ"
date: 2026-03-12T14:37:05.666Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.zetter-zeroday.com/iranian-hacktivists-strike-medical-device-maker-stryker-in-severe-attack-that-wiped-systems/"
source_title: "Iranian Hacktivists Strike Medical Device Maker Stryker in &quot;Severe&quot; Attack that Wiped Systems"
source_id: 47350578
excerpt: "イランのハクティビストが医療機器大手Strykerをワイプ攻撃、世界の病院が危機に"
image: "https://www.zetter-zeroday.com/content/images/size/w1200/2026/03/Screenshot-2026-03-11-at-12.30.48---PM-1.png"
---

# Iranian Hacktivists Strike Medical Device Maker Stryker and Wiped Systems - イランのハクティビストが医療機器メーカーStrykerを攻撃、システムをワイプ
世界中の病院を止めかねない衝撃――医療機器大手Strykerを狙った「ワイプ攻撃」の全貌

## 要約
海外報道によれば、医療機器メーカーStrykerがグローバルなサイバー攻撃を受け、ログイン画面の改ざんや多数の端末・サーバのワイプ（消去）、データ持ち出しが主張されています。攻撃は「Handala」と名乗るハクティビストによるとされ、被害は広範囲に及んでいる可能性があります。

## この記事を読むべき理由
医療機器は生命に直結するため、製造・管理側のサイバー事故は診療継続性や供給チェーン、国防分野にも波及します。日本企業や病院が取り得る対応やリスク管理の教訓を短時間で掴めます。

## 詳細解説
- 攻撃の性質：報道では「ワイパー（破壊型マルウェア）」が用いられ、OSのリセットや端末の初期化指示が配信され、ログインページが改ざんされたとされます。ワイパーは復旧が難しく、バックアップが無ければ復元不能になることが多いです。過去の代表例に2012年のShamoon（サウジ石油会社）、2014年のSony攻撃などがあります。  
- 侵害経路と影響：報告では管理者アカウントの奪取や、端末管理（Intune等）に介入された可能性が示唆されています。これにより社内アプリやメール、二要素認証（スマホ経由）の利用が阻害され、業務が全面停止したとする投稿がありました。  
- 規模と主張：ハッカー側は数十万台や50TBのデータ流出を主張していますが、これらは現時点で完全には確認されていません。Stryker側は「Windows環境でのグローバルなネットワーク障害」を認め、復旧作業中としています。  
- 背景（政治的動機）：攻撃グループは報復を理由に主張しており、国家間対立や軍事支援がサイバー標的の動機になる例が増えています。医療機器メーカーが軍向け契約を持つ場合、リスクが高まる点は注目に値します。

## 実践ポイント
- 早急対策：疑いを確認したら影響範囲のネットワーク隔離、管理者権限のロックダウン、外部接続の遮断を優先。  
- 認証対策：管理者アカウントはハードウェアトークン等の堅牢なMFAへ切替え、電話ベースの2FAだけに依存しない。  
- バックアップと復旧：オフライン・不変（immutable）なバックアップを複数地点で保有し、定期復旧テストを行う。  
- エンドポイント管理：MDM/EDRの設定確認、リモートワイプ設定とその誤用リスクを含めた運用ルールを整備。  
- 事業継続計画（BCP）：医療系顧客や取引先への代替手順、手動業務フロー、緊急連絡網を整える。  
- 情報共有：サプライチェーンを含む関係者へ迅速に状況を共有し、所管の当局や業界団体と連携する。

（注）本件は続報が出る可能性があります。技術的詳細や被害規模は今後の公式発表で確認してください。
