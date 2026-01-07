---
  layout: post
  title: "Everyone hates OneDrive, Microsofts cloud app that steals and deletes files - OneDriveがファイルを奪い削除する？Microsoftのクラウドアプリに批判噴出"
  date: 2026-01-07T15:06:10.442Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://boingboing.net/2026/01/05/everyone-hates-onedrive-microsofts-cloud-app-that-steals-then-deletes-all-your-files.html"
  source_title: "Everyone hates OneDrive, Microsoft&#039;s cloud app that steals then deletes all your files - Boing Boing"
  source_id: 46526376
  excerpt: "知らぬ間にファイルがクラウドへ移動しローカルから消えるOneDriveの危険と対処法"
  ---

# Everyone hates OneDrive, Microsofts cloud app that steals and deletes files - OneDriveがファイルを奪い削除する？Microsoftのクラウドアプリに批判噴出
魅力的な日本語タイトル: 「気づいたらファイルが消えている？OneDriveの“知らない間に同期・削除”問題を分かりやすく解説」

## 要約
Boing Boingの記事によれば、Windows上で自動的に有効になるOneDriveの挙動が原因で、ユーザーのファイルがクラウドへ移されローカルから消える事例が報告されています。設定が分かりにくく、パニックになるケースがあるとされています。

## この記事を読むべき理由
日本でもWindowsは広く使われ、OneDriveはプリインストールされています。知らないうちにクラウドへ移されたり、ローカルコピーが消えると業務・個人データに深刻な影響が出るため、仕組みと対処法を知っておくことが重要です。

## 詳細解説
- 問題の本質  
  元記事では「OneDriveがユーザーの既存ファイルをクラウドに移し、さらにローカルから削除してしまう挙動」が指摘されています。これにはユーザーに分かりにくいUI（いわゆるダークパターン）や、既定で有効になる「バックアップ（Known Folder Move）」や「Files On‑Demand」の仕組みが絡みます。

- Files On‑Demand とオンライン専用ファイル  
  OneDriveはローカルのファイルを「オンライン専用」にしてディスク容量を節約できます。見た目は残りますが中身はクラウドにあり、ネットワークがないと開けません。これを誤解すると「ファイルが消えた」と感じることがあります。

- Known Folder Move（デスクトップ/ドキュメント/画像の自動保管）  
  Windowsのセットアップやアップデート時に、OneDriveが既存のユーザーフォルダをクラウドへ移動するよう促す、あるいは勝手に有効化されるケースが報告されています。設定や説明が分かりにくく、オプトアウトしにくいと感じるユーザーが多いようです。

- 実際の被害とリスク  
  記事では、クラウド上にあるファイルを「ダウンロードしてからMicrosoftに削除させる」とローカルのファイルも再び消される、といった報告が紹介されています。見た目がランサムウェアに似ているため混乱を招く点も指摘されています。企業ではポリシーや管理者設定で制御できますが、個人環境だと対策が手薄になりがちです。

## 実践ポイント
- まず状態確認  
  - OneDriveのトレイアイコンを右クリックして設定を確認する（同期状況、バックアップ設定、Files On‑Demand）。
  - エクスプローラーでファイルのアイコンに「クラウド」マーク（オンライン専用）や緑のチェックが付いているか確認する。

- すぐできる対処
  - 「バックアップ」→「フォルダーの管理（Manage backup/Known Folder Move）」を確認し、不要なら停止する。
  - Files On‑Demandを無効にすると、オンライン専用ファイルをローカルにダウンロードして保持できる（ただし容量に注意）。
  - OneDriveの「このPCのリンクを解除（Unlink this PC）」で同期を止める。ただしリンク解除前に重要ファイルがローカルにあるか確認する。

- データ復旧の候補
  - OneDriveのウェブ版のごみ箱を確認する（クラウド上で削除されていれば復元可能な場合あり）。
  - Windowsのファイル履歴やバックアップ、外付けドライブから復元できるか確認する。

- 予防策
  - 重要ファイルはクラウドとは別にローカルのバックアップ（外付けHDDやNAS）を取る。
  - WindowsにMicrosoftアカウントでログインするかローカルアカウントで使うかのポリシーを明確にする。
  - 企業利用なら管理者がグループポリシーやIntuneでKnown Folder Move等を制御する。

元記事はOneDriveの強引な導入やUIの分かりにくさを批判しています。個人・企業を問わず、挙動を理解して設定を見直すことが被害を避ける最も確実な一歩です。
