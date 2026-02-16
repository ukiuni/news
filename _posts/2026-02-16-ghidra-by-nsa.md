---
layout: post
title: "Ghidra by NSA - Ghidra（NSA製リバースエンジニアリングフレームワーク）"
date: 2026-02-16T15:11:41.600Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/NationalSecurityAgency/ghidra"
source_title: "GitHub - NationalSecurityAgency/ghidra: Ghidra is a software reverse engineering (SRE) framework"
source_id: 47011548
excerpt: "NSA製オープンソースGhidraで即戦力の逆解析環境を無料導入"
image: "https://opengraph.githubassets.com/380741ffea4cb29f969d0e30ee311db99c8a11385f5b302babcf5898f7014565/NationalSecurityAgency/ghidra"
---

# Ghidra by NSA - Ghidra（NSA製リバースエンジニアリングフレームワーク）
NSAが公開した「無料で高機能」な逆アセンブル／逆コンパイル環境──日本の現場で即役立つGhidra入門

## 要約
Ghidraは米NSAが公開したオープンソースのソフトウェア逆解析（SRE）フレームワークで、ディスアセンブル・逆コンパイル・グラフ表示・スクリプト自動化などを備え、Windows/macOS/Linuxで動作します。

## この記事を読むべき理由
サイバーセキュリティ、マルウェア解析、脆弱性調査、あるいは組み込み機器の解析やリバース学習に対し、ライセンス負担なく高機能ツールを導入できる点は日本企業や研究者にとって大きな利点です。

## 詳細解説
- 背景と目的  
  - NSAがスケーリングとチーミング問題を解くために開発し、研究・運用両面で使える拡張性を重視した設計。オープン化により外部コントリビューションが可能。  
- 主要機能（技術的ポイント）  
  - ディスアセンブル／アセンブル、逆コンパイル（高水準言語の復元）、フローチャートや依存グラフ表示。  
  - 多数のプロセッサ命令セットと実行形式に対応。  
  - GUIの対話モードと自動解析バッチモードの両対応。  
  - スクリプト／拡張はJava（主要）とPython（PyGhidra）で作成可能。  
  - 開発者向けにはEclipse用GhidraDevやVisual Studio Code連携を提供（VSCodeでモジュール生成が可能）。  
- ビルドと実行要件（実務的注意）  
  - 実行にはJDK（公式はJDK 21推奨）。開発ビルドはGradle、Python 3.9–3.13、ネイティブコンパイラ（gcc/clang や MSVC）が必要。  
  - 公式配布はプラットフォーム共通のリリースZIPを展開して ./ghidraRun（Windowsは ghidraRun.bat）で起動。PyGhidra用ランナーも同梱。  
  - セキュリティ注意：既知の脆弱性情報があるため、導入前にSecurity Advisoriesを確認し最新版を使うこと。  
- ライセンスとコミュニティ  
  - Apache‑2.0ライセンスで商用利用も可能。GitHub上で多数のコントリビュータと活発なリリースがあるため、日本の現場でも安心して採用・改良が進められる。

## 実践ポイント
- まずは公式リリースZIP＋JDK 21で動かしてUIに慣れる。  
- 自動化や解析の反復はPyGhidraでスクリプト化すると効率的（Python習熟者に敷居が低い）。  
- VSCode連携でスクリプト開発ワークフローを整備（Tools → Create VSCode Module project）。  
- 導入前にSecurity Advisoriesを必ずチェックし、社内ポリシーに従ってサンドボックス環境で評価する。  
- 日本語ドキュメントや社内ナレッジを充実させ、CTFや脆弱性調査でトレーニングに活用することで即戦力化できる。  

Ghidraは「無料で高機能」を実現する実務ツールです。まずは公式リリースで触ってみて、社内の解析ワークフローにどう組み込むかを検討してみてください。
