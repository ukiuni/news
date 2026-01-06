---
  layout: post
  title: "CES 2026: Taking the Lids Off AMD's Venice and MI400 SoCs - CES 2026：AMDのVeniceとMI400 SoCのベールを剥ぐ"
  date: 2026-01-06T23:13:38.212Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://chipsandcheese.com/p/ces-2026-taking-the-lids-off-amds"
  source_title: "CES 2026: Taking the Lids off AMD&#x27;s Venice and MI400 SoCs"
  source_id: 46519326
  excerpt: "CESで公開：AMDのVeniceとMI400がHBM4・最大256コア級でパッケージ刷新"
  image: "https://substackcdn.com/image/fetch/$s_!qd_2!,w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc4e23adc-da36-42af-b245-11459f567dcc_1674x960.png"
---

# CES 2026: Taking the Lids Off AMD's Venice and MI400 SoCs - CES 2026：AMDのVeniceとMI400 SoCのベールを剥ぐ
EPYC史上最大級のパッケージ変化と、HBM4を抱える超大型MI400──CESで見えた「本当のサイズ感」

## 要約
AMDがCES 2026でVenice（サーバー向けZen 6）とMI400（データセンター向けアクセラレータ）の実物シリコンを初公開。パッケージ設計やダイ構成が大きく変わり、コア数・IO容量・HBM構成がスケールアップしている。

## この記事を読むべき理由
日本のクラウド事業者、HPCやAIインフラを扱う企業、サーバー設計者にとって、VeniceとMI400は次世代の計算基盤・消費電力・冷却要件に直結する製品。早めに設計や調達方針を検討する価値がある。

## 詳細解説
- Venice（EPYC系Zen 6）
  - CCDとIOダイの接続/パッケージングが従来の有機基板経由から、Strix HaloやMI250Xに似た高度な実装に変化。これにより電気的性能や密度が改善される可能性が高い。
  - ダイ構成はCCD×8、各CCDが32コアでパッケージ最大で $8\times32=256$ コアを実現する想定。
  - 各CCDは約165 mm²のN2プロセスと推定。もしコアあたりL3を4MBで維持すると、CCDあたりL3は128MB。
  - Zen 6コア＋4MB L3の面積はコアあたり約5 mm²（Zen 5世代の値と類似）。
  - IOダイは2つ構成で、それぞれ約353 mm²、合計で約700 mm²超と大幅に拡大（従来の約400 mm²から増加）。これがI/O帯域・メモリチャネル・PCIeの強化を示唆。
  - パッケージ両端の小さなダイ群は、構造用シリコンか深掘りキャパシタ（deep trench capacitor）で、電力供給安定化に寄与する可能性。

- MI400（データセンターGPU/アクセラレータ）
  - パッケージは12枚のHBM4スタックを搭載。2つのベースダイ（各約747 mm²）と、上下に配置されたオフパッケージIOダイ（各約220 mm²）が確認される。
  - 計算チップレットは合計でおそらく8個（各ベースダイに4個ずつ）。各コンピュートダイは概算で140–160 mm²、最大で約180 mm²程度が推定。
  - MI440X/MI430X/MI455Xといったラインナップの拡充が発表され、MI440Xは8-way UBBボックス向けにMI300/350の置換を想定。

- Venice‑X（V‑Cache版）の示唆
  - V‑Cache版（Venice‑X）が登場すると、1CCDあたり最大384MBのL3（同比率なら）となり、チップ全体で約$3\ \mathrm{GB}$のL3キャッシュに到達する可能性がある。キャッシュ依存のワークロードで劇的な性能改善が見込まれる。

## 実践ポイント
- インフラ計画：IOダイ増大とHBM4搭載は帯域幅と電力消費の増大を意味する。ラック電力・冷却能力を再評価すること。
- ソフトウェア最適化：多コア化（最大256コア）と大容量L3を活かすため、スレッド配置・キャッシュフレンドリーなアルゴリズムを検討する。
- ハード選定：MI440Xのような製品は既存MI300/350搭載システムの置換候補。8-way UBB互換性を確認して長期調達計画に組み込む。
- ベンダー連携：マザーボード／BIOSベンダー、OSベンダーと早めに連携し、PCIe/UALinkや電源管理のサポート状況を確認する。
- ベンチマーク計画：V‑Cacheの実効効果やHBM4の実効帯域を自社負荷で検証し、導入価値を数値で示す。

CESでの「見た目」が示すのは、単なるスペックアップではなくパッケージ設計の転換。日本の現場でも電力・冷却・ソフト最適化の観点から、早めに検討を始める価値がある。
