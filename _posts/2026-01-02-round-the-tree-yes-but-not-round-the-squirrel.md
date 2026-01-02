---
  layout: post
  title: "Round the tree, yes, but not round the squirrel - 木の周りを回ったけれどリスの周りは回っていない"
  date: 2026-01-02T09:15:33.029Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.futilitycloset.com/2026/01/02/round-and-round/"
  source_title: "Round and Round - Futility Closet"
  source_id: 46462592
  excerpt: "木の周りは回れてもリスの顔は見えない――視界とトポロジーの盲点を実践例で説明"
  image: "https://www.futilitycloset.com/wp-content/uploads/2026/01/2026-01-02-round-and-round.jpg"
---

# Round the tree, yes, but not round the squirrel - 木の周りを回ったけれどリスの周りは回っていない
見えている「背中」だけで判断するな — リスと木の小さなパラドックスが教える視界・トポロジー・ロボット工学の落とし穴

## 要約
ヤコフ・ペレルマンの短い寓話は、「木の周りを回る」と「リスの周りを回る」が同義かをめぐる混乱を描く。これは視界の遮蔽や参照フレームの違いが結論を変えることを示す、技術者にとって示唆深い例だ。

## この記事を読むべき理由
ロボット、自動運転、AR/VR、コンピュータビジョンなどで「何を囲んでいるか」を正しく判定することは安全性と性能に直結する。日常的な「見えているか／見えていないか」の差が、アルゴリズムやテスト設計で重大なバグを生むため、日本のエンジニアも押さえておくべき思考実験だ。

## 詳細解説
- 問題の本質：話の人物は「中心の木を回った」ことは確かだが、リスが木の表面を回って顔だけをこちらに向け続ければ「リスの背中を見ていない」ことになる。ここで問われるのは「どの対象を基準にして『回っている』と判断するか」というメタ的な定義の問題だ。
- コンピュータサイエンス的帰着：
  - 可視性（visibility）と遮蔽（occlusion）：センサーは対象の位置とは独立に、視線が届くかどうかで情報を得る。物体が支持面（木）に接している場合、対象の幾何位置と可視可能領域は一致しないことがある。
  - トポロジー（包囲判定）：平面上でパスがある点を「囲む」かどうかは winding number（巻数）や点内判定で定式化できる。連続的に囲めば数学的には含まれるが、視界ベースの「見えた」定義とは異なる。
  - 追跡・追跡回避（pursuit–evasion）やアートギャラリー問題：エージェントが相手を視認できるか、あるいは隠れられるかは戦略・センサー配置の設計課題になる。
- 数学的表現：連続曲線 γ(t) が点 p を何回回ったかを表す winding number は
  $$w=\frac{1}{2\pi}\oint_{\gamma} d\theta$$
  離散的には角度差の総和で計算する。
- 実務的含意：単に「中心点を囲む経路を作れば良い」という発想は不十分。視認性を基準に評価する場合は、対象表面の向き、遮蔽物、センサーの視錐台（frustum）を考慮する必要がある。

## 実践ポイント
- 点を囲んでいるかの判定には「点内判定（ray casting）」「winding number」を使い分ける。連続ループのトポロジーを確認したいなら winding number を。
- 視認性評価は幾何的包囲だけでなく、遮蔽モデル（ray castingによる可視判定）を入れる。シミュレータ上で視線を射出してテストすること。
- ロボットやドローンのパス設計では、対象の「表面法線」や向きも考慮する（例：カメラが正面を向いているかで意味が変わる）。
- テストケース設計：中心オブジェクトと接触する小さな対象（リスのような）を使い、包囲は成功でも視認失敗になるケースを用意しておく。
- 簡単な手早い実装例（点に対する巻数の離散計算）を試し、可視性テストと組み合わせて評価する。

```python
# python
import math

def winding_number(path, px, py):
    total = 0.0
    n = len(path)
    for i in range(n):
        x1,y1 = path[i]
        x2,y2 = path[(i+1)%n]
        ang1 = math.atan2(y1-py, x1-px)
        ang2 = math.atan2(y2-py, x2-px)
        d = ang2 - ang1
        if d <= -math.pi: d += 2*math.pi
        if d > math.pi: d -= 2*math.pi
        total += d
    return round(total / (2*math.pi))
```

