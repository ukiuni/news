---
layout: post
title: "PR Review Guidelines: What I Look For in Code Reviews - PRレビューのガイドライン：コードレビューで私が見るポイント"
date: 2026-01-14T22:27:52.115Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://shbhmrzd.github.io/software-engineering/best-practices/2026/01/14/pr-review-guidelines.html"
source_title: "PR Review Guidelines: What I Look For in Code Reviews | Shubham Raizada’s Blog"
source_id: 426714653
excerpt: "言語慣習・構造化エラー・ログで障害調査を劇的に減らすPRレビュー指南"
---

# PR Review Guidelines: What I Look For in Code Reviews - PRレビューのガイドライン：コードレビューで私が見るポイント
思わず「今すぐ見直したくなる」PRレビューの鉄則 — 小さな習慣が重大インシデントを防ぐ

## 要約
コードレビューで大事なのは「言語の自然な書き方」「構造化されたエラー」「構造化ログ」「可読性と最適化のバランス」。これらは保守性・観測性・信頼性を大きく改善する。

## この記事を読むべき理由
日本の開発現場でも、サービス規模が大きくなると単純なミスやログ設計の甘さが原因で障害調査やアラート地獄に陥りがち。この記事はPRでチェックすべき実践的な観点を、初心者にも分かりやすく整理してくれる。

## 詳細解説
1) 言語の「自然な書き方」を尊重する  
各言語には慣用表現（idioms）があり、それに従うと可読性とコンパイラ最適化の両方で有利になる。Rustの例では、手動インデックスループよりイテレータチェインの方が境界チェックを回避しやすく、結果的に同等かそれ以上の性能になることが多い。

```rust
// 手動ループ（インデックス）
let mut result = Vec::new();
let mut i = 0;
while i < items.len() {
    if items[i] > 10 {
        result.push(items[i] * 2);
    }
    i += 1;
}

// イディオマティックなイテレータ
let result: Vec<_> = items
    .iter()
    .filter(|&x| *x > 10)
    .map(|x| x * 2)
    .collect();
```

また、エラー伝播にはRustの `?` 演算子のような言語機能を使い、ネストを平坦化して「ハッピーパス」が追いやすいコードにすることが重要。

```rust
fn read_user_config(user_id: UserId) -> Result<Config, Error> {
    let user = fetch_user(user_id)?;
    let raw_config = load_config_file(&user.config_path)?;
    let config = parse_config(raw_config)?;
    validate_config(&config)?;
    Ok(config)
}
```

2) 文字列ではなく構造化されたエラーを使う  
エラーをただの文字列で返すと、個別の失敗モードをプログラムで扱えない。列挙型やエラーコードにするとコンパイラや監視ツールで扱いやすくなる。変更時に取りこぼしが出にくいという利点もある。

```rust
#[derive(Debug)]
enum DatabaseError {
    InvalidUrl(String),
    NetworkUnreachable(String),
    AuthenticationFailed,
    ConnectionTimeout,
}
```

3) printではなく構造化ログを使う  
ログはまず機械で解析できることが大事。JSONやキー・バリュー形式のログを出し、ログ上でフィルタ・集計・アラートが設定できるようにする。たとえば tracing のようなライブラリでフィールド付きログを出すと、監視ツールにそのまま拾わせられる。

```rust
use tracing::{info, error};

info!(user_id = %user_id, amount = %amount, "payment_attempted");
error!(order_id = %order_id, error_type = %error.code(), "payment_failed");
```

注意点としては、機微な個人情報をログに残さないこと、過剰なログ出力で性能を壊さないこと。

4) 可読性と最適化のバランス  
まずは読みやすいコードを書く。最適化はプロファイルしてから。POCやプロトタイプでは速度より実装速度を優先する場合もあるが、本番境界では可読性・観測性を犠牲にしない設計に戻すべき。

## 実践ポイント
- PRテンプレートに「言語慣習に従っているか」「エラーが構造化されているか」「ログが構造化されているか」をチェック項目として追加する。
- 重大なエラーはenum／コードで定義し、ログやメトリクスでそのコードをキーに集計する。
- ローカルでは println、共有環境（staging/prod）では構造化ログを使うルールを明文化する。
- パフォーマンス問題は必ずプロファイラで確認してから最適化を行う（先に最適化しない）。
- 日本の商用サービスではログの取り扱いで個人情報保護やログ保存期間といった法的要件にも配慮する（Pマークや個人情報保護法の観点）。

以上の習慣をPRレビューで守るだけで、保守コスト・障害対応時間・監視の精度が大きく改善します。
