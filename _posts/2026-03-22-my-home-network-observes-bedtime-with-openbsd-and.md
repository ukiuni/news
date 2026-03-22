---
layout: post
title: "My home network observes bedtime with OpenBSD and pf - 自宅ネットワークが就寝時間を守る仕組み（OpenBSD + pf）"
date: 2026-03-22T15:45:15.122Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ratfactor.com/openbsd/pf-gateway-bedtime"
source_title: "My home network observes bedtime with OpenBSD and pf - ratfactor"
source_id: 1022313832
excerpt: "OpenBSDとpfで夜間に自宅の全接続を自動遮断し、必要端末だけ例外許可する手順と運用ノウハウを解説"
---

# My home network observes bedtime with OpenBSD and pf - 自宅ネットワークが就寝時間を守る仕組み（OpenBSD + pf）
就寝時間に自動で家庭のインターネットを遮断し、必要なサーバーだけ夜間に例外を許可する――OpenBSDのpfで実現する“就寝モード”の作り方

## 要約
OpenBSDをルーターにしてpfのテーブルとアンカー機能を使い、スケジュールで自宅ネットワークのインターネット接続を自動的に遮断／復帰する仕組みを作る手順とコツを紹介する。

## この記事を読むべき理由
家庭のルーターをソフトウェアで制御することで、子どもの利用制限や夜間メンテの共存、ローカルDNSでの邪魔ドメイン遮断（Pi‑hole類似）などが低コストかつ透明に実現できる。日本でも手軽なミニPCや中古機で導入可能で、既存の商用機器より学びやすく拡張性が高い。

## 詳細解説
- ハードウェア選定  
  - RealTek系のNICはOpenBSDで問題が出ることがあるため、Intel系NIC搭載の小型PC（例：Qotom Q305p）を推奨。低消費電力でファンレス機種が家庭用に向く。
- 基本セットアップ（参考：OpenBSD Handbook）  
  - 役割：DHCP(dhcpd)、NAT/pf、DNSキャッシュ(unbound)、IPフォワーディングを構成。  
  - まずはOpenBSDの安定版をインストールし、Handbookの「Build a Simple Router and Firewall」を踏襲する。
- pfの設計方針  
  - デフォルトは「block all」。日中はDHCPで払い出された端末全体からの接続を許可し、就寝時は例外リストのみ許可する。  
  - 主要要素：2つのテーブル（<leased_ips> = dhcpd管理、<bedtime_exempt> = 手動管理）と「anchor」によるルール差し替え。
- テーブル連携  
  - dhcpd側で払い出しIPをpfのテーブルに自動登録：/etc/rc.conf.local に dhcpd_flags="-L leased_ips" を設定。  
  - 例外テーブルはテキストファイル(no_bedtime.txt)で管理し、pfctlで置換する：  
    ```sh
    # 例外テーブル更新
    pfctl -t bedtime_exempt -T replace -f no_bedtime.txt
    ```
- アンカー（anchor）でルールを差し替え  
  - 起動時は「awake」ルール（pass from <leased_ips>）をアンカーに入れておき、就寝時間でアンカーのルールを丸ごと差し替える。
  - アンカー差し替えは即時反映され、文法エラーなら安全に弾かれる。
- 接続状態（state）の強制切断  
  - pfは既存コネクションをstate tableで保持するため、就寝 enforcement 時は該当ネットワークのstateを削除する必要がある。例：  
    ```sh
    # ネットワークのstateを削除（例: 10.0.0.0/24）
    pfctl -k 10.0.0.0/24
    ```
  - 現状、テーブル差分だけを指定してstateだけ殺す簡易な方法は難しく、スクリプト側で差分計算するかラベルによる工夫が必要。
- 自動化と運用スクリプト  
  - 著者は "bedtime" スクリプトを作成し、enforce / lift / update-table / 情報表示 のサブコマンドで運用。cronでスケジューリングして自動化。  
  - Cron例：  
    ```sh
    # 毎日22:30に就寝開始、05:30に解除
    30 22 * * * /home/dave/bedtime enforce
    30 5  * * * /home/dave/bedtime lift
    ```
- バックアップと再現性  
  - 設定ファイルをまとめてGitリポジトリに保存する update-repo.sh を用意。設定散逸を防ぎ、別機への移行も簡単にできる。
- 運用上の注意  
  - TCPは制御しやすいが、UDP/ICMPは例外が必要になる場合がある（ボイスチャットやゲーム等）。運用中に必要な例外を逐次追加すること。
  - ルーター変更やNIC種別の違いでトラブルが出るため、先にテスト環境で動作確認するのが安全。

## 実践ポイント
- ハード選び：Intel NIC搭載のファンレス小型PCを選ぶ（RealTekは避ける）。  
- まずHandbookの「Simple Router」を構成してからpf改造に入る。  
- dhcpd_flags="-L leased_ips" でDHCP→pfテーブル連携を有効化。  
- no_bedtime.txtで例外を管理し、pfctl -t … -T replace -f で更新する。  
- アンカーを使って「日中」と「就寝」のルールを切り替え、就寝時は pfctl -k でstateを切る。  
- スクリプト化（enforce/lift/update-table）してcronで自動化、設定はGitでバックアップする。  

興味があれば、元記事のリポジトリ（pf-bedtime）を参照して実際のpf.confやbedtimeスクリプトを確認すると再現が早い。
