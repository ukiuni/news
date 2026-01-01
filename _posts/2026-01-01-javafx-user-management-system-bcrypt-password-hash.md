---
layout: post
title: "JavaFX User Management System – BCrypt Password Hashing (Part 6) - JavaFX ユーザ管理システム — BCrypt パスワードハッシュ（パート6）"
date: 2026-01-01T06:38:11.970Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=LDD1Kan7tOI&amp;t=4s"
source_title: "JavaFX User Management System – BCrypt Password Hashing (Part 6)"
source_id: 473904310
excerpt: "JavaFX×MySQLでBCrypt導入、UI凍結回避と実務向け安全保存を解説"
---

# JavaFX User Management System – BCrypt Password Hashing (Part 6) - JavaFX ユーザ管理システム — BCrypt パスワードハッシュ（パート6）
最短で「安全なパスワード保存」を実装する：JavaFX と MySQL で実務レベルの認証を組み込む方法

## 要約
JavaFX のユーザインターフェースと MySQL を組み合わせ、BCrypt を用いてパスワードを安全にハッシュ・保存・検証する実装を解説する。UI の凍結を避ける非同期処理や DB 保存時の注意点も含む。

## この記事を読むべき理由
日本の開発現場でも、社内システム・業務アプリ・スタートアップのユーザー認証は必須。簡単に見落としがちな「ハッシュ化の正しい運用」「UI の応答性」「DB 側の型設計」など、実装で直接役立つポイントを短時間で押さえられる。

## 詳細解説
- BCrypt の基本と利点  
  - BCrypt は内部でソルトを生成し、計算コスト（work factor）を指定できるためレインボーテーブルや単純な辞書攻撃に強い。ハッシュ文字列は通常 60 文字前後（例: $2a$12$...）で、ソルトはハッシュに含まれるため別途保存不要。
  - 設定例：コスト 10〜12 が一般的。サーバー性能に応じて調整する。

- Java での実装（ライブラリ）  
  - jBCrypt や Spring Security の BCryptPasswordEncoder がよく使われる。API はシンプルで、生成と検証はワンライナーに近い。

- UI（JavaFX）における注意点  
  - BCrypt は意図的に CPU 集中型。UI スレッドで実行するとアプリが固まるため、Task / ExecutorService でバックグラウンド実行する。処理中はボタン無効化やスピナー表示を行う。
  - パスワード入力は PasswordField を利用し、クリップボードへの不要なコピーを避ける。

- DB（MySQL）側の設計と安全策  
  - ハッシュ保存列は CHAR(60) または VARCHAR(60)。平文は絶対に保存しない。  
  - PreparedStatement を使い SQL インジェクションを防ぐ。DB 接続は TLS/SSL を有効化する。  
  - パスワードリセットはワンタイムトークン（期限付き・ハッシュ化保存）を用いる。メールトークンの運用では短い有効期限と使い捨て設計を採る。

- 運用上の追加対策  
  - ブルートフォース対策：ログイン失敗回数で一時ロック、CAPTCHA、IP レート制限。  
  - コスト引き上げのためのリハッシュ戦略：ユーザがログインした際にハッシュのコストが古ければ再ハッシュして更新する。  
  - より先進的な選択肢として Argon2 もあるが、現行のエコシステムや互換性を考慮して選定する。

## 実践ポイント
- ハッシュ生成と検証の最小コード（jBCrypt 使用例）:
```java
// java
String hashed = BCrypt.hashpw(plainPassword, BCrypt.gensalt(12));
boolean ok = BCrypt.checkpw(inputPassword, hashed);
```
- JavaFX で UI を固めないサンプル（Task 利用）:
```java
// java
Task<String> task = new Task<>() {
  @Override protected String call() {
    return BCrypt.hashpw(plainPassword, BCrypt.gensalt(12));
  }
};
task.setOnSucceeded(e -> { String hash = task.getValue(); /* DB 保存 */ });
new Thread(task).start();
```
- DB 保存時の注意点: カラムは CHAR(60)、PreparedStatement を使う。例:
```java
// java
String sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
  ps.setString(1, username);
  ps.setString(2, hashed);
  ps.executeUpdate();
}
```
- 運用チェックリスト（短め）
  - ハッシュコストをドキュメント化し、定期的に見直す  
  - 平文やパスワードをログに出さない  
  - DB 接続に TLS を使う、最小権限の DB アカウントを用いる  
  - パスワードリセットは短期トークン＋検証済みメールで実装

## 引用元
- タイトル: JavaFX User Management System – BCrypt Password Hashing (Part 6)  
- URL: https://www.youtube.com/watch?v=LDD1Kan7tOI&t=4s
