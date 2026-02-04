---
layout: post
title: "I prefer to pass secrets between programs through standard input - プログラム間の秘密は標準入力で渡すのが好き"
date: 2026-02-04T12:39:54.774Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://utcc.utoronto.ca/~cks/space/blog/programming/PassingSecretsViaStdin"
source_title: "Chris&#39;s Wiki :: blog/programming/PassingSecretsViaStdin"
source_id: 1165557985
excerpt: "stdin/stdoutで秘密を安全に受け渡す具体的手法と注意点"
---

# I prefer to pass secrets between programs through standard input - プログラム間の秘密は標準入力で渡すのが好き
シェルで「秘密」を安全に受け渡す、最も手軽で堅実なワザ

## 要約
コマンドライン引数や環境変数に秘密を載せると露出リスクがあるため、旧来のUnix流である標準入出力（stdin/stdout）やファイル記述子を使ってプログラム間で秘密を渡す方が安全で実用的、かつSSH越しにも簡単に拡張できる。

## この記事を読むべき理由
日本の現場でもシェルスクリプトや簡易な自動化で「動的に生成される秘密（ワンタイムトークン、APIキー、パスフレーズなど）」を扱うことが多く、簡便で安全な受け渡し手法を知っておくと事故や情報漏洩を減らせます。

## 詳細解説
- 問題点：コマンドライン引数はps等のプロセス一覧で見え、環境変数は/procや外部ツールで参照可能。これらは秘密の漏洩経路になり得る。  
- 解決策：秘密を標準出力で出して、別プロセスの標準入力で読む（パイプ）。ファイルを置かないので一時ファイルの管理やパーミッション問題も減る。  
- シェル上の注意点：
  - 変数をexportすると環境に入るので秘密はexportしない。
  - echoは多くのシェルでbuiltinなので比較的安全だが、printfが外部コマンドだとコマンド引数に現れるケースを注意。
  - 文字集合や改行に注意し、必要ならbase64などでエンコードして送受信する。  
- 複数項目を渡す場面では「とても小さなプロトコル（順序、区切り、長さ指定等）」を決めると安全に扱える。  
- マシン間の転送：passwordless SSHが使える環境なら、パイプをそのままssh経由で繋げられる（provide | ssh remote consume）。  
- ファイル代替：bashのプロセス置換（<(...)）や/dev/fdを使えば、ファイルを要求するプログラムに対しても「ファイルを使っているように見せかけて」stdin経由で渡せる。  
- 限界と代替：LinuxのキーリングやD-Busのような仕組みを別途使う手もあるが、動的でスクリプト主体のワークフローではstdin経由が最も汎用的で実装コストが低い。

## 実践ポイント
- 絶対にコマンドライン引数やexportで秘密を渡さない。  
- 可能なら秘密は標準出力で生成し、受け側は標準入力で受け取る。例：
```bash
# bash
provide-secret | consume-secret
# 遠隔で
provide-secret | ssh remote consume-secret
```
- 改行やバイナリを含む可能性があるときは base64 でエンコード／デコードする。  
- 複数データを渡す場合は newline や長さ付きヘッダなどの小さなプロトコルを決める。  
- 外部コマンドを不用意に使わず、できるだけシェルのbuiltinで済ませる（外部プロセス化による露出リスク低減）。

短く言えば、面倒に見えても「stdin/stdout と小さなプロトコル」を採ればスクリプト中心の現場で安全かつ実用的に秘密を扱えます。
