---
layout: post
title: "The Holy Grail of Linux Binary Compatibility: Musl and Dlopen - Linuxバイナリ互換性の聖杯：musl と dlopen"
date: 2026-01-26T09:51:29.425Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/quaadgras/graphics.gd/discussions/242"
source_title: "The Holy Grail of Linux Binary Compatibility: musl + dlopen · quaadgras/graphics.gd · Discussion #242 · GitHub"
source_id: 46762882
excerpt: "musl+dlopenでGPU対応の単一静的バイナリがどのLinuxでも動く仕組み解説"
image: "https://opengraph.githubassets.com/03f6c3f9930847a8bc42b21d6f6562c79d9ac5d7ff9fbcd7042c4852cd6d251b/quaadgras/graphics.gd/discussions/242"
---

# The Holy Grail of Linux Binary Compatibility: Musl and Dlopen - Linuxバイナリ互換性の聖杯：musl と dlopen
魅力的なタイトル: どのLinuxでも動く「単一静的バイナリ」を実現する秘密 — musl + dlopen の仕組みと実例

## 要約
Goで作った単一の静的バイナリにGPUアクセラレーションを付けて、glibc ⇄ musl の壁を越えてあらゆるLinux上で動かす手法（musl + dlopen）を紹介します。

## この記事を読むべき理由
コンテナや軽量ディストロ（Alpine、Void musl版など）が増える中、配布用Linuxバイナリがglbic/muslの違いで動作しない問題は現実的な障害です。日本の開発者やゲーム/グラフィクス系アプリ作者が配布の煩雑さを減らすために必読です。

## 詳細解説
- 背景：Goは単一の静的バイナリを簡単に出力でき、配布が非常に楽。しかしGPUやX11/Wayland、OpenGL/VulkanなどはCの動的ライブラリ（dlopen）を通して動作し、これらはlibcに依存する（典型はglibc、対して一部ディストロはmusl）。
- 問題点：glibc向けに作ったバイナリはmusl上で動かない（逆も同様）。muslは静的バイナリでのdlopenを基本的にサポートしない。さらにGoの c-shared / c-archive のmusl対応は不完全で、標準的な方法ではmusl環境でのグラフィクス連携が難しい。
- 回避策の要点：
  1. graphics.gdでは GOOS=musl を新設し、Goランタイムにパッチ（ビルドオーバーレイ）を当ててmusl向けビルドを可能にした。
  2. c-sharedをやめて c-archive 経由でGoコードをGodotにリンクして単一バイナリ化を試行。
  3. 最大のハードルは静的化（-static）時に musl が dlopen を無効にする点。だが dlopen は弱シンボルなので、アプリ側で独自実装を提供できる可能性がある。
  4. 実装アプローチ：小さなネイティブCヘルパープログラムを同梱／生成し、ホストの動的リンカを取り込んでシステムの dlopen を「奪う（steal）」。その後プロセス内で戻り、動的にロードした関数呼び出し時はアセンブリのトランポリンでTLS（Thread-Local Storage）をシステムlibc側に切り替えてから実行する。これにより TLS 実装差（glibc vs musl）による不整合を避ける。
  5. 既存手法との関係：同様の発想は C の detour 技法や Cosmopolitan の dlopen に先例があり、ここではそれを musl 向けに拡張している。
- 結果：musl + dlopen の組合せで、ハードウェアアクセラレーション対応の「単一静的バイナリ」を作成でき、kernel 3.2 以降の多くのLinux上で動作させられる。

## 実践ポイント
- すぐ試すコマンド（graphics.gdベースのプロジェクトで）:
  - GOOS=musl GOARCH=amd64 gd build
  - （新しい musl エクスポートプリセットを追加するために）export_presets.cfg を削除する必要がある場合あり
- 実行環境：ターゲットマシンに gcc が必要（ヘルパーをロードするため）。
- 配布方針：現時点では「glibc用ビルド」と「musl用ビルド」を用意するか、この musl+dlopen アプローチでユニバーサルな単一バイナリを作るかを検討する。コンテナ利用（Alpine 等）が多いサービスや組込み系では musl 対応が重要。
- 参考／試用ビルド：graphics.gd のサンプル静的ビルド（例）を試してみると挙動確認がしやすい（ホストに gcc が必要）。

短くまとめると、musl での dlopen 回避策は「配布の煩雑さを大幅に減らす実用的なトリック」であり、特にコンテナ／軽量ディストロが多い現場では大きな価値があります。
