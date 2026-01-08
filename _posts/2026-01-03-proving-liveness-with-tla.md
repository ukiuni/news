---
  layout: post
  title: "Proving Liveness with TLA - TLAで生存性（liveness）を証明する"
  date: 2026-01-03T03:11:38.024Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://roscidus.com/blog/blog/2026/01/01/tla-liveness/"
  source_title: "Proving liveness with TLA - Thomas Leonard's blog"
  source_id: 46471699
  excerpt: "TLA+/TLAPSで必ず起きることをXen vchan事例で実証する手順と回避策"
---

# Proving Liveness with TLA - TLAで生存性（liveness）を証明する
魅力的な日本語タイトル: TLA+で「必ず起きること」を証明する技術 — Xen vchanで学ぶ生存性の作法

## 要約
TLA+ Toolbox（TLAPS含む）で「生存性」（ある状態がやがて実現すること）を実証する手順と落とし穴を、単純チャネルモデルからXenのvchan実プロトコルまで試した解説。TLAPSの現在の限界と回避策も具体例で示す。

## この記事を読むべき理由
分散・仮想化・通信ミドルウェアを扱うエンジニアは、データが「必ず届く（Availability）」ことを数学的に保証したい場面が増えています。日本のクラウド／仮想化現場でも役立つ実践的パターンとTLAPS固有のワークアラウンドが得られます。

## 詳細解説
まず考えるのは「一方通行チャネル」の簡単モデル（送信者と受信者、サイズ$BufferSize>0$の共有バッファ）。状態変数は送信済みバイト数$Sent$と受信済みバイト数$Got$だけです。バッファ使用量と空きは
$$
BufferUsed = Sent - Got,\quad BufferFree = BufferSize - BufferUsed
$$
で表されます。

狙いの性質（Liveness）は次です：
$$
Liveness \equiv \forall n\in\mathbb{N}:\ (Sent = n)\ \Rightarrow\ \lozenge (Got \ge n)
$$
「ある時点で$Sent=n$なら、やがて$Got\ge n$になる」。

TLAでアルゴリズムは初期条件と「一歩ごとのアクション」で書きます。代表的なアクションは次のように表現できます（簡略）：

```tla
CONSTANT BufferSize
VARIABLES Sent, Got

Init == /\ Sent = 0 /\ Got = 0

Send == \E n \in 1 .. BufferFree : /\ Sent' = Sent + n /\ UNCHANGED Got

Recv == /\ BufferUsed > 0 /\ Got' = Got + BufferUsed /\ UNCHANGED Sent

Next == \/ Send \/ Recv

Spec == /\ Init /\ [][Next]_<<Sent, Got>> /\ WF_<<Sent, Got>>(Recv)
```

ポイント解説：
- Specに含めた弱公正性 WF_vars(Recv) により、「受信可能な状態が無限に続くなら受信はやがて行われる」と保証される。これは生存性証明の要。
- まず不変量（SentとGotは自然数で、常にSent >= Gotなど）をTLAPSで機械証明しておくと、以降の議論が楽になる。これらは大半が通常の（一時点の）論理だけで扱える。

TLAPS（TLA Proof System）の現状とコツ：
- TLAPSは「非時相（非-modal）な証明」はよく扱えるが、時相演算子（[] や <>）を含む命題は扱いが限られる。時相部分は PTL（Propositional Temporal Logic）に委ねられるが、PTLは第一階述語論理の多くを知らない。
- そのため「[]P => Q」のようなステップは、まず非時相の補題（時相演算子を含まない）を証明してから、PTLステップで一般化する、という分割戦略が必須。
- TLAPSは内部で「分かち替え（coalescing）」を行い、ソルバが扱えない部分を一時変数に置き換える。このため「今の世界のみで成り立つ」仮定を残したままだと一般化できず失敗することがある。解決策は補題化か、該当命題を先に証明してから時相的結論を述べること。
- 定義の「隠蔽（HIDE DEF）」や、時相式を関数で包んでおく手法（例：L1_prop(n) == ...）は、TLAPSのバグや一般化の制約を回避する実用テクニック。ただし記事ではTLAPSのバグ（同じ式でも失敗・成功を繰り返す事例）も報告されており、そのときは名称を変えたり小分けにして試す必要がある。

生存性証明の典型パターン（単ステップで到達できる場合）：
A ~> B（AからやがてBへ）を証明するには、しばしば以下の条件を示す：
- A /\ Recv ==> B'  （Aかつ受信アクションで次にBが成り立つ）
- A ==> ENABLED <<Recv>>_vars  （Aなら受信が可能）
- WF_vars(Recv)  （受信アクションは公正である）
- A /\ [Next]_vars ==> (A \/ B)'  （Aにいる限り次はAかB）
これらを組み合わせて PTL 一段で結論を出すのがパターンです。

実プロトコル（Xen vchan）に戻すと、単純例より状態数やアクションが増えるため、
- 「ReadLimit」「WriteLimit」「Availability」などの性質ごとに分割して証明
- まずTLCで小モデルを回してバグや想定違いを検出
- 不変量と局所補題を多用して時相推論は最小化
といった実務的な流儀が有効です。

## 実践ポイント
- まずTLCで小さなパラメータ範囲をモデルチェックして構造ミスを潰す。
- 不変量（types・順序関係）は最初に証明しておくと時相証明が楽に。
- PTLステップを最小化：時相式は補題化して非時相部分だけで証明→最後にPTLで一般化する。
- ENABLEDやWFの扱いを明示し、公正性条件をSpecに入れる（WF/ SFの違いに注意）。
- TLAPSの挙動に依存しないために、時相式は関数で包み HIDE DEF や SUFFICES を活用する。バグに遭遇したら命名や分割で回避する。
- Xen/vchanのような仮想化通信実装に対しては、単体のバッファ操作だけでなく、障害や遅延・再試行を考慮したモデル化も行い、日本のクラウド運用（商用VM、オンプレVDI等）での事故防止に活用する。

この記事で取り上げた手法は、単なる学術演習ではなく、仮想化ミドルウェアや分散システムの信頼性を高める実務スキルです。まずは小さなチャネルモデルでTLAPSの分割証明パターンを練習すると良いでしょう。
