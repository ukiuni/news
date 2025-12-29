---
layout: post
title: When NOT to use Pydantic
date: 2025-12-28 14:28:15.242000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://ossa-ma.github.io/blog/when-not-to-use-pydantic
source_title: When NOT to use Pydantic | Ossama Chaib
source_id: 436147054
excerpt: Pydanticがボトルネック化する場面とmsgspecで高速化する実践ガイド
---
# Pydanticを“無条件”に使ってはいけない瞬間 — パフォーマンスと代替の見極め方

## 要約
Pydanticは開発体験が優れる反面、1モデルあたり10〜50μs（複雑なら100μs超）のオーバーヘッドがあり、高スループットやサブミリ秒要求のシステムではボトルネックになる。高速な代替としてmsgspecがあり、構造によっては数倍〜数十倍速い。

## この記事を読むべき理由
日本のプロダクトやマイクロサービスでも「使い慣れたPydanticをそのまま流用」しがちだが、トラフィックが増えたときのレイテンシ/コスト影響は無視できない。意思決定の指針と即実行できる対策を示す。

## 詳細解説
- レイテンシ感覚（目安）
  - Safe（Pydanticで問題なし）: リクエスト許容遅延 >10ms、スループット <1k req/s  
  - Gray（注意）: 許容遅延 1–10ms、スループット 1k–10k req/s  
  - Danger（要検討）: 許容遅延 <1ms、スループット >10k req/s — Python自体の見直しも検討
- オーバーヘッドの原因
  - Pydanticは柔軟性重視で、辞書・ORMオブジェクトなど様々な入力を受け付けるため、中間辞書生成や汎用的なバリデーション処理が発生する。
- ベンチマーク（要旨）
  - 単純フラット構造: msgspec ≒0.2μs、Pydantic v2 ≒1.2μs（約6x遅い）
  - ネスト構造: msgspec ≒1.2μs、Pydantic v2 ≒29μs（約24x遅い）  
  - 差が大きくなるのはPydanticがネストごとに中間辞書を作るため。
- msgspecの特徴
  - JSONバイト列を直接Structにデコードしてその場で検証する設計（辞書を挟まない）。
  - JSON/MessagePack/YAML向けに最適化されたシリアライザ兼バリデータ。
  - ただしPydanticが提供する豊富なDX機能（詳細なエラーメッセージ、FastAPI連携、OpenAPI自動生成、settings管理など）は持たない。
- トレードオフ
  - パフォーマンスが最重要であればmsgspecや別言語（高頻度取引など）を検討。
  - 開発効率・エコシステム連携を取るならPydanticが有力。現場では「ホットパスだけ高速化する」というハイブリッド運用が現実的。

簡単なmsgspec利用例:
```python
# python
import msgspec

class Data(msgspec.Struct):
    id: int
    name: str
    value: float

obj = msgspec.json.decode(json_bytes, type=Data)
```

## 実践ポイント
- まず測る: プロファイルしてPydanticが実際に遅延の原因かを確認する（per-request, per-model計測）。
- 階層化戦略:
  - 全面置換ではなく、ホットパス（高頻度API、低レイテンシ要求箇所）だけmsgspec等へ置換する。
- 軽量化テクニック:
  - Pydantic v2の最適化オプションを確認・適用する。
  - モデル数やネストを減らす、バリデーションを簡潔化する。
  - キャッシュ・バッチ処理で検証頻度を下げる。
- 運用面:
  - スタートアップ時間やメモリ影響も要確認（特にコンテナ/サーバーレス環境で重要）。
  - 日本の事業要件（セキュリティ・ログ要件、OpenAPI自動生成の有無など）に合わせてDXと性能の優先度を明確化する。
- 選定判断フロー（簡易）
  1. RPS・許容遅延を確認
  2. Pydanticがボトルネックならベンチ（msgspecなど）で置換効果を試す
  3. 必要ならハイブリッド運用で段階的移行

