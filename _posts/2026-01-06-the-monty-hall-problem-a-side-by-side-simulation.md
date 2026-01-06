---
  layout: post
  title: "The Monty Hall Problem, a side-by-side simulation - モンティ・ホール問題：並列シミュレーション"
  date: 2026-01-06T19:58:32.638Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.pcloadletter.dev/blog/monty/"
  source_title: "The Monty Hall Problem, a side-by-side simulation"
  source_id: 469415396
  excerpt: "並列可視化で勝率差の収束を直感で示す、実装解説付きモンティ・ホールデモ。"
  ---

# The Monty Hall Problem, a side-by-side simulation - モンティ・ホール問題：並列シミュレーション
2つのボードで「切り替えあり／なし」を同時に回すと、直感を覆す確率の収束が視覚でわかる

## 要約
「最初の選択を切り替えると勝率が上がる」というモンティ・ホール問題を、切り替えするケースとしないケースを並べて同時にシミュレーション表示することで直観的に示すデモとその実装解説。

## この記事を読むべき理由
確率の直感が間違いやすいことは日本の教育現場や技術プレゼン、採用面接でも頻出。フロントエンドでの視覚化と小さな非同期シミュレーション実装は、教育ツールやデモの作り方、また小規模な可視化プロジェクトの参考になるため、エンジニアや技術系ライターに有用です。

## 詳細解説
このデモは「切り替えするボード」と「切り替えしないボード」を並べて同時に回すことで、それぞれの勝率が繰り返し試行で収束する様子を見せます。実装の要点は以下。

- UI構成（概略）
  - 3つの扉を表す要素が2つのボード（switch / no-switch）にそれぞれ配置される。
  - スタート／ストップ、速度調整、スコアボード表示を用意。

- シミュレーションの流れ（1試行）
  1. 3つの扉のうち1つに車、残り2つにヤギを配置（乱数で決定）。
  2. プレイヤーがランダムに1つを選択。
  3. ホストがプレイヤーの選択でも車でもない扉（ヤギ）を1つ公開。
  4. 「切り替え」ボードは残った未公開の扉に選択を切り替え、「切り替えなし」ボードはそのまま維持。
  5. 扉を開けて勝敗判定しスコア更新。

- 実装ポイント（JavaScript）
  - 単純な乱数関数 randi(n) = floor(random()*n)。
  - 非同期でアニメーション的に遅延を入れる sleep 関数。
  - MontyBoard クラスが各ボードの状態更新とループを管理。
  - ホストが開ける扉は「選択でも勝ち扉でもない」扉群からランダムに選ぶのが重要（公平性のため）。

- 理論的な収束
  - 初回選択で車を当てる確率は $1/3$、外す確率は $2/3$。
  - 初回選択が車のとき（確率 $1/3$）に切り替えると負け、外しているとき（確率 $2/3$）に切り替えると勝つ。よって切り替えた場合の勝率は
  $$
  P(\text{win}|\text{switch}) = \tfrac{2}{3}
  $$
  切り替えない場合は初回のままなので
  $$
  P(\text{win}|\text{no switch}) = \tfrac{1}{3}
  $$
  デモはこれらが試行回数の増加とともに収束する様子を視覚的に示します。

## 日本市場との関連
- 教育現場：確率論・統計の授業で直感と理論のギャップを見せるデモ教材に最適。
- 採用・面接：アルゴリズムや確率の問いを視覚的に提示する面接問題の補助ツールとして使える。
- プロダクトデモ：UXやデータ可視化の事例紹介、社内ハッカソンでの短時間デモに向いている。
- ローカライズの余地：UI訳・アクセスビリティ強化（スクリーンリーダー対応）や TypeScript 化は日本企業でも実用的。

## 実践ポイント
- まずはコードをローカルで動かし、試行回数を増やして収束を確かめる（例：10万〜100万試行）。
- デモを教育用にするなら、試行ごとの確率推移をグラフで表示すると説得力が増す。
- 改良案
  - シード可能な乱数で再現性を持たせる。
  - TypeScript へ移植して型安全にする。
  - 並列で大量試行する場合は UI 描画と計算を分離（Web Worker など）。
- すぐに試す簡単なヘッドレス・シミュレーション例（試行数を増やして収束を観察）：

```javascript
javascript
function randi(n){return Math.floor(Math.random()*n);}
function trial(switching){
  const win = randi(3);
  let guess = randi(3);
  // host reveals a goat that's neither guess nor win
  const revealChoices = [0,1,2].filter(i=>i!==guess && i!==win);
  const doorToReveal = revealChoices[randi(revealChoices.length)];
  if(switching){
    guess = [0,1,2].find(i=>i!==guess && i!==doorToReveal);
  }
  return guess===win;
}
(function run(n=100000){
  let swWins=0, nsWins=0;
  for(let i=0;i<n;i++){
    if(trial(true)) swWins++;
    if(trial(false)) nsWins++;
  }
  console.log('switch', swWins/n, 'no-switch', nsWins/n);
})(1000000);
```

この手の小さな可視化は「なるほど」と納得させる力が強いので、プレゼンや教材、社内勉強会で一度は実装してみる価値があります。
