---
layout: post
title: "Twenty Years Since My First PHP Script - 私の最初のPHPスクリプトから20年"
date: 2026-04-14T04:03:28.890Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://iampavel.dev/blog/twenty-years-since-my-first-php-script"
source_title: "Twenty Years Since My First PHP Script • Asaduzzaman Pavel"
source_id: 362341916
excerpt: "20年越しのPHP失敗から学ぶ、即効で直せる実践的改善点（SQL/パスワード/Git対応）"
image: "https://iampavel.dev/og/twenty-years-since-my-first-php-script.png"
---

# Twenty Years Since My First PHP Script - 私の最初のPHPスクリプトから20年
16歳の“動く”コードが教えてくれた、今すぐ直せる現場の落とし穴

## 要約
著者が16歳で作った掲示板から20年。生のユーザ入力をそのままDBに投げる、平文パスワード、FTPオンリーの運用など当時の失敗から学んだ「実践的改善点」を振り返る話。

## この記事を読むべき理由
日本ではWordPressやレガシーPHPが現役のまま使われ続けています。古いコードや趣味プロジェクトで同じミスを繰り返さないために、最低限押さえるべき安全策と現代の実務ツールを短時間で学べます。

## 詳細解説
- 根本的なミス：ユーザ入力を文字列連結でSQL実行（SQLインジェクション）、パスワードを平文保存、PHPとHTMLの混在、エスケープ不足（XSS）など。セキュリティ概念が無く、攻撃を受けて初めて学ぶパターン。
- 運用リスク：FTPで直接編集、バックアップが記憶頼み。バージョン管理未使用のため、誤上書きで復旧不能になる危険。
- 言語の罠：PHPの古いAPIや関数名の揺れ（mysql_*系、htmlspecialchars/ htmlentities、strposの戻り値仕様など）により初心者がハマりやすい。
- 現代との差分：PHP 8.xやフレームワーク（Laravel/Symfony）、ORM、テンプレート、静的解析（PHPStan/Psalm）、パッケージ管理、Gitなどが揃い、同じ機能を安全に短期間で構築可能。
- マインドセット：完璧を目指すより「作って壊して直す」反復で学ぶべきだが、セキュリティやバージョン管理だけは早期に習慣化すべき、という教訓。

## 実践ポイント
- SQLは準備済みステートメント（PDO）を使う。  
- パスワードは必ずハッシュ化（password_hash／password_verify）。  
- 出力時は適切にエスケープしてXSSを防ぐ。CSRFトークンを利用する。  
- Gitで履歴管理、ローカル→リモートのワークフローを習慣化する。  
- フレームワークやライブラリを使って再発を減らす（Laravelならルーティング・認証が整備済）。  
- 静的解析とテストで「気づかないバグ」を減らす（PHPStan/Psalm、ユニットテスト）。  
- 変数名は意味ある名前に。小さな命名改善が保守性を劇的に上げる。

参考の最小例（パスワード保存と準備済みステートメント）:

```php
<?php
// password hashing
$hash = password_hash($password, PASSWORD_DEFAULT);

// PDO prepared statement
$stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email');
$stmt->execute(['email' => $email]);
$user = $stmt->fetch();
```

短くても効果の大きい改善をひとつずつ取り入れてください。古い“動く”コードは最高の教材です。
