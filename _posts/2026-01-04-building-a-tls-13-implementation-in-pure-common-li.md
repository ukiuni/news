---
  layout: post
  title: "Building a TLS 1.3 Implementation in Pure Common Lisp - 純粋な Common Lisp で書く TLS 1.3 実装"
  date: 2026-01-04T04:29:13.942Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://atgreen.github.io/repl-yell/posts/pure-tls/"
  source_title: "Building a TLS 1.3 Implementation in Pure Common Lisp | REPL Yell!"
  source_id: 711090239
  excerpt: "Common LispだけでOpenSSL不要のTLS1.3を実装し依存を排除"
---

# Building a TLS 1.3 Implementation in Pure Common Lisp - 純粋な Common Lisp で書く TLS 1.3 実装
OpenSSL不要へ：Common Lispだけで動くTLS 1.3を作ったら何が変わるのか？

## 要約
Common Lispで動く完全なTLS 1.3実装「pure-tls」は、Ironcladの暗号プリミティブとOSネイティブの信頼ストア連携を活用し、C依存を排した実験的だが実用的な代替手段を提示する。

## この記事を読むべき理由
- Windows/macOS/LinuxでOpenSSLのインストールやバイナリ依存に悩む日本の開発者にとって、プラットフォーム依存を減らす選択肢になる。  
- TLS 1.3という現代的プロトコルに絞ることで実装の攻撃面を抑えつつ、実運用に耐える設計判断（信頼ストア利用、サイドチャネル対策）が示されている。

## 詳細解説
- なぜTLS 1.3か：RFC 8446に基づき、レガシー機能を削ぎ落としてハンドシェイクが短く、攻撃面が小さい。サポートする主要暗号は ChaCha20-Poly1305, AES-256-GCM, AES-128-GCM。鍵交換は楕円曲線（X25519, P-256）に限定されるため実装がシンプルになる。
- 暗号基盤：IroncladがAES/ChaCha20/Poly1305、SHA-2、HMAC、楕円曲線演算を提供。pure-tlsはこれらを組織してTLS 1.3の鍵スケジュールとレコード層を実装する。
- 鍵スケジュール：HKDF連鎖で共有秘密からハンドシェイク用・通信用のシークレット／鍵／IVを導出する。この流れはRFCのテストベクタで検証可能。
  $$
  \text{shared\_secret} \xrightarrow{\text{HKDF}} \text{handshake\_secret} \xrightarrow{\text{HKDF}} \text{traffic\_secrets} \to \text{keys/IVs}
  $$
- I/O統合（Gray Streams）：Common Lispのグレイストリームを実装することで、アプリ側は普通のバイナリストリームを読み書きするだけでTLSが透過的に動作する。
  ```lisp
  (lisp
  (pure-tls:with-tls-client-stream (tls socket :hostname "example.com")
    (write-sequence request-bytes tls)
    (force-output tls)
    (read-sequence response-buffer tls)))
  ```
- 証明書検証：ASN.1/DERパーサを実装しつつ、ルート信頼はOS側のストアに委ねる設計（Linuxはファイル、WindowsはCryptoAPI、macOSはSecurity.framework）。WindowsではCFFI経由でCertGetCertificateChain等を呼ぶ。
  ```lisp
  (lisp
  (cffi:defcfun ("CertGetCertificateChain" %cert-get-chain) :boolean
    (chain-engine :pointer) (cert-context :pointer) ... ))
  ```
- cl+ssl互換レイヤー：既存ライブラリ（例：Drakma）との互換性を保つため、ASDFに「cl+sslが既に読み込まれた」と見せるトリックで差し替え可能。
- サイドチャネル対策：定数時間比較、エラーを均一化、ソフトウェア実装ではChaCha20-Poly1305を推奨（AES-GCMはテーブル参照でキャッシュ攻撃の懸念）。
- AI支援の開発体験：実装はAIアシスタントでスピードアップ。Lispはデータ量が少ないためパーリィもあったが、テスト可能な領域ではAI生成コードの誤りが速やかに検出できたという。

## 実践ポイント
- まずはocicl等の低リスク環境で試す：pure-tlsはociclで既に利用されており、ダウンロード処理のような低影響領域で実運用テストを積める。  
- 依存排除を重視するシステムなら導入候補：ビルド/配布環境でCライブラリを避けたい場合、有力な代替手段となる。  
- 暗号スイート選定：ソフトウェアのみで動かす場合は ChaCha20-Poly1305 を優先。AESのハードウェア支援が無い環境ではパフォーマンスと安全性のバランスが重要。  
- 証明書検証はOSネイティブに委ねる：Windows/macOSのネイティブAPIを利用することで企業内PKIや運用ポリシーに自然に追随できる。  
- セキュリティ検証を怠らない：RFCテストベクタ、ライブ接続テスト、そして特にフラッド/ファズテストで実運用前に検証を推奨。  
- 既存コードベースとの移行：ASDFの互換レイヤーを活用すれば、ほとんどのアプリはソース修正なしでC依存を切り替えられる。

参考：元実装はMITライセンスで公開中（github.com/atgreen/pure-tls）。production投入前に自組織での監査と十分なテストを。
