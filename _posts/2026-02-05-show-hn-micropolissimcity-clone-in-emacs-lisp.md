---
layout: post
title: "Show HN: Micropolis/SimCity Clone in Emacs Lisp - Emacs Lispで作られたSimCity風クローン"
date: 2026-02-05T10:36:55.087Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/vkazanov/elcity"
source_title: "GitHub - vkazanov/elcity: A simple SimCity clone in Emacs Lisp"
source_id: 46897332
excerpt: "Emacs上で遊べるSimCity風ElCity：純粋コア×ASCII UIで学べる都市育成"
image: "https://opengraph.githubassets.com/bab95e43f1fd3f6d91ce0f5543626c24061c7ba2c5cd115526452547946ba1e4/vkazanov/elcity"
---

# Show HN: Micropolis/SimCity Clone in Emacs Lisp - Emacs Lispで作られたSimCity風クローン
Emacsの中で動く“ちいさなSimCity”を遊びながら学べる――ターミナルEmacs向けのASCII都市シミュレーション

## 要約
Emacs Lispで書かれたターン制の都市開発ゲーム「ElCity」。UIはASCIIで端末Emacsに最適化、ゲーム本体は「純粋なコア（pure core）／命令の殻（imperative shell）」設計を採用しています。

## この記事を読むべき理由
- Emacs愛好家や軽いゲームで学習したい日本の開発者に最適。  
- 「関数型コア＋手続き的UI」という設計が小規模プロジェクトでどう効くか、実例で学べます。

## 詳細解説
- 言語／要件: Emacs Lisp、Emacs 30.1+（Easkは任意）。  
- アーキテクチャ: シミュレーション部分は決定論的で純粋。UIはレンダリングと入力処理を担う分離設計。これによりデバッグしやすく自動テストが書きやすい。  
- ゲームロジック（主なルール）: ターン制。ターン進行で収入は $ \text{Funds増加} = \frac{\text{Population}}{2} + (\text{Commercial level} + \text{Industrial level}) $（要旨）。  
  - City Hallは道路接続の起点で唯一で、取り壊せない。  
  - 道路はCity Hallとつながって初めて“接続”と判定。  
  - 発電所はマンハッタン距離6タイルを供給。  
  - ゾーン（住宅/商業/工業）は電源と道路隣接で毎ターン成長、条件喪失で減衰。最大レベルは3。  
- 操作: R/C/Iでゾーン選択、rで道路、p発電所、h市役所、nでターン進行、矢印でカーソル、oでオーバーレイ切替、uでundo 等。  
- マップ: 行文字列のリストでカスタム起動可能（例: "H=R0", "...."）。トークンは .., ~~ , == , PP , HH , R0..R3 など短縮形も可。  
- 開発ワークフロー: make run（起動）、M-x elcity-start、make test（ERTテスト）、make lint、バイトコンパイルなど。プロジェクト構成は core/UI/tiles/maps に分離。

## 実践ポイント
- すぐ試す（use-package例）:
```emacs-lisp
(use-package elcity
  :load-path "/path/to/elcity"
  :commands (elcity-start))
;; 起動: M-x elcity-start か プロジェクトルートで make run
```
- 学習用途: 「純粋なコア／命令の殻」パターンを試す教材に最適。状態管理を分離してユニットテスト（ERT）を書く練習ができる。  
- 日本向け活用案: 社内勉強会・新人研修のハンズオン教材、Emacsユーザーイベントでのデモ、UIローカライズやタイル追加による拡張演習に向く。

元リポジトリ: https://github.com/vkazanov/elcity
