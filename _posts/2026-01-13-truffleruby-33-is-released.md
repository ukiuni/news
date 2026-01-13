---
layout: post
title: "TruffleRuby 33 is Released - TruffleRuby 33 がリリース"
date: 2026-01-13T22:04:11.773Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://truffleruby.dev/blog/truffleruby-33-is-released"
source_title: "TruffleRuby 33 is Released | The TruffleRuby Blog"
source_id: 975387034
excerpt: "最速インストール＆Hashの本気のスレッド安全化でTruffleRuby 33を試す価値あり"
---

# TruffleRuby 33 is Released - TruffleRuby 33 がリリース
インストール最速＆Hashが本気でスレッドセーフに——今すぐ試したくなるTruffleRuby 33の注目点

## 要約
TruffleRuby 33は、Rubyバージョン互換性の新しい方式、Hashの本格的なスレッド安全化、そしてlibssl/libyamlへの依存をなくしてインストールを劇的に簡単／高速化したメジャーアップデートです。

## この記事を読むべき理由
- ローカル開発やCIで「速く」「確実に」Ruby環境を用意したいエンジニア。
- マルチスレッド処理やJavaアプリへの組み込みで安定したRuby実行環境が欲しい開発者。
- 日本の企業環境（古めのUbuntuやRHELを使うケース）でも扱いやすくなったため導入検討に価値があります。

## 詳細解説
- バージョニングの変更  
  TruffleRubyのメジャーバージョンが対象のRubyバージョンを示す方式に変わりました。TruffleRuby 33 は Ruby 3.3 と互換、以降は 34 → 3.4、40 → 4.0 のように対応します。これで互換性が一目で分かります。

- Hashのスレッド安全化（大きな改善点）  
  TruffleRuby 33では組み込みのHashが並列実行環境で安全に動くようになりました。GVL（Global VM Lock）を持たないTruffleRubyはスレッドが並列で動くため従来は同一Hashへの同時アクセスで問題が起きやすかったのですが、新実装では
  - 平行読み取り（h[]）と平行書き込み（h[]=）をサポート、
  - 単一スレッドしか参照しないHashに対してはオーバーヘッドなし、
  - 「iteration中の変更でRuntimeErrorが出る」ような一時的エラーを回避（CRubyより柔軟）、
 という性質を持ちます。実装は「Lightweight Layout Lock」などの軽量ロックとノンブロッキング同期技術に基づいています。  
  ただし、挿入順を保持するHashの性質上、末尾エントリへの強い競合が発生するため、書き込み並列性が重要なケースでは concurrent-ruby の Concurrent::Map の使用が推奨されます。

- インストールが史上最速＆最も簡単に  
  TruffleRuby 33はシステムの libssl / libyaml に依存しなくなり、ビルドを伴う手順が不要になりました。配布バイナリをダウンロードして展開するだけで動作します（Ubuntu 18.04 や RHEL8 までサポート）。例えば：
  ```bash
  # 直接ダウンロードして展開して実行
  curl -L https://github.com/truffleruby/truffleruby/releases/download/graal-33.0.0/truffleruby-33.0.0-linux-amd64.tar.gz \
    | tar xz && truffleruby-33.0.0-linux-amd64/bin/ruby -v
  ```
  ソースからコンパイルするCRubyに比べてインストール時間が大幅短縮され、CIやコンテナでの利用コストが下がります。

- Javaへの組み込みが簡単に  
  system libssl/libyaml が不要になったため、TruffleRubyをJava（GraalVM Polyglot）へ組み込む際の面倒なネイティブ拡張ビルドが不要になりました。Mavenの座標も変更されています。
  ```xml
  <!-- Maven -->
  <dependency>
    <groupId>org.graalvm.polyglot</groupId>
    <artifactId>polyglot</artifactId>
    <version>25.0.1</version>
  </dependency>
  <dependency>
    <groupId>dev.truffleruby</groupId>
    <artifactId>truffleruby</artifactId>
    <version>33.0.0</version>
    <type>pom</type>
  </dependency>
  ```
  ```groovy
  // Gradle
  implementation("org.graalvm.polyglot:polyglot:25.0.1")
  implementation("dev.truffleruby:truffleruby:33.0.0")
  ```

- 開発の公開化とコミュニティ主導化  
  リポジトリは oracle/* から truffleruby/* に移り、Oracleのスポンサーシップから独立。GitHub上で公開開発され、CLA不要、CIが早く回るためPRの反映が速くなります。リリース頻度も上がる見込みです。

## 日本市場との関連性
- 日本の企業では古いベースOS（Ubuntu 18.04、RHEL 8）を使い続けるケースが多く、TruffleRuby 33のバイナリ互換性は導入障壁を下げます。
- OpenSSLのバージョン差異やネイティブライブラリのビルド手間が原因で導入を見送っていたプロジェクトでも、依存削減により採用検討がしやすくなります。
- Javaと連携したエンタープライズシステム（Spring等）内でRubyを埋め込みたい場合、ビルド不要で組み込みが簡単になる点は大きなメリットです。

## 実践ポイント
- まずは既存アプリ／テストスイートをTruffleRuby 33で動かしてみる（問題があればGitHubに報告）。  
  ```bash
  # rbenv / asdf 等でのインストール例
  rbenv install truffleruby-33.0.0
  # または
  asdf install ruby truffleruby-33.0.0
  ```
- マルチスレッドでHashを共有する重い書き込みワークロードでは、Concurrent::Mapを検討する（書き込み並列性の向上）。
- Javaアプリに組み込む場合はMaven/Gradleの依存をdev.truffleruby:trufflerubyに切り替え、ネイティブ拡張の再ビルドが不要になった恩恵を利用する。
- 本番導入前にCIで素早く検証できるため、TruffleRubyを用いたパフォーマンス・安定性比較を短周期で回すと効果的。

興味があれば、まずは手元の小さなプロジェクトやCI上でTruffleRuby 33を試してみることをおすすめします。問題が見つかれば upstream のGitHubに報告すると改善が早く反映されます。
