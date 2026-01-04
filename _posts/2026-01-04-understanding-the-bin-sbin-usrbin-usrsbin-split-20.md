---
  layout: post
  title: "Understanding the bin, sbin, usr/bin, usr/sbin split - bin、sbin、usr/bin、usr/sbin の分割を理解する"
  date: 2026-01-04T16:25:22.870Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://lists.busybox.net/pipermail/busybox/2010-December/074114.html"
  source_title: "Understanding the bin, sbin, usr/bin , usr/sbin split"
  source_id: 46487921
  excerpt: "起源から実務的移行手順まで解説、/binと/usr/bin分割の整理法"
  ---

# Understanding the bin, sbin, usr/bin, usr/sbin split - bin、sbin、usr/bin、usr/sbin の分割を理解する
シンプルな歴史と現代的な結論：なぜ「/bin と /usr/bin の分離」は残っているのか、そして今どう扱うべきか

## 要約
Unix の初期設計（数メガバイトのディスク事情）で生まれた / と /usr の分割が、時代遅れになった理由と、現代のシステムや組込み機器での実務的な対処法を短く説明します。

## この記事を読むべき理由
この分割は歴史的な“遺物”だが、実際のシステム設計、ディストリビューション運用、組込み/IoT イメージ作成、コンテナ最適化に直接影響します。正しい理解があれば無駄な複雑化を避け、起動や更新のトラブルを減らせます。

## 詳細解説
- 起源：1970年代、Ken Thompson と Dennis Ritchie が PDP-11 上で OS を拡張する際、容量不足でシステムファイルを別ディスクに逃がし、そこで /usr をマウントしたことが分割の始まり。/usr 以下に /bin, /sbin, /lib… を複製して使い始めたのが元です。
- 起動順の制約：初期ブートで /usr をマウントできないと必要なコマンドが見つからない「ニワトリと卵」問題が発生。これが当時の運用ルールを生んだ理由です。
- なぜ時代遅れか：
  1. initrd / initramfs により、ブート時の依存関係は一時的なルートで解決可能になった。
  2. 共有ライブラリの普及で /lib と /usr/bin は組み合わせて一致している必要があり、別々に運用する利点が薄れた。
  3. 大容量ディスクとパーティション操作の普及で、物理容量制約が問題でなくなった。
- 派生的ルール：/usr/local, /opt, /var や /tmp の取り扱いなど、歴史的経緯から各ディストロが独自ルールを追加してきたため複雑化している点。
- 実務上の傾向：多くの現代システムや組込み向け構成では /bin, /sbin, /lib を /usr 以下に統合（あるいは /bin -> /usr/bin 等のシンボリックリンク）してシンプル化する例が多い。BusyBox は過去の慣習に合わせてバイナリを配置するだけ、というのが実情。

## 実践ポイント
- コンテナ/イメージ：可能なら /usr 統合を採用するとレイヤ構成やパッケージ管理が簡単になります。
- 組込みデバイス：最小イメージを作るときは BusyBox を使い、/lib と /usr の依存を揃えること。initramfs を使えばブート時の依存を柔軟に処理できます。
- ファイル配置の確認コマンド例：
```bash
# どのバイナリがどこにあるかを確認
which kill
readlink -f /bin/sh
ls -l /bin /usr/bin /sbin /usr/sbin
```
- シンボル的統合（注意して実施）：
```bash
# 例: /bin を /usr/bin に統合する（ルートで慎重に）
mv /bin /bin.backup
ln -s /usr/bin /bin
```
- 注意点：既存システムでの移行は依存関係を十分に検証すること。特に起動中に参照されるライブラリや init スクリプトのパスに注意。

短い結論：/bin と /usr/bin の分割は歴史的経緯によるもので、現代では多くの場合不要。用途（組込み、サーバ、コンテナ）に応じて統合かシンプルなシンボリックリンクで解決するのが実務的です。
