---
  layout: post
  title: "Show HN: TCP chat server written in C# and .NET 9, used in the terminal - ターミナルで動く C#/.NET 9 製 TCP チャットサーバー"
  date: 2026-01-07T09:22:10.324Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/Sieep-Coding/simple-chat-csharp"
  source_title: "GitHub - Sieep-Coding/simple-chat-csharp: A simple chat server written in C#"
  source_id: 46472047
  excerpt: "端末で動く.NET 9製のシンプルTCPチャットで学べる実践プロトタイプ"
  image: "https://opengraph.githubassets.com/acf0bf411a113a245584bceee3e2c5b78334055e45944ccbd72236a474b682f1/Sieep-Coding/simple-chat-csharp"
---

# Show HN: TCP chat server written in C# and .NET 9, used in the terminal - ターミナルで動く C#/.NET 9 製 TCP チャットサーバー
Linux端末でサクッと動く、学習にも実用プロトタイプにも使えるシンプルなC#チャット — TCPとストリーム処理を.NET 9で体験する

## 要約
.NET 9で書かれた端末ベースのTCPチャット実装。サーバーがポート8000で待ち受け、複数クライアントを受けてメッセージをブロードキャストするシンプル構成で、Message/Userモデルによる構造化データの受け渡しを採用している。

## この記事を読むべき理由
TCPソケットやストリーム処理、クライアント/サーバー設計を実際のコードで学べるため、.NET開発者やネットワーク入門者、日本のスタートアップや社内ツール開発者が短時間でプロトタイプを作る際の良い教材になるから。

## 詳細解説
- 対象リポジトリ: Sieep-Coding/simple-chat-csharp（MITライセンス、スター12）
- 技術スタック: C# / .NET 9。端末（ターミナル）上で動作するクライアント／サーバー構成。
- 動作環境: .NET 9 SDK が必要。Linux/macOS/Windows対応をうたうが、作者はPopOS!（Linux）での動作確認のみ強調。
- 動作概要:
  - サーバーは既定でポート8000をリッスンし、接続されたクライアントからのメッセージを受け取り、他のクライアントへブロードキャストする。リアルタイムログを出力。
  - クライアントは起動時にユーザー名を入力し、メッセージをEnterで送信する。サーバーからのメッセージ受信も端末に表示。
- プロジェクト構成（主要ファイル）:
  - CSharpStream.Server — TCPサーバー実装（接続管理／ブロードキャスト）
  - CSharpStream.Client — クライアント実装（送受信）
  - CSharpStream.Models — Message / User モデル（構造化データ）
  - ChatServer.cs — サービスレイヤー相当
  - Program.cs — コマンドライン引数で client/server を切り替え
- 実行方法（リポジトリREADMEに従う）:
  - サーバー: dotnet run --project CSharpStream server（デフォルトポート8000）
  - クライアント: dotnet run --project CSharpStream client
- 注意点:
  - ファイアウォールやネットワーク制限で接続が拒否される場合がある。サーバーが起動していることを確認すること。
  - Ctrl+Cでクリーンに終了。

## 実践ポイント
- とりあえず動かす（ローカルで確認）:
  - git clone して、.NET 9 SDK を入れ、別ターミナルでサーバーと複数クライアントを起動して挙動を確認する。
  - Example:
```bash
# リポジトリをクローンして実行
git clone https://github.com/Sieep-Coding/simple-chat-csharp.git
cd simple-chat-csharp
dotnet run --project CSharpStream server
# 別ターミナルで
dotnet run --project CSharpStream client
```
- 学習用途の活用案:
  - TCPの基本（接続/切断/ブロードキャスト/ストリームの扱い）を説明するハンズオン教材に最適。
  - Message/Userモデルがあるため、シンプルなプロトコル設計（JSONやバイナリのフレーミング）を実装して比較実験する演習ができる。
- 改良アイデア（実務的に入れる価値が高いもの）:
  - TLS（SSL）で通信を暗号化する（企業内で使うなら必須）。
  - 接続数増加に耐える非同期/スケーラブル実装（async/await、SocketAsyncEventArgs等）へのリファクタ。
  - メッセージのフレーミング（長さプレフィックスやJSON化）とエラーハンドリング強化。
  - systemdサービス化やWindowsサービス化で常時稼働させる運用設計。
  - Terminal.Gui などを使ったTUI化で使い勝手向上。
- 日本市場での活用シーン:
  - 社内チャットの最小プロトタイプや、社内IoT機器のシンプルなメッセージング実験に向く。教育や勉強会で「ネットワークとC#の基礎」を教える教材として採用しやすい。

短時間で「動くもの」として触れて学べるリポジトリなので、.NETでネットワークを学びたい人や、社内ツールのプロトタイプを作りたい日本のエンジニアにはまず触ってみることをおすすめする。
