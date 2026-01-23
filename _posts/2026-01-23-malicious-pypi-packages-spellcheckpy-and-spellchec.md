---
layout: post
title: "Malicious PyPI Packages spellcheckpy and spellcheckerpy Deliver Python RAT - 悪意あるPyPIパッケージ spellcheckpy と spellcheckerpy が配布する Python RAT"
date: 2026-01-23T19:13:32.334Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.aikido.dev/blog/malicious-pypi-packages-spellcheckpy-and-spellcheckerpy-deliver-python-rat"
source_title: "Malicious PyPI Packages spellcheckpy and spellcheckerpy Deliver Python RAT"
source_id: 419390962
excerpt: "インポートするだけで侵入、偽PyPIが辞書埋込ペイロードでPython RATを展開"
---

# Malicious PyPI Packages spellcheckpy and spellcheckerpy Deliver Python RAT - 悪意あるPyPIパッケージ spellcheckpy と spellcheckerpy が配布する Python RAT

あなたの依存パッケージがバックドアに？Basque辞書に隠された「インポートで起動する」Python RATの手口

## 要約
PyPI上の偽パッケージ spellcheckpy / spellcheckerpy が、辞書データ（resources/eu.json.gz）内に埋め込んだ base64 ペイロードを経由してステージング型の Python RAT（リモートアクセス型マルウェア）を配布。インポート時に実行トリガーを仕込み、ディスクを汚さずに永続的にC2と通信する高度な手口です。

## この記事を読むべき理由
日本でもPython依存が広がる中、typosquatting／パッケージの偽装によるサプライチェーン攻撃は現実的な脅威です。特に企業やOSS利用者は「普通にimportするだけで侵入されうる」ケースを知っておく必要があります。

## 詳細解説
- 偽装手口：攻撃者は正規の pyspellchecker を装い、resources/eu.json.gz（Basque語の辞書）に base64 エンコードされたダウンローダを混入。見た目は正当な辞書データ。
- 初期の“眠った”バージョン：最初のリリースではペイロードを抽出するが exec は呼ばれず“装填のみ”。攻撃者は後のバージョンでスイッチを入れる設計に。
- トリガー実装（v1.2.0）：WordFrequency.__init__ 内に難読化した実行トリガを追加。bytes.fromhex("65786563") が "exec" を復元して動的に実行することで静的検知を回避。Importして SpellChecker をインスタンス化するだけで発動。
- ステージ構成：
  - ステージ1：辞書から復元した downloader を実行し、https://updatenet[.]work/settings/history.php からステージ2を取得。subprocess.Popen(..., start_new_session=True) により親プロセス終了後も生き残る（メモリ上実行、ファイル非作成）。
  - ステージ2（RAT）：環境フィンガープリント取得、カスタムバイナリプロトコル（[4B cmd][4B len][XOR payload]）、二層XOR（16バイトキー + 0x7B）で通信を難読化、コマンドID 1001 で受信コードを exec。5秒間隔で Beacon（https://updatenet[.]work/update1.php）を送信し、SSL検証は無効化。
- インフラと関連性：C2ドメイン updatenet[.]work はCloudzy/RouterHostingのIP（172.86.73.139）を利用。過去の同様キャンペーン（spellcheckers 等）と手口が一致し、同一アクターの可能性あり。

## 実践ポイント
- まず確認・除去：
  - pip list / pip freeze で spellcheckerpy / spellcheckpy がないか確認。あれば即アンインストール：pip uninstall spellcheckerpy spellcheckpy
- 監査と防御：
  - 依存関係は署名・作者確認・ハッシュ固定（pip hash / lockfile）で厳格化。
  - SCAツールで typosquatting / 名称類似パッケージを検出するルールを追加。
  - CIでインストール直後に resources/*.json.gz の中身をチェック（base64や異常キーを探す）。
- ネットワーク対策：
  - updatenet[.]work および関連IP（172.86.73.139）をブロックまたは監視。
  - 開発/ビルド環境のアウトバウンド通信を最小化・ホワイトリスト化。
- 検出指標（IOC）：
  - パッケージ名：spellcheckerpy, spellcheckpy（全バージョン）
  - C2：https://updatenet[.]work/settings/history.php, https://updatenet[.]work/update1.php
  - IP/ASN：172.86.73[.]139 (AS14956 RouterHosting LLC / Cloudzy)
  - キャンペーンID：FD429DEABE
  - ペイロード位置：resources/eu.json.gz のキー "spellchecker"
- 個人開発者へ：知らない作者名・GitHubリンクを安易に信用せず、virtualenv と最小権限でテストしてから本番環境へ導入する習慣を。

この記事をきっかけに、依存管理とインストール前の簡易検査（特に辞書やリソース類の中身チェック）をチームの標準に加えることを強く推奨します。
