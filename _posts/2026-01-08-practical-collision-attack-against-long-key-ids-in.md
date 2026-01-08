---
  layout: post
  title: "Practical Collision Attack Against Long Key IDs in PGP - PGPのLong Key IDに対する実用的な衝突攻撃"
  date: 2026-01-08T02:14:52.064Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://soatok.blog/2026/01/07/practical-collision-attack-against-long-key-ids-in-pgp/"
  source_title: "Practical Collision Attack Against Long Key IDs in PGP - Dhole Moments"
  source_id: 1743036328
  excerpt: "実証済み：PGPの64ビット長キーIDは数日で衝突し、ID確認だけは危険"
  image: "https://i0.wp.com/soatok.blog/wp-content/uploads/2026/01/BlogHeader-2026-PGP-LongKeyIDs.png?fit=1200%2C675&#038;ssl=1"
---

# Practical Collision Attack Against Long Key IDs in PGP - PGPのLong Key IDに対する実用的な衝突攻撃
見出し：PGPの「長いキーID」は安全じゃない？数日で同一IDを作れる実話とその対策

## 要約
OpenPGP/GnuPGの「Long Key ID」（64ビット）は誕生日攻撃で実際に衝突が作れることが示され、短い確認手順に依存すると偽鍵に騙されるリスクがあることが実証されました。

## この記事を読むべき理由
日本でもOSSパッケージやリポジトリの署名検証、開発者間の鍵交換にPGPを使う場面は多く、手順として「Key IDだけ確認する」運用をしていると、実害につながる可能性があるため必読です。

## 詳細解説
- 問題の本質：OpenPGPのLong Key IDは64ビットの出力空間を持ち、出力空間が小さいため誕生日攻撃に弱い。出力空間が $2^{64}$ であれば、衝突の期待値は約
$$\sqrt{2^{64}} = 2^{32} \approx 4.3\times10^9$$
となり、十分なリソースがあれば現実的に衝突を見つけられます。
- 実証（概要）：記事著者は2つの異なる公開鍵（と対応する秘密鍵）を作り、長いKey ID（64ビット）が一致する事例を提示。gpgの表示上は同じKey IDに見えるが、フルフィンガープリントは異なるため、見かけ上の同一性に騙され得ます。
- 手法：ラップアップすると、著者はノートPCで数日かけて大量に鍵を生成し（鍵生成＋タイムスタンプ等を変数にしてバリエーションを作成）、各組み合わせのLong Key IDを計算してソートし衝突を探索。クラウドを使えばさらに高速化可能です。
- 実際のリスク：攻撃者があらかじめ衝突する鍵を作っておき、被害者がKey IDしか確認しない運用（READMEや署名検証手順でKey IDを案内しているなど）の場合、配布先の公開鍵を偽鍵に差し替えられると、検証が通りバックドア入りのソフトを受け取ってしまう危険があります。衝突は事前準備型の攻撃であり、検出が難しい点も問題です。

## 実践ポイント
- Key IDだけで検証しない：必ずフルフィンガープリント（fingerprint）を確認する。コマンド例：gpg --fingerprint <鍵ファイル>（短縮確認は危険）。
- ツールとドキュメントを更新：導入手順やREADME、署名検証の説明から「Key ID確認」だけの案内を排除し、フルフィンガープリント確認を明記する。
- 署名チェーンの強化：信頼できる配布チャネル（公式サーバ、HTTPS、署名のタイムスタンプや透明性ログなど）や、可能ならsigstore等の新しい署名基盤の導入を検討する。
- 運用的対策：配布鍵は複数の独立経路でチェックする、キーサーバー運用を監査する、重要なパッケージは複数の署名を要求する等の防御を追加する。
- 開発者向け：自分のプロジェクトで公開する公開鍵はリリースページにフルフィンガープリントを明記し、ユーザーにはコピペで確認できるようにしておく。

この事件は「暗号の直感的な安全性」に疑問符をつける良い教訓です。PGPを使う現場では、短いIDに頼るクセを今すぐ見直してください。
