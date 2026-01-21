---
layout: post
title: "Claude Chill: Fix Claude Code's Flickering in Terminal - Claude Code の端末チラつきを直す「claude-chill」"
date: 2026-01-21T01:49:30.272Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/davidbeesley/claude-chill"
source_title: "GitHub - davidbeesley/claude-chill"
source_id: 46699072
excerpt: "Claude Codeの大量出力で起きる端末のチラつきを差分描画で瞬時に防ぐPTTYプロキシ"
image: "https://opengraph.githubassets.com/231f2b668d41350cc6f4b3eba5901590d3418f683ea7564f4e109a1fcfc2d28d/davidbeesley/claude-chill"
---

# Claude Chill: Fix Claude Code's Flickering in Terminal - Claude Code の端末チラつきを直す「claude-chill」
ターミナルが大量出力でフリッカー・固まる問題を一発解決。AIコーディングツールの出力を「差分だけ表示」して快適にする軽量PTTYプロキシの紹介。

## 要約
Claude Code が端末に送る「全画面を一度に更新する」巨大な同期ブロックを仲介して差分描画に変換し、表示のチラつき・ラグ・スクロール履歴消失を防ぐツールが claude-chill。VT100 エミュレーションで画面状態を追い、差分のみを出力する。

## この記事を読むべき理由
- ターミナルで AI コード補助（例：Claude Code）を使うと、数千行の一括描画で表示が固まったりスクロール履歴が消える問題に直面する場面がある。  
- 日本の開発現場でもターミナル中心の開発が多く、出力が扱いやすくなるだけでデバッグ効率や作業の快適さが大きく改善される。

## 詳細解説
- 問題点：Claude Code は出力を「同期ブロック」マーカー（\x1b[?2026h ... \x1b[?2026l）で包み、端末側で原子的に描画する方式を取る。だが実際には「画面全体の再描画」を何千行も送ることがあり、端末は大きな更新を受けてラグやチラつき、スクロール履歴の消失が発生する。
- 解決アプローチ（claude-chill の仕組み）：
  - PTY（疑似端末）を作成して Claude Code を子プロセスとして起動し、端末と Claude の間にプロキシを置く。
  - 出力を走査して同期ブロックを検出し、大量の「全画面更新」をそのまま通さない。
  - VT100 エミュレータに出力を流して仮想スクリーンの状態を追跡し、前回状態との差分だけを実際の端末に書き出す（差分描画）。
  - 描画履歴をバッファに蓄積し「ルックバック（見返し）モード」で履歴をスクロール可能にする。
  - Ctrl+6（デフォルト）でルックバックを切り替え。5秒無操作で自動的に履歴をダンプするオプションあり（デフォルト 5000ms）。
  - シグナル（SIGWINCH、SIGINT、SIGTERM）は Claude に転送され、入力は通常通り透過。ただしルックバック中は出力がキャッシュされる。
- 実装上の注意：
  - 履歴は「最後のフル画面描画」以降の内容が対象。フルリードローが来ると履歴はクリアされる点に注意。
  - Linux/macOS で動作確認されているが、全ての端末エミュレータや環境での動作は保証されない。
  - Rust 製。インストールは cargo を使う。

## 実践ポイント
- まず試すコマンド（環境に cargo が入っている前提）：
  - インストール: cargo install --path crates/claude-chill
  - 実行例: claude-chill -- claude --verbose
- よく使うオプション：
  - -H, --history : 履歴行数（例: -H 50000）
  - -k, --lookback-key : ルックバック切替キー（例: -k "[f12]"）
  - -a, --auto-lookback-timeout : 自動ルックバックのタイムアウト(ms)。0で無効化（例: -a 0）
- 設定ファイル（例）: ~/.config/claude-chill.toml で history_lines や lookback_key を指定可能。
- 運用上のコツ：
  - VS Code の統合ターミナルや Windows の端末で使う場合は互換性を確認する。PTY を扱うため一部エミュレータで挙動が異なることがある。
  - 履歴サイズを大きくしすぎるとメモリを消費するため適切に調整する。
  - 自動ルックバックは便利だが、切替時に一瞬画面のちらつきが発生するので気になる場合は無効化する。
- 注意事項：
  - 個人開発向けツールとして公開されており、あらゆる端末での網羅的検証はされていない。重要な作業環境で使う前にローカルで挙動を確認すること。

短時間で体感改善が得られるユーティリティなので、ターミナルで Claude 系ツールを多用しているなら一度試しておくと作業のもたつきがだいぶ減る。
