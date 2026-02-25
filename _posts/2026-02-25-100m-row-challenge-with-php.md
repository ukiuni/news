---
layout: post
title: "100M-Row Challenge with PHP - PHPで1億行チャレンジ"
date: 2026-02-25T12:58:17.306Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/tempestphp/100-million-row-challenge"
source_title: "GitHub - tempestphp/100-million-row-challenge"
source_id: 47149752
excerpt: "PHPで1億行のアクセスログを低メモリで高速集計する実践ベンチと最適化指南"
image: "https://opengraph.githubassets.com/d36ff49b139a05850b5d2b2253c4a16c58f16fd8b1fd0e664ad2652ce4e5edb0/tempestphp/100-million-row-challenge"
---

# 100M-Row Challenge with PHP - PHPで1億行チャレンジ
PHPで1億行のアクセスログを「高速かつ実用的」に集計する――あなたのコードを競わせるベンチイベント

## 要約
PHPで生成された最大100,000,000行のCSV（URL, タイムスタンプ）を日次訪問数の辞書型JSONに変換するベンチチャレンジ。正確性・メモリ制約・速度が勝敗を分ける。

## この記事を読むべき理由
日本でもまだ多くのサイトでPHPが使われており、ログ解析やバッチ集計の現場で「大量データを低メモリで高速に処理する技術」は即戦力になるため。実務で役立つ最適化パターンを短時間で学べます。

## 詳細解説
- ゴール：CSVの各行（URL, ISO8601タイムスタンプ）をパスごとに日付順で集計し、pretty JSONで出力。例：{ "/blog/xxx": { "2025-01-24": 1, "2026-01-24": 2 }, ... }。
- リポジトリ：Parser実装箇所は app/Parser.php の parse(string $inputPath, string $outputPath): void に差し替えて提出。検証コマンドやデータ生成コマンドが用意されています。
- ローカル実行：デフォルトは1,000,000件。実際のベンチは100,000,000件（実データはシードなしで秘密）。
- データ生成例／検証コマンド：
```bash
composer install
php tempest data:generate        # デフォルトで1_000_000
php tempest data:generate 100_000_000   # ローカルで1億（要ディスク／時間）
php tempest data:parse
php tempest data:validate
```
- 制約と環境：ベンチは 2 vCPU / 1.5GB メモリのDigitalOceanプレミアムで実行。JITは無効、FFIは使用不可。利用可能な拡張一覧も公開されている（例：json, mbstring, igbinary 等）。
- 提出方法：リポジトリをforkしてPRで提出。手動検証後に専用サーバで計測し leaderboard.csv に記録。上位3名にスポンサー賞あり。

## 実践ポイント
- ストリーミング処理を最優先：ファイルを一括読み込みせず、fopen + fgets / SplFileObject::READ_CSV で逐次処理。
- メモリ節約の集計戦略：ネストした連想配列で集計（$map[$path][$date]++）は簡潔だがメモリを使う。必要ならパス単位で中間ファイルに分割してマージする手法を検討。
- 日付処理：ISO8601から "YYYY-MM-DD" を取り出すだけなら substr/strpos で高速化。DateTimeは安全だがコスト高。
- 文字列処理：parse_urlでpath抽出、または手早く path 部分だけを取り出す専用ロジックを使う（正規表現は遅い場合あり）。
- 出力：最終集計後にキー（日付）を昇順ソートして json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES)。
- 再現性：ローカルで seed を固定して検証 → 本番はノンシードでの差分を考慮。
- プロファイル：Xdebug/Tideways等でボトルネック（メモリ増加・ホットループ）を計測し、ループ内の余分なオブジェクト生成を削る。
- まずは検証通過を目指す：正しさ（data:validate）→ 次に速度改善、最後にPRでベンチへ挑戦。

短時間で学べて実務直結の良い演習です。興味があればリポジトリをforkしてローカルで1Mから試してみてください。

参考（実装箇所のサンプル）：
```php
<?php
final class Parser {
    public function parse(string $inputPath, string $outputPath): void {
        throw new Exception('TODO');
    }
}
```
