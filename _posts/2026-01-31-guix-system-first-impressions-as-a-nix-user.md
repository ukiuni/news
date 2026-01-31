---
layout: post
title: "Guix System First Impressions as a Nix User - Guix System：Nixユーザーの第一印象"
date: 2026-01-31T11:38:17.242Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nemin.hu/guix.html"
source_title: "Guix System First Impressions as a Nix User"
source_id: 1126144744
excerpt: "Nixユーザーが3日で判明したGuixの強みとミラー・GPU・チャネル運用の落とし穴を具体解説"
---

# Guix System First Impressions as a Nix User - Guix System：Nixユーザーの第一印象
魅力的なタイトル: 「Nixの次はこれ？Guixを3日間触ってわかった“宣言型Linux”の現実と落とし穴」

## 要約
NixユーザーがGuix System（Schemeベースの宣言的ディストリ）を試した初期感想。インストーラは素直だが、ミラー速度、GPUドライバ周り、チャネル/更新フローの違いで泥沼化する可能性あり。

## この記事を読むべき理由
Nixに興味がある日本のエンジニアやハッカーにとって、Guixが持つ思想的共通点と運用上の差分――特に「Guile/Schemeでの設定」「ユーザ毎のguix実行環境」「非自由ソフトの扱い（Nonguix）」は実務で直面しやすく、導入前に知っておくべき情報だから。

## 詳細解説
- 背景：GuixはNixと同じ“宣言的”な仕組みをとるが、言語はNix式→Guile Schemeへ。システム定義をコードで管理する点は共通で、再現性や環境分離が得られる。
- インストーラ：Ncurses系のシンプルなTUIでKDE Plasmaが公式選択肢に追加されるなど進化。だがインストール時のパッケージ取得が遅く、現状ミラー選びで体感が大きく変わる。
- 更新／実行モデルの違い：Nixと異なり、guixはユーザーごとにインストールされる実行系があり、単に`guix pull`しただけでは全ユーザー／システムが即座に新バージョンを使うわけではない。システム構成変更は`guix system reconfigure /etc/config.scm`が必要。
- GPU/ドライバ問題：GNU方針でlinux-libre（非非自由ファームウェア）を優先するため、最新GPU（例：RTX 50xx系）はNouveauでは動かない場合がある。Nonguixチャネル（非自由パッケージ集）を有効化してプロプライエタリドライバを導入する手段はあるが、古いISOやチャネル設定の取り扱いミスでブート不能やカーネルパニックになるリスクがある。
- チャネル運用とミラー：Guixのチャネル設定は~/.config/guix/channels.scmや/etc/guix/channels.scmで管理。古いイメージはSavannahを参照して遅くなるため、Codebergミラーへの切替やチャンネル導入手順を正しく行う必要がある。

例：Nonguixをチャネルに追加する基本形（参考）
```scheme
;; scheme
(cons* (channel
        (name 'nonguix)
        (url "https://gitlab.com/nonguix/nonguix")
        (introduction
         (make-channel-introduction
          "897c1a470da759236cc11798f4e0a5f7d4d59fbc"
          (openpgp-fingerprint
           "2A39 3FFF 68F4 EF7A 3D29 12AF 6F51 20A0 22FB B2D5"))))
       %default-channels)
```

## 実践ポイント
- まずはVMで試す：ハードウェア依存のトラブルを避けるため実機導入前に仮想環境で確認する。
- GPUが怪しいならnomodesetやLXQtなど軽量DEで挙動確認を。Nouveauで動かない場合はNonguixやNVIDIA変換を検討するが、事前バックアップ必須。
- チャネル運用を理解する：`guix pull`だけで終わらない点、ユーザー毎の実行ファイル、`guix system reconfigure`の流れを把握する。
- ミラー/チャネルの設定をチェック：古いISOやデフォルトミラー（Savannah）は遅い。Codeberg等の現行リポジトリに切り替える。
- コミュニティを活用：問題はチャット（#guix）や文書で解決することが多い。英語情報が中心だが、日本でも試行例が増えつつある。

短評：思想的には魅力的だが、ハードウェア周りやチャネル運用の学習コストを許容できるかが導入の分かれ目。
