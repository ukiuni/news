---
layout: post
title: "An Introduction to Jackson 3 in Spring 7 and Spring Boot 4 - Spring 7 / Spring Boot 4 における Jackson 3 入門"
date: 2025-12-30T09:20:16.742Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hantsy.medium.com/an-introduction-to-jackson-3-in-spring-7-and-spring-boot-4-cba114aa36b1?source=friends_link&amp;sk=223b72099dabd422595f79b7f6f45db7"
source_title: "An Introduction to Jackson 3 in Spring 7 and Spring Boot 4"
source_id: 434788851
excerpt: "Spring7/Boot4でJackson3移行ガイド：JsonMapper・日付・ロケール要点"
---

# An Introduction to Jackson 3 in Spring 7 and Spring Boot 4 - Spring 7 / Spring Boot 4 における Jackson 3 入門
魅力的な日本語タイトル: Spring 7 / Boot 4 で変わるJSON処理――Jackson 3に移行する際にまず押さえるべき5つのポイント

## 要約
Spring 7 / Spring Boot 4 から Jackson 3 がデフォルトになり、JsonMapper とビルダーAPIへの移行、日付/ロケール表現の仕様変更など互換性に関わる変更点が導入されています。既存プロジェクトは設定とテストの見直しが必要です。

## この記事を読むべき理由
国内のJavaバックエンド開発でもSpring 7への移行が現実的になってきました。JacksonはSpringアプリで最も広く使われるJSONライブラリです。移行を誤るとシリアライズ結果やテストが壊れるため、事前に押さえておくべき実務的なポイントを手短に解説します。

## 詳細解説
- デフォルトの変更  
  Spring Boot 4のスターターは Jackson 3 の JsonMapper を提供します。従来の ObjectMapper を直接いじるパターンから、JsonMapper.builder() を使ったビルダー中心の設定へと設計が変わりました。

- 日付/時間の取り扱い  
  デフォルトで ISO‑8601 形式の文字列を出力するため、従来よく使っていた WRITE_DATES_AS_TIMESTAMPS を無効化する設定は不要になります（つまりタイムスタンプから文字列へ既定が変わった）。

- 名前空間と後方互換性  
  Jackson 3 はツール群を tools.jackson 名前空間で提供しますが、注釈モジュールは旧来の com.fasterxml.jackson を共有しており、一部で見た目がおかしく感じられますが互換性維持のための意図的な設計です。

- カスタマイズ方法  
  Spring Boot 4 では JsonMapperBuilderCustomizer で設定をチューニングできます。また application.properties でも spring.jackson.* 系の設定が利用可能です。

- テストサポート  
  spring-boot-starter-jackson-test を使うと @JsonTest と JacksonTester による最小限のJSONテストコンテキストが提供されます。独自のシリアライザ／デシリアライザや mixin の影響を検証可能です。

- 互換上の注意点  
  - Locale のシリアライズ形が変わり、例えば Jackson 2 の "zh_CN" が Jackson 3 では "zh-CN"（LanguageTag形式）になります。比較やマイグレーションスクリプトで影響を受ける可能性あり。  
  - もしどうしても Jackson 2 に戻したい場合、jackson2 モジュールを追加して Spring のプロパティ（spring.http.converters.preferred-json-mapper または spring.http.codecs.preferred-json-mapper）で jackson2 を指定できます。

簡潔な設定例（Jackson 3 の JsonMapper を Bean 定義する例）:

```java
// Java
@Configuration(proxyBeanMethods = false)
class JacksonConfig {
    @Bean
    JsonMapper jsonMapper() {
        var builder = JsonMapper.builder();
        builder
            .changeDefaultPropertyInclusion(i -> i.withValueInclusion(JsonInclude.Include.NON_NULL))
            .disable(SerializationFeature.FAIL_ON_EMPTY_BEANS)
            .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
            .enable(DeserializationFeature.ACCEPT_SINGLE_VALUE_AS_ARRAY)
            .findAndAddModules();
        return builder.build();
    }
}
```

application.properties での設定例:

```properties
spring.jackson.default-property-inclusion=non_null
spring.jackson.serialization.indent-output=true
```

テストで JacksonTester を使った簡単な検証例:

```java
// Java
@JsonTest
class JsonTests {
    @Autowired
    JacksonTester<Person> tester;

    @Test
    void serializeAndParse() throws Exception {
        var person = new Person("Yamada", LocalDate.of(1990,1,1), Gender.MALE);
        var json = tester.write(person).getJson();
        tester.parse(json).assertThat().hasFieldOrPropertyWithValue("name", "Yamada");
    }
}
```

## 実践ポイント
- まずはプロジェクト全体でカスタム ObjectMapper を使っている箇所を洗い出す（Bean 定義、MappingJackson2HttpMessageConverter 等）。
- JsonMapper ビルダーへ設定を移行し、日付やロケールの出力が期待どおりかサンプルJSONで検証する。
- @JsonTest と JacksonTester を使い、カスタムシリアライザ／mixin の挙動を回帰テストに追加する。
- 外部システムと Locale や日付フォーマットで契約がある場合は、Jackson 3 の出力形式に合わせるか、互換レイヤを用意する。
- どうしても互換性が必要なら Jackson 2 を再指定できるが、長期的には Jackson 3 前提での移行計画を立てる。

