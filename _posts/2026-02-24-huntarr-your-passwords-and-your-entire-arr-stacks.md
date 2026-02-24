---
layout: post
title: "Huntarr - Huntarr: あなたのパスワードとARRスタック全体のAPIキーがネットワーク上（あるいはインターネット上）で丸見えになる"
date: 2026-02-24T05:59:30.213Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://reddit.com/r/selfhosted/comments/1rckopd/huntarr_your_passwords_and_your_entire_arr_stacks/"
source_title: "Reddit - The heart of the internet"
source_id: 1097101422
excerpt: "Huntarrの脆弱性でARR系の全APIキーとパスが一撃で流出、公開中は即停止"
---

# Huntarr - Huntarr: あなたのパスワードとARRスタック全体のAPIキーがネットワーク上（あるいはインターネット上）で丸見えになる
あなたのメディア環境が一撃で乗っ取られる――Huntarrの致命的な認証欠陥を今すぐ知るべき理由

## 要約
Huntarr（v9.4.2）には認証を迂回する致命的な脆弱性が多数あり、公開されたインスタンスに対して単一のリクエストでSonarr/Radarr/ProwlarrなどのAPIキーやパスワードが平文で取得可能です。

## この記事を読むべき理由
日本でも自宅サーバーやNASで*arr系（Sonarr/ Radarr 等）を運用する人が増えています。Huntarrはそれらをまとめるために使われますが、もし使っている・使おうとしているなら即座にリスクを把握し対策する必要があります。

## 詳細解説
- 致命的な問題点（抜粋）
  - POST /api/settings/general が認証不要で設定を書き換え・全設定（各アプリのAPIキー含む）を返す。1回のcurlで全APIキー取得が可能。
  - 2FAのセットアップが未認証でTOTPシークレットとQRを返す→認証なしで2FAを設定しアカウント乗っ取り可能。
  - POST /api/setup/clear が認証不要でセットアップをリセット→攻撃者がオーナーを置き換え可能。
  - auth/recovery-key/generate が認証を要求しない（400を返すが認証チェックがない）。
  - zipfile.extractall() をそのまま使っておりZip Slipで任意ファイル書き込みが可能。コンテナがroot実行だと致命的。
  - バックアップIDのパス処理にパス・トラバーサル、shutil.rmtree() により任意ディレクトリ削除。
  - X-Forwarded-For を信用してローカルアクセス制限を回避可能。
- 原因の本質
  - auth.py に設定されたホワイトリストが最もセンシティブなエンドポイントをスキップしている（明示的ミス）。
  - コードレビューやPRプロセスが欠如し、自動スキャン／基本的なセキュリティ対策が機能していない。
- 検証方法
  - レビュー者はbandit, pip-audit 等と手動コードレビューで21件（critical/high/medium）を報告。再現スクリプトとCIで検証可能なリポジトリが公開されている。

例：一発で設定ダンプを取るコマンド
```bash
# bash
curl -X POST http://your-huntarr:9705/api/settings/general \
  -H "Content-Type: application/json" \
  -d '{"proxy_enabled": true}'
```

## 実践ポイント
- 今すぐやること（優先度高）
  1. Huntarrをインターネット直結で動かしているなら即停止またはポート遮断（9705等）。外部公開を解除する。  
  2. Huntarr経由で接続しているSonarr/Radarr/Prowlarr等のAPIキー／パスワードを全てローテーション（再発行）し、連携を再設定する。  
  3. コンテナをrootで動かしている場合は停止し、可能ならイメージ削除。  
  4. ログに不審なアクセスや操作がないか監査。侵害の痕跡があればさらに調査・復旧。
- 中期対応
  - Huntarrを代替するか、公式ARRアプリを直接使う。Huntarrを使う場合は修正が公式に入るまで信頼しない。  
  - リバースプロキシで認証を強化（VPNや認証付きリバプロ）、ファイアウォールでアクセス制限。  
  - CIでbandit/pip-audit等の自動スキャンを導入し、コンテナは非root実行に変更。
- コミュニティ／判断
  - プロジェクトに寄付する前に開発・レビュー体制とセキュリティ対応の透明性を確認する。  
  - 同様の問題を見つけたら公開ディスカッションと第三者によるレビューを促す。

短く言うと：Huntarrを公開しているなら即シャットダウンしてAPIキーを回収・再発行し、信頼できる代替か修正が入るまで運用を中止してください。
