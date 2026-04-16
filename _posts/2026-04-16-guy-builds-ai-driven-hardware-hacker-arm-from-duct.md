---
layout: post
title: "Guy builds AI driven hardware hacker arm from duct tape, old cam and CNC machine - ダクトテープと古いカメラで作るAI駆動ハードウェア・ハッカーアーム"
date: 2026-04-16T22:15:51.624Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/gainsec/autoprober"
source_title: "GitHub - GainSec/AutoProber: Hardware hacker’s flying probe automation stack for agent-driven   target discovery, microscope mapping, safety-monitored CNC motion, probe review, and   controlled pin probing. · GitHub"
source_id: 47800033
excerpt: "古いカメラとCNCで作るAI駆動の低コスト自動プローバ、家庭工作台で飛行プローブ級の自動検査を実現"
image: "https://opengraph.githubassets.com/4e28f7131da435e59a16afe86c5e884a1f630f920461a19ab6956e788ea9479a/GainSec/AutoProber"
---

# Guy builds AI driven hardware hacker arm from duct tape, old cam and CNC machine - ダクトテープと古いカメラで作るAI駆動ハードウェア・ハッカーアーム
魅力的タイトル: 家庭の工作台が飛行プローブラボに変身する──“AutoProber”が示す低コスト自動化の可能性

## 要約
GitHubのAutoProberは、既存の小型CNC・USB顕微鏡・オシロスコープを組み合わせて、エージェント駆動でターゲット検出→顕微撮影→安全監視付きのプロービングまで自動化するソース公開のスタックです。安全モデルや作業フローを重視した実験向けのリポジトリです。

## この記事を読むべき理由
国内のメイカースペース、大学研究室、ハードウェアセキュリティに関わる初学者〜中級者にとって、「安価なハードウェア資源で何が自動化できるか」を具体例で示す重要なケーススタディだからです。日本の小規模ラボや教育現場での実践導入可能性とリスク管理の参考になります。

## 詳細解説
- 何をするものか：AutoProberは「飛行プローブ（flying probe）」の自動化スタック。ターゲットを検出して顕微鏡画像を撮り、フレームを縫い合わせてマップ化。候補ピンをダッシュボードで承認し、承認後に限定的・監視下でプローブ動作を行う。
- 構成要素：Python制御パッケージ、Flaskベースのシングルページダッシュボード、CADで出力するカスタムツールヘッド、ドキュメント群。リポジトリは apps/, autoprober/, dashboard/, docs/, cad/ 等で整理される。
- ハードウェアスタック（プロトタイプ）：GRBL対応の3018系CNC（USBシリアル）、USB顕微鏡（mjpg-streamer経由）、Siglentオシロスコープ（LAN/SCPI）を安全監視用に利用、光学エンドストップ、3Dプリントのツールヘッド、（任意で）ネットワーク制御コンセント。
- 安全モデルの重視：物理運動を伴うため機械制御として扱う設計。オシロスコープのChannel 4を独立安全エンドストップとして継続監視し、異常電圧・トリガ・CNCアラーム・実機リミットで即停止。自動復帰は行わずオペレータ確認が必須。docs/safety.md と docs/operations.md の順守が強調される。
- ライセンスと責任：PolyForm Noncommercial 1.0.0で非商用利用が許可。商用利用は別途連絡要。リポジトリは「許可された機器・ターゲット」での実験を前提としており、不正利用は禁止。

## 実践ポイント
- まずはドキュメント（docs/safety.md, docs/operations.md, BOM）を読んで、実験環境と法的・倫理的枠組みを確認すること。許可のない対象や他者の機器への使用は厳禁。
- ダッシュボードはローカル・信頼ネットワーク内で運用し、公開ネットワークには接続しない。校内・社内の運用ルールに従う。
- 実機では「顕微鏡→プローブのXYオフセット測定」と「その場で生成したキャリブレーションファイル」が必須。キャリブレーションを別環境で偽装しないこと。
- 部品調達前にリポジトリのBOMとデバイス仕様を確認し、電圧・コネクタ互換性を必ず検証する。
- 教育・研究目的でのアイデア検証やプロトタイピングには有用だが、常に安全監視・手動承認と組み合わせて運用する。

（出典）GainSec / AutoProber — GitHub リポジトリ（PolyForm Noncommercial 1.0.0）
