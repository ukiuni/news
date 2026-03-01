---
layout: post
title: "Bringing Claude Code Skills into Neovim via ACP - NeovimでClaude CodeのSkillsをそのまま使う方法"
date: 2026-03-01T06:38:38.207Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://memoryleaks.blog/tech/2026/02/28/nvmegachad-acp.html"
source_title: "Memory Leaks | Bringing Claude Code Skills into Neovim via ACP"
source_id: 393742592
excerpt: "NeovimでClaude CodeのSkills/MCPをそのまま利用、ACPでAPI鍵管理不要に"
---

# Bringing Claude Code Skills into Neovim via ACP - NeovimでClaude CodeのSkillsをそのまま使う方法
Neovim内チャットが「本物の」Claude Codeセッションになる──面倒なツール設定とAPIキー管理から解放される小技。

## 要約
ACP（Agent Client Protocol）を使って、NeovimのCodeCompanionをAnthropicの生APIではなくローカルのClaude Codeセッションに接続する手法を紹介。SkillsやMCP、プロジェクトメモリをそのままエディタ内で利用できるようになる。

## この記事を読むべき理由
日本でもチームでカスタムSkillや運用ツールをClaude上で整備するケースが増えています。Neovimで開発するエンジニアが、端末で使っているワークフローをそのままエディタ内に持ち込み、生産性を落とさずに統合できる実用的な手法です。

## 詳細解説
- 問題点：CodeCompanionが直接Anthropic APIに繋がる構成だと、エディタ側でモデルやツール承認の設定を自前で持つ必要があり、プロジェクト内の.claude/に定義したSkillsやMCP設定が使えない。
- ACPとは：LSPが言語サーバーの問題を解くように、ACPはエージェント（AIツール）とクライアント（エディタ等）を分離するオープンプロトコル。クライアントもエージェントもACPを話せば相互運用可能になる。
- 仕組み：claude-agent-acp（ACP対応ブリッジ）をPATHに置き、CodeCompanion側をclaude_codeアダプタに切り替えると、Neovim内チャットはローカル/チームのClaude Codeセッション（Skills・MCP・メモリ含む）と直接やり取りするようになる。
- 利点：モデルキーやツール一覧の手動管理が不要。Claude Code側の権限モデルで承認を扱うため、エディタ側は設定から解放される。さらにClaude Codeが持つ豊富なツール群と継続的なアップデートの恩恵を受けられる。
- 例：直接API構成（面倒）とACP経由の最小構成（簡潔）

例：直接API（抜粋）
```lua
-- lua
strategies = {
  chat = {
    adapter = { name = "anthropic", model = "claude-opus-4-6" },
    tools = { -- 手動でツール承認や一覧を管理
      ...
    },
  },
}
```

例：ACP経由（簡潔）
```lua
-- lua
interactions = {
  chat = {
    adapter = "claude_code",
    roles = { user = "NvMegaChad Companion" },
  },
  inline = {
    adapter = { name = "anthropic", model = "claude-haiku-4-5" }, -- 低レイテンシ用は直接API
  },
}
```

- セットアップのポイント：ローカルにClaude Codeとclaude-agent-acpを入れる（macOS例：`brew install claude-agent-acp`）。あとはCodeCompanionのadapterを切り替えるだけでOK。

## 実践ポイント
- まずチーム共通のSkillsを.claude/に置き、ローカルでClaude Codeが動くことを確認する。
- claude-agent-acpをインストールしてPATHに通す（macOS: brew install claude-agent-acp）。
- CodeCompanion設定を上の「ACP経由」例のように変更し、チャットを起動してSkillやMCPが読み込まれていることを確認する。
- インライン補完等は低レイテンシのため直接Anthropic APIを残すのが現実的（用途によって使い分ける）。
- セキュリティ：チーム内Skillに機密操作がある場合はClaude Code側の権限管理を整備してから導入する。

短くて確実な手順で、NeovimをチームのClaude Codeワークフローに溶け込ませられます。ぜひ自分のプロジェクトで試してみてください。
