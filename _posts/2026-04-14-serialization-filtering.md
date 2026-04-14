---
layout: post
title: "Serialization Filtering - シリアライズフィルタリング"
date: 2026-04-14T17:08:11.955Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://docs.oracle.com/en/java/javase/17/core/serialization-filtering1.html#GUID-55BABE96-3048-4A9F-A7E6-781790FF3480"
source_title: "Serialization Filtering"
source_id: 363071439
excerpt: "JavaのシリアライズフィルタでRCEやDoSを防ぐ実践ガイド"
---

# Serialization Filtering - シリアライズフィルタリング
無防備なデシリアライズを封じる：Javaのシリアライズフィルタで簡単に攻撃リスクを下げる

## 要約
Javaのシリアライズフィルタは、受信したバイトストリームからどのクラスをデシリアライズして良いかを事前に判定し、リモートコード実行やDoSにつながる危険なオブジェクト生成を防ぐ仕組みです。

## この記事を読むべき理由
JVM上で動くアプリ（RMI、JMX、SpringのHTTPインボーカなど）はデシリアライズを通じた脆弱性を狙われやすく、日本の企業でもレガシー連携やマイクロサービス間通信で該当するケースが多いため、今すぐ対策すべき基本知識です。

## 詳細解説
- なぜ危険か：デシリアライズは受け取ったデータの内容で任意のクラスのインスタンスを生成し、readObject 等で任意コードが実行され得るため「ガジェットクラス」を使ったRCEや状態破壊のリスクがあります。
- フィルタの役割：許可（allow）/拒否（reject）をクラス名やパッケージ、モジュール単位で判定でき、配列サイズ／グラフ深度／参照数／ストリーム長といったリソース上限も設定できます。
- 適用範囲：
  - JVM-wide filter（jdk.serialFilter）: JVM全体のデシリアライズに適用されるパターンベースのフィルタ（起動時またはjava.securityで設定）。
  - Stream-specific filter: 個々の ObjectInputStream に設定するプログラム的フィルタ（ObjectInputStream#setObjectInputFilter 等）。
- パターン文法のポイント：
  - パターンはセミコロン(;)で区切る。ワイルドカード * と ** が使える。
  - 先頭に ! を付けると拒否（reject）。例: !com.evil.*;com.trusted.*;!* で最小化。
  - リソース制限は maxarray, maxdepth, maxrefs, maxbytes のように指定。
- フィルタファクトリ：BinaryOperator<ObjectInputFilter> を登録してストリームごとにフィルタを選択・合成可能。RMI用の組み合わせなどに有用。
- カスタムフィルタ：ObjectInputFilter API でラムダ／クラス／パターンで実装して ObjectInputStream にセットできます。

## 実践ポイント
1. 可能なら「信頼できないデータはデシリアライズしない」。代替としてJSON等の安全なフォーマットを検討。  
2. JVM-wide で基本ポリシーを設定（起動オプションまたは $JAVA_HOME/conf/security/java.security）。例：  
   <java>java -Djdk.serialFilter="maxarray=100000;maxdepth=20;maxrefs=500" -jar app.jar</java>
3. アプリ側でストリーム単位の厳格フィルタを追加：許可リスト方式（allow-list）を基本に、既知の危険クラスは reject-list で明示。下は簡単な例：  
   <java>try (ObjectInputStream ois = new ObjectInputStream(in)) {
       ObjectInputFilter f = ObjectInputFilter.Config.createFilter("com.example.Safe*;!*");
       ois.setObjectInputFilter(f);
       Object obj = ois.readObject();
   }</java>
4. フィルタファクトリでコンテキスト依存の選択を行う（複数ストリーム／RMI向けに有効）。  
   <java>ObjectInputFilter.Config.setSerialFilterFactory((existing, stream) -> /* return combined filter */ );</java>
5. 追加対策：SSL/TLSで接続を保護、readObject 内でフィールド検証、JDKの最新パッチ適用、フィルタのログ有効化・テスト。

まずは JVM-wide の簡易フィルタ（リソース上限＋許可クラス）を導入し、既存の通信パスに対して段階的に厳格化していくのが現実的な手順です。
