---
layout: post
title: "Reading leaked Claude Code source code - 流出した「Claude Code」ソースを読む"
date: 2026-04-01T02:54:14.010Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lr0.org/blog/p/claude-code-source/"
source_title: "Reading leaked Claude Code source code | La Vita Nouva"
source_id: 1639169970
excerpt: "流出コードで判明、シェル防御やVim互換等の実践的安全設計と遊び心"
---

# Reading leaked Claude Code source code - 流出した「Claude Code」ソースを読む
魅惑の内部ドキュメントと“アヒル”が暴く、実運用レベルの安全設計と遊び心

## 要約
流出した約132,000行のTypeScriptから、Anthropicの実運用で育てられた「攻めと守り」の設計思想――ビルド時の機密チェック、過剰とも言えるシェル防御、権限判定のML、細部まで作り込まれたユーザー体験（Vim実装やペット）――が読み取れます。

## この記事を読むべき理由
この解析は単なるゴシップではなく、商用LLMプロダクトが現場で抱えるセキュリティ／UXトレードオフや設計実装の実例集です。日本のサービス運営者や開発者が安全運用・QA・機能設計で学べる点が多くあります。

## 詳細解説
- コードネーム“カナリア”対策：種名（duck 等）を全て16進でランタイム生成しているのは、ビルド出力に未公開モデル名が漏れるのを防ぐため。ビルド時に excluded-strings.txt をgrepするチェックがあり、文字列リテラルを避ける工夫が見える。
- 内部専用コマンドとフラグ：bughunter や goodClaude（無効化済）など内部コマンドが存在。PROACTIVE／COORDINATOR_MODE／AGENT_TRIGGERS 等のフラグは自律性・マルチエージェント運用を想定した機能群。
- 強制的なアナリティクスタイプ名：I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS という型名を通すことで、開発者に「送信して良いデータか」を明示的に確認させる実装的強制力を持たせている。
- マルチセッション検出：30分ウィンドウで session1→session2→session1 を検出し並列利用を計測。利用実態分析に活用。
- シェル防御（bashSecurity.ts 等、約2.6k行）：zsh/zsh拡張（=cmd）、heredoc注入、ANSI-C引用、プロセス代入、zcpc/ztcp 的なビルトイン経路など、多彩な攻撃パターンを列挙して検証。PowerShell版の類似チェックもあり、危険コマンド（rm -rf、git reset --hard、kubectl delete 等）には文言で注意喚起。
- 権限システムと“YOLO”分類器：default／acceptEdits／dontAsk／bypassPermissions／auto の5モード。autoは高速判定＋拡張推論の二段階のML判定で実行可否を決定。ファイル名 yoloClassifier.ts が示すユーモアと現実性。
- Vim互換キーバインドを自前実装：INSERT/NORMAL、演算子・モーション・テキストオブジェクト・ドットリピート等を含む完全なステートマシン。プラグイン以上の完成度。
- クエリオーケストレーションの“思考ルール”：thinkingブロック取り扱いに関する3つのルールが厳格に定められ、コードに中世英語の警告コメントが残るほど運用上の苦労があった跡が見える。
- バディ（ペット）システム：ユーザーIDを決定論的にPRNGで振って種・レアリティを生成し、名前／性格はモデルで一度だけ生成。アスキーアート3フレームでアニメーション、ステータスや帽子などゲーム的要素を持つ。機能フラグで隠蔽。
- その他の小ネタ：186種類のローディング動詞、/stickers が外部サイトを開くだけ、メモリ同期は“the lesser evil” 戦略、端末プロトコル差を吸収するキーボードパーサ等。

## 実践ポイント
- ビルドパイプラインでの「漏洩チェック」は文字列リテラルだけでなくランタイム生成の抜け道まで想定する（excluded-strings と出力grepの設計検討）。
- シェルや外部ツール呼び出しの検証は正規表現＋文脈解析でカバー幅を広げる。zsh固有挙動やプロセス代入などを見落とさない。
- アナリティクス送信時の「強制的自己チェック」型名のように、開発者のミスを防ぐAPI設計を取り入れる。
- 権限自動化は二段階判定（高速ヒューリスティック＋詳細モデル）で運用コストと安全性を両立できる可能性あり。
- UXの細部（Vimキーバインドやペットの演出）は、ユーザー体験の差別化につながる。小さな遊び心は製品愛着を高める一方、機能フラグで段階展開すること。

以上は流出コードの公開解析に基づく学びの抽出です。実運用の安全性や法的側面は慎重に扱ってください。
