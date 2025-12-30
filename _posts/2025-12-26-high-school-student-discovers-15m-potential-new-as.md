---
layout: post
title: High School Student Discovers 1.5M Potential New Astronomical Objects - 高校生、150万個の潜在的な新しい天体を発見
date: 2025-12-26 15:29:35.585000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://www.smithsonianmag.com/smart-news/high-school-student-discovers-1-5-million-potential-new-astronomical-objects-by-developing-an-ai-algorithm-180986429/
source_title: High School Student Discovers 1.5 Million Potential New Astronomical
  Objects by Developing an A.I. Algorithm
source_id: 46392815
excerpt: 18歳がNEOWISEの2000億行をAI解析し、約150万の新天体候補を抽出したVarWISE公開
---
# High School Student Discovers 1.5M Potential New Astronomical Objects - 高校生、150万個の潜在的な新しい天体を発見

## 要約
18歳のマッテオ・パズが、NEOWISEの未活用データ約2000億行を機械学習で解析し、約1.5百万の変光天体候補を抽出した。成果はVarWISEカタログとして公開され、天文学コミュニティで注目を集めている。

## この記事を読むべき理由
大規模時系列データに対する実践的なML適用例であり、日本の研究者やデータサイエンティスト、学生にとって「小さなチームでも発見を生む」現実的な道筋を示すから。天文データ解析の手法は地球観測や産業データにも横展開可能で、国内研究・教育の参考になる。

## 詳細解説
- 背景：NASAの近地球天体赤外線観測機器NEOWISEは2009年以降、近地球小惑星探索を主目的に観測を続け、多数の時系列赤外線検出（検出ごとの記録）を蓄積していた。しかし全データは解析され切れておらず、変光（時間に応じて輝度が変わる現象）を示す天体の検出が未整備だった。
- データ規模：解析対象は「検出ごとのテーブル」約2000億行。手作業では到底追い切れない規模で、従来はサブセットだけが解析されていた。
- アプローチ：パズはCaltechのメンター（Davy Kirkpatrick）と共に、時系列データ内の微小な赤外線変動を自動で拾う機械学習モデルを設計・学習させた。ポイントは「時系列（temporal）フォーマット」の変動検出に特化させたことで、ノイズや偽陽性を抑えつつ変化シグナルをスケールして抽出した。
- 成果：モデルは約150万件の変光候補（超新星候補、活動的な降着天体やバイナリなどを含む）をフラグし、VarWISEというカタログにまとめられた。CaltechやNEOWISE関係者はこのカタログを既に研究に利用している。
- 応用可能性：パズ自身は、この手法が任意の「時系列データ」に適用可能だと指摘している（例：大規模な株価チャート解析、大気汚染の時間変動解析など）。

## 実践ポイント
- 学びの出発点：まずPython（pandas, numpy）と時系列解析、機械学習（scikit-learn, PyTorch/TensorFlow）を実務レベルで習熟する。
- データ取得：公的天文データ（NASA/IPAC, NEOWISEアーカイブ, ZTF, Pan-STARRS 等）は公開されている。小さなサブセットから試してパイプラインを構築する。
- モデル設計：時系列ノイズ除去、特徴量（周期性、フラックス変化の統計量）、異常検知モデル（autoencoder, isolation forest, RNN系）を組み合わせると実用的。
- 計算基盤：数百億行の処理には分散処理やクラウド（GCP/AWS/Azure）の利用、バッチ処理、効率的なI/O設計が必須。
- 共同と公開：小さな発見でも公開カタログやプレプリントで共有することで、他研究者のフォローアップを促せる。メンターや研究機関と連携する価値は高い。
- 日本市場への応用：JAXAや国内望遠鏡の時系列観測データ、地球観測（大気汚染・森林火災の時間変動）に同手法を適用できる。高校・大学の教育プログラムに組み込み、若手の実戦的研究機会を増やすことも有効。

