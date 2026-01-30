---
layout: post
title: "challenge to compress 1M rows to the smallest possible size - 1M行を最小サイズへ圧縮する挑戦"
date: 2026-01-30T08:20:10.622Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/agavra/compression-golf"
source_title: "GitHub - agavra/compression-golf: 🏌️ a fun challenge to compress 1M rows to the smallest possible size"
source_id: 413885113
excerpt: "GitHubイベント100万件をロスレスで最小化、Rustで圧縮ゴルフに挑め"
image: "https://opengraph.githubassets.com/49a177303aafecc8825d722ebfa1153932557082cd2eebfac98a03a68caad464/agavra/compression-golf"
---

# challenge to compress 1M rows to the smallest possible size - 1M行を最小サイズへ圧縮する挑戦
GitHubイベント100万件を「最小バイナリ」に詰め込む圧縮ゴルフ — 君のアルゴリズムで記録を塗り替えよ

## 要約
GitHubイベント（JSON）をロスレスで最小バイト数に圧縮するオープン挑戦。Rustで独自のコーデックを実装してリーダーボード上位を目指すコンテスト。

## この記事を読むべき理由
実データ（GitHubイベント）に対する実践的な圧縮技術の試験場であり、文字列の正規化・辞書化・可変長整数・差分符号化など、実務で役立つ技術を短期間で学べるため。日本のサービスデータ圧縮やログ最適化にも応用可能。

## 詳細解説
- 目標：与えられたイベント列を完全復元可能にロスレス圧縮し、バイト数を最小化する。既存のベンチは最良で6,847,283 bytes（XiangpengHao）。Naive baselineは約210MB。
- データ構造（イベントは以下のフィールドを含む）
  - EventKey: id（数値文字列）、event_type（14種類程度）
  - EventValue: repo（id, name, url）、created_at（ISO8601）
- 参加方法（要点）
  - リポジトリをforkし、src/<github-username>.rs に EventCodec トレイトの実装を追加
  - コーデックは encode/decode を実装し、byte-identical に復元可能でなければならない
  - PR は実装ファイル1つだけを追加するルール（レビューフレンドリー）
- ルールの重要点
  - 決定的（deterministic）であること、外部データや学習済みモデルの利用不可、stable Rustでコンパイル可能であること。
- 評価
  - リポジトリ付属の training dataset で順位付け。別途隠しの evaluation dataset による最終評価も実施される（過学習対策）。
- 実装上の典型テクニック
  - カテゴリ化：event_type や repo id/name を辞書化して短いインデックスに置換
  - 共有情報の分離：URLや"owner/repo"のパターン分解（owner と repo を別にエンコード）
  - 数値・時間の差分化と可変長符号（varint）で小さくする
  - 頻度順の辞書＋ハフマン/算術符号やエントロピー符号化
  - リピート除去（リポジトリや時間の連続性を利用したランレングス／差分）
  - バイナリフォーマット設計：タグ付け・フィールド順固定化でオーバーヘッド削減
- 環境：Rust + bytes クレートで実装、cargo run --release で動作確認

## 実践ポイント
- まず手を動かす：リポジトリを clone して付属データで動かす。
```bash
git clone https://github.com/agavra/compression-golf
cd compression-golf
gunzip -k data.json.gz
cargo run --release
```
- 優先する改良案（短時間で効果が出やすい順）
  1. event_type と repo.id を固定長ではなく小インデックスにマップ（辞書化）
  2. id や created_at の差分→可変長整数化
  3. repo.name のスプリット（owner/repo）と共通サブストリング辞書化
  4. 最後にエントロピー符号（Huffman/算術）や軽量なバックエンド圧縮を試す
- 提出ルールを守る：PRは src/<username>.rs のみ追加、デコード結果が元データと完全一致することを必ず確認する。
- 日本向け応用：ログ圧縮やイベントストリーム保存（監査ログ・CI履歴など）で同様の手法が即戦力になるため、学んだテクニックは自社データ最適化にも使える。

以上。興味があれば、特定の圧縮技術（辞書化、varint、ハフマンなど）について実装例を示す。希望する技術を指定されたし。
