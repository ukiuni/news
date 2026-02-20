---
layout: post
title: "FBI says ATM 'jackpotting' attacks are on the rise, and netting hackers millions in stolen cash - FBIが警告：ATM「ジャックポッティング」攻撃が急増、ハッカーは数百万ドルを着服"
date: 2026-02-20T12:29:42.941Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://techcrunch.com/2026/02/19/fbi-says-atm-jackpotting-attacks-are-on-the-rise-and-netting-hackers-millions-in-stolen-cash/"
source_title: "FBI says ATM &#039;jackpotting&#039; attacks are on the rise, and netting hackers millions in stolen cash | TechCrunch"
source_id: 437054312
excerpt: "ATMが数分で現金を大量吐き出す新手口、あなたの地域も標的に"
image: "https://techcrunch.com/wp-content/uploads/2026/02/atm-cash-machine-1236158262.jpg?resize=1200,800"
---

# FBI says ATM 'jackpotting' attacks are on the rise, and netting hackers millions in stolen cash - FBIが警告：ATM「ジャックポッティング」攻撃が急増、ハッカーは数百万ドルを着服
魅力を引く見出し：日本のATMも他人事ではない――現金を瞬時に吐き出す「ジャックポッティング」が再び猛威

## 要約
FBIの報告によると、ATMを物理的・ソフト的に奪取して現金を大量に吐き出させる「ジャックポッティング」攻撃が2025年に700件超、被害額は2,000万ドル以上に達した。主に物理鍵の悪用とPloutusのようなマルウェアが使われている。

## この記事を読むべき理由
日本は世界でも現金利用が根強く、コンビニや銀行のATMは日常インフラ。海外で増える手口は日本の金融機関・ATM運営者、店舗オーナー、セキュリティ担当者にとって対策優先度の高いリスクを示している。

## 詳細解説
- 手口の概要：攻撃者はまずATMへの物理的アクセスを取得（正規のフロントパネル鍵や共通鍵を悪用）し、内部のハードディスクやUSBポートからマルウェアを植え付ける。マルウェアはATMのOS（多くはWindows）上で動作し、XFS（金融端末でハードウェアを統合するAPI）を悪用して現金払出し装置を直接制御する。  
- 代表的なマルウェア：PloutusはXFSを通じてATMを制御し、顧客口座を操作せずに「即金化」させる点が特徴。攻撃は数分で完了し、検出が遅れやすい。  
- 歴史的背景：2010年にセキュリティ研究者Barnaby JackがBlack HatでATMから現金を吐き出させる実演を行ったことが話題になり、その手法は「実験」から犯罪ビジネスへと進化した。  
- 検出の難しさ：顧客口座に異常が出ないため、通常の不正送金検知では見逃されやすく、物理的被害発生時点で初めて発覚するケースが多い。

## 実践ポイント
- 物理保護を強化：フロントパネル鍵の管理厳格化、共通鍵の廃止・交換、カメラとセンサーで不審な開閉を検知。  
- OS・ソフト更新：ATMのOS（Windows系）の定期パッチ適用、XFSやベンダーソフトの最新化。  
- ポート制御と暗号化：USB/シリアルなど外部接続の制限、内部ストレージのフルディスク暗号化。  
- ログと異常検知：払出し指示の不自然なパターンや短時間大量出金を監視するアラート設定。  
- 教育と連携：店舗スタッフへの不審者対応教育、インシデント発生時の警察・金融当局への迅速な報告ルート整備。  

海外の調査は「手口が成熟し、短時間で大金を抜き取る」ことを示しています。日本の現場でも物理＋ソフト両面の見直しを急ぎましょう。
