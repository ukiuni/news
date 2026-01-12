---
layout: post
title: "BTS of OpenTelemetry Auto-instrumentation - OpenTelemetry 自動計測の舞台裏"
date: 2026-01-12T15:13:51.072Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://newsletter.signoz.io/p/bts-of-opentelemetry-auto-instrumentation"
source_title: "BTS of OpenTelemetry Auto-instrumentation - by Elizabeth"
source_id: 428648551
excerpt: "OpenTelemetry自動計測の仕組みをNodeやJava例で解説、導入時の落とし穴も詳述"
image: "https://substackcdn.com/image/fetch/$s_!IKwd!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e373ed1-e673-4829-b141-2b92a06f938d_3000x2000.png"
---

# BTS of OpenTelemetry Auto-instrumentation - OpenTelemetry 自動計測の舞台裏
ワンクリックで始める観測性？OpenTelemetryの「自動計測」がどう動くかをやさしく解剖

## 要約
OpenTelemetryの自動計測は、コードを書き換えずにアプリからトレースやメトリクスを取る仕組みで、言語ごとに異なる「実装トリック（モンキーパッチ、バイトコード差し込み、AST変換など）」で実現されている。仕組みを知れば導入・トラブルシュートがぐっと楽になる。

## この記事を読むべき理由
観測性（Observability）はマイクロサービス運用や障害対応で必須で、日本のSRE/開発チームが短期間で可視化を得る上で自動計測は強力な武器。だが「何もせずにデータが出る」裏には制約と副作用があるため、仕組みを理解すると導入判断や運用改善に役立つ。

## 詳細解説
- API と SDK の役割  
  - OpenTelemetry API：アプリコードや自動計測が呼ぶ「start/span」などのインターフェース。  
  - OpenTelemetry SDK：APIで発生したデータをどう処理（サンプリング、バッチ、エクスポート）するかを決める実装。自動計測はAPI呼び出しを生成し、SDKがそれを取り扱う流れになる。

- 動的言語と静的言語の違い  
  - 動的言語（例：Node.js、Python、Ruby）は実行時に関数を書き換えやすく、ランタイムで関数を包む（ラップする）手法が多用される。  
  - 静的言語／VM上言語（例：Java、.NET、Kotlin）はバイトコード改変やエージェントでロード時に差し込み、Goのようなネイティブ静的言語はコンパイル前にASTを書き換えるケースが多い。

- 代表的な技術パターン
  1. モンキーパッチ（動的言語）  
     実行時に既存関数を別の「ラッパー関数」で置き換え、前後で計測やコンテキスト伝播を注入する。たとえばNode.jsの概念例：
     ```javascript
     const original = module.exports.fn;
     function wrapped(...args) {
       const start = process.hrtime.bigint();
       const res = original.apply(this, args);
       const dur = process.hrtime.bigint() - start;
       console.log(`fn took ${dur} ns`);
       return res;
     }
     module.exports.fn = wrapped;
     ```
     Pythonでも同様に関数参照を差し替えることで実現する。
     ```python
     original_request = requests.request
     def wrapped_request(method, url, **kwargs):
         start = time.time()
         resp = original_request(method, url, **kwargs)
         duration = time.time() - start
         collect(method, url, resp.status_code, duration)
         return resp
     requests.request = wrapped_request
     ```

  2. バイトコード（/クラス）差し込み（JVM/.NET）  
     - JVMでは-agent（-javaagent）で起動し、premainでクラス変換器を登録、ロード時にバイトコードを改変してトレース呼び出しを埋め込む。例（概念）：
     ```java
     public static void premain(String args, Instrumentation inst) {
       new AgentBuilder.Default()
         .type(ElementMatchers.nameStartsWith("com.example"))
         .transform((builder, td, cl, mod, pd) ->
           builder.method(ElementMatchers.named("targetMethod"))
                  .intercept(MethodDelegation.to(MethodInterceptor.class)))
         .installOn(inst);
     }
     ```
     - JVMエコシステムならJava/Kotlin/Scalaなど言語横断で効く一方、起動時の設定や若干のオーバーヘッドがある。

  3. AST書き換え（Goなど）  
     - ソースを解析して抽象構文木（AST）に計測コードを埋め込み、修正済みソースをコンパイルする。ランタイム負荷はほぼゼロだが、ソースアクセスやビルドパイプライン改修が必要で、サードパーティのバイナリには効きにくい。

- トレードオフのまとめ  
  - 自動計測は導入コストが低く迅速だが、ライブラリのバージョン依存、サードパーティコードのカバレッジ不足、ランタイムの互換性問題、想定外の副作用（例：シリアライズやサイドエフェクトの変化）が起こる可能性がある。深いカスタム計測は手動での補完が必要。

## 実践ポイント
- まずはステージングで有効化して影響範囲と性能を評価する（特に- javaagentやプロファイラ系は注意）。  
- SDK設定（サンプラー、エクスポーター、バッファサイズ）を必ず確認して、データ量とコストをコントロールする。  
- 自動計測で得られない深い意味付け（ビジネス指標やカスタムタグ）は手動計測で補う。  
- Goなどソース書き換え型はビルドパイプラインに組み込む手間を見積もる。  
- 日本のレガシーシステムやオンプレ環境ではネットワークやセキュリティポリシーに配慮してエクスポート先を検討する（社内Collector経由がおすすめ）。  
- 問題発生時は「どのレイヤーで計測が差し込まれているか（モンキーパッチ／エージェント／AST）」を切り分けると原因特定が速くなる。

以上を理解すれば、OpenTelemetryの自動計測を「黒魔術」ではなく運用可能なツールとして使いこなせます。導入前に言語特性と運用要件を照らし合わせて計画を立てましょう。
