---
layout: post
title: "Turn Dependabot Off - Dependabotを無効にしよう"
date: 2026-02-20T22:27:11.645Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://words.filippo.io/dependabot/"
source_title: "Turn Dependabot Off"
source_id: 47094192
excerpt: "Dependabotを止めてgovulncheckとCIでノイズを激減、Goプロジェクト向け実践手順"
image: "https://assets.buttondown.email/images/9bea93bf-77e5-44cf-9ae5-ada68918cf6a.jpeg?w=960&amp;fit=max"
---

# Turn Dependabot Off - Dependabotを無効にしよう
魅力的なタイトル: Dependabotを切って、本当に必要なアラートだけ受け取る方法 — Go案件の現場で今すぐやるべきこと

## 要約
Dependabotの大量の自動PRやセキュリティ通知はノイズが多く、かえってセキュリティ対応を阻害する。代わりにgovulncheckと「最新依存でのCI」を定期実行するスケジュール型GitHub Actionsへ置き換えることを推奨する。

## この記事を読むべき理由
- 日本のスタートアップや組込み・WebサービスでもGo採用が増加中。無差別な依存更新通知は開発効率とOSS維持に悪影響を与える。  
- 実運用で有用な「ノイズを減らす具体策」がすぐ導入できる。

## 詳細解説
- 問題点：Dependabotはモジュール単位での一致や脆弱性メタ情報だけでPRと警告を大量に出すため、実際には影響のないケース（サブパッケージだけ使っているなど）でもアラートが飛び、対応疲れ（alert fatigue）を招く。これが誤検知の増加、トリアージの放棄、OSSメンテナの負担増につながる。
- 技術的背景：Go向けにはGo Vulnerability Databaseが脆弱性ごとに「影響を受けるモジュール・パッケージ・シンボル」を保有している。govulncheckは静的解析で「脆弱なシンボルが実際に呼ばれているか（到達可能か）」を判定できるため、実害がありそうな箇所だけ通知できる。
- 具体例：ある暗号ライブラリの微小な修正（ほとんど使われないメソッドの修正）に対して大量PRが出たが、govulncheckはプロジェクト内からそのシンボルが呼ばれていないことを検出して通知を抑制した。
- 依存更新の考え方：依存を常に自動で即更新するより、「自分たちの開発サイクルで意図的に更新する」ほうが安全。だが最新でテストを回すことで互換性破壊や問題は早期に検知できる。

## 実践ポイント
1. Dependabotのセキュリティアラートを無効化し、代わりにgovulncheckを定期実行するGitHub Actionを設定する。例：
```yaml
# yaml
name: govulncheck
on:
  schedule:
    - cron: '22 10 * * *' # 毎日
  workflow_dispatch: {}
jobs:
  govulncheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with: { persist-credentials: false }
      - uses: actions/setup-go@v6
        with: { go-version-file: 'go.mod' }
      - run: go run golang.org/x/vuln/cmd/govulncheck@latest ./...
```
2. 依存の「最新」でCIを回すジョブを追加し、破壊的変更はCI上で検出してから手動で採用する。例（depsをlatestでテスト）：
```yaml
# yaml
name: Go tests
on: [schedule, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy: { fail-fast: false, matrix: { deps: [locked, latest] } }
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-go@v6
      - run: |
          if [ "${{ matrix.deps }}" = "latest" ]; then
            go get -u -t ./...
          fi
          go test -v ./...
```
3. ローカルやCIでgovulncheckを使うコマンド例：
```bash
# bash
go run golang.org/x/vuln/cmd/govulncheck@latest ./...
```
4. サードパーティのスキャナを使う場合は「パッケージ単位のフィルタリング」以上（可能ならシンボル到達性分析）を求める。
5. CI実行はサンドボックス化（gVisor等）を検討し、依存の悪意あるコードがCIから本番へ広がるリスクを下げる。

短いまとめ：Dependabotの自動PRと警告をそのまま受け入れるのは非効率。Goならgovulncheck＋最新依存での定期CIに切り替え、実際に影響ある脆弱性だけ確実に拾う運用へ移行しよう。
