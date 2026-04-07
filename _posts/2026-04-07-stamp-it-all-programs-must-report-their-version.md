---
layout: post
title: "Stamp It! All Programs Must Report Their Version - すべてのプログラムはバージョンを報告せよ"
date: 2026-04-07T01:18:46.774Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://michael.stapelberg.ch/posts/2026-04-05-stamp-it-all-programs-must-report-their-version/"
source_title: "Stamp It! All Programs Must Report Their Version"
source_id: 1281910374
excerpt: "ビルドにVCSハッシュ等を埋めて実行中バイナリを即特定し障害対応を劇的短縮せよ"
---

# Stamp It! All Programs Must Report Their Version - すべてのプログラムはバージョンを報告せよ
全てのビルドに「版スタンプ」を埋め込み、実行中の実体が何なのか即座に分かるようにしておけば、障害対応で失う時間を劇的に減らせます。

## 要約
ビルドにVCSリビジョンやビルド日時などの「スタンプ」を入れ、実行中プロセスが何を動かしているかを簡単に報告できる仕組み（Stamp it! Plumb it! Report it!）を全プロジェクトに導入せよ、という提言。

## この記事を読むべき理由
障害対応やユーザサポートで「何が動いているか分からない」状況は致命的。日本の開発・運用チーム（オンプレ、クラウド、組み込みまで）でも、簡単な仕組みの導入でデバッグ時間と人的コストを大幅に削減できます。

## 詳細解説
- バージョン表記の粒度は用途で変わる（例: 製品名／メジャー／フルバージョン／VCSコミット）。トラブル時は最も詳細な識別子（VCSハッシュ＋リリース日時）が有効。  
- i3の事例：`i3 --version`で基本情報、`i3 --moreversion`で「実際に動いているプロセスのバイナリ、ロードされた設定ファイルと最終更新時刻、PID」など実稼働情報を返す。これがあると「ビルドして配置したつもり」と「実際に動いているもの」が一致しているか即確認できる。  
- VCSリビジョンの埋め込みは最も有益：誰がどのコミットを動かしているかが確定できる。  
- Goの扱い：Goはビルド時に情報を埋める手段（リンク時に変数を書き換える、あるいは runtime/debug.ReadBuildInfo でモジュール情報を読む）がある。Nixのような再現性重視のビルド環境では、デフォルト設定だとVCS情報が抜けることがあるため、ビルドレシピで明示的にリビジョンを渡す必要がある。作者はNix用のオーバーレイやビルド情報注入の回避策を示している（概念的には「ビルド時に git rev を渡す」）。

- Nix固有のポイント：Nixストアのパスはハッシュ付きでビルド識別に便利だが、ビルド中にVCS情報を埋めるにはfetchGitやオーバーレイで明示的に情報を渡すか、ビルドステップで -ldflags 等を使うのが現実的。

簡単なGo例（ビルド時にversionを注入）:
```go
package main

import "fmt"

var version = "dev"

func main() {
    fmt.Println("version:", version)
}
```
ビルド例（bash）:
```bash
go build -ldflags "-X main.version=1.2.3+abc123" ./...
```

## 実践ポイント
- 全アプリに --version（簡易）と可能なら --moreversion（実行中の実体や設定も返す）を実装する。  
- スタンプ内容に最低限含めるもの：製品名、フルバージョン、VCSリビジョン（短縮不可）、ビルド日時、ビルドパス/パッケージID、ビルド者またはCI識別子。  
- Go：runtime/debug.ReadBuildInfo を試す／ビルド時に -ldflags で埋める。  
- Nix：fetchGit やビルドオーバーレイで git rev を渡す、あるいはビルドレシピ内で明示的にstampする。  
- 運用フローに組み込み：監視アラート・障害対応手順書に「まず該当ホストで --moreversion を取得する」を入れる。

小さな変更で障害対応が格段に楽になります。まず1プロジェクトから「Stamp it! Plumb it! Report it!」を始めてください。
