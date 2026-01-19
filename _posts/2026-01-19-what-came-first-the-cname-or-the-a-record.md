---
layout: post
title: "What came first: the CNAME or the A record? - CNAMEとAレコード、どちらが先に来るべきか？"
date: 2026-01-19T18:53:48.733Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.cloudflare.com/cname-a-record-order-dns-standards/"
source_title: "What came first: the CNAME or the A record?"
source_id: 46681611
excerpt: "Cloudflareの処理変更でCNAMEとAの順序が入れ替わり、古い実装が解決失敗—対策を解説"
image: "https://cf-assets.www.cloudflare.com/zkvhlag99gkb/4z0yCrFGmJHm2Hg2ZH0zMj/4c975397c739e20c18b70c41379f0c04/What_came_first-_the_CNAME_or_the_A_record-OG.png"
---

# What came first: the CNAME or the A record? - CNAMEとAレコード、どちらが先に来るべきか？
DNSの“当たり前”が崩れた日：CNAMEは本当に先に並ばなきゃいけないのか？

## 要約
Cloudflareの1.1.1.1でのキャッシュ最適化がレコード順序を変えたことで、一部のDNSクライアント（glibcのgetaddrinfoや一部のCisco機器）が名前解決に失敗し、広範な影響が発生した。原因はRFCの曖昧さと、順序に依存する古い実装だ。

## この記事を読むべき理由
DNSはインフラの基礎であり、小さな実装の変化がサービス停止やネットワーク機器の異常につながる。日本の開発者・運用者は、自社のスタックやルータ/スイッチが同様の順序依存で壊れないか確認する必要がある。

## 詳細解説
- CNAMEチェーンの仕組み（初心者向け）
  - www.example.com → cdn.example.com → server.cdn-provider.com → 198.51.100.1 のように、CNAMEは別名（エイリアス）を指し、再帰的にたどって最終的なA/AAAAを得る。
  - 各レコードはTTLを持ち、チェーン中の一部だけが期限切れ（部分的にexpired）でも該当部分だけ再解決してレスポンスを合成する。

- 発端：キャッシュ結合のロジックを「効率化」した変更
  - 以前は新しく解決したレコード（CNAME群）を先に入れてから既存の回答を追加していた（CNAMEが先に来る）。
  - メモリコピー削減のため、既存の配列に新規レコードを追加するよう変更した結果、CNAMEが末尾に来ることがあった。

- なぜ壊れたか（順次走査する古い実装）
  - 一部のクライアントは回答を先頭から順に処理し、CNAMEに出会うと「期待する名前」を更新して次のレコードがその名前に一致するかを期待する実装だった。CNAMEが最後に来ると、期待する名前と一致するAレコードを見逃して解決失敗になる。
  - 影響例：glibcのgetaddrinfo（getanswer_rの実装）、一部CiscoスイッチのDNSCプロセス（再起動ループを引き起こした）。

- RFCの曖昧さと歴史的経緯
  - RFC1034（1987）は「CNAMEで始まることを“可能性”として例示」するが、現代のRFCで用いる MUST/SHOULD 等の明確な語は使われておらず、メッセージ内のRRセット間の順序について明示していない。
  - 結果として実装ごとに挙動が分かれ得る。Cloudflareは互換性のため元に戻し、IETFへのドラフト（order明確化）提出を行った。

- 一部の実装は堅牢
  - systemd-resolvedのようにレスポンスをまず全体的にパースして検索できる構造に入れる実装は、レコード順に依存しないため壊れない。

（簡略化した挙動イメージ）
```rust
// 旧: CNAMEが先に来る（元の実装イメージ）
answer_rrs.extend_from_slice(&self.records); // CNAMEs first
answer_rrs.extend_from_slice(&entry.answer); // Then A/AAAA
```

```rust
// 新: 既存配列に追加したためCNAMEが後ろに来る場合がある
entry.answer.extend(self.records); // CNAMEs last
```

## 実践ポイント
- 自社チェックリスト（優先順で実行）
  1. 使っているLinuxディストリやglibcのバージョンを確認し、影響が報告されているか調べる。getaddrinfoを使うアプリは要注意。
  2. ネットワーク機器（ルータ／スイッチ）のファームウェアを点検。特に組込み機器は古い実装で順序依存が残る可能性がある。ベンダーのガイダンスを確認。
  3. 公開/社内DNSリゾルバのレスポンスをランダムな順序ケースも含めてテストする。CNAMEチェーンを含むテストケースを作り、クライアントが正しく解決できるか確認する。
  4. アプリケーションでの回避策：可能ならstub resolverに依存せず、より堅牢なライブラリ経由で名前解決する、あるいはOS側でsystemd-resolved等のモダンな解決器を使う。
  5. モニタリング強化：DNSエラー率やリゾルバのタイムアウト増加をアラート化する。
  6. IETFドラフトの追跡：draft-jabley-dnsop-ordered-answer-section の議論をウォッチし、仕様が明確化されたらそれに合わせて運用を更新する。

短い結論：RFCの曖昧さと歴史的な実装の違いが原因であり、「順序は関係ない」と仮定するのは危険。互換性を優先してCNAMEを先に出す運用や、クライアント側の堅牢化が実務的な対策になる。
