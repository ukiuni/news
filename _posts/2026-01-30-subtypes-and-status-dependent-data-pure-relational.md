---
layout: post
title: "Subtypes and status-dependent data: pure relational approach - サブタイプとステータス依存データ：純粋リレーショナル手法"
date: 2026-01-30T19:23:31.081Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://minimalmodeling.substack.com/p/subtypes-and-status-dependent-data"
source_title: "Subtypes and status-dependent data: pure relational approach"
source_id: 1625886041
excerpt: "エラー混在を物理的に禁止する、矛盾ゼロのステータス別DB設計手法"
image: "https://substackcdn.com/image/fetch/$s_!9mZ5!,f_auto,q_auto:best,fl_progressive:steep/https%3A%2F%2Fminimalmodeling.substack.com%2Ftwitter%2Fsubscribe-card.jpg%3Fv%3D110723407%26version%3D9"
---

# Subtypes and status-dependent data: pure relational approach - サブタイプとステータス依存データ：純粋リレーショナル手法
エラーも検出結果も混在させない！定数カラムで作る矛盾ゼロの画像処理DB設計

## 要約
ステータスごとに有効な属性だけを持たせ、矛盾したデータ（例：完了済みにエラーメッセージがある）を物理的に不可能にする手法を、定数カラム + 複合外部キーで実現する紹介。

## この記事を読むべき理由
設計ミスでデータ整合性をアプリ側で補う必要があるなら、DBレベルで「無効状態を表現不可能」にする純粋リレーショナルなパターンは即効性があり、特に日本のプロダクトで運用負荷やバグを減らせます。

## 詳細解説
問題設定：画像アップロードに対しステータスが三種類（pending, invalid, completed）あり、invalid ならエラーメッセージ、completed なら検出された動物リストを保持する。NULLやアプリ側ロジックで補う「ゆるい」設計だと、矛盾した状態を作れてしまう。

解法の核：子テーブル側に「定数カラム」（常に同じ値を持つ status カラム）を置き、そのカラムを含む複合主キー／複合外部キーで images(id, status) を参照する。親テーブル images には (id, status) のユニーク制約を置く。これにより、子テーブルへ挿入できる行は親の対応するステータスを持つ行だけになる。

主要スキーマ例（要点のみ）：

```sql
CREATE TABLE images (
  id INTEGER NOT NULL,
  status VARCHAR(16) NOT NULL,
  image TEXT NOT NULL,
  CHECK (status IN ('pending','invalid','completed')),
  PRIMARY KEY (id),
  UNIQUE (id, status)
);

CREATE TABLE invalid_images (
  id INTEGER NOT NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'invalid',
  error_message VARCHAR(128) NOT NULL,
  CHECK (status = 'invalid'),
  PRIMARY KEY (id, status),
  FOREIGN KEY (id, status) REFERENCES images (id, status)
);

CREATE TABLE detected_animals (
  image_id INTEGER NOT NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'completed',
  ndx INTEGER NOT NULL,
  latin_name VARCHAR(64),
  CHECK (status = 'completed'),
  PRIMARY KEY (image_id, status, ndx),
  FOREIGN KEY (image_id, status) REFERENCES images (id, status)
);
```

効果：pending のままでは invalid_images / detected_animals に行を入れられない。invalid のレコードが残っている限り images のステータスを別の値に変更できない（参照整合性で保護）。NULLを使わず、DB制約だけで状態依存データの一貫性を保証できる。

注意点：定数カラムは少し奇妙に見えるが、CHECK と DEFAULT を併用すると運用が楽。ストレージ最適化や ENUM 化は実運用で考慮する。

## 実践ポイント
- 親テーブルに (id, status) のユニーク制約を追加しておく。  
- 子テーブルに status を DEFAULT + CHECK（定数）で置き、PRIMARY KEY に含める。  
- 子→親は複合外部キー (id,status) を参照させ、状態外の参照をDBレベルで禁止する。  
- ステータス変更は依存行の削除や移行をトランザクション内で行う（参照制約で拒否されるため）。  
- 実運用ではステータス列を小さな整数や ENUM に変換して容量を節約。  

このパターンは「サブタイプ／ステータス依存データ」を明示的に分離して整合性を保つ、シンプルで堅牢な設計です。
