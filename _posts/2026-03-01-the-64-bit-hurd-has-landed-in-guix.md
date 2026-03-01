---
layout: post
title: "The 64-bit Hurd has landed in Guix - 64ビットHurdがGuixに到来"
date: 2026-03-01T11:04:56.310Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://guix.gnu.org/en/blog/2026/the-64-bit-hurd/"
source_title: "The 64-bit Hurd is Here! — 2026 — Blog — GNU Guix"
source_id: 1686748178
excerpt: "Guixで64ビットGNU/Hurdが実用域へ、VMで今すぐ試せる"
---

# The 64-bit Hurd has landed in Guix - 64ビットHurdがGuixに到来
魅力的なタイトル: 「Guixで64ビットGNU/Hurdがついに実用域へ — 今すぐ試せる手順と日本での意義」

## 要約
Guixがx86_64（64ビット）GNU/Hurdサポートを公式に取り込み、インストーラ／クロスツールチェーン／多数のパッケージ修正を経て、VMや裸メタルで動かせるようになりました。ただしパッケージ互換性やテストの未解決事項は残ります。

## この記事を読むべき理由
GNU/HurdはUnixの思想やデバッグしやすさで注目される実験的OSです。日本の開発者やOS好きにとって、Guix上で64ビットHurdが動くことは「試せる」「貢献できる」敷居が大幅に下がった重要ニュースです。

## 詳細解説
- 何が起きたか：Guixにx86_64-gnu（64ビットHurd）ターゲットが追加され、インストーラやイメージ生成、クロスビルド環境が整備されました。重要なアップデートはGCCを14系へ移行した点で、これに伴う厳格化を受けて173パッケージを修正、さらに109パッケージを更新しています。
- 技術課題：GCC14はコンパイル時の厳格さが増したため多数のビルド修正が必要になったこと、いくつかのテスト（openssl・python・cmake等）が64ビット環境でハングする問題が残っている点が挙げられます。ビルドデーモンの認証問題やShepherdテスト、procサーバのゾンビプロセス対応など多面的な修正も行われました。
- ネットワーク／デバイス：RumpNET経由でIntel i8254x（wmX）ギガビットNICドライバが利用可能になり、仮想NICや一部実機でのネットワークが動作します。SMP（複数CPU）対応パッチも進行中で、近くマルチプロセッシング対応が期待されています。
- 現状のエコシステム：Debian GNU/Hurdでは多数のパッケージが利用可能ですが、Guix上のHurdはまだ提供パッケージ比率が低く（抜粋時点で32bit約1.7%、64bit約0.9%）、今後のパッケージ増強が課題です。
- コミュニティ／資金：NLnetなどの支援で作業が進展。パッチ交換やレビューには多数の貢献者が関わっています。参加窓口は libera.chat の #guix / #hurd やメーリングリストです。

## 実践ポイント
- まずはVMで試す（例：イメージ作成→起動→ssh接続）
bash
./pre-inst-env guix system image --image-type=hurd64-qcow2 \
  gnu/system/examples/bare-hurd64.tmpl

bash
guix shell qemu -- qemu-system-x86_64 -m 2048 -M q35 \
  --enable-kvm \
  --device e1000,netdev=net0 \
  --netdev user,id=net0,hostfwd=tcp:127.0.0.1:10022-:2222 \
  --snapshot \
  --hda /gnu/store/...-disk-image

- 起動後の接続例（ポートフォワードでSSH）
bash
ssh -p 10022 root@localhost

- ローカルでパッケージをテストする
bash
guix build --system=x86_64-gnu hello

- 試す際の注意点：64ビットHurdはまだXや多くのパッケージが未対応／不安定な部分あり。GCC14関連のビルド失敗やテストハングに遭遇したら、ログと再現手順を持ってコミュニティに報告すると貢献につながります。
- 貢献の入口：ビルド修正、ドライバ（RumpNET）検証、Wi‑Fiサポート、SMP検証、インストーラ改善などが歓迎されています。参加は libera.chat の #guix / #hurd へ。

興味があれば、まずはVMで一度立ち上げて「動く雰囲気」を掴んでみてください — 貴重な学びと貢献の機会が待っています。
