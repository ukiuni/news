---
  layout: post
  title: "A lightweight, client-only spreadsheet web application. All data persists in the URL hash for instant sharing, No backend required. Optional AES-GCM password protection keeps shared links locked without a server - 軽量・クライアント完結のスプレッドシート：URLハッシュで状態を共有、サーバ不要。AES-GCMでリンクをロック可能"
  date: 2026-01-01T19:08:27.569Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/supunlakmal/spreadsheet"
  source_title: "GitHub - supunlakmal/spreadsheet: A lightweight, client-only spreadsheet web application. All data persists in the URL hash for instant sharing, No backend required. Optional AES-GCM password protection keeps shared links locked without a server"
  source_id: 473579723
  excerpt: "サーバ不要でURL共有、AES-GCMで鍵付き保存できる軽量スプレッドシート"
  image: "https://repository-images.githubusercontent.com/1124524892/10291cc9-9e5f-4ec9-8cf7-8a31ac967b62"
---

# A lightweight, client-only spreadsheet web application. All data persists in the URL hash for instant sharing, No backend required. Optional AES-GCM password protection keeps shared links locked without a server - 軽量・クライアント完結のスプレッドシート：URLハッシュで状態を共有、サーバ不要。AES-GCMでリンクをロック可能
驚くほどシンプルに共有できる“URLだけで完結する”スプレッドシート — サーバ不要で即シェア、必要ならブラウザ内でAES-GCM暗号化して鍵付きリンクに

## 要約
ブラウザだけで動く軽量スプレッドシート。全データはLZ-Stringで圧縮してURLハッシュに格納され、コピーで即共有。任意でPBKDF2→AES-GCMによるクライアント側暗号化を行い、パスワード付きURLとして配布できる。

## この記事を読むべき理由
- 社内で手軽に表を共有したいがサーバ構築やホスティングを避けたい開発者／プロダクト担当者に最適。
- URLだけで状態を完結させるアプローチは、プライバシー配慮（パスワード暗号化）やライブデモ配布、ハックデイのプロトタイプで有効。
- 日本の業務環境（Slack/LINE共有、イントラでの簡易共有、教育用途）にマッチする実用性が高い。

## 詳細解説
- クライアント完結の設計  
  - アプリはVanilla HTML/CSS/JSで実装。全状態（セル内容、表示式、スタイル、行列サイズ、テーマ等）はJSON化してLZ-Stringで圧縮し、URLハッシュに保存。サーバは不要で、単にURLを渡すだけで同じ表が再現される。
- 共有と暗号化の仕組み  
  - 暗号化はWeb Crypto APIで、PBKDF2（100kイテレーション、ランダムソルト）で鍵派生→AES-GCM（256ビット、ランダムIV）。暗号化ペイロードはURLセーフなBase64で格納され、ENC:プレフィックスを付与。パスワードはブラウザから外に送信されず、受信者がローカルで復号する方式。GCMにより改ざん検出も可能。
- 機能面のポイント  
  - グリッドは最大30行×15列（A–O）、デフォルト10×10。セル編集、フォント/色/配置スタイル、B/I/Uショートカット、セル選択（ドラッグ／Shift拡張）、列幅/行高調整をサポート。CSVのインポート/エクスポート（式は保持）も可能。式は =SUM / =AVG の範囲サポートおよびオートコンプリート機能を備える。
- 永続性と履歴  
  - 編集は200msでデバウンスしてURL更新。ブラウザの戻る／進むで過去状態を復元できる（履歴保存）。
- セキュリティと洗練された実装上の配慮  
  - 入力HTMLはDOMParserベースでホワイトリスト化、式は正規表現で検証、長すぎるハッシュは拒否する等のガードあり。CSPを設定し、URLハッシュはGoogle Analyticsの追跡から除外する配慮もある。
- 制約と注意点  
  - URL長の制限（特に大きな表や暗号化時）や、暗号化したリンクはパスワードを失うと復旧不可、式はSUM/AVGに限定などの機能上のトレードオフがある。

## 実践ポイント
- すぐ試す：リポジトリをクローンしてローカルで動かすか、配布されているデモ（spreadsheetlive.netlify.app）で確認。ローカル起動は例：  
  ```bash
  npx serve .
  ```
- 即シェア：作成後にURLをコピーして共有。簡易議事メモやテンプレート配布、ワークショップのハンズオン資料に便利。
- 機密データを共有するなら：必ず「Lock（パスワード設定）」を使う。パスワードはブラウザ外には送られないが、パスワード紛失は復元不可なので管理に注意。
- URL長短縮の工夫：大きな表なら列・行を最小化して不要データを削除する、またはCSVで分割して配布する（暗号化済みURLは通常より長くなる）。
- 検討すべき実運用ルール（日本向け提案）  
  - 社内共有用はパスワード付きURL＋社内パスワード配布ルールを決める。  
  - 公開リンクは運用ポリシーに沿って期限を決め、ログやキャッシュに残るリスクを説明する。  
  - 教育用途ではファイル配布を省いて即時演習に使えるため、授業での導入コストが低い。
- 開発者向け：拡張ポイントは式の種類追加、URL短縮サービスとの連携、サーバ不要の共同編集（CRDT等）検討。社内ツール化するなら、許容できるURL長と暗号ポリシーを事前に評価する。

## 引用元
- タイトル: A lightweight, client-only spreadsheet web application. All data persists in the URL hash for instant sharing, No backend required. Optional AES-GCM password protection keeps shared links locked without a server
- URL: https://github.com/supunlakmal/spreadsheet
