---
layout: post
title: "My PostgreSQL database got nuked lol - PostgreSQLデータベースが吹っ飛んだ lol"
date: 2026-03-12T14:24:44.004Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://akselmo.dev/posts/they-broke-my-server/"
source_title: "My PostgreSQL database got nuked lol"
source_id: 824479418
excerpt: "Dockerの公開ポートと無防備VPSでPostgresが乗っ取られデータ消失—即防御方法を解説"
---

# My PostgreSQL database got nuked lol - PostgreSQLデータベースが吹っ飛んだ lol
驚愕の教訓：夜中に消えた個人サービス、原因は「Dockerのポート公開」と「無防備なVPS」だった

## 要約
フィンランドの開発者が自宅VPSで動かしていたLinkhut派生サービスのPostgreSQLが外部から改ざんされ、データが消失。原因はDockerで公開されたポートと弱い認証、そしてファイアウォール未導入。

## この記事を読むべき理由
自分でVPSやDockerを触る日本の個人開発者やスタートアップにとって「いつか起きるかもしれない」実務的な落とし穴とその対策が凝縮されているため、手元の運用を見直す良いきっかけになります。

## 詳細解説
- 何が起きたか：開発者はDockerコンテナでPostgresを動かしており、ポート公開設定を明示していなかったためホスト上でポートが外向けに開いていた。加えてデフォルトの認証（postgres:postgres）を使っていたため、夜間にボットがスキャンして侵入・テーブルを書き換え・データ消失に至った。
- Dockerの挙動：docker run / docker-composeでportsを指定すると、明示的にlocalhostバインドしない限り0.0.0.0で公開されることがあり、ホストのiptablesやネットワーク設定に影響を与える場合がある（外部から到達可能になる）。
- 環境の脆弱性：VPSにUFWなどのホストファイアウォールが入っておらず、全ポートが開いていた。これがスキャンやボットの標的になった主因。
- 攻撃の特徴：自動化ボットは夜間に一斉スキャンを行い、脆弱なDBに書き込みを残すことがよくある（データ盗難より破壊・身代金要求メッセージを置くケース）。

## 実践ポイント
- docker-composeで明示的にループバックにバインドする：
```yaml
# yaml
services:
  db:
    image: postgres
    ports:
      - "127.0.0.1:5432:5432"
```
- ホスト側ファイアウォールを必ず導入（UFW例）：
```bash
# bash
sudo apt update && sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
# postgresを外部公開しない場合は不要なポートを許可しない
```
- DB認証は強力なパスワードに変更し、初期値を使わない。
- 不要ならポートマッピング自体をやめて、アプリとDBを同一Dockerネットワーク内で通信させる（外部公開を避ける）。
- 定期バックアップを取り、運用監視（ログ、ポートスキャン、fail2banなど）を導入する。
- 設定変更後にnmap等で外部から見えていないかを確認する。

以上を実践すれば、同様の「夜間にデータが消えた」悲劇は大幅に減ります。
