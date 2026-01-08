---
  layout: post
  title: "Ring programming language version 1.25 is released! - Ring 1.25がリリースされました！"
  date: 2026-01-06T22:07:52.661Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://ring-lang.github.io/doc1.25/whatisnew25.html"
  source_title: "What is new in Ring 1.25 &mdash; Ring 1.25.0 documentation"
  source_id: 469324057
  excerpt: "Ring 1.25はC生成・ML高速化・Pico対応で試作と組込みが高速化"
---

# Ring programming language version 1.25 is released! - Ring 1.25がリリースされました！
Ring 1.25で広がる可能性：C生成・機械学習アクセラレーション・セキュリティ強化でプロトタイプがもっと速くなる

## 要約
Ring 1.25は、Cコード生成ツールや機械学習向け拡張、セキュリティチェック関数、ネットワーク用のコールバック強化などを含む大幅アップデートで、プロトタイピングから組み込み開発、Web/GUI/ゲームまで実用領域を広げます。

## この記事を読むべき理由
日本の開発者やものづくりコミュニティにとって、手早く試作できる言語が「Cの生成」「Raspberry Pi Pico対応」「ML用高速ライブラリ」を手に入れたことは魅力的です。少人数チームやハック用途での生産性向上、また組み込み／セキュアな実運用を考える際の選択肢として注目に値します。

## 詳細解説
主な追加・改善点を技術的に整理します。

- 付属アプリとサンプル
  - Stock Analysis（Yahoo Financeから時系列取得、モメンタム解析、ベンチマーク比較）やRingVaders（Allegroで作られたゲーム）、Im2ANSI（画像→ANSI/ASCII変換）などの実例パッケージが増え、Ringで「作って試す」までの敷居が下がっています。
  - サンプル群も増強され、Qt関連やNaturalLibの上級例、天文計算など実務寄りの例が豊富。

- 言語／ランタイムの拡張
  - Callable Functions as Methods：関数をオブジェクトのメソッドとして呼べる構文が追加され、関数オブジェクトと状態（属性）を自然に組み合わせられます。オブジェクト志向とファンクショナルの橋渡しが容易に。
  - Flexible Statement Separation / Newline Callbacks Inside Braces 等：文の区切りやブロック内の改行処理に柔軟性が増し、DSLライクな記述がしやすくなっています。
  - 内部識別子の翻訳やRingVM用の新API（RingVM_TranslateCFunction, RingVM_ErrorHandler, RingVM_RingoLists, RingVM_WriteRingo 等）は、C/C++などへ埋め込み／拡張する際の制御性を高めます。組み込み用途やホスティング環境でのエラーハンドリング拡張が期待できます。

- セキュリティとコード評価
  - TokensLibにcheckRingCode()が追加され、eval()する前に「安全なリスト表現か」を検査できます。キーワードや演算子のホワイトリスト指定が可能で、外部入力を評価する場面での安全性が大幅に向上しました。Ring NotepadやRingPMなど多くのツールがこのチェックを導入済みです。

- ネットワークと外部連携
  - RingLibCurlの強化で、書き込み／ヘッダ／進捗／アップロード読み込みなどをコールバックで受け取れるようになりました。HTTP連携が多いアプリで非同期風の処理が書きやすくなります。

- パッケージ／エコシステム
  - RingPMに多数の新パッケージ：Argon2/Bcrypt（ハッシュ）、LibSQL、UUID、RingTensor / RingML（行列・NN向け）、RingQML、Ring-HTML、Ring2EXE-Plusなど。特にRingTensorは行列計算を高速化する拡張で、プロトタイプの機械学習実験がローカルで試せます。
  - MyCTiger：RingからCソースを生成し、実行ファイルまで作るツール。生成Cを使えば性能と移植性（マイコンなど）を両立できます。Raspberry Pi Pico向けの活用シナリオも想像しやすいです。

- 開発体験
  - RingQtでデスクトップ／モバイル／WebAssembly対応、フォームデザイナ、Ring2EXEやDocker/Heroku対応など、デプロイとUI作りのパイプラインが揃っています。小規模チームでの「試作→配布」までが短くなりました。

## 実践ポイント
すぐに試せる具体的アクション：

- RingとRingPMでパッケージを入れて動かす（まずはサンプルを動かして感触を掴む）
  ```bash
  # bash
  ringpm install stockanalysis
  ringpm install im2ansi
  ringpm install ringvaders
  ```

- セキュリティ対策：外部からのコード評価は必ずcheckRingCode()を通す。設定ファイルやプラグインを読み込む前に呼び出して安全性を検証する。
  - TokensLibのcheckRingCode([:code=... , :safekeywords=[...], :safeoperators="..."]) を活用する。

- 組み込み／マイコン用途のプロトタイプにはMyCTigerを試す
  - Ringの柔軟な記法でDSLを作り、MyCTigerでCに変換してマイコン向けにビルドするワークフローを検討する。

- ネットワーク連携はRingLibCurlのコールバックを使う
  - 大きなレスポンスやストリーム処理、進捗表示などはコールバックで受け取り、UI／ログに逐次反映する。

- ML／数値処理の実験：RingTensorやRingMLで簡単な行列演算や小規模NNを試し、性能感を把握する。必要ならC拡張でボトルネックを詰める。

- 貢献／カスタム拡張
  - RingはC/C++での拡張やVM APIが整っているので、社内ライブラリや特殊デバイス向けのバインディング作成を検討すると、プロダクト化が早くなります。

まとめ：Ring 1.25は「プロトタイプを速く作り、必要ならCレベルへ落とし込める」流れを強化しました。日本のハード・ソフト融合プロジェクトやスタートアップ、教育用途でも試す価値が高いリリースです。興味があれば最初にサンプルパッケージを動かして、NaturalLib＋MyCTigerの組合せで小さなDSLを作るところから始めるのが近道です。
