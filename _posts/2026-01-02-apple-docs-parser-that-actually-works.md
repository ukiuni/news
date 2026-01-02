---
  layout: post
  title: "Apple Docs Parser that actually works? - なぜ私はApple DocCのカスタマイズを諦め、自分でパーサを書いたか"
  date: 2026-01-02T17:08:53.572Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://nedimf.substack.com/p/why-i-gave-up-on-customizing-apple"
  source_title: "Why I Gave Up on Customizing Apple DocC and Wrote My Own Parser Instead"
  source_id: 474100358
  excerpt: "DocCの限界を突破、Goで.doccarchiveを変換して高速で実用的なAPIドキュメントを生成"
  image: "https://substackcdn.com/image/fetch/$s_!irmi!,w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02038a35-5032-4854-8619-89d4fc6569b5_2376x1534.png"
---

# Apple Docs Parser that actually works? - なぜ私はApple DocCのカスタマイズを諦め、自分でパーサを書いたか
クリックせずにはいられない：DocCを無理に曲げるより「変換」したほうが早い—実運用で効くdocc2jsonの舞台裏

## 要約
AppleのDocCはXcode向けの優れたドキュメントレンダラだが、WebやSDK配布向けにカスタマイズするには不向きだった。著者は最終的にGoで独自のdocc2jsonパーサを作り、DocCを「ソース」として変換するアプローチで解決した。

## この記事を読むべき理由
日本でもiOS/SwiftのSDKを公開するチームや、複数プラットフォームで統一したドキュメントポータルを運用する開発者は、DocCの限界にぶつかりやすい。DocC任せにして失敗する前に、現実的な代替と実装の肝を知っておく価値がある。

## 詳細解説
- DocCの本質：DocCは「レンダラ」であり、Xcode向け表示に最適化された大量のJSON（.doccarchive内）を出力する。だが公開APIや拡張フック、安定したデータモデルは提供しない。
- JSONの扱いにくさ：メソッド署名が文字列ではなくトークン配列で表現され、型名はマングリングされる（例：Sendableが内部表現に変わる）。ドキュメント本文は断片化され、期待するフィールドにテキストが無いこともある。
- カスタマイズ不可能性：DocC側でシンボルのグルーピングやナビゲーションの決定が行われ、開発者側で論理的セクションや独自のフィルタ（公開APIのみ、標準ライブラリ除外など）を強制できない。
- 解決策（docc2json）：著者はGoでCLIツールを作成し、.doccarchiveを走査して並列処理で多数のJSONを解析、トークンから署名を再構築、参照解決、文字列復元、マングリング解除、標準プロトコルの自動除外を行い、Web/ツール向けのクリーンなJSONスキーマを出力する。Goの並列処理で数万ファイルを超高速に処理できる点も強調されている。

## 実践ポイント
- 「DocCをいじる」より「DocCをソースとして変換する」方が現実的：カスタムUIや独自のグルーピングが必要なら、変換パイプラインを作る。
- 小さく検証する：まずは小さな.doccarchiveで署名再構築とドキュメント復元のルールを試す。
- 重要処理：トークン→署名再構築、ID参照解決、マングリング解除、ドキュメントセクション再連結は優先して実装する。
- ツール選び：並列処理とバイナリ配布を考えるならGoは有力。CIに組み込んでビルド時に変換を自動化するのが実運用向け。
- 日本市場での活用：日本語ローカライズや既存のドキュメントポータルとの統合（API参照の整合、SEO対応、アクセシビリティ）を前提に変換後のJSONにメタ情報を付与しておくと良い。

短期的にはdocc2jsonのような「DocC→自前スキーマ」変換が最も現実的な選択肢。DocC自体は良いツールだが、Webやカスタムドキュメント体験を本気で作るなら「変換してから描画する」設計を検討してみてください。
