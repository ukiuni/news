---
layout: post
title: "Distraction-Free Writing with the Micro Journal Rev.2 (and Neovim) - Micro Journal Rev.2（と Neovim）で実現する“邪魔されない”執筆環境"
date: 2026-03-27T15:57:51.081Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.ssp.sh/brain/my-distraction-free-typewriter-micro-journal/"
source_title: "Distraction-Free Writing with the Micro Journal Rev.2 (and Neovim)"
source_id: 1222655422
excerpt: "eインク端末とNeovimで通知ゼロの携帯執筆環境を自作する具体ガイド"
---

# Distraction-Free Writing with the Micro Journal Rev.2 (and Neovim) - Micro Journal Rev.2（と Neovim）で実現する“邪魔されない”執筆環境
eインク端末×Neovimで書く――「集中」を取り戻すミニ・タイプライター改造ガイド

## 要約
Micro Journal Rev.2（Raspberry Pi Zero 2W搭載の小型ePaperライター）をNeovim中心にカスタムして、通知やアプリの誘惑を遮断した「持ち運べる執筆環境」を作る試み。キーマップやスイッチ交換、ファイル同期、Wi‑Fi共有スクリプトなどで実用性を高めている。

## この記事を読むべき理由
- 日本でもリモートやカフェ執筆が当たり前になる中で、集中作業用デバイスの具体例と実装ノウハウはすぐ役立つ。  
- 小型ハード＋オープンソースソフトで「書くためだけ」の環境を作る実践アイデアは、ハード改造やEmacs/Vim派にも刺さる。

## 詳細解説
- ハード構成：Micro Journal Rev.2（Un Kyu Lee版）、Raspberry Pi Zero 2W、48キーのオーソリニアキーボード、Akko V3 Pro Creamy Blue（クリック）やKAM Playgroundキーキャップ、18650バッテリ。電源はモバイルバッテリでも可。
- OS/ソフト：Debian系でNeovimをワードプロセッサ化。Vimモーションでの高速移動、分割画面、ファイルのファジー検索、Markdownレンダリング、[[wikilink]]対応などを活用。
- ファイル管理と同期：Rust製ファイラー「yazi」を採用（Rangerより高速）。執筆はMarkdownでGit管理し、ラップトップと同期して継続作業可能に。
- ネットワークと共有：端末単体でホットスポットを立てるbashスクリプトを用意し、スマホと直接ファイル共有（外部Wi‑Fi不要）。
- キーマップ／ファームウェア：QMK/VialでレイヤーやFnキーを定義。キー配列やZ/Y入れ替えなど慣習に合わせたカスタマイズ。書き換え時はUSB接続・ブート挙動に注意（USB‑A→USB‑Cケーブル推奨、SDカード保護のため接続中はしばらく待つ）。
- カスタム＆UX：テーマ切替（屋外での明るさ用）、スプラット画面で参考資料と作業領域を分割、スペルチェックON/OFFで執筆モード切替など、端末の「制限」を逆手に取った設計。

## 実践ポイント
- NeovimをMarkdown向けワードプロセッサにする：textwidth・conceal・markdownプラグイン（glowやnvim-markdown）やFZF/telescopeで快適化。  
- Gitで執筆管理：ローカル→リモートの同期フローを作れば移行がスムーズ。  
- ファイル共有は簡易APで完結：以下のようなシンプルなスクリプトでホットスポット＋ファイルブラウザを起動できる（要適宜設定）。
```bash
#!/bin/bash
sudo systemctl start NetworkManager.service
sleep 5
sudo nmcli device wifi hotspot ssid microjournal password microjournal ifname wlan0
filebrowser -r ~/microjournal/documents -a 0.0.0.0 --noauth > /dev/null 2>&1
```
- キーボード改造：好みのスイッチ／キーキャップに交換し、QMK/Vialでレイヤー割当て。書き換え時はSDカード破損を避けるため接続後しばらく待つこと。  
- 省エネ設計：ePaperの利点を活かし、通知や常駐アプリを排除して「書くことだけ」に最適化する。

軽量・移動性・集中力を重視するなら、Micro Journal Rev.2のアプローチは試す価値があります。興味があれば、Neovim設定例やVialでのキーマッピング手順を別途まとめますか？
