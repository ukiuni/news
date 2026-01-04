---
  layout: post
  title: "Stop Forwarding Errors, Start Designing Them - エラーを転送するのをやめて、設計しよう"
  date: 2026-01-04T20:53:05.326Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://fast.github.io/blog/stop-forwarding-errors-start-designing-them/"
  source_title: "Stop Forwarding Errors, Start Designing Them | FastLabs / Blog"
  source_id: 46491051
  excerpt: "エラーを転送せず、kind/statusと文脈を分離してデバッグと復旧を高速化"
  image: "https://fast.github.io/og_image.png"
---

# Stop Forwarding Errors, Start Designing Them - エラーを転送するのをやめて、設計しよう
魅力的なタイトル: もう「エラー伝播」で夜を潰さない──原因と対処を分けるエラーデザイン入門

## 要約
単にエラーを上に投げる「Error Forwarding」は情報を失わせ、復旧／デバッグを困難にする。本稿は「機械が使うための平坦で行動指向なエラー」と「人間がデバッグするための文脈付きエラー」を分けて設計する実践を紹介する。

## この記事を読むべき理由
日本でも非同期サービス、マイクロサービス、Rust採用が増える中で、深夜に意味のないログを追う作業は高コスト。正しく設計されたエラーは自動復旧やSRE対応を劇的に楽にし、オンコール負荷低減・MTTR短縮に直結する。

## 詳細解説
現状の問題点（要点）
- std::error::Error の「単一の source() チェーン」は、複数原因（バリデーション複数箇所の失敗や並列処理の複数エラー）を表現できない。
- バックトレースは「エラーの作成場所」を示すだけで、非同期タスク経路やリクエスト文脈は見えない。かつ取得コストが高い。
- Provide/Request 的な動的型提供は柔軟だが予測性と最適化に問題を生む。
- thiserror は「どこから来たか」を示すが、呼び手が「どう対処すべきか」は教えてくれない。
- anyhow の便利さは文脈追加を怠らせ、型システムでの抑止がないため 3am の火消しを招く。

二つの受け手（機械 vs. 人間）
- 機械（リトライミドルウェア等）は「どう振る舞うべきか（retryable？）」を知りたい。ネストチェーンを辿るのは不要でコスト高。
- 人間は「どのリクエスト、どのユーザー、どのモジュールで何をしようとして失敗したか」を知りたい。文脈（task id、user id、ファイル位置など）が必須。

提案される設計（要旨）
1. 平坦で行動指向なエラー型（ErrorKind / ErrorStatus）
   - ErrorKind は 「NotFound」「RateLimited」「PermissionDenied」など、呼び手が取るべき行動で分類する。
   - ErrorStatus は再試行可能性を明示する（Temporary / Permanent / Persistent）。
   - 単一のライブラリ・モジュールは一つのフラットな Error 構造体を持ち、context フィールドで追加情報を渡す。

例（要旨）:
```rust
pub enum ErrorKind {
    NotFound,
    PermissionDenied,
    RateLimited,
    // ...
}

pub enum ErrorStatus {
    Permanent,
    Temporary,
    Persistent,
}

pub struct Error {
    kind: ErrorKind,
    message: String,
    status: ErrorStatus,
    operation: &'static str,
    context: Vec<(&'static str, String)>,
    source: Option<anyhow::Error>,
}
```

2. 人間のための低摩擦コンテキスト捕捉
   - #[track_caller] や軽量な「フレーム木」の採用で、コストを抑えつつ発生箇所（file:line）を自動収集する。
   - コンテキスト追加 API を非常に使いやすくして、境界での文脈付与を開発者に強制する（exn の or_raise パターン）。
   - これにより、モジュール境界で「ここで何をしようとして失敗したか」を必ず書くようにできる。

or_raise を使った境界での強制（概念）:
```rust
let user = db.query(user_id).or_raise(|| ServiceError::new(format!("failed to fetch user {}", user_id)))?;
```
型が合わないとコンパイラがエラーを出すため、context を付与せざるを得ない。

3. 両者の共存
   - 機械向けの構造化情報（kind/status/コード）と、人間向けの逐次的なコンテキスト（フレームツリー）を組み合わせる。
   - ログやトレースには task_id や user_id を含め、監視・SLO と連携しやすくする。

制約と注意
- 過剰な抽象（Provide/Request のようなランタイム提供）は可読性と最適化を損なう可能性がある。
- anyhow の利便性は否定しないが、アプリのコア境界では型を使って文脈付与を強制することが重要。

## 実践ポイント
- ErrorKind を「どう振る舞うか」で設計する（origin ベースで分けない）。
- ErrorStatus で再試行性を明確化する（Temporary / Permanent）。
- モジュール境界で必ず文脈を付ける仕組みを導入する（or_raise 風の API、あるいはコンパイラでチェックできる方針）。
- #[track_caller] を使ってファイル/行情報をコスト低く収集する。
- ログ／トレースには必ず識別子（task_id / request_id / user_id）を含める。エラーにはその ID を context として付与する。
- ライブラリは機械向けのフラットな Error 型を提供し、アプリはそれを受けて文脈を付与して投げ直す（wrap & annotate）。
- anyhow を使うなら、CI やコードレビューで「境界での context 追加」が実行されているか確認するルールを設ける。
- SRE/オンコール経験者と設計レビューし、3am の再現フロー（どのログで原因がたどれるか）を必ず確認する。

最後に一言：エラーは「型合わせ」の問題ではなく「コミュニケーション」の問題である。機械と人間両方に伝わるようにエラーを設計すれば、夜間のトラブルは確実に減る。
