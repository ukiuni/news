---
  layout: post
  title: "go.sum Is Not a Lockfile - go.sumはロックファイルではない"
  date: 2026-01-06T00:59:36.326Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://words.filippo.io/gosum/"
  source_title: "go.sum Is Not a Lockfile"
  source_id: 1289033893
  excerpt: "go.sumは検証用のチェックサムで、依存解釈はgo.modを信頼せよ"
  image: "https://assets.buttondown.email/images/9dee32df-d645-4828-a59b-63c73524e3af.jpg"
---

# go.sum Is Not a Lockfile - go.sumはロックファイルではない
誤解だらけのgo.sum：依存解析で「見てはいけない」ファイルを切り分ける

## 要約
go.sumはロックファイルではなく、モジュール版とそのハッシュを保持するローカルなチェックサムキャッシュに過ぎない。依存関係の解決やビルドのバージョン決定で参照すべきはgo.modだ。

## この記事を読むべき理由
多くの開発者がgo.sumを解析して依存グラフを作ろうとしているが、それは誤りで、結果として誤った依存把握やセキュリティ判断につながる。日本のCI運用やサプライチェーン対策を行う現場では特に重要な区別だ。

## 詳細解説
- go.sumの役割  
  go.sumは「モジュールバージョン -> 暗号ハッシュ」のマップで、Go Checksum Databaseと連携してモジュールの内容整合性を検証するためのローカルキャッシュ。バージョン解決に影響を与えないため、外部で解析して依存グラフ作成に使うべきではない。

- go.modが唯一のソース・オブ・トゥルース  
  go.modは直接・推移的な依存を含め、メインモジュールをビルドするために使われる正確なバージョンを記録する（Go 1.17以降）。これがmanifestとlockfileの両方の役割を兼ねる設計で、他言語で見られる「manifest + lockfile」モデルと異なる。

- コマンドと挙動の注意点  
  - goコマンドの-modフラグ: modでは欠落を自動追加、readonlyでは変更をエラーにする。go mod tidyやgo getはデフォルトでmod、他の多くはreadonlyをデフォルトとする。  
  - go list -m allは全モジュール（ビルドに寄与しないものも含む）を出力するため、依存の把握には向かない。go list -f '{{.Module}}' all はローカルのビルド制約（GOOS/GOARCH）を適用する。cmd/go外でgo.sumを解析するユースケースは基本的に無い。

- セキュリティと実務的意味合い  
  go.sumはChecksum Databaseと組み合わせることで、ダウンロード経路に依存せず同じコンテンツであることを保証するための仕組み。CIなどのエフェメラル環境で透明性を確保する点で重要だが、これはセキュリティ目的であり、バージョン解決の意味論には関係しない。

## 実践ポイント
- 依存解析やバージョンの真偽を確認するときはまずgo.modを読む。  
- go.sumは「整合性チェック用のキャッシュ」と理解し、外部ツールで依存グラフ作成に使わない。  
- 依存をJSONで扱いたければ次を使う：
```bash
# go.modのJSON表現を得る
go mod edit -json
# 全モジュールを一覧（注意：ビルドに寄与しないものも含む）
go list -m all
```
- 再現性の高いビルドを目指すならビルドやCIで-mod=readonlyを適用し、依存の自動追加は意図的に行う。  
- ライブラリ設計ではオプションパッケージで依存を分離すると、利用者側のトランジティブトラストを減らせる（例：AWS SDKのサブパッケージ設計）。

短くまとめると、go.sumは検証のための鍵であって、依存「決定表」ではない。依存の解析／運用はgo.modを基点に行う習慣をつけると安全で分かりやすくなる。
