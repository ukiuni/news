---
layout: post
title: "We deserve a better streams API for JavaScript - JavaScriptにはもっと良いStreams APIが必要だ"
date: 2026-02-27T15:20:15.613Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.cloudflare.com/a-better-web-streams-api/"
source_title: "We deserve a better streams API for JavaScript"
source_id: 47180569
excerpt: "現行ストリームAPIはロックやBYOBで扱いにくく、モダンJS向けの高速で直感的な再設計を提案"
image: "https://cf-assets.www.cloudflare.com/zkvhlag99gkb/610CHZf0Ig8hBHyPlId5MD/b1e7752eb5dc47c4ef5aa4143770d947/OG_Share_2024-2025-2026__9_.png"
---

# We deserve a better streams API for JavaScript - JavaScriptにはもっと良いStreams APIが必要だ
もうストリームでハマらない！モダンなJSで使いやすく高速なストリーム設計を考える

## 要約
Web Streams規格は広く採用されたが、ロッキングやBYOB、バックプレッシャー、Promiseの過剰生成といった設計上の負担が残り、モダンなJavaScriptの書き方と性能要件にそぐわない。より言語プリミティブを活かした代替設計で大幅な性能改善が可能だ。

## この記事を読むべき理由
Cloudflare Workers、Node.js、Deno、Bun、主要ブラウザなど、実運用でストリームを使う日本の開発者／運用者にとって、現行APIの落とし穴を知ることはバグ回避・性能改善・将来設計に直結するため必読です。

## 詳細解説
- 背景  
  WHATWGのStreams標準は2014–2016年に策定され、ブラウザとサーバー横断でストリームを扱う共通APIを目指した。しかし当時の言語機能（例えば async iteration）は未整備で、独自のreader/lockモデルやコントローラ設計が採られた。結果、API上の「儀式（ceremony）」が増え、現代のJSの書き方と齟齬が出ている。

- 読取の冗長さ（ロックとリーダー）
  典型的な読み取りは getReader()/read()/releaseLock() の三段階で煩雑。async iteration が使えるようになったとはいえ、内部のロックやBYOBといった仕組みは残り、誤った releaseLock の忘れでストリームが永久にロックされる等の落とし穴がある。例：
  ```javascript
  // javascript
  const reader = stream.getReader();
  const chunks = [];
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }
  ```
  async iteration の方が簡潔：
  ```javascript
  // javascript
  const chunks = [];
  for await (const chunk of stream) {
    chunks.push(chunk);
  }
  ```

- BYOB（Bring Your Own Buffer）の複雑さ  
  再利用バッファを直接渡すBYOBは理論的にゼロコピーを狙えるが、専用のリーダー型やバッファの"detachment"など実装と使用の複雑さが高く、実運用での採用は低い。多くの実装者はデフォルト経路を選ぶため、BYOBの実装負荷だけが残る。

- バックプレッシャーの限界  
  desiredSize / highWaterMark 等の信号は存在するが「助言」止まりで強制力がない。tee() のように一方の分岐でバッファが無制限に膨らむケースもあり、実際にはメモリ増大や遅延の原因になる。

- Promise の隠れコスト  
  spec準拠のために内部で多数のPromiseが生成される箇所があり、高頻度なストリーミング（動画フレーム、パケット等）ではオーバーヘッドが無視できない。著者が示す代替設計は言語のプリミティブ（async iteration等）をより直接活用することで、2x〜120xの性能改善をベンチで示している。

- 代替の方向性（概要）  
  reader/lockの手動管理を減らし、async iterablesや言語レベルの逐次処理をファーストクラスにする設計。BYOBはランタイム側で最適化しユーザーAPIは簡潔に保つ。これにより実装と利用双方の複雑さが減り、実測で大きな性能改善が得られると主張している。

## 実践ポイント
- まずは async iteration を第一選択に：for await...of でコードを簡潔に保つ。  
- getReader()/releaseLock() を使う場合は必ず try/finally で releaseLock() を呼ぶ。  
- BYOB は本当に必要か再検討する。多くは標準読み取りで十分。ランタイムが最適化しているならそちらを活用。  
- バックプレッシャー設計は高WaterMark/size関数や writer.ready を正しく扱って明示的に設定する（ただし万能ではない）。  
- 性能敏感パスはプロファイルしてPromise生成やキューリングのオーバーヘッドを確認する。可能なら言語プリミティブや軽量なラッパーで実装を簡素化する。  
- コミュニティ／仕様ディスカッションに参加して、現場での問題点・改善案を共有する（標準改善は実運用に直結します）。

以上を踏まえ、既存のWeb Streamsを「諦める」のではなく、使いどころを見極めつつ代替設計やランタイム最適化に注目することが今後の安定性と性能向上につながります。
