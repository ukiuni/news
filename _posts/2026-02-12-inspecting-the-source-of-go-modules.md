---
layout: post
title: "Inspecting the Source of Go Modules - Goモジュールのソースを検査する"
date: 2026-02-12T19:42:41.877Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://words.filippo.io/go-source/"
source_title: "Inspecting the Source of Go Modules"
source_id: 1240894619
excerpt: "pkg.go.dev表示と実際のモジュールzipをchecksumで照合し改ざんを検出する方法"
image: "https://assets.buttondown.email/images/0c2a763b-ba3a-4d2c-8ecf-263871d7b4b6.jpeg?w=960&amp;fit=max"
---

# Inspecting the Source of Go Modules - Goモジュールのソースを検査する
pkg.go.devで見ているファイルは“本物”か？GoのチェックサムDBと新しいソースビューアで安全に確認する方法

## 要約
Goのチェックサムデータベース(sumdb)がモジュールの整合性を保証する一方で、GitHubなどのWeb表示は必ずしも“ビルドに使われる実際のソース”を示さない。pkg.geomys.devなどのツールといくつかのコマンドで、正しいソースを確かめられる。

## この記事を読むべき理由
依存ライブラリの供給連鎖攻撃が増える中、表示されているコードが実際のビルドに使われるものと一致しているかを簡単に確認する手順は、開発者・セキュリティ担当者、日本のプロダクトチームにとって必須の知識です。

## 詳細解説
- Go Checksum Database（sumdb）は、モジュール名＋バージョンごとの暗号ハッシュを保存し、世界中のGoクライアントが同じソースを取得していることを保証する仕組み。タグのforce-pushやコードホスティング側の差し替えを検出できる。
- ただし、GitHubのファイルビューは可変なタグやforce-pushの影響を受けるため、Web上の表示と実際のモジュールアーカイブ（proxy や sumdb が参照するzip）が一致するとは限らない。過去にtyposquattingとforce-pushを組み合わせた攻撃が実際に発生している。
- 解決策の一つが、実際にモジュールアーカイブからソースを読むアプローチ。pkg.geomys.dev は proxy.golang.org が持つモジュールzipに対して HTTP Range リクエストを送り、ブラウザ内でアーカイブを展開して該当ファイルだけを表示する。これにより pkg.go.dev 上の「ソース表示」よりも信頼できるビューが得られる（ただし現状は proxy の配布する zip をそのまま信頼しており、sumdb の透明性証明までは検証していない）。
- 透明性証明（transparency log）や proof を検証するなら、dirhash を計算するためにモジュールのzip全体を取得する必要がある。将来的に geomys は proxy の CORS 修正後にオプションで証明検証を実装する予定。
- 開発者向けの実用的なツール：ローカルで確実にそのバージョンのソースを読むなら go mod download -json を使い、返ってきた Dir を参照する。将来的には go mod verify -tag でローカルgitリポジトリとsumdbを突き合わせて検証できる予定。
- 運用上の注意点：GOPROXY=direct を使うと直接git cloneするため攻撃面が増える。proxy.golang.org を使って直接フォールバックを切る（GOPROXY=proxy.golang.org）運用を推奨するケースが多い。

## 実践ポイント
- 実際のソースをローカルで読む（安全な方法）:
```bash
# 例: モジュールのソースディレクトリを取得して移動
go mod download -json filippo.io/age@v1.3.1 | jq -r .Dir
cd "$(go mod download -json filippo.io/age@v1.3.1 | jq -r .Dir)"
```
- pkg.go.dev のソースリンクを信頼せず、手早く確認したいときは URL の go.dev を geomys.dev に置き換えるか、pkg.geomys.dev のブラウザ拡張を使う。
- CI/ポリシー：GOPROXY を proxy.golang.org のみに設定して direct フォールバックを無効にする（攻撃面を減らす）。
- 将来的な追加保証：go mod verify -tag が利用可能になったら、リポジトリのタグ内容と sumdb の内容を突き合わせて検証するワークフローを組み込む。
- 日本の現場では、外部依存の可視化と検証をデプロイ前チェックやセキュリティレビューに組み込むことを検討する（サードパーティ製ライブラリの信頼性確保）。

--- 
元記事著者: Filippo Valsorda（words.filippo.io）
