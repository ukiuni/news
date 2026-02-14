---
layout: post
title: "One line of code, 102 blocked threads - 1行のコードが102スレッドを塞いだ話"
date: 2026-02-14T15:08:18.535Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@nik6/a-deep-dive-into-classloader-contention-in-java-a0415039b0c1"
source_title: "One line of code, 102 blocked threads"
source_id: 441914663
excerpt: "DatatypeFactory再生成がClassLoader同期を詰め、静的キャッシュで即改善"
---

# One line of code, 102 blocked threads - 1行のコードが102スレッドを塞いだ話
たった1行でサービスが渋滞：DatatypeFactory.newInstance()が引き起こしたClassLoader競合と即効で効く対処

## 要約
高スループットなJavaサービスで、DatatypFactory.newInstance()を繰り返し呼ぶことでURLClassPathの同期ロックに大量のスレッドが詰まり、レイテンシスパイクを招いていた。静的に1回だけ初期化して使うだけで問題の大半が解消した。

## この記事を読むべき理由
- 日本でもマイクロサービスやSpring Bootで多数のJARを使うアプリが増加中。知らないうちにClassLoaderの同期がボトルネックになる可能性が高い。
- 初級エンジニアでも取るべき簡単な対策（ファクトリのキャッシュや簡易キャッシュ導入）で即効性のある改善ができる。

## 詳細解説
- 問題の本質  
  DatatypeFactory.newInstance() は内部で ServiceLoader を使い、クラスパス上の実装を探すために getResources() 等を呼ぶ。これが最終的に jdk.internal.loader.URLClassPath.getLoader(...) の synchronized ブロックに入る設計で、同時に多数のスレッドがここで待ち行列になると全体が停滞する。

- 呼び出しチェーン（概略）  
  DatatypeFactory.newInstance() → FactoryFinder → ServiceLoader.load() → ServiceLoader$LazyClassPathLookupIterator.hasNext() → ClassLoader.getResources(...) → URLClassLoader.findResources() → URLClassPath.getLoader()（synchronized）

- なぜ悪化するか  
  - 高並列（例: 800 req/s）でリクエストごとに newInstance() を繰り返す  
  - classpath上のJAR数が多いほど ServiceLoader の走査コストが増える  
  - 同一ロックをファイル読み込み系（getResourceAsStream 等）も共有しているため相互に競合する

- 問題箇所のイメージ（簡易化した同期メソッド）
```java
// java
// URLClassPath の簡易イメージ（実装はJDK内部）
private synchronized Loader getLoader(int index) {
    // lazy init するので同期が必要だが高並列でボトルネックになり得る
}
```

- 診断  
  - プロダクションのスレッドダンプで多数の THREAD BLOCKED が同一ロックを待っているスタック（URLClassPath, ServiceLoader, DatatypeFactory 等）を確認
  - JFRやメトリクスで ClassLoader.getResource* の頻度やロック待ちを観察

## 実践ポイント
- DatatypeFactory等のファクトリは初期化コストが高い／ServiceLoaderを使う設計なので、ホットパスで毎回作るな。シンプルな対処例：
```java
// java
private static final DatatypeFactory DATATYPE_FACTORY;
static {
    try {
        DATATYPE_FACTORY = DatatypeFactory.newInstance();
    } catch (DatatypeConfigurationException e) {
        throw new RuntimeException(e);
    }
}
public XMLGregorianCalendar getXMLGregorianCalendarValue(Date date) {
    GregorianCalendar cal = new GregorianCalendar();
    cal.setTime(date);
    return DATATYPE_FACTORY.newXMLGregorianCalendar(cal);
}
```
- クラスパス内の静的リソースは都度読み込まずキャッシュする（Caffeine等を推奨）。ConcurrentHashMapベースのキャッシュはClassLoaderの粗い同期より競合が少ない。
```java
// java
Cache<String,String> cache = Caffeine.newBuilder()
    .maximumSize(100)
    .expireAfterWrite(60, TimeUnit.MINUTES)
    .build();
String text = cache.get(fileName, k -> {
    try (InputStream is = getClass().getClassLoader().getResourceAsStream(k)) {
        return IOUtils.toString(is, StandardCharsets.UTF_8);
    } catch (Exception e) { return null; }
});
```
- 検出習慣をつける  
  - ピーク時のスレッドダンプ分析を定期化する  
  - JFRでロック待ちやClassLoader領域の活動を監視する  
  - Canaryデプロイでキャッシュ導入の影響を観察し、すぐにロールバックできる仕組みを用意する

短時間の対策（ファクトリの静的化＋クラスパスリソースのキャッシュ）でClassLoader競合はほぼ解消され、ピークでのブロックスレッド数が劇的に減る。まずは自分のコードで newInstance() や getResource* の頻度を調べることをおすすめする。
