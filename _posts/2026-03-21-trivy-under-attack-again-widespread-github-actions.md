---
layout: post
title: "Trivy Under Attack Again: Widespread GitHub Actions Tag Compromise Exposes CI/CD Secrets - Trivyが再び被害：GitHub Actionsタグの改竄でCI/CDの秘匿情報が流出"
date: 2026-03-21T21:38:25.256Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://socket.dev/blog/trivy-under-attack-again-github-actions-compromise"
source_title: "Trivy Under Attack Again: Widespread GitHub Actions Tag Comp..."
source_id: 377322454
excerpt: "TrivyのActionタグ改竄でCI/CD秘密が流出、SHA固定と監査を今すぐ"
image: "https://cdn.sanity.io/images/cgdhsj6q/production/6afe7a11b9f6e0eaca499016e7760f5674917627-1024x1024.png?w=1000&amp;q=95&amp;fit=max&amp;auto=format"
---

# Trivy Under Attack Again: Widespread GitHub Actions Tag Compromise Exposes CI/CD Secrets - Trivyが再び被害：GitHub Actionsタグの改竄でCI/CDの秘匿情報が流出

魅惑の見出し案：トラストを壊す「タグ攻撃」――TrivyのGitHub Actionが強制タグ書き換えでCI/CD秘密が丸見えに

## 要約
Trivyの公式GitHub Actionの大量タグ（75/76）が攻撃者によりforce-pushされ、エントリポイントに情報窃取マルウェアが埋め込まれて多数のCI/CDパイプラインで秘密情報が流出する事案が発生。実被害範囲は広範で、@0.35.0以外のタグが危険。

## この記事を読むべき理由
日本の開発チームでもGitHub ActionsとTrivyは広く使われており、タグ参照のワークフローがそのままマルウェア配布経路になる可能性があるため、即時チェックと対策が必要。

## 詳細解説
- 攻撃手法：攻撃者はTrivyリポジトリの書き込み権限を入手し、既存のバージョンタグをforce-pushで別コミットに差し替え。タグ参照（例: aquasecurity/trivy-action@0.33.0）はタグが指すコミットを解決するため、利用者側のワークフローは自動的に悪意あるコードを取得して実行してしまう。  
- タグ改竄の巧妙さ：各タグ用に「元のコミット情報を模した」メタデータを作り、見た目上は正規リリースに見えるように偽装。GPG署名の有無や「release の比較が0 commits to master」など僅かな差異が観察点。  
- マルウェアの挙動：entrypoint.shに埋められたマルウェアは3段階で動作（収集→暗号化→外部送信）。収集ではランナーの環境変数、SSH鍵、各種クラウド資格情報、Kubernetesトークン等をファイルやプロセスメモリ（GitHubホスト型ランナーではsudoで /proc/<pid>/mem をダンプ）から取得する。暗号化はAES-256-CBC＋RSAで包装、最終的に攻撃者制御サーバへ送信する。  
- 根本原因：以前の事件で漏えいしたCI用クレデンシャルの残存アクセスが今回の実行権限を許した可能性。つまり「トークンローテーションが原子化されていなかった」ことが原因の一端。  
- 影響範囲：10,000超のワークフローファイルがこのアクションを参照しており、被害の“爆発力”が大きい。タグ固定（バージョン番号）を使っている多くのパイプラインが影響を受ける。

## 実践ポイント
- すぐ確認すること
  - リポジトリで aquasecurity/trivy-action を参照しているワークフローを検索し、タグ参照を使っている箇所を洗い出す。  
  - 影響タグ（例: @0.34.2, @0.33.0, @0.18.0 等）を使っていないか確認。@0.35.0のみ安全と報告されているが常に最新情報を確認。
- すぐできる対策
  - アクションは可能な限り完全なコミットSHAでピン留めする（例: @<full-sha>）。GitHubはSHA固定のみが真に不変と説明。  
  - 問題が発生したら該当ワークフローの実行を無効化し、当該アクションの参照を安全なSHAか公式修正版に差し替える。  
  - CI用トークンやキーは最小権限化／用途別分離し、ローテーションを確実に行う（原子的に無効化→再発行できる運用）。  
  - GitHubホスト型ランナーでのsudo権限や自己ホストランナーの権限設定を見直し、実行環境の分離を強化する。  
  - リポジトリと組織の監査ログ・ワークフロー実行ログをチェックし、怪しい外部へのHTTP送信や不審なプロセスダンプの痕跡を探す。  
  - 署名付きコミットやGPG署名を導入し、リリースメタ情報の整合性を検証する運用を検討する。  
  - サードパーティ製アクションを使う際はダウンストリーム依存を可視化し、定期スキャン（SBOM/依存関係チェック）と脆弱性監視を組み込む。  

短くまとめると：タグ参照は信頼の盲点。日本のチームも即座にワークフローを点検し、SHAピン留め・権限最小化・ログ監視を行って被害を防いでください。
