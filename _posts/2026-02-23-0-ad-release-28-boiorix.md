---
layout: post
title: "0 A.D. Release 28: Boiorix - 0 A.D. リリース28：「ボイオリクス」"
date: 2026-02-23T07:25:23.164Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://play0ad.com/new-release-0-a-d-release-28-boiorix/"
source_title: "0 A.D. | A free, open-source game of ancient warfare"
source_id: 47078112
excerpt: "Boiorixでゲルマン実装＆日本語表示が劇的改善、最新版RTSを体験しよう"
---

# 0 A.D. Release 28: Boiorix - 0 A.D. リリース28：「ボイオリクス」
古代戦争RTSが一段と進化！「ゲルマン」新勢力と日本語表示が劇的に改善された最新版を遊び尽くす

## 要約
オープンソースRTS「0 A.D.」の正式リリース第28弾「Boiorix」が公開。新勢力「Germans（ゲルマン）」追加、動的フォントレンダリング導入、エンジン更新や多数のバランス調整が含まれます。

## この記事を読むべき理由
日本語や東アジア言語の表示が大幅改善され、Hi‑DPIやLinux配布（AppImage/Snap/Flatpak）対応も強化。ゲーム開発やオープンソース貢献に関心がある日本の読者にとって“試す・参加する”価値が高いアップデートです。

## 詳細解説
- リリース名と意味：リリース28「Boiorix」は、紀元前のゲルマン王ボイオリクスに由来。これが象徴するように史実を意識した拡張が中心。
- 新勢力「Germans」：キンブリなどのケルト・ゲルマン連合を再現。移動式経済（Supply Wagons・Wagon Encampments）、固有技術（Wagon Trains, Migratory Resettlement）、強力な攻城ユニットや霊能者ユニットを特色にした半遊牧的プレイが可能。
- UIと表現の改善：
  - Gendered Civilians：市民表示を性別バリエーションに改め、史実に沿った表現（市民＝戦闘可能な市民兵、民衆＝補助民）に整理。ゲームバランスは変更なし。
  - Direct Font Rendering：Freetypeによる動的フォント描画を導入。膨大な文字アトラス不要でメモリ負荷低減、中文・日本語など東アジア文字の標準サポートが容易に。Hi‑DPI対応やフォント差し替えも改善。
- エンジン／プラットフォーム：
  - SpiderMonkey（JSエンジン）をv128へ更新。これにより Windows 7/8.1・古いmacOSは切り捨て。Windows向け64ビットビルド提供開始（次回デフォルト化予定）。
  - Linux向けに公式AppImageを追加。Snap/Flatpakとも連携。
- ネットワーク／安全性：ロビーでTLS証明書検証がデフォルト有効化。今後必須化予定でMITM対策が強化。
- ゲーム性の調整：海戦ユニットのリバランス（火船/矢船強化、衝角/偵察船調整）、群れ移動ロジック改善、各文明の固有バランス調整（例：Carthageの採石ボーナス、Hanの大臣調整、Mauryasのユニット差別化）など多数の細かな改修。
- 開発・コミュニティ：映像編集やSNS運用、ウェブデザインなどの貢献者募集中。翻訳はTransifex経由で参加可能。バグ報告はGiteaへ。

## 実践ポイント
- 今すぐ試す：公式サイトからWindows/Mac/Linux用をダウンロード。既存のMODは更新前に無効化すること。
- 日本語ユーザーへ：Direct Font Renderingで日本語表示が改善されているため、標準版でのプレイを推奨。Hi‑DPI環境でもUI拡大で見やすくなる。
- Linuxユーザー：AppImageで手軽に最新版を試せる。Snap/Flatpakも追って更新予定。
- 貢献方法：翻訳（Transifex）、バグ報告（Gitea）、ドネーションでサーバー維持に協力。動画編集やSNS運用のスキルがあれば即戦力。
- 開発者メモ：SpiderMonkeyアップデートで古いOSサポートが切られたため、ターゲット環境を確認してから導入を。Windowsは64-bit版推奨。

（元記事：0 A.D. Release 28: Boiorix — play0ad.com）
