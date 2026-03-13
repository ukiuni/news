---
layout: post
title: "Plan 9's Acme: The Un-Terminal and Text-Based GUIs - Plan 9のAcme：アンターミナルとテキスト中心GUI"
date: 2026-03-13T04:37:43.338Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.danielmoch.com/posts/2025/01/acme/"
source_title: "Acme: The Un-Terminal | Daniel Moch's Web Home"
source_id: 803084940
excerpt: "設定不要のテキスト中心GUIでCLIと直結し開発効率を劇的に改善"
image: "https://www.danielmoch.com/assets/initials-blue.jpg"
---

# Plan 9's Acme: The Un-Terminal and Text-Based GUIs - Plan 9のAcme：アンターミナルとテキスト中心GUI
驚くほどシンプルで強力な「テキストGUI」──設定地獄から解放される開発体験

## 要約
AcmeはPlan 9由来の「テキストを中心にしたGUI」で、テキスト選択をそのままコマンドにパイプし、出力をウィンドウに戻すことでCLIツールと深く統合するエディタです。9Pプロトコルによる柔軟な外部連携が特徴で、「設定や色テーマで迷う時間」を激減させます。

## この記事を読むべき理由
日本でもVS Codeやターミナル併用が主流になるなか、Acmeの設計思想は「テキスト優先でツールをつなぐ」実践的なヒントを与えます。設定まみれの環境に疲れたエンジニアや、シェル志向のワークフローを洗練させたい人に特に有用です。

## 詳細解説
- 背景：Acmeは1990年代のPlan 9で生まれ、plan9portでUnix系へ移植されました。見た目はGUIだが、動作はテキスト中心で「ターミナルではないターミナル（Un-Terminal）」という位置づけです。  
- テキスト優先の利点：ビットマップを多用する現代GUIと違い、テキストのみだとインターフェースが制約され、共通の操作パターンが生まれやすく学習コストが下がります。  
- コマンドのシームレス統合：任意のテキストを選択して任意のコマンドへパイプでき、出力は新ウィンドウに出すか選択箇所を置き換えられます。これによりエディタが「全ツールのハブ」になります。  
- 9Pプロトコル：Acmeは内部で9Pを使い、ウィンドウや操作をファイル的に公開します。POSIX上ではUnixドメインソケット経由でやり取りでき、ヘルパーはシェルスクリプトでも書けるほどシンプルです。  
- 設定の不在が美点：色テーマや大量のプラグイン、細かい設定を排した設計は長寿命化に寄与。必要ならacme-lspなどの拡張もありますが、デフォルトで「ノブが少ない」体験を提供します。  
- IDEとの比較：従来の「Integrated Development Environment」とは逆方向の「Integrating Development Environment」という概念。VS Codeはターミナル統合で似たアプローチを一部実現していますが、Acmeはより原始的かつ軽量にCLIと結びつきます。

## 実践ポイント
- まずは触ってみる：plan9portを入れてAcmeを起動するか、Russ CoxのAcmeツアー動画を視聴して操作感を掴む。  
- 小さな実験：エディタ内でテキストを選択→例: grep／wc／sed等へパイプして結果をウィンドウへ返す操作を試す。  
- acme-lspを試す：言語サーバ連携が必要ならacme-lspのような拡張を使う。  
- ワークフローの見直し：VS Codeを使う場合でも、ターミナルとテキスト中心の操作を意識して「設定の数」を減らすだけで生産性が上がることが多い。  
- スクリプトで拡張：9P相当の連携が使える環境なら、ヘルパーはまずシェルスクリプトで書いてみると敷居が低い。

出典：Daniel Moch, "Plan 9's Acme: The Un-Terminal and Text-Based GUIs" (2025)
