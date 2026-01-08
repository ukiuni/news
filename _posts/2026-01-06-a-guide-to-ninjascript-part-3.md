---
  layout: post
  title: "A Guide To NinjaScript - Part 3 - NinjaScriptガイド（パート3）"
  date: 2026-01-06T00:06:13.741Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://nobulltechguide.medium.com/the-no-bullshit-guide-to-ninjascript-part-3-8f93c237c804?source=friends_link&amp;sk=7ada58d2b79338238aa6086fe2e28c8d"
  source_title: "A Guide To NinjaScript - Part 3"
  source_id: 471344435
  excerpt: "チャート右下にティック毎で滑らかに残秒表示する実装手順と注意点を東京市場向けに解説。"
---

# A Guide To NinjaScript - Part 3 - NinjaScriptガイド（パート3）
チャート上に「あと何秒？」を常時表示する――NinjaScriptで作る正確で滑らかなバー・カウントダウン

## 要約
NinjaTraderのNinjaScriptで、任意の時間軸に対応する「バーの残り秒数」カウントダウンを作る手法を解説する。ティック毎に更新し、セッションの切れ目や非時間バーも考慮する実装のポイントを示す。

## この記事を読むべき理由
バーの閉じるタイミングを正確に把握できれば、エントリーやアラートの精度が格段に上がる。海外の記事の実装指針を日本の取引環境（東京市場やFXトレーダーの使い方）向けに噛み砕いて紹介するので、すぐ使える実装ノウハウが得られる。

## 詳細解説
この記事のゴールは以下の要件を満たすカウントダウンを作ること。
- 現在のバーに残っている秒数を表示
- 滑らかに（ティック毎に）更新される
- どの時間軸でも動作（ただし「秒」や「分」ベースのバーに限る）
- チャート右下など常に見える場所に表示
- セッション切れや非時間ベースのバー（ティックバー等）を適切に扱う

実装の考え方（要点）
1. 更新タイミング  
   Calculate を Calculate.OnEachTick にして、OnBarUpdate がティックごとに呼ばれるようにする。これで滑らかなカウントダウンが可能になる。

2. バー長の算出  
   BarsPeriod の型（Minute、Second 等）と値から「バーの長さ（秒）」を決定する。たとえば 5 分足なら barLength = 5 * 60 秒。非時間ベース（Tick/Range等）は「時間で意味のないバー」なのでカウントダウン表示を抑止または N/A を表示する。

3. 残り秒の計算ロジック（概念）  
   - 「最後に確定したバーの終了時刻（＝次のバーが閉じる予定の時刻）」を求める。  
   - 現在の時刻（チャート上の最新ティック時刻）との時間差を取れば残秒が出る。式は簡潔に $remaining = barLength - elapsed$。  
   - セッションの切れ目（取引休止時間）やサマータイム考慮も必要。セッション外なら表示を消すか「Session」と表示する。

4. 表示方法  
   Draw.TextFixed（固定位置）や Draw.Text を同一タグで更新すると、毎ティック書き換えができる。常に同じタグを再利用するのがポイント（毎回オブジェクトを作り直すとパフォーマンスが落ちる）。

5. 実運用での落とし穴と対策  
   - 時刻のズレ：チャートとOSのタイムゾーン差やサーバ時刻に注意。日本の取引所を扱うなら Tokyo 標準時（JST）を意識する。  
   - 高頻度更新による描画負荷：描画は最小限に留め、1秒未満の分解能が不要なら更新頻度を落とす。  
   - 非時間足対応：ティック足やレンジ足では残秒の概念がないため表示をオフにするか「--」にする。

短い実装スケルトン（概念的なC#例）
```csharp
// csharp
protected override void OnStateChange()
{
    if (State == State.SetDefaults)
        Calculate = Calculate.OnEachTick;
}

protected override void OnBarUpdate()
{
    if (BarsPeriod.BarsPeriodType != BarsPeriodType.Minute &&
        BarsPeriod.BarsPeriodType != BarsPeriodType.Second)
    {
        Draw.TextFixed(this, "cnt", "N/A", TextPosition.BottomRight);
        return;
    }

    // barLengthSeconds を BarsPeriod から決定（例: Minutes -> value * 60）
    int barLengthSeconds = (BarsPeriod.BarsPeriodType == BarsPeriodType.Minute)
        ? BarsPeriod.Value * 60
        : BarsPeriod.Value;

    // 概念: lastClosedBarTime を取得 → nextClose = lastClosedBarTime + barLength
    DateTime lastClose = Bars.GetTime(Bars.Count - 1); // 実装環境で調整が必要
    DateTime nextClose = lastClose.AddSeconds(barLengthSeconds);

    double remaining = Math.Max(0, (nextClose - Time[0]).TotalSeconds);
    string text = $"{Math.Ceiling(remaining)}s";
    Draw.TextFixed(this, "cnt", text, TextPosition.BottomRight);
}
```

## 実践ポイント
- まずは Calculate.OnEachTick を有効化して、Draw.TextFixed で表示するだけの最小実装を試す。描画が確認できたら残り秒の算出ロジックを入れる。
- 日本向けにはチャート時刻が JST であるかを確認し、国内取引所（JPXなど）やFXの24hセッションでの表示挙動を検証する。
- Tick/Range/Volume ベースのバーは時間概念がないため「表示オフ」か「N/A」扱いにする。必要ならユーザー設定で切り替え可能にする。
- セッション切れやニュース前後の急ブレ対応として、残り秒が負になったら表示をリセットする安全措置を入れる。

短時間で体感できる改善効果：チャート監視中のエントリー遅れが激減し、戦略確認のタイミングが安定する。まずは小さな時間軸（1分足）で試してみてほしい。
