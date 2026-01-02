---
  layout: post
  title: "Python Numbers Every Programmer Should Know - プログラマが知っておくべきPythonの「数字」（性能・メモリ）"
  date: 2026-01-01T16:57:19.800Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://mkennedy.codes/posts/python-numbers-every-programmer-should-know/"
  source_title: "Python Numbers Every Programmer Should Know • Michael Kennedy&#39;s Thoughts on Technology"
  source_id: 46454470
  excerpt: "ベンチ実測で判明、Pythonの速度・メモリ節約法を具体数値で示し設計を劇的に改善"
  image: "https://cdn.mkennedy.codes/posts/python-numbers-every-programmer-should-know/python-numbers-every-programmer-should-know-social.webp"
---

# Python Numbers Every Programmer Should Know - プログラマが知っておくべきPythonの「数字」（性能・メモリ）
驚くほど役立つ！現場で差がつくPythonの“速さと容量”ベストプラクティス

## 要約
CPython 3.14上で計測された実測値から、基本操作・コレクション・シリアライザ・Webフレームワーク・IO・DBなどで「どれがどれだけ速い／重いか」を整理。相対比較を知れば設計判断が劇的にシンプルになる。

## この記事を読むべき理由
限られたリソースで高速化を図るとき、経験則だけで判断するとミスを招く。日本のプロダクトやサービス開発でも使える具体的な数値と実践的指針を短時間で得られる。

## 詳細解説
- 環境メモ: CPython 3.14.2、Apple M4 Pro上でのベンチ。絶対値は環境依存だが「相対比較」が重要。
- メモリの感覚
  - 空のPythonプロセス: 約 15.73 MB
  - 文字列: 空文字 41 bytes、1文字ごとに +1 byte（例: 100文字で約141 bytes）
  - 数値: 小さなintでも約28 bytes、floatは約24 bytes — C系の固定長想定より大きい。
- コレクションとアクセス
  - list.append(): 約28.7 ns → 3,480万 ops/sec 程度
  - dict lookup: 約21.9 ns、set membership: 約19.0 ns — ハッシュ構造は極めて高速
  - list内検索 (1,000要素): 約3.85 μs — listでの存在判定は要素数に比例して遅くなる
  - イテレーション: 1,000要素の列挙は数μsオーダー
- 生成・反復スタイル
  - list内包表記 (1,000要素): 約9.45 μs、同等のfor+appendは約11.9 μs → 内包表記が約20%高速
- オブジェクト設計（メモリ最適化）
  - 通常クラスのインスタンスと __slots__ を使った場合の1,000個あたりの差は約165.2 KB vs 79.1 KB — 大量保持するなら __slots__ が圧倒的に有効
- シリアライズ（JSON等）
  - 標準json.dumps (複雑): 約2.65 μs、一方 orjson.dumps は ~310 ns — orjson は数倍〜十倍高速
  - msgspec も高速な選択肢（やや機能差あり）
- Webフレームワークのオーバーヘッド（単純JSONレスポンス）
  - FastAPI / Starlette / Litestar: 約8 μs台（高スループット）
  - Django / Flask: やや遅め（設計上の機能差が影響）
- ファイル/DB/キャッシュ
  - ファイルオープン/クローズ: 約9 μs、1KB読み込み: 約10 μs、1MB書き込み: 約207 μs
  - SQLite（JSON blob挿入）: 約192 μs、主キー検索: 約3.57 μs
  - diskcache.set: 約23.9 μs / get: 約4.25 μs — ローカルキャッシュとして有力
  - MongoDBはネットワーク要因で insert/find が ~100 μs オーダー
- 関数呼び出し・asyncコスト
  - 空関数呼び出し: 約22 ns（関数呼び出しは意外と軽い）
  - coroutine作成: ~47 ns、run_until_complete(empty): ~27.6 μs、asyncio.sleep(0): ~39.4 μs — 非同期処理にはコストがあるので細粒度タスクで乱発すると逆効果

## 実践ポイント
- 大量データの存在確認は list ではなく set/dict を使う（速度差は数十〜数百倍）。
- 連続追加が多いリストは list.append() で十分高速だが、頻繁に拡張や中間検索があるなら別構造を検討。
- JSONの高速化は即効性あり：orjson / msgspec を導入すればシリアライズが数倍〜10倍速くなる（互換性と挙動は要確認）。
- メモリ節約が必要な大量インスタンスは __slots__ または dataclass(slots=True) を検討（数千〜数万単位で差が出る）。
- 小さな関数を大量に呼ぶ設計は問題ないが、async タスクを大量生成する場合はオーバーヘッドに注意。短時間のIO待ちを伴わない非常に細かいasync処理は同期実装の方が速いこともある。
- DB選択はユースケース次第：頻繁書き込み→diskcache、単純キー読み→SQLiteでも高速、分散性が必要ならMongoDB。ただしネットワーク遅延の影響を考慮する。

