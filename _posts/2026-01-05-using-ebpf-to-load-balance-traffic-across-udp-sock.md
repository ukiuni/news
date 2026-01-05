---
  layout: post
  title: "Using eBPF to load-balance traffic across UDP sockets with Go - eBPFでUDPソケット群の負荷分散を行う（Go版）"
  date: 2026-01-05T15:53:50.077Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://vincent.bernat.ch/en/blog/2026-reuseport-ebpf-go"
  source_title: "Using eBPF to load-balance traffic across UDP sockets with Go"
  source_id: 832749615
  excerpt: "eBPFでSO_REUSEPORTの偏りを解消しGoでUDPを均等負荷分散"
  ---

# Using eBPF to load-balance traffic across UDP sockets with Go - eBPFでUDPソケット群の負荷分散を行う（Go版）
魅惑の見出し: 「GoでUDP受信を劇的に改善するeBPFトリック — SO_REUSEPORTの弱点を破り、パケットロスを消す方法」

## 要約
LinuxのSO_REUSEPORTだけではフロー偏りやロスが発生することがあるが、SO_ATTACH_REUSEPORT_EBPFとeBPFのSK_REUSEPORTプログラムでランダム／カスタムな振り分けを実装すれば、複数ワーカー間で公平かつ切替可能な負荷分散が可能になる。この記事はGoからそのeBPFを組み込み、グレースフル再起動まで扱う手順をわかりやすく解説する。

## この記事を読むべき理由
- UDPベースのフロー集約（sFlow, IPFIX, DNS等）を扱う日本のサービスではパケット処理遅延やロスが致命的。簡単な設定変更で安定性とスループットを改善できる。
- eBPFを用いたカスタム選択は、アップグレード時のソケット入替やワーカースケールにも強く運用に有用。
- Goで動く実装例と実践的な注意点（ビルド、カーネル互換、グレースフル終了）をまとめているため、即試せる。

## 詳細解説
- 問題点の本質  
  SO_REUSEPORTは受信パケットを4タプルハッシュでソケットに割り当てる。結果として「特定の送信元（エクスポーター）に偏る」ため、同一送信元から来る多数のフローが1つのワーカーに集中し、他ワーカーでアイドル／ロスが生じる。

- eBPFでできること  
  LinuxはSO_ATTACH_REUSEPORT_EBPF経由でSK_REUSEPORTタイプのeBPFプログラムをソケット群に紐付けできる。プログラムはBPF_MAP_TYPE_REUSEPORT_SOCKARRAY（またはREUSEPORT_ARRAY）に格納されたソケット群のインデックスを返して、どのソケットへ渡すかを決定する。これにより
  - ランダムや独自のハッシュで均等に振り分け
  - 新インスタンスへの切替（グレースフルリスタート）を安全に実施
 などが可能になる。

- eBPFプログラムの要点（Cでの最小構成）  
  - グローバルにワーカー数を示す定数を設定（ロード前に設定）  
  - REUSEPORTソケット配列マップを作り、各インデックスにソケットFDを入れる  
  - bpf_get_prandom_u32() で擬似乱数を取り、index = rand % num_sockets とする  
  - bpf_sk_select_reuseport() を呼んで選択を確定し、SK_PASSで受理する  

  （原理上少し先頭インデックスに偏りが出るが実運用では許容範囲）

- Go側の実装ポイント  
  - net.ListenConfigのControlコールバックでSO_REUSEPORTを有効にして複数のUDPソケットを同一ポートにbindする。  
  - libbpfのツール群（bpf2go）を使うと、eBPFプログラムのコンパイルとGo用ラッパー生成が簡単。gen.goにgo:generate指示を書いてgo generateで生成。  
  - 生成したspecに対して、Variables["num_sockets"].Set(uint32(n))で定数を初期化し、mapsに各ソケットFDをPutする。  
  - 先頭ソケットに対して unix.SetsockoptInt(socketFD, SOL_SOCKET, SO_ATTACH_REUSEPORT_EBPF, progFD) でプログラムを紐付ける。  
  - 受信は各ワーカーがUDPConn.Readループでカウント。テスト送信で均等分配を確認できる。

- グレースフルリスタート  
  新プロセスが自分のソケット群とmapを作り、先にeBPFプログラムをアタッチするとカーネルは新インスタンスに流し始める。旧プロセスは既に割り当てられたパケットをドレインするためにconn.Read()を続け、タイムアウトを使って安全に終了する（GoではSetReadDeadlineで期限を設け、期限切れ時に終了フラグをチェック）。

- 実運用で気をつける点  
  - カーネル要件：SK_REUSEPORTプログラムやREUSEPORT_ARRAYはカーネルバージョン依存。使う機能に応じて最低カーネル（例: 4.19以降を推奨）を確認。  
  - bpftool / clang / libbpf の整備：vmlinux.h生成やbpf2goの利用にはツールが必要。vmlinux.hは巨大になることがあるので必要最小限だけを切り出す運用も可能。  
  - セキュリティと権限：eBPFのロードは特権が必要な場合が多い。コンテナ/OCI環境ではCAP_BPF等を検討。  
  - テスト：パケット分布、ロス、再起動時のドレイン挙動を負荷下で検証すること。

## 実践ポイント
- カーネルとツールを確認する（例: kernel >= 4.19 を目安、bpftool/bpf2go/clang/libbpfを準備）。  
- Goで複数ワーカーを同じポートにbindする際は net.ListenConfig の Control で unix.SetsockoptInt(fd, SOL_SOCKET, SO_REUSEPORT, 1) を呼ぶ。  
- eBPFは小さく保つ：num_sockets定数、REUSEPORT_SOCKARRAYマップ、乱数選択、bpf_sk_select_reuseportの4点だけで十分。  
- bpf2goで生成したspecに num_sockets をセットして、mapsにソケットFDをPutし、最初のソケットにSO_ATTACH_REUSEPORT_EBPFでプログラムをアタッチする。  
- グレースフル再起動は「新インスタンス先にeBPFアタッチ → カーネルが新へ誘導 → 旧はReadをdeadline付きでドレインして終了」が実務で安全。  
- 日本の現場では大量のフロー収集やDNSキャッシュサーバ、プローブ/メトリクス収集で効果が出やすい。まずはステージングでパケット分布とロスを測定してから本番導入する。

参考になる最小Goコード（ソケット作成時のSO_REUSEPORT設定例）:

```go
package main

import (
	"net"
	"syscall"
	"golang.org/x/sys/unix"
)

var lc = net.ListenConfig{
	Control: func(_, _ string, c syscall.RawConn) error {
		var err error
		c.Control(func(fd uintptr) {
			err = unix.SetsockoptInt(int(fd), unix.SOL_SOCKET, unix.SO_REUSEPORT, 1)
		})
		return err
	},
}
```

以上を踏まえ、まずは小規模なワーカープールでeBPFを当てて効果検証を行い、カーネル互換と運用手順を固めることを勧める。
