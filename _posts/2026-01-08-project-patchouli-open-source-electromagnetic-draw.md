---
  layout: post
  title: "Project Patchouli: Open-source electromagnetic drawing tablet hardware - Project Patchouli：オープンソースEMR描画タブレットハードウェア"
  date: 2026-01-08T06:22:00.117Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://patchouli.readthedocs.io/en/latest/"
  source_title: "Project Patchouli Documentation"
  source_id: 46537489
  excerpt: "商用ペンが使える低遅延EMR描画タブレットをオープンソースで自作する方法を解説"
  ---

# Project Patchouli: Open-source electromagnetic drawing tablet hardware - Project Patchouli：オープンソースEMR描画タブレットハードウェア
商用ペンがそのまま使える！低遅延・オープンソースのEMRタブレットを自作する方法

## 要約
Project Patchouliは、コイルアレイ、汎用部品で組むRFフロントエンド、信号処理アルゴリズムを備えたオープンソースのEMR（電磁共鳴）描画タブレット実装で、Wacomなど既存の商用ペンと互換性を持たせることを目指しています。

## この記事を読むべき理由
EMR技術は「バッテリ不要で精度の高いペン入力」を実現する主要技術の一つで、日本のデジタイザ市場（クリエイター向け周辺機器や産業用途）との親和性が高く、自作・研究・製品開発の出発点として実用的かつ学習価値が高いためです。

## 詳細解説
- 技術の全体像  
  EMRはタブレット側のコイルがRFを発生し、ペン内の回路がそれを変調して戻すことで位置・筆圧などを検出する方式です。Project Patchouliはその仕組みをハードウェア（コイル配置・RFフロントエンド回路）とソフトウェア（DSPによる位置推定・データ復号）で再現します。

- ハードウェア構成のポイント  
  - コイルアレイ：位置分解能とスキャン戦略（走査レート、並列化）に直結。  
  - RFフロントエンド（AFE）：市販の部品で組む設計を公開。封止・裏面シールドやフェライト板などの実装ノウハウも記載。  
  - 既存ASICのリバースエンジニアリング情報：Wacom系（W6005S/W6008など）やHanvon、XP-Penなどのペン/コントローラのピン配置・通信プロトコルに関する解析がまとめられており、互換性確保に役立ちます。

- 信号処理とプロトコル  
  - 包絡検出、ピーク外挿（Peak Extrapolation）、物理シミュレーションを用いた位置推定。  
  - ペン⇄タブレットのデータリンク（3-PSKなどの変調方式、フレーミング、圧力・IDの符号化）を解析し、ソフト側で復号する手順が文書化されています。

- プロジェクトの状況と運営  
  - 2024年1月開始、同年3月に小規模プロトタイプを検証、2025年1月にドキュメントをRead the Docsで公開。  
  - ライセンス：ドキュメントはCC BY 4.0、ハードはCERN-OHL-S（強い相互帰属）、コードはGPLv3。商用利用や派生配布の条件はライセンスで確認が必要。  
  - スポンサー：NLnet Foundation（NGI Zero Core Fund）。メンテナはGitLabとDiscordで公開・連絡可能（prj.patchouli@gmail.com）。

## 実践ポイント
- まずはドキュメントを読む：Read the Docsの実装節（コイル設計、AFE回路、DSPアルゴリズム）を順に確認する。  
- リポジトリをクローンしてプロトタイプを試す：小規模コイルと市販部品で動作確認が可能。商用ペン互換性の恩恵を活かし、既存ペンで検証すると開発が速い。  
- 測定環境を準備する：オシロスコープ／ロジックアナライザでRFパルスと復調信号を観測し、包絡検出→ピーク検出→位置推定の流れを追う。  
- ライセンスを確認する：ハードやコードをベースに製品化する際はCERN-OHL-SとGPLv3の条件を事前に把握する。  
- コミュニティ参加：Discordで質問・議論、GitLabでIssue/PRを出して協力することで実装ノウハウが得られる。  
- 日本市場での応用例を考える：教育キット、低コストなデジタイザ端末、IoTや業務機器の手書き入力など、既存の商用ペン対応を活かしたプロトタイピングに向く。

参考リンク：Project PatchouliのRead the DocsドキュメントとGitLabリポジトリを参照。連絡先は prj.patchouli@gmail.com。
