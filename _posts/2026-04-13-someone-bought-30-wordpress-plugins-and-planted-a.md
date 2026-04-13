---
layout: post
title: "Someone Bought 30 WordPress Plugins and Planted a Backdoor in All of Them - 30のWordPressプラグインが買収され全てにバックドアが仕込まれた"
date: 2026-04-13T18:43:44.680Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://anchor.host/someone-bought-30-wordpress-plugins-and-planted-a-backdoor-in-all-of-them/"
source_title: "Someone Bought 30 WordPress Plugins and Planted a Backdoor in All of Them."
source_id: 47755629
excerpt: "30プラグイン買収でバックドア、wp-config注入とSEOスパム"
image: "https://anchor.host/wp-content/uploads/2026/04/wordpress-plugin-supply-chain-attack-1.webp"
---

# Someone Bought 30 WordPress Plugins and Planted a Backdoor in All of Them - 30のWordPressプラグインが買収され全てにバックドアが仕込まれた
「あなたのサイトも狙われているかも」——買収で生まれた“供給連鎖型”バックドアの実態

## 要約
フリーの人気WordPressプラグイン群が第三者に買収され、作者の最初のコミットでPHPのシリアライズ型バックドアが差し込まれた。8か月後に悪用され、複数サイトで隠れたSEOスパムやリダイレクトが配信された。

## この記事を読むべき理由
プラグインの所有権移転は日本でも増えるM&A・マーケットプレイス利用と直結するリスクです。個人や中小の運用チームが被害に遭いやすく、対応手順を知らないと被害が拡大します。

## 詳細解説
- 何が起きたか：開発元「Essential Plugin」名義で管理されていた30以上のプラグインが、Flippaで買収された後に悪意あるコードが挿入された。WordPress.orgは検出後に一括でプラグイン閉鎖・強制更新を実施したが、wp-config.phpへ注入されたペイロードは自動修正されなかった。
- 技術のキモ：
  - 悪用された手口はPHPのunserialize()を使うリモートRCE。攻撃者が返すデータ内に関数名や引数を入れ、任意実行させる設計（匿名関数呼び出しの任意実行）。
  - プラグイン内に未認証の REST エンドポイント（permission_callback: __return_true）が追加され、外部からの命令受信を可能にしていた。
  - マルウェアはwp-config.phpに大きなPHPブロックを追記。Googlebotにだけ見せるSEOスパムを配信し、所有者には気づかれにくい隠蔽がなされていた。
  - コマンド&コントロール(C2)のドメイン解決にEthereumスマートコントラクトを利用。ブロックチェーン経由でC2を更新できるため従来のドメイン差し止めが効きにくい。
- タイムライン要点：バックドアは2025年8月リリースのバージョンで仕込まれ、2026年4月に武器化。植え付けから検出まで8か月間の猶予があった。

## 実践ポイント
- まず確認：使っているサイトで該当プラグイン（記事に挙がっているスラッグ群）を検索する。
- wpos-analyticsを探す：プラグインディレクトリ内に「wpos-analytics」フォルダがあれば要注意。
- wp-config.phpをチェック：require_once ABSPATH . 'wp-settings.php'; の行と同じ行に不審な追記がないか。ファイルサイズが通常より約6KB大きい場合は感染の可能性が高い。
- 即時対応：該当プラグインを無効化・削除するか、信頼できるパッチ版を適用。単に強制更新されただけではwp-config.phpの注入を除去できない。
- 復旧と精査：感染が疑われる場合はクリーンなバックアップから復元し、管理者パスワードとAPIキーを全てローテーション。外向き通信のログや不審なRESTコールの痕跡を調査する。
- 予防策：所有権変更があったプラグインはソース差分を必ずレビューし、マーケットプレイスで買収履歴・公開情報をチェックする運用ルールを組織化する。

この記事は、プラグイン買収という“信頼の承継”がそのまま攻撃ベクトルになり得る点を警告します。まずは自分のサイトのプラグイン一覧とwp-config.phpを今すぐ確認してください。
