---
  layout: post
  title: "FreeBSD Home NAS, part 2: Introduction to the PF firewall - FreeBSD ホームNAS（パート2）：PFファイアウォール入門"
  date: 2026-01-03T11:36:13.252Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://rtfm.co.ua/en/freebsd-home-nas-part-2-introduction-to-packet-filter-pf-firewall/"
  source_title: "FreeBSD: Home NAS, part 2 – introduction to Packet Filter (PF) firewall"
  source_id: 1279229185
  excerpt: "FreeBSDでNASを最小公開・最大防御にするPFの実践設定とSSH安全運用術"
  image: "https://rtfm.co.ua/wp-content/uploads/2025/11/freebsd_logo1.jpg"
---

# FreeBSD Home NAS, part 2: Introduction to the PF firewall - FreeBSD ホームNAS（パート2）：PFファイアウォール入門
家庭用NASを「見せない」化する——FreeBSDのPFで最小の出口・最大の防御を実現する方法

## 要約
FreeBSDでホームNASを堅牢にするためのPF（Packet Filter）入門。PFの基本概念、ルール記述法、運用上の注意（特にSSH越しの作業）とログ取得の実用テクニックを短くまとめる。

## この記事を読むべき理由
日本でも自宅サーバ／NASの運用が増える中、FreeBSDはZFSや安定性で魅力的な選択肢。PFはOpenBSD由来で扱いやすく機能が豊富。家庭ネットワークで最低限の公開サービスだけを残し攻撃面を減らす実践手順は、すぐ使える実用知識になる。

## 詳細解説
- PFの位置づけ  
  FreeBSDにはPF（OpenBSD由来）、ipfw（歴史的）、ipf の3種類がある。PFはシンタックスが読みやすく、状態追跡（stateful）やテーブル、アンカーなど実用機能を備えており、最近のデフォルト選択肢になっている。

- 基本概念（簡潔）  
  - inclusive / exclusive：許可がデフォルトか拒否がデフォルトか。家庭では通常「デフォルト拒否（exclusive）」を推奨。  
  - stateful / stateless：PFは接続の状態を追跡でき、確立済みコネクションの復帰を自動で許可する（keep state）。  
  - マッチルールの評価順：PFは「後勝ち（last match wins）」。ルールの並びが結果に直接影響する点に注意。

- 主要ユーティリティ  
  - pfctl：設定の検査・読み込み・操作  
  - pflog：ログ出力用（仮想インターフェース pflog0 を作る）  
  - pftop：動的な状態やテーブルの確認用

- ルール記述の要素（抜粋）  
  action [direction] [log] [quick] [on interface] [af] [proto protocol] from src to dst [port] [flags] [state]  
  代表的なキーワード：pass/block, in/out, log, quick, keep state, flags S/SA（TCP接続開始用自動付与）

- 最低限のテスト用例（意図は「SSHだけ許可して他を遮断」）  
  /etc/pf.conf の簡単な骨子（例）：
  ```bash
  # /etc/pf.conf（例）
  set skip on lo
  block all
  pass in proto tcp from { 192.168.0.165, 192.168.0.164 } to any port 22 keep state
  pass out all keep state
  ```
  - これでローカルループバックは無視、全受信を拒否しつつ指定ホストからのSSHのみ許可する。

- 運用上の注意（SSH越しの設定）  
  SSH経由で誤ったルールを読み込むと再接続不能になるため、必ず構文チェック pfctl -vnf /etc/pf.conf を行い、以下のような安全策を使う：
  ```bash
  # 構文確認
  pfctl -vnf /etc/pf.conf

  # テストで一時的に起動して自動で止める（安全策）
  service pf start; (sleep 120; service pf stop) &

  # 運用時はリロードで更新
  pfctl -f /etc/pf.conf    # または service pf reload
  ```
  また、start/restart はSSHセッションを確実に切ることがあるため、編集→構文チェック→fでの差し替えを推奨。

- ルール順序と quick の使い分け  
  PFは最後に一致したルールが採用されるため、例外ルールや一時的に優先させたいルールには quick を使うと即座に処理を打ち切れる（順序の影響を明確にコントロールできる）。

- ログ（pflog）の取得と解析  
  - /etc/rc.conf に pf_enable/pflog_enable を設定して起動。  
  - pflog が作る pflog0 を tcpdump で監視： tcpdump -n -e -ttt -i pflog0  
  - /var/log/pflog は pcap 形式なので tcpdump -r /var/log/pflog で読む。  
  - 騒音を減らすために全拒否を log しないで、SSH の拒否のみ log する等ルール設計で制御する。

- スケール対応（簡単に）  
  テーブル（table）やマクロ、アンカー（anchor）を使えば多数のIPや複雑なルールセットを整理可能。テーブルはランタイムで pfctl -t <table> -T add <addr> で編集でき、pf.conf に定義を書いておくと再起動時に反映される。

## 実践ポイント
- まずは構文チェック： pfctl -vnf /etc/pf.conf を常に実行する。  
- SSH越しの導入は「自動停止タイマー」を併用して安全確認する： service pf start; (sleep 120; service pf stop) &  
- 最小設定のテンプレートを作る：loopbackスキップ、block all、許可するホストだけpass in。  
- ルール設計では「最後に勝つ」挙動を意識する：例外は後ろに置く or quick を使う。  
- ログは必要最小限に絞る：block all に log を付けるとノイズが大量に出る。SSHだけログを取る等、ターゲットを絞る。  
- 大量IPは table に入れて運用： pfctl -t friends -T add 192.168.0.0/24 、pfctl -t friends -T show で確認。テーブルはpf.confに定義を書いて永続化する。

短時間で安全に試せて、運用にすぐ生かせるポイントをまとめた。FreeBSDのPFは学べば学ぶほど表現力が高くなるので、まずはローカルで上記テンプレートを試してから段階的に機能（テーブル／アンカー／synproxyなど）を導入すると良い。
