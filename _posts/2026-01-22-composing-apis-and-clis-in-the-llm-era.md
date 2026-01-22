---
layout: post
title: "Composing APIs and CLIs in the LLM era - LLM時代のAPIとCLIの“合成”"
date: 2026-01-22T23:59:04.311Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://walters.app/blog/composing-apis-clis"
source_title: "The best code is no code: composing APIs and CLIs in the era of LLMs"
source_id: 46722074
excerpt: "Restishとoauth2cでOpenAPI＋シェルを組合せ、LLMでコードほぼ不要の運用を実現"
---

# Composing APIs and CLIs in the LLM era - LLM時代のAPIとCLIの“合成”
シェルでつなげば「コードを書かない」自動化が現実になる — LLMとCLIで作る可搬性の高い運用パイプライン

## 要約
LLMに対してAPI仕様（OpenAPI）やシェルコマンドを「実行可能なプログラム」として与え、Restishやoauth2cのような既存ツールで解釈・実行することで、独自のクライアントコードをほとんど書かずに強力な自動化を実現する手法を紹介する。

## この記事を読むべき理由
日本のプロダクト開発／SRE現場でも、SaaSやクラウドAPIの運用自動化が求められる中、保守コストを下げつつ人間とLLMの両方にフレンドリーな「シェル中心の設計」が即効性のある実戦解になるため。

## 詳細解説
- 二つの設計選択：  
  1) LLMに細粒度ツールを直接渡してツール呼び出しさせる方法。  
  2) モデルに使えるシェルコマンドを教え、exec_bash的にコマンド列を発行させる方法。記事は後者を推す。理由は「コマンド合成（パイプ）」があることでトークン節約、スクリプト化、対話実行が容易になるため。

- OpenAPIを「プログラム」と見なす：  
  SaaSが公開するOpenAPI仕様をそのまま実行できるインタプリタ（Restish等）を使えば、APIごとのラッパーを手書きする必要が大幅に減る。Restishはエンドポイントをサブコマンドとして露出し、補完も生成する。

- 認可フローの外部化：  
  OAuth 2.0等の認可は「パラメータ群＝プログラム」とみなし、oauth2cのような汎用クライアントで実行する。結果として数百行のカスタムコードがシンプルなパイプに置き換わる。

- macOSキー チェーンの実用トリック：  
  長期リフレッシュトークンを安全に保存するため、security CLIで格納時に -T "" を指定するとデフォルトの呼び出しアプリ参照が外れ、読み出し時にデバイスパスコード/生体認証が要求される。例：
  ```bash
  # トークン保存（例）
  security add-generic-password -s google-api -a my-account -w "$REFRESH_TOKEN" -T ""
  ```

- API仕様がない場合：  
  ブラウザでの操作をHARで保存し、HAR→サニタイズ→LLMに渡してクライアントコード（Python等）を生成させるワークフローで非公開APIを逆エンジニアリングする実例がある。

## 実践ポイント
- まずRestishでOpenAPIを読み込ませ、実際にCLIで叩いてみる。  
  ```bash
  restish api configure cool-api https://api.example.com/openapi.yaml
  restish cool-api --help
  ```
- 認可はoauth2cに外注して、トークンはパイプで渡す。  
  ```bash
  oauth2c "https://accounts.google.com/..." | restish google drive-files-list
  ```
- macOSではキー チェーン保存に -T "" を使い、読み出し時にパスコードを要求させる。  
- OpenAPIが無いサービスはHAR取得→sanitizer→LLMによりクライアントを自動生成して試す。  
- 生成したパイプラインはスクリプト化し、CIや運用ドキュメントに組み込む。権限・監査・トークン寿命は必ず運用ルールを定義すること。

以上を試すことで、日本のチームでも「最小限の自作コード」でLLMと人的操作が両立する堅牢な自動化パイプラインを構築できる。
