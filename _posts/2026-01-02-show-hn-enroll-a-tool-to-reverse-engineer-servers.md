---
  layout: post
  title: "Show HN: Enroll, a tool to reverse-engineer servers into Ansible config mgmt - Enroll：サーバーを逆解析してAnsible構成管理に変換するツール"
  date: 2026-01-02T01:02:20.482Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://enroll.sh"
  source_title: "Enroll - Reverse-engineering servers into Ansible"
  source_id: 46449852
  excerpt: "既存Linuxサーバを解析して短時間でAnsibleのroles/playbook化するツール"
  ---

# Show HN: Enroll, a tool to reverse-engineer servers into Ansible config mgmt - Enroll：サーバーを逆解析してAnsible構成管理に変換するツール
レガシーサーバーを“秒でコード化”する――Enrollで「雪だるまサーバ」をAnsible管理下へ

## 要約
Enrollは既存のLinuxホストを解析して、必要な状態を抜き出しAnsibleのroles/playbooksを自動生成するツールです。数秒〜数分で“雪だるま”（一品限りの手作り構成）を管理可能なコードに変換できます。

## この記事を読むべき理由
日本企業にはオンプレ旧サーバや人手で育てた“手作り”構成が多く、Ansible化や運用標準化に踏み切れない現場が多いです。Enrollは既存環境を安全にスナップショットし、最小限の手間で構成管理へ取り込めるため、移行初期の作業負荷を劇的に下げます。

## 詳細解説
- 基本設計
  - Enrollは主に2フェーズで動きます：Harvest（ホストの状態収集）とManifest（収集データからAnsibleをレンダリング）。オプションでDiff（差分検出・通知）を実行できます。
  - 対応はDebian系／RedHat系が中心。パッケージや設定ファイル、ユーザ情報、サービス設定など“再現に必要な”情報を抽出してテンプレート化します。

- 安全性と収集ポリシー
  - デフォルトでパスのdenylist、コンテンツスニッフィング、サイズ上限などを設け、機密情報漏洩を避けます。必要ならより広範な収集を明示的にオンにできます。
  - 収集バンドルは--sopsを使ってGPGで暗号化(.tar.gz.sops)して保管可能。DR用途や長期保存に向きます。

- 運用モード
  - single-shot：1台をその場でHarvest→Manifestして即Ansible出力を得る→ローカルでansible-playbook実行。
  - remote over SSH：自 workstation からリモートをHarvestし、ローカルでManifestを生成。sudo不要でも動くが情報が限定されます。
  - multi-site（--fqdn）：ロールはデータ駆動にして、ホスト固有状態はインベントリで決める。多数台を段階的に管理下に置く際に有効。
  - diff：過去のHarvestと比較してドリフトを検出し、Webhookやメールで通知できます。

- なぜ現場で刺さるか
  - 災害復旧のスナップショット、既存“黄金イメージ”の抽出、少ない工数でAnsible管理へ移行する際の橋渡しに最適です。既存の複雑な設定から「再現可能なロール」を短時間で得られる点が強み。

## 実践ポイント
- まずは非本番でsingle-shotを試す：
```bash
# Harvest → Manifest を一気に生成
enroll single-shot --out ./ansible

# 生成したplaybookをローカルで動かす（テスト）
ansible-playbook -i "localhost," -c local ./ansible/playbook.yml
```
- リモート収集の例（テスト用に鍵／ユーザを用意）：
```bash
enroll single-shot \
  --remote-host myhost.example.com \
  --remote-user myuser \
  --harvest /tmp/enroll-harvest \
  --out ./ansible \
  --fqdn myhost.example.com
```
- 多台運用では --fqdn モードで共有ロール＋ホスト固有データに分離するのが保守的。逐次enrollしてinventoryを充填するワークフローがおすすめ。
- セキュリティ：Harvestを長期保管する場合は必ず --sops を使い暗号化する。機密パスはdenylistに入れられているか確認する。
- ドリフト検知：定期的にenroll diffを実行し、変更をWebhookでCIに流すと「いつ変わったか」が追跡できる。
```bash
enroll diff --old /path/to/harvestA --new /path/to/harvestB --format markdown
```
- 運用上の注意：--no-sudoは情報が制限されるので、完全な再現性が必要ならsudo権限でのHarvestを検討する。

