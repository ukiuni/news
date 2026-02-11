---
layout: post
title: "Go - Unit & Integration Testing - Go のユニット＆統合テスト"
date: 2026-02-11T21:00:27.928Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.linkedin.com/pulse/go-unit-integration-testing-callum-willcocks-q0mse/?trackingId=SAMFUE8FQpiV%2BVsNzwEeeA%3D%3D"
source_title: "Go - Unit &amp; Integration Testing"
source_id: 445305876
excerpt: "GoのDIとモック＋testcontainersで高速ユニットと本番近似統合テストを実践できる手順"
image: "https://media.licdn.com/dms/image/v2/D4E12AQGY-FKiklWHkQ/article-cover_image-shrink_720_1280/B4EZxIBOS5K8AI-/0/1770734807163?e=2147483647&amp;v=beta&amp;t=IhKSpUoZkhAFqw-zuNQ13g-r_kUpCVqVqgFouVJMP08"
---

# Go - Unit & Integration Testing - Go のユニット＆統合テスト
魅力的なタイトル: 実務で効く！Goで学ぶユニットテストと統合テストの実践ガイド

## 要約
Goでのテストの基本（ユニット／統合）と、インターフェース＋依存性注入で「差し替え可能な実装」を作りモックで単体テスト、testcontainersで統合テストを回す実践手法を解説します。

## この記事を読むべき理由
テストは品質とコスト削減に直結します。特にGoプロジェクトではインターフェース設計と依存性注入がテスト容易性を大きく左右するため、日本のチームがCI/本番品質を高めるうえで必須の知見です。

## 詳細解説
- ユニットテスト vs 統合テスト  
  - ユニットテスト：関数やメソッド単位で外部依存（DB, API）をモックして高速・独立に検証。  
  - 統合テスト：実際のDBや外部サービスと連携して、システム間の協調を検証（例：Postgresコンテナを使う）。

- インターフェースと依存性注入（DI）  
  - Goのインターフェースは暗黙的。実装を差し替えられる設計（例：UserRepositoryインターフェース）にすることで、テスト時にモック実装を注入できる。  
  - コントローラは interface 型を受け取ることで、実運用のDB実装／テスト用のインメモリ実装を簡単に切り替え可能。

- モックの作り方（例）  
  - インメモリ map を内部に持つ mockUserRepository を用意し、AddUser／FindUser／DeleteUser を実装してテスト用の振る舞いを提供する。  
  - HTTPハンドラは CreateRouter(userRepository) のように DI しておき、httptest.NewRecorder() でハンドラの動作を検証する。

- 統合テスト：testcontainers を利用  
  - testcontainers-go で Postgres コンテナを立ち上げ、実際の DB に対してリポジトリを動かす。これによりマイグレーションや SQL 実行の動作確認が可能。

- よく使うライブラリ  
  - テスティング：github.com/stretchr/testify（assert/require）  
  - Web：github.com/gin-gonic/gin  
  - コンテナ：github.com/testcontainers/testcontainers-go（postgres モジュール含む）

- 短いコード例（ユニットテスト）  
```go
// go
func TestMultiplyInteger(t *testing.T) {
    got := MultiplyInteger(7, 2)
    if got != 14 {
        t.Fatalf("expected 14, got %d", got)
    }
}
```

## 実践ポイント
- まずはインターフェースを設計する（例：UserRepository）。実装は隠蔽してDIで注入する。  
- ユニットテストは外部依存をモックで完全に置き換え、高速で回せる状態に。  
- 統合テストは testcontainers を導入し、CI でコンテナを立ち上げて本番に近い検証を行う。  
- 必要なパッケージ（最小例）:
  - go get github.com/gin-gonic/gin@v1.10.1
  - go get github.com/stretchr/testify@v1.11.1
  - go get github.com/testcontainers/testcontainers-go@v0.40.0
- CI（GitHub Actions/GitLab CI）では、ユニットは常時、統合テストは必要時（または nightly）に実行する運用が現実的。

この流れを取り入れれば、ローカル開発とCIで安定したテスト基盤を持てます。
