---
layout: post
title: "Entire Claude Code CLI source code leaks thanks to exposed map file | 512,000 lines of code that competitors and hobbyists will be studying for weeks. - Claude Code CLIの全ソースが流出：50万行超の設計図が公開に"
date: 2026-04-01T00:49:00.995Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/ai/2026/03/entire-claude-code-cli-source-code-leaks-thanks-to-exposed-map-file/"
source_title: "Entire Claude Code CLI source code leaks thanks to exposed map file - Ars Technica"
source_id: 409213010
excerpt: "Claude Code CLIのソースマップ流出で50万行超の内部実装が公開、解析が加速"
image: "https://cdn.arstechnica.net/wp-content/uploads/2026/03/claude-code-1152x648.jpg"
---

# Entire Claude Code CLI source code leaks thanks to exposed map file | 512,000 lines of code that competitors and hobbyists will be studying for weeks. - Claude Code CLIの全ソースが流出：50万行超の設計図が公開に
Anthropicの「Claude Code」CLIが丸裸に——50万行のソースマップ流出で競合も解析者も数週間は読みふける事態に

## 要約
Anthropicが公開したnpmパッケージにソースマップが混入し、約2,000のTypeScriptファイル、51万行超のClaude Code CLIのソースが流出した。Anthropicは「リリースパッケージの人的ミス」と説明しているが、設計やメモリ管理、プラグイン体系など重要な内部実装が外部に暴露された。

## この記事を読むべき理由
日本の開発チームやAIスタートアップにとって、自社プロダクトのリリースプロセスやサプライチェーン管理、知的財産保護の教訓が詰まっている。類似ミスはnpmなどのパッケージ配布で起こりやすく、日本でも同様の被害リスクがあるため必読です。

## 詳細解説
- 何が起きたか：Anthropicが公開したClaude Code v2.1.88のパッケージにソースマップ（.map）が含まれており、それを辿ることでトランスパイル前のTypeScriptソース約2,000ファイル・512,000行が取得可能になった。最初に指摘したのはセキュリティ研究者Chaofan Shouで、以後GitHubで公開され数万フォークが作られた。
- 公開された情報の中身：メモリアーキテクチャ（バックグラウンドでのメモリ書き換え、使用前の検証手順など）、プラグインやツール体系（約4万行規模）、クエリシステム（約4.6万行）など、実運用を想定した「プロダクション級」の実装が詳述されている。解析者はClaude Codeが単なるAPIラッパーではなく、開発体験を重視した大規模な設計であると評価している。
- リスクと影響：競合他社がアーキテクチャ上の知見を吸収して追随を早めるほか、攻撃者にとってはガードレールの回避方法や脆弱性探索の手がかりになる。法的には企業秘密としての保護はあるが、既に広く出回った情報の取り戻しは困難。
- Anthropicの対応：同社は顧客データや資格情報は流出していないと表明し、再発防止策を導入するとしているが、現実的なダメージコントロールと継続的な監査が必要。

## 実践ポイント
- リリース前チェック：CIでソースマップやデバッグ情報、未削除のビルドアーティファクトを検出・除外する自動チェックを必須化する。
- secrets検出とローテーション：公開前にトークンや鍵のスキャンを行い、疑わしいものは即時ローテーションする。
- パッケージ供給のガバナンス：npmなど公開レジストリにアップする前にSLSA等の供給連鎖証明を整備し、署名付きリリースを採用する。
- 内部教育と手順化：人的ミスが原因になりやすいので、リリース手順書・チェックリストの整備と定期トレーニングを行う。
- モニタリングと法務対応：流出が起きたら即時に公開状況を監視し、必要なら法務・規制対応（CE、個人情報漏洩の有無確認など）を準備する。
- コミュニティ活用：バグバウンティや外部研究者との協働で早期発見を促す。

日本の開発現場でも「一つのビルド設定ミス」が重大な知財・セキュリティ被害に直結します。今回の事例は、リリース品質とサプライチェーン管理の重要性を再確認する良い警鐘です。
