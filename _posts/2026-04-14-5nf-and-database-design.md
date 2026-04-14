---
layout: post
title: "5NF and Database Design - 第5正規形とデータベース設計"
date: 2026-04-14T09:15:52.608Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kb.databasedesignbook.com/posts/5nf/"
source_title: "5NF and Database Design | Database Design Book"
source_id: 1275130459
excerpt: "業務要件→アンカー→リンクの手順で5NFを実務的に簡潔化、事例で即実践可能"
---

# 5NF and Database Design - 第5正規形とデータベース設計
もう迷わない！5NF（第5正規形）を実務視点でスッキリ理解する — アイスクリームとコンサートで学ぶ設計のコツ

## 要約
第5正規形（5NF）は「結合依存」の分解に関する理論だが、実務ではまず業務要件から論理モデル（エンティティ＝アンカーとリンク）を作ることが正解。典型パターンは「三角（AB-BC-AC）」と「星型（ABC+D）」で、適切に設計すれば5NFを意識せずに正規化は達成できる。

## この記事を読むべき理由
日本の開発現場でも、要件漏れや冗長データによる不整合はコストになる。5NFの教科書的な混乱を避け、実務で使える設計手順と典型パターンを押さえることで、安全で保守しやすいスキーマが作れます。

## 詳細解説
- 問題点：教科書やWikipediaの5NF例（旅行販売員×ブランド×製品）には不自然な前提が入りやすく、学習者を混乱させる。まず「テーブルが何を意味するか」を問うより「業務が何を要求するか」を明確にすることが第一歩。
- 論理モデル（アンカー＋リンク）アプローチ：実務では「アイテム（ブランド・味・友人）＝アンカー」を定義し、関係（link）を整理する。M:N は必ず接合テーブル（junction table）にする。
- AB-BC-AC 三角パターン（アイスクリーム例）：
  - アンカー：Brand、Flavour、Friend
  - リンク：brand_flavours（Brand↔Flavour）、friend_brands（Friend↔Brand）、friend_flavours（Friend↔Flavour）
  - 前提：友人が好きなブランドと好きな味が「交差」して許容される組合せを表す（ブランドが提供する組合せに限定）。
- ABC+D 星パターン（演奏・コンサート例）：
  - アンカー：Concert、Musician、Instrument、（概念としての）Performance
  - Performance を軸に Concert:Performance, Musician:Performance, Instrument:Performance がすべて 1:N となる設計。Performance は演奏という概念を表す実体。
- 物理設計とキーの選び方：
  - ビジネス要件で (concert_id, musician_id, instrument_id) の組が一意なら、合成主キーでもよいし、synthetic id + UNIQUE 制約でもよい。設計上の選択は可搬性と運用しやすさで決める。

例（synthetic id + UNIQUE）
```sql
CREATE TABLE performances (
  id INTEGER PRIMARY KEY,
  concert_id INTEGER NOT NULL,
  musician_id INTEGER NOT NULL,
  instrument_id INTEGER NOT NULL,
  UNIQUE (concert_id, musician_id, instrument_id)
);
```

例（合成主キー）
```sql
CREATE TABLE performances (
  concert_id INTEGER NOT NULL,
  musician_id INTEGER NOT NULL,
  instrument_id INTEGER NOT NULL,
  PRIMARY KEY (concert_id, musician_id, instrument_id)
);
```

- 結論的視点：5NFは理論的には重要だが、多くの実務ケースでは論理モデル→教科書的なテーブル化手順で十分。無理に5NFにこだわって非現実的な前提を導入する必要はない。

## 実践ポイント
- 1) まず業務要件を文章で厳密に書く（「だけど」「しか」などの言葉に注意）。  
- 2) アンカー（実体）を見つけ、アンカー間のリンク（M:N や 1:N）を明示する。  
- 3) M:N は接合テーブルにしておく（ブランド×味など）。  
- 4) 一意性が必要なら合成PKかsynthetic+UNIQUEを選ぶ。運用・参照パターンで判断。  
- 5) 5NFの理論は知っておくが、まずは論理モデルを丁寧に作ることで混乱を避ける。

日本のeコマース／CRM／レコメンド等で多対多関係は頻出です。まず要件→アンカー→リンクの順で設計すれば、5NFに悩む時間を機能開発やデータ品質向上に回せます。
