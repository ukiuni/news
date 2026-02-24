---
layout: post
title: "Manjaro website off-line again due to lapsed certificate - Manjaroのサイトが再びオフライン（証明書失効）"
date: 2026-02-24T21:44:59.414Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://distrowatch.com/dwres.php?resource=showheadline&story=20140"
source_title: "Manjaro website off-line again due to lapsed certificate"
source_id: 47141385
excerpt: "Manjaro公式サイトが証明書切れで閲覧不能、公式ミラー確認を。"
---

# Manjaro website off-line again due to lapsed certificate - Manjaroのサイトが再びオフライン（証明書失効）
Manjaro公式サイトがまたダウン：証明書の更新漏れで生じる混乱と、今すぐできる対処法

## 要約
2026年2月24日、Manjaroの公式サイトがHTTPS証明書の期限切れでオフラインになりました。過去にも2015年・2022年に同様の事象が起きており、自動更新の失敗が原因と見られます。

## この記事を読むべき理由
証明書切れは初心者でも体感できる「サイトに入れない」問題を引き起こします。日本のManjaroユーザーや検討中の人が影響範囲を判断し、安全に行動するために知っておくべき基本と実用的対処法を短くまとめます。

## 詳細解説
- なぜ起きるか：多くの配布サイトはHTTPS証明書（例: Let's Encrypt）を約90日ごとに自動更新します。自動化スクリプトやネットワーク障害、設定変更で更新が失敗すると期限切れになります。  
- 影響範囲：主に公式サイトの閲覧やダウンロードページにアクセスできなくなる、ブラウザが接続を警告する、公式情報に辿り着けないといった影響。既にセットアップ済みのシステムのパッケージ更新が直ちに停止するかはリポジトリやミラーの状態次第です。  
- 前例：同様の証明書失効は2015年・2022年にも発生しており、プロジェクト運営側の自動化監視が切り口となることが多いです。

## 実践ポイント
- まずブラウザでアクセスし、証明書エラーか確認する（エラーメッセージをスクリーンショットで保存）。  
- サイトの証明書期限を端末で確認する（例）:
```bash
# 証明書の有効期限を確認
echo | openssl s_client -servername manjaro.org -connect manjaro.org:443 2>/dev/null | openssl x509 -noout -dates
```
- 公式のSNSやフォーラムで運営のアナウンスを確認（Twitter/Forum/IRCなど）。  
- パッケージ更新に不安がある場合は、公式ミラーを確認・切替えるか、mirrorsが使えるなら速やかにミラー経由で更新する：
```bash
# Manjaroでミラーを更新して高速ミラーを使う例
sudo pacman-mirrors --fasttrack && sudo pacman -Syu
```
- 怪しい代替ダウンロードや非公式ビルドは避け、公式復旧を待つか信頼できるミラーを利用する。

短期的な影響は主に情報入手性ですが、継続的な運用・信頼性のためにプロジェクト側の自動更新監視の重要性を改めて意識しておくと良いでしょう。
