---
  layout: post
  title: "Statistical Methods for Reliable Benchmarks - 信頼できるベンチマークのための統計手法"
  date: 2026-01-06T23:14:27.351Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://modulovalue.com/blog/statistical-methods-for-reliable-benchmarks/"
  source_title: "Statistical Methods for Reliable Benchmarks | modulovalue"
  source_id: 469242448
  excerpt: "中央値・CV%・ランダム化で誤差を排し、信頼できるベンチ結果を得る実践ガイド"
---

# Statistical Methods for Reliable Benchmarks - 信頼できるベンチマークのための統計手法
ベンチマークの“嘘”を見抜く：実運用で使える統計的測定ガイド

## 要約
単純な平均だけで性能を比べると誤った結論を出しがち。中央値、変動係数（CV%）、複数サンプル、ウォームアップ、ランダム化などの基本的統計手法で「信頼できる」ベンチマークが得られる、という主張をDart向けパッケージbenchmark_harness_plusの実装例とともに解説する。

## この記事を読むべき理由
- 日本でも増えるFlutter/Dart採用やクラウド・サーバーサイドの性能改善で、誤ったベンチ結果に基づく判断はコストやユーザー体験に直結する。  
- 開発者・QA・SREが短時間で信頼性のある比較をするための実践的手法がわかる。

## 詳細解説
- なぜ平均がダメか：平均（mean）は外れ値に弱い。例えば多くの実行が5μsでも一回50μsのGCが挟まると平均が大きく歪む。中央値（median）は外れ値の影響を受けにくく、典型的な実行時間の把握に適する。  
- いつ平均が必要か：スループットやシステム容量の計算では平均が重要。Little's Lawのように平均を前提にした法則（$L=\lambda\times W$）があるため、遅い例外も含めた平均レイテンシが必要な場面がある。  
- 変動係数（CV%）：分散の大きさを平均に対する割合で表す指標。  
  $CV\% = (\sigma / \mu) \times 100$  
  CV%で結果の信頼性を判断する。ざっくりの目安：<10%（Excellent）、10–20%（Good）、20–50%（Moderate）、>50%（Poor）。  
- ベンチマークの実務テクニック（benchmark_harness_plusのアプローチ）:  
  1. 複数サンプル（デフォルトはサンプル数=10）を取得し統計量を算出する。  
  2. 十分なウォームアップ（JIT・キャッシュ・初期化対策）を行い、その結果は破棄。  
  3. バリアント実行順をランダム化して系統誤差を減らす（CPU周波数スケーリングや熱設計の影響対策）。  
  4. 変なタイミングでGCが起きるのを減らすため、バリアント間でGCを誘発して分散を均す。  
  5. 各結果にCV%と信頼度を表示し、高CV%なら警告する。  
- 出力の読み方：まずCV%を確認、次に中央値で比較、平均と中央値の差で外れ値の有無を読み取り、信頼できる場合に比率（何倍速いか）を評価する。

## 実践ポイント
- 実装比較（典型比較）には中央値を使う。容量計算やスループット見積もりには平均を使う。  
- 測定結果の信頼性はCV%で判断する。$CV\%>50$はノイズが支配的。  
- サンプルあたりの実行時間が短すぎる（サブマイクロ秒）ならイテレーション数を増やし、各サンプルが少なくとも約10ms以上かかるようにする。  
- CIやローカル実行ではバックグラウンドプロセスを減らす、温度やCPU周波数の影響を考慮する。  
- 入力がランダムでばらつくなら決定的なテストデータを使う。性能が本質的に変動する処理（外部I/Oやキャッシュ依存）では高CV%自体を「仕様」として扱う。  
- 実際に試す（Dart例）:

```dart
dart
import 'package:benchmark_harness_plus/benchmark_harness_plus.dart';

void main() {
  final benchmark = Benchmark(
    title: 'List Creation',
    variants: [
      BenchmarkVariant(
        name: 'growable',
        run: () {
          final list = <int>[];
          for (var i = 0; i < 100; i++) list.add(i);
        },
      ),
      BenchmarkVariant(
        name: 'fixed-length',
        run: () {
          final list = List<int>.filled(100, 0);
          for (var i = 0; i < 100; i++) list[i] = i;
        },
      ),
    ],
  );
  final results = benchmark.run(log: print);
  printResults(results, baselineName: 'growable');
}
```

まとめ：単純な平均値に頼らず、中位値・CV%・複数サンプル・ウォームアップ・ランダム化を組み合わせれば、実運用で信頼できるベンチマークが取れる。Dart/Flutter開発やサーバーサイドの性能改善判断に即役立つ技術だ。
