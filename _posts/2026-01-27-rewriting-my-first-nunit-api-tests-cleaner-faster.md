---
layout: post
title: "Rewriting My First NUnit API Tests: Cleaner, Faster, Better - 初めてのNUnit APIテストを作り直す：よりクリーンに、速く、賢く"
date: 2026-01-27T08:18:29.637Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/m4rri4nne/rewriting-my-first-nunit-api-tests-cleaner-faster-better-24fa"
source_title: "Rewriting My First NUnit API Tests: Cleaner, Faster, Better - DEV Community"
source_id: 3199958
excerpt: "NUnit＋C#でRestSharpと設定分離を使い、APIテストを高速かつ保守容易に再設計する方法"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F9hv6dgjlmax4t8h94k62.png"
---

# Rewriting My First NUnit API Tests: Cleaner, Faster, Better - 初めてのNUnit APIテストを作り直す：よりクリーンに、速く、賢く

魅力的タイトル: 古いテストを“作り直す”だけで劇的改善 — NUnit＋C#で作る再現性の高いAPIテスト設計

## 要約
古くなったNUnit＋C#のAPIテストを、リクエスト抽象化・バリデーション分離・設定管理で再設計し、可搬性・保守性・CI適性を高める手順を紹介する。

## この記事を読むべき理由
- 日本の開発現場でも多い「Postman→コード化」や「テストが肥大化して保守できない」問題に直接効く具体策が得られる。  
- CI／ローカル双方で安全に機密を管理する実践パターンが学べる。

## 詳細解説
- リクエスト層の抽象化：RestSharpを使い、GET/POSTなどを汎用ジェネリックメソッドにまとめることで、エンドポイントごとの重複を排除。結果、テスト自体は意図（検証）に集中できる。
- 非同期化：テストをasyncにしてHTTP待ちを正しく扱い、並列実行やタイムアウト制御に強くする。
- レスポンス検証の分離：チェックロジック（例：CheckBodyResponse）を別クラスに切り出し、複数テストで再利用・一箇所修正で済むようにする。
- 設定と機密管理：.runsettings（ローカル）と環境変数（CI）を切り替えるTestConfigパターンで、APIキーやURLをコードから分離して安全に運用する。
- 具体的な検証：HTTPステータスコードの厳密なチェック、JSONをエンティティにデシリアライズしてフィールド単位で検証（FluentAssertions推奨）する。

サンプル（要点のみ）：

```csharp
// csharp
public class Requests {
  private readonly RestClient _client;
  public Requests(string baseUrl) => _client = new RestClient(baseUrl);
  public async Task<RestResponse<T>> GetAsync<T>(string endpoint, Dictionary<string,string>? headers = null) {
    var req = new RestRequest(endpoint, Method.Get);
    headers?.ToList().ForEach(h => req.AddHeader(h.Key, h.Value));
    return await _client.ExecuteAsync<T>(req);
  }
  public async Task<RestResponse<T>> PostAsync<T>(string endpoint, object? body = null, Dictionary<string,string>? headers = null) {
    var req = new RestRequest(endpoint, Method.Post);
    if (body != null) req.AddJsonBody(body);
    headers?.ToList().ForEach(h => req.AddHeader(h.Key, h.Value));
    return await _client.ExecuteAsync<T>(req);
  }
}
```

設定読み込みの骨子：

```csharp
// csharp
public static Config GetConfig() {
  bool isCi = Environment.GetEnvironmentVariable("GITHUB_ACTIONS") == "true";
  if (isCi) return new Config { ApiToken = Environment.GetEnvironmentVariable("API_TOKEN") ?? throw new Exception("API_TOKEN") , /*...*/ };
  return new Config {
    BaseUrl = TestContext.Parameters["BaseUrl"] ?? "",
    ApiToken = TestContext.Parameters["ApiToken"] ?? ""
  };
}
```

## 実践ポイント
1. まずRequestsクラスでHTTP呼び出しを1箇所に集約する。  
2. レスポンス検証はCheckクラスへ切り出し、FluentAssertionsでフィールド単位の保証を行う。  
3. .runsettingsをローカルで使い、CIでは環境変数を使うTestConfigを実装する（.runsettingsは.gitignoreへ）。  
4. 各テストはasync Taskで書き、ステータスコード＋ボディ内容を両方アサートする。  
5. 機密（APIキー等）は決してリポジトリにコミットしない。CIシークレット管理を活用する。

短時間で効果が出る手順は「抽象化→分離→設定管理」の順。まずは1〜2のリファクタから始めると改善が実感しやすい。
