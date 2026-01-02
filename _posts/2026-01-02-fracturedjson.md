---
  layout: post
  title: "FracturedJson - フラクチャードJson"
  date: 2026-01-02T13:04:56.310Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/j-brooke/FracturedJson/wiki"
  source_title: "Home · j-brooke/FracturedJson Wiki · GitHub"
  source_id: 46464235
  excerpt: "一目で分かる表形式や多列表示でJSONを自動整形しレビュー効率を劇的に向上させる"
  image: "https://repository-images.githubusercontent.com/304152687/a82ee280-1ba9-11eb-9932-339cbd5a28fa"
---

# FracturedJson - フラクチャードJson
人間が一瞬で理解できるJSONに変えるフォーマッタ — 見た目で差がつく「読める」JSON整形術

## 要約
FracturedJsonは、可読性を最優先にしつつコンパクトさも保つJSON整形ツール群で、ブラウザ・.NET・JavaScript/TypeScript・VS Code・Pythonなど複数プラットフォームで利用可能。配列やオブジェクトを状況に応じて1行、表形式、複数列の縮約、あるいは展開表記に切り替えることで読みやすさを最大化する。

## この記事を読むべき理由
設定ファイルや大きなデータ構造を扱う日本の開発現場では、読みやすいJSONがデバッグ・コードレビュー・差分確認の生産性を直接改善する。VS CodeやCIに組み込めばチームの作業効率がすぐ向上する。

## 詳細解説
- 意図：ミニファイ（圧縮）と従来のインデント整形の中間を目指す。人が「ざっと見て理解できる」出力を自動生成する。  
- フォーマット手法（4種）  
  - Inlined（インライン）: 複雑さと長さが条件を満たす場合、オブジェクト/配列を1行で表記。MaxInlineComplexityで許容するネスト深度を制御。  
  - Compact Multiline Array（多列コンパクト配列）: 長い配列は複数アイテムを1行に並べつつ複数行で表示。MaxCompactArrayComplexityで深さを調整（-1で無効化）。  
  - Table（表形式）: 同種の要素が続く配列やオブジェクトはフィールドを整列しテーブル状に表示。必要に応じてフィールド順を入れ替え、内側のコンテナを折りたたんで全体を収める。MaxTableRowComplexityで行のネスト許容度を制御。TableCommaPlacementでカンマ位置を調整可能。  
  - Expanded（展開）: 上記が適さない要素は従来の複数行展開（子要素は改行＋インデント）で出力。  
- コメントの扱い：JSON標準はコメント非対応だが、実務上コメント付きJSONは多いため"コメント保持"オプションがあり、関連する要素とコメントをできるだけ一緒に保つ。  
- 実装形態：ブラウザベースのフォーマッタ、.NETコアのライブラリ／CLI、npmパッケージ（JS/TS）、Visual Studio Code拡張、Python向けラッパー等が用意されているため既存ワークフローへの導入が容易。  
- 実際の動作例：似た構造のオブジェクト群はフィールド揃えでテーブル表示され、長い座標配列は複数列で圧縮表示されるため視認性が大きく向上する。

## 実践ポイント
- まずブラウザ版で手早く試す。フォーマット例を比較してチーム合意を作る。  
- VS Code拡張を導入して保存時フォーマットを有効にすると差分が読みやすくなる。  
- CIに組み込み、PRで整形ルールを自動適用してレビュー負荷を低減する。  
- 設定例：MaxInlineComplexityを調整して1行表示の許容度を決める。大規模ネストは-1で無効化して可読性を優先することも有効。  
- コメント保持をオンにしてドキュメント的コメントを残しつつ整形する（設定で挙動を確認）。  
- 設定をチームのコーディング規約としてリポジトリに保存すれば、異なるエディタ間でも一貫した見た目を維持できる。

## 引用元
- タイトル: FracturedJson  
- URL: https://github.com/j-brooke/FracturedJson/wiki
