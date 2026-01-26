---
layout: post
title: "Locale-dependent case conversion bugs persist (Kotlin as a real-world example) - ロケール依存の大文字小文字変換バグが残る（Kotlinを実例に）"
date: 2026-01-26T11:59:49.463Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sam-cooper.medium.com/the-country-that-broke-kotlin-84bdd0afb237"
source_title: "Locale-dependent case conversion bugs persist (Kotlin as a real-world example)"
source_id: 417194302
excerpt: "見えないロケール（İ）でKotlinビルドや実行が壊れる危険"
---

# Locale-dependent case conversion bugs persist (Kotlin as a real-world example) - ロケール依存の大文字小文字変換バグが残る（Kotlinを実例に）
魅力的なタイトル: トルコ語の「İ」がコンパイラを壊した話 — 見えないロケール設定があなたのビルドを壊す

## 要約
Kotlinのコンパイラと標準ライブラリで、システムのロケール（特にトルコ語）の影響を受ける大文字／小文字変換が原因で、ビルド失敗や実行時のNoSuchMethodErrorが何年も見逃されていた事例を解説する。

## この記事を読むべき理由
ロケール依存の文字変換は日本でもCIや開発者間で再現性のない障害を生む可能性があり、特にAndroid／JVM開発や依存関係を扱うプロジェクトでは致命的になり得ます。再現性確保と安全な文字操作のベストプラクティスを学べます。

## 詳細解説
- 問題の核心  
  KotlinのCompilerOutputParserはXMLタグ名（例: INFO）を小文字に変換して内部マップで照合していた（qName.toLowerCase() → "info"）。しかしトルコ語ロケールでは "I" の小文字がドット無しの 'ı' になり、"INFO".toLowerCase() が "ınfo" となってマップ照合に失敗。結果として「Unknown compiler message tag」が発生した。

- トルコ語アルファベットの特性  
  トルコ語には「i（点あり）」と「ı（点なし）」の別があり、大文字・小文字変換が言語に依存する（U+0049 I → 小文字 U+0131 など）。そのため、ロケールを指定せずにケース変換を行うと期待と異なる結果になる。

- 深刻化した経緯（コルーチン導入）  
  Kotlinがコルーチンでボクシング関数（boxInt など）をコンパイラ生成コードで呼ぶ際、型名の先頭文字を大文字・小文字変換する処理がロケール依存で誤変換され、実行時に本来存在しない boxİnt のようなメソッド名が生成されて NoSuchMethodError を招いた。報告は2016年から断続的に上がり、コルーチン普及で顕在化して長期間放置された。

- 技術的な対策ポイント（原理）  
  文字列の大文字／小文字変換は常に明示的なロケール（例: Locale.ROOT / Locale.ENGLISH）で行うべき。デフォルトロケールに依存すると環境差でバイナリやシンボル名が変わり得る。

## 実践ポイント
- すぐやること（開発・CI共通）
  - 文字列変換を明示的に行う: Kotlin/Javaでは Locale を指定する。
    ```kotlin
    // kotlin
    val safe = qName.toLowerCase(java.util.Locale.ROOT)
    ```
  - CI／ビルド環境に明確なロケールを設定する（例: LANG=en_US.UTF-8）。
    ```bash
    # bash
    export LANG=en_US.UTF-8
    ./gradlew build
    ```
  - ローカルとCIで同一のロケール／エンコーディングを揃える（Dockerイメージやビルドサーバの設定を見直す）。

- 調査のヒント
  - 「Unknown compiler message tag」やスタックトレースに見慣れない大文字（İ など）が含まれていないか検索する。
  - 問題が特定のマシンでしか起きない場合、ロケール差を疑う（locale / env を比較）。

- 長期対策
  - ライブラリ／ツール側でロケール非依存のAPI（Locale.ROOT）を使うよう貢献する。
  - ビルドツールやコンパイラのテストに複数ロケールを追加して回帰を防ぐ。

以上。ロケールは「見えない依存性」です。環境差による不具合を避けるため、明示的な指定とCI整備を習慣化しましょう。
