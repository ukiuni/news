---
layout: post
title: "Claude Code's binary reveals silent A/B tests on core features - Claude Codeのバイナリが明かす：コア機能への無通知A/Bテスト"
date: 2026-03-14T12:08:39.966Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://backnotprop.com/blog/do-not-ab-test-my-workflow/"
source_title: "Do Not A/B Test My Workflow"
source_id: 47375682
excerpt: "**有料版Claude Codeが無通知でA/Bテストに晒され、出力を強制短縮して業務に支障**"
image: "https://backnotprop.com/_astro/og-default.CtYXdJzI.png"
---

# Claude Code's binary reveals silent A/B tests on core features - Claude Codeのバイナリが明かす：コア機能への無通知A/Bテスト
有料プラン利用者が知らないうちに「ワークフローを劣化させる実験」に回されていた——あなたのAIツールは本当に安定ですか？

## 要約
有料版Claude Codeのバイナリから、ユーザーに無通知で適用されるA/Bテスト（GrowthBook管理）が見つかり、プラン出力（Plan mode）の構造や長さを強制的に変えるvariant（null／trim／cut／cap）が存在。最も厳しい「cap」は40行で出力を上限し、文脈や説明文を削除するなどワークフローを損なう挙動をする。テレメトリでvariant割当や承認結果を収集している。

## この記事を読むべき理由
有料で業務に組み込むAIが「静かに実験」されると、作業効率や品質に直接影響する。日本の企業や開発者も同様のリスクを持つため、透明性・制御を求める観点から必読。

## 詳細解説
- 証拠：著者がClaude Codeのバイナリを解析し、GrowthBookで管理されるA/Bテスト名（tengu_pewter_ledger）とvariant実装を発見。  
- variant一覧：null, trim, cut, cap。各variantはプラン出力の詳細度を段階的に制限。  
- capの振る舞い：プランを最大40行に強制、コンテキストや背景セクションを省略、プローズ（説明文）を削除する命令をモデルに与える。  
- UXへの影響：著者は有料プラン（月額約$200）で、オプトイン無しにsub-agentが自動生成した短い箇条書きだけが返ってきて対話や指示の余地が消えたと報告。  
- テレメトリ：プラン終了時に "tengu_plan_exit" として planLengthChars, outcome, clearContext, planStructureVariant（割当variant）などをログ収集。どの指標で最適化しているかはバイナリからは不明。  
- 問題点：有料ユーザーが実験対象にされること、通知・設定・オプトアウト手段がないこと、業務に与える影響に対する説明責任の欠如。

（日本の文脈）企業導入では、こうした無通知の実験は品質管理・コンプライアンスや契約上の問題になりうる。特にSaaS契約や社内ワークフローに依存する場面では事前合意・オプション設定が重要。

## 実践ポイント
- ベンダーへの確認：契約時／更新時に「実験（A/B）適用の可否」「オプトアウト」「影響の通知」を明記させる。  
- テスト環境での受け入れ試験：本番導入前に有料機能を固定版で検証し、出力や挙動を比較する。  
- 監視とログ収集：重要ワークフローの出力差分を自動検知するモニタを設置し、異常が出たら即ロールバック／報告。  
- 交渉ポイント：企業はSLAに「実験による機能変更の事前通知」「重大なUX変更時の同意」条項を入れる。  
- 代替策検討：業務クリティカルならバージョン固定やオンプレ／オープンソースの選択肢も検討する。

短く言えば、有料だからといって「実験に勝手に使われない」保証は自分で作る必要があります。
