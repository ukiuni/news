---
layout: post
title: "Releasing rainbow tables to accelerate Net-NTLMv1 protocol deprecation - Net‑NTLMv1プロトコル廃止を加速するためのレインボーテーブル公開"
date: 2026-01-16T23:03:10.430Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cloud.google.com/blog/topics/threat-intelligence/net-ntlmv1-deprecation-rainbow-tables"
source_title: "Releasing Rainbow Tables to Accelerate Protocol Deprecation | Google Cloud Blog"
source_id: 46652617
excerpt: "レインボーテーブル公開でNet‑NTLMv1攻撃が低コスト化、即時廃止と対策を"
image: "https://storage.googleapis.com/gweb-cloudblog-publish/images/03_ThreatIntelligenceWebsiteBannerIdeas_BA.max-2600x2600.png"
---

# Releasing rainbow tables to accelerate Net-NTLMv1 protocol deprecation - Net‑NTLMv1プロトコル廃止を加速するためのレインボーテーブル公開
「放置は即リスクに変わる」──公開されたレインボーテーブルが示すNet‑NTLMv1の“今すぐ直すべき”現実

## 要約
Mandiant（Google Cloudと連携）は、Net‑NTLMv1を狙ったレインボーテーブルを公開し、旧式認証プロトコルの脆弱性をデモンストレーションできるようにした。これにより、従来は高コストだった鍵復元が比較的安価な環境でも現実的になり、速やかな廃止と対策が求められている。

## この記事を読むべき理由
日本企業でもActive Directoryやレガシー認証を使う環境は依然多く、Net‑NTLMv1が残っているとドメイン全体の乗っ取り（最悪はドメインコントローラの資格情報流出）につながる可能性がある。今回の公開は「脆弱性が実際に悪用可能である」ことを示す証拠となり、優先対応の判断材料になる。

## 詳細解説
- Net‑NTLMv1の本質: Net‑NTLMv1は古いチャレンジ／レスポンス型の認証で、既知の平文（known‑plaintext）を使った暗号解析が成立しやすい設計上の弱点がある。研究自体は1990年代からあり、既に実用的な攻撃手法が確立されている。
- レインボーテーブルの役割: レインボーテーブルは時間と記憶領域をトレードオフする事前計算済みの逆引き表で、特定の平文を想定できる場合に鍵の探索を劇的に速める。Mandiantの公開は、これまで高価だった「現場での再現」を低コストで可能にし、脆弱性の実証を容易にしている。
- 危険な攻撃の連鎖: Net‑NTLMv1経由で取得した認証情報は、機械アカウントや高権限アカウントの乗っ取りに使われ得る。特にドメインコントローラ関連の資格情報が奪われると、DCSyncなどを通じた横展開でAD全体が危険にさらされる。
- 公開の意図: 攻撃手法そのものを促進するためではなく、現場の防御側に「手元でリスクを再現して検証・説得」する手段を提供する目的がある。つまり、速やかな移行と監視強化を促す圧力に相当する。

## 実践ポイント
- 今すぐ監査する: AD環境や境界のWindows機でNet‑NTLMv1が使われていないかログ（認証パッケージ情報等）で検出する。使用検出をトリガーに段階的な対応計画を立てる。
- 設定で強制する: グループポリシーまたはローカルセキュリティポリシーで「LAN Manager認証レベル」を「Send NTLMv2 response only」に設定し、NTLMv1の送信を防ぐ（適用前にレガシー機器の影響を確認すること）。
- レガシー互換機器の洗い出しと対策: 古いNASやプリンタ、サードパーティ製ミドルウェアなどでNTLMv1依存が残ることが多い。段階的にアップデート、置換、あるいは専用セグメントへ隔離する。
- 監視とアラート強化: NTLMv1やLMを示すログイベントを検出・集約してアラート化する。認証誘導（coercion）や異常な機械アカウントの利用を監視対象にする。
- 検証と訓練: 管理者やSOCチームで“脆弱性が現実的に悪用可能である”ことを再現（責任あるテスト環境で）し、インシデント対応手順を整備する。

以上を踏まえ、Net‑NTLMv1は「知識と時間さえあれば現場で悪用が可能」な状態である。組織は設定変更・資産棚卸・監視強化を優先し、レガシー認証からの脱却を急ぐべきである。
