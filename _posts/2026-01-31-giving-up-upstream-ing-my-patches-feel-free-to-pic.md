---
layout: post
title: "Giving up upstream-ing my patches & feel free to pick them up - パッチの上流取り込みを断念、自由に引き継いでください"
date: 2026-01-31T20:16:29.811Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mail.openjdk.org/pipermail/hotspot-dev/2026-January/118080.html"
source_title: "Giving up upstream-ing my patches &amp; feel free to pick them up"
source_id: 46835454
excerpt: "OCA審査長期停滞で上流断念、Zero/llvm/Loongson向け有用パッチを公開"
---

# Giving up upstream-ing my patches & feel free to pick them up - パッチの上流取り込みを断念、自由に引き継いでください
「レビューが止まったら、あなたが引き継いでください」——OpenJDK貢献で起きた現実的な問題提起

## 要約
OpenJDKにパッチを出そうとした投稿者が、OCA（Oracle Contributor Agreement）の審査が1年以上進まず、上流取り込みを断念。小さな有用パッチ群を公開して「好きに拾ってください」と宣言しています。

## この記事を読むべき理由
貢献フロー（CLA/OCA）やビルド周りの小修正は、エコシステムの健全性に直結します。日本のディストリビュータや組み込み系・ローカルフォーク運用者にも影響するため、手元で再利用・適用できる知見になります。

## 詳細解説
- 経緯：投稿者（xtex/Bingwu Zhang）は2025年1月にOpenJDKに関わり始め、OCA提出後に追加情報を求められたものの、その後問い合わせを繰り返しても1年以上レビューが滞ったため、上流取り込みを断念したという告知メール。
- 問題意識：投稿者は中国本土在住で、米国の輸出管理や制裁に触れるような契約関係はないと主張。審査が長引くなら明確に拒否してほしい、という要望を出しています。
- 技術的内容（主なパッチ）
  - llvm-config の壊れ検出チェック：ビルド時にllvm/clangの設定が壊れているケースを検出するスクリプト的修正（ビルド安定化）。
  - Zero VM向けのスレッドスタック既定サイズ拡張：JDK 24をZeroビルドするとjavacでスタックオーバーフローが発生する問題を回避するための既定スタックサイズ増加（Zeroはインタプリタ向けの軽量VM、クロスビルドや一部アーキで使われる）。
  - Loongson向けフォーク用パッチ群：Loongson（中国系CPU）向けのアーキ依存修正も含まれ、上流でブロックされたためフォーク側で管理されている。
- 公開状況：投稿者はGitHub上にコミット／PR一覧を挙げており、パッチ自体は参照可能（元メールに複数リンク／コミットハッシュあり）。

## 実践ポイント
- パッチを引き継ぐ方法
  1. 同じ変更を「原著作物でない形で」書き直せばOCAの署名問題を回避できる（投稿者の明言）。または自分でOCAを提出して上流へ出す。
  2. まずはローカルでZeroビルド＋javacテストを再現し、スタックサイズ調整の効果を検証する（ビルドログと再現手順を添えてPRを出すと通りやすい）。
  3. llvm-configチェックはビルドスクリプト（configure／configure.ac等）に組み込む形でテストを追加すると貢献が通りやすい。
- 組織的対応案（日本のプロジェクト向け）
  - 自社やOSSディストリに当該パッチを一時採用（フォーク）して運用し、将来的に上流へ再提案する。
  - OCAや審査に関する遅延が続く場合、メーリングリストやコミュニティで透明性を求める（build-dev / hotspot-dev 等）。
- リンク参照：元投稿にはコミットやPRの一覧（llvm-configチェック、Zeroスタック修正、Loongson PR群）が挙がっています。興味があれば該当リポジトリをクローンして内容を確認してください。

以上。興味があれば、特定のパッチ（llvm-config のチェックや Zero スタック変更）の差分を要約して紹介します。
