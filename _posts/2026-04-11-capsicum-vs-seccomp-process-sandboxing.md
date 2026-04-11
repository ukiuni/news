---
layout: post
title: "Capsicum vs seccomp: Process Sandboxing - Capsicumとseccomp：プロセスサンドボックス"
date: 2026-04-11T01:23:28.022Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vivianvoss.net/blog/capsicum-vs-seccomp"
source_title: "Capsicum vs seccomp: Process Sandboxing"
source_id: 1223789077
excerpt: "FreeBSDのCapsicumとLinuxのseccomp、実運用でどちらが安全で効率的か？"
---

# Capsicum vs seccomp: Process Sandboxing - Capsicumとseccomp：プロセスサンドボックス
魅力的タイトル: 「現場で使えるサンドボックス対決：FreeBSDのCapsicumとLinuxのseccomp、どっちを選ぶべきか？」

## 要約
Capsicumは「ファイル記述子（FD）ベースの権限制御」でアプリケーションの権利を細かく削ぎ落とすFreeBSDの仕組み。seccomp（特に seccomp-bpf）はLinuxで「システムコールを絞る」ことでプロセスの振る舞いを制限する手法。目的は同じでも設計思想と利点・欠点が大きく異なります。

## この記事を読むべき理由
日本の多くのサーバやコンテナ基盤はLinuxで稼働しており、seccompはコンテナセキュリティの第一線にあります。一方で、金融・通信などでFreeBSDが選ばれる場面もあり、Capsicumの「権利委譲」モデルは設計段階から堅牢なアプリを作る上で参考になります。どちらをいつ・どう使うかが現場での安全性と運用コストを左右します。

## 詳細解説
- 基本設計の違い
  - Capsicum（FreeBSD）
    - 「capability-oriented security」：プロセスをcapability modeに入れる（cap_enter）と、カーネルがグローバルな名前解決を禁止。既に持っているファイル記述子（FD）や権利だけで動くようにする。
    - FDごとに操作可能な権利（読み取り/書き込み/送受信など）を細かく制限でき、権利を別プロセスに委譲（FDを渡す）可能。
    - 設計的に「権利の最小化」をアプリのAPI設計時に反映しやすい。
  - seccomp（Linux）
    - システムコールレベルでフィルタを適用。古いモードは単純に syscall の許可/拒否（SECCOMP_MODE_STRICT）、現在は seccomp-bpf によるBPFフィルタで柔軟な条件分岐が可能（SECCOMP_MODE_FILTER）。
    - libseccompなどでルール記述を簡単にでき、コンテナランタイム（Docker, runc）がプロファイルとして利用。
    - syscall単位なので「どのFDに対して」操作を許すかといった精細さは弱いが、カーネルレベルでの侵害範囲制限に有効。

- セキュリティ上のトレードオフ
  - Capsicumは「持っているものだけで動く」設計により、権利の委譲と分離が強力。アプリ側に設計変更の負担があるが、逃げ道が少ない（設計次第で非常に堅牢）。
  - seccompは導入が比較的容易で既存Linux環境・コンテナに馴染むが、BPFルールのミスやカーネルのsyscall増加によるメンテナンスが課題。さらに、syscallインタフェース自体の不変性を前提にしているため、アプリの裏側で別のsyscall経由で脱出されるリスクもある。

- 運用とデバッグ
  - seccompはフィルタでsyscallを落とすため、ログ/診断が難しいことがある（seccomp_notifyでユーザー空間処理を挟めるが複雑）。
  - Capsicumはアプリの設計に応じて失敗箇所が明確になりやすいが、FreeBSD環境に限定される。

- 性能
  - seccomp-bpfはsyscallごとにBPF評価が走るため極端に高頻度なsyscallが多いワークロードでオーバーヘッドが出ることがある。
  - Capsicumは権利チェックがFD向けの操作に限定されるため、適切に設計すれば低コスト。

- 実装・エコシステム
  - Linux: libseccomp、seccomp-tools、Docker/Kubernetesでのプロファイル活用。
  - FreeBSD: Capsicum API（cap_enter, cap_rights_limit 等）、関連ライブラリと設計パターン。

（補足）OpenBSDのpledgeやunveilも近い目的だが設計思想が異なる点があり、用途に応じた選択が必要。

## 実践ポイント
- まず資産を棚卸し：アプリが使うsyscallと外部リソース（ソケット、ファイル）を列挙する。
- Linuxなら
  - コンテナではまず既存のseccompプロファイルを適用（Dockerのデフォルト）し、libseccompで段階的に絞る。
  - テスト用に seccomp-tools でどのsyscallが呼ばれているかを観察し、フィルタを作る。
  - supervisorが必要なら seccomp_notify を検討（ただし実装は複雑）。
- FreeBSDなら
  - Capsicum設計を検討（cap_enterを使うポイント、FDを必要最小限で渡す設計）。
  - cap_rights_limit でFDの権利を削る習慣を付ける。権利の委譲でプロセス分離を検討。
- 共通のベストプラクティス
  - 最小権限の原則（least privilege）を設計段階で適用する。
  - ロギング・ステージング環境で段階的に適用し、現場での実行パスを把握してから本番へ。
  - 監査と自動テストを組み込み、サンドボックス適用後の挙動をCIで検証する。
- ツール
  - Linux: libseccomp, seccomp-tools, Docker seccomp profiles
  - FreeBSD: Capsicum API ドキュメント、実戦的サンプル（cap_enter + cap_rights_limit）

ミニ例（Capsicumでcap_enter後は外部名解決が不可）:
```c
// C
#include <capsicum.h>
cap_enter(); // 以降はグローバルな名前解決不可、既存のFDのみを利用
```

ミニ例（libseccompでopenを禁止するイメージ）:
```c
// C
#include <seccomp.h>
scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);
seccomp_rule_add(ctx, SCMP_ACT_ERRNO(EPERM), SCMP_SYS(open), 0);
seccomp_load(ctx);
```

まとめ：既存のLinuxコンテナ環境ならまずseccompでプロファイル運用を検討。FreeBSDで設計段階から堅牢化するならCapsicumが強力。用途と運用体制に応じて使い分けを。
